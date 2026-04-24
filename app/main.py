"""
FastAPI Application Entry Point

This is the main application file that initializes FastAPI,
sets up middleware, includes routers, and defines core endpoints.

Architecture Benefits:
- Clean separation of concerns
- Easy to add new routes and middleware
- Centralized error handling
- Health check endpoints for monitoring
"""

from fastapi import FastAPI, Depends, HTTPException
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException
from sqlalchemy.orm import Session
import logging
from contextlib import asynccontextmanager

from app.config import settings
from app.database import get_db, test_connection, get_db_info, init_db
from app.services.nepse_api_client import create_api_client

# Configure logging
logging.basicConfig(
    level=getattr(logging, settings.log_level),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),  # Console output
        # File handler will be added when logs directory is created
    ]
)

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application lifespan manager
    
    Handles startup and shutdown events for the application.
    This is the modern way to handle startup/shutdown in FastAPI.
    
    Startup:
        - Test database connection
        - Initialize database tables
        - Log application info
    
    Shutdown:
        - Close database connections
        - Cleanup resources
    """
    # Startup
    logger.info("=" * 60)
    logger.info(f"Starting {settings.app_name} v{settings.app_version}")
    logger.info(f"Environment: {settings.environment}")
    logger.info("=" * 60)
    
    # Test database connection
    logger.info("Testing database connection...")
    if test_connection():
        logger.info("✅ Database connection successful")
        
        # Initialize database tables (in production, use Alembic migrations)
        if settings.is_development():
            logger.info("Initializing database tables...")
            try:
                init_db()
                logger.info("✅ Database tables initialized")
            except Exception as e:
                logger.error(f"❌ Failed to initialize database: {e}")
    else:
        logger.error("❌ Database connection failed")
        logger.error("Please check your database configuration in .env file")
    
    # Test API connection (non-blocking: run in background so lifespan yields
    # immediately even when the upstream NEPSE endpoint is geo-blocked/slow)
    logger.info("Scheduling NEPSE API connection probe in background...")
    import asyncio

    async def _probe_nepse_api():
        try:
            def _blocking():
                client = create_api_client("nepse")
                try:
                    return client.health_check()
                finally:
                    client.close()
            ok = await asyncio.to_thread(_blocking)
            if ok:
                logger.info("✅ NEPSE API connection successful")
            else:
                logger.warning("⚠️  NEPSE API health check failed (bot will use cached data)")
        except Exception as e:
            logger.error(f"❌ NEPSE API connection failed: {e} (bot will use cached data)")

    asyncio.create_task(_probe_nepse_api())
    
    logger.info("=" * 60)
    logger.info(f"Application started successfully!")
    logger.info(f"API Documentation: http://{settings.host}:{settings.port}/docs")
    logger.info("=" * 60)
    
    yield
    
    # Shutdown
    logger.info("Shutting down application...")
    logger.info("Application shutdown complete")


# Create FastAPI application
app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="""
    A configuration-driven NEPSE trading bot that generates buy signals 
    based on a comprehensive 4-component trading strategy.
    
    ## Features
    
    * **Sector Identification**: Analyze sectors and identify bullish trends
    * **Liquidity Hunt**: Detect demand zones and entry points
    * **Market Depth Analysis**: Monitor order book and detect institutional activity
    * **Floorsheet Analysis**: Track broker activity and detect manipulation
    * **Risk Management**: Calculate position sizing, stop-loss, and take-profit
    
    ## Strategy Components
    
    1. **Sector Identifier**: Daily/weekly chart comparison, stock screening
    2. **Liquidity Hunter**: Demand zones, volume patterns, candlestick patterns
    3. **Market Depth Analyzer**: Order book analysis, bid wall detection
    4. **Floorsheet Analyzer**: Broker tracking, manipulation detection
    5. **Risk Manager**: Position sizing, stop-loss, take-profit calculation
    """,
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Root endpoint
@app.get("/", tags=["Root"])
async def root():
    """
    Root endpoint
    
    Returns basic information about the API.
    """
    return {
        "name": settings.app_name,
        "version": settings.app_version,
        "environment": settings.environment,
        "status": "running",
        "docs": "/docs",
        "health": "/health"
    }


# Health check endpoint
@app.get("/health", tags=["Health"])
async def health_check():
    """
    Health check endpoint
    
    Returns the health status of the application and its dependencies.
    This is useful for monitoring and load balancers.
    """
    # Check database connection
    db_healthy = test_connection()

    # Check API connection (offloaded to a thread so the event loop never blocks
    # on geo-blocked upstream calls; capped with a short wall-clock timeout)
    import asyncio

    def _blocking_api_check():
        client = create_api_client("nepse")
        try:
            return client.health_check()
        finally:
            client.close()

    api_healthy = False
    try:
        api_healthy = await asyncio.wait_for(
            asyncio.to_thread(_blocking_api_check), timeout=3.0
        )
    except asyncio.TimeoutError:
        logger.warning("API health check skipped (upstream slow/blocked)")
    except Exception as e:
        logger.error(f"API health check failed: {e}")
    
    # Overall health status
    healthy = db_healthy and api_healthy
    
    return {
        "status": "healthy" if healthy else "unhealthy",
        "version": settings.app_version,
        "environment": settings.environment,
        "checks": {
            "database": "healthy" if db_healthy else "unhealthy",
            "api": "healthy" if api_healthy else "unhealthy"
        }
    }


# Database info endpoint
@app.get("/db-info", tags=["Database"])
async def database_info():
    """
    Database information endpoint
    
    Returns information about the database connection.
    Useful for debugging and monitoring.
    """
    try:
        info = get_db_info()
        return {
            "status": "success",
            "data": info
        }
    except Exception as e:
        logger.error(f"Error getting database info: {e}")
        return JSONResponse(
            status_code=500,
            content={
                "status": "error",
                "message": str(e)
            }
        )


# Test database connection endpoint
@app.get("/test-db", tags=["Database"])
async def test_db_connection():
    """
    Test database connection endpoint
    
    Tests the database connection and returns the result.
    """
    try:
        success = test_connection()
        if success:
            return {
                "status": "success",
                "message": "Database connection successful",
                "database": settings.db_name,
                "host": settings.db_host,
                "port": settings.db_port
            }
        else:
            return JSONResponse(
                status_code=500,
                content={
                    "status": "error",
                    "message": "Database connection failed"
                }
            )
    except Exception as e:
        logger.error(f"Database connection test failed: {e}")
        return JSONResponse(
            status_code=500,
            content={
                "status": "error",
                "message": str(e)
            }
        )


# Test API connection endpoint
@app.get("/test-api", tags=["API"])
async def test_api_connection():
    """
    Test NEPSE API connection endpoint
    
    Tests the NEPSE API connection and returns the result.
    """
    try:
        api_client = create_api_client("nepse")
        
        # Test health check
        healthy = api_client.health_check()
        
        # Get API info
        info = {
            "base_url": api_client.get_base_url(),
            "timeout": api_client.get_timeout(),
            "retry_attempts": api_client.get_retry_attempts()
        }
        
        api_client.close()
        
        if healthy:
            return {
                "status": "success",
                "message": "API connection successful",
                "api_info": info
            }
        else:
            return JSONResponse(
                status_code=500,
                content={
                    "status": "error",
                    "message": "API health check failed",
                    "api_info": info
                }
            )
    except Exception as e:
        logger.error(f"API connection test failed: {e}")
        return JSONResponse(
            status_code=500,
            content={
                "status": "error",
                "message": str(e)
            }
        )


# Configuration endpoint
@app.get("/config", tags=["Configuration"])
async def get_configuration():
    """
    Get application configuration
    
    Returns non-sensitive configuration information.
    """
    return {
        "app_name": settings.app_name,
        "app_version": settings.app_version,
        "environment": settings.environment,
        "debug": settings.debug,
        "api_base_url": settings.nepse_api_base_url,
        "scheduler_enabled": settings.enable_scheduler,
        "intervals": {
            "market_data_fetch": settings.market_data_fetch_interval,
            "sector_analysis": settings.sector_analysis_interval,
            "stock_screening": settings.stock_screening_interval,
            "pattern_detection": settings.pattern_detection_interval,
            "market_depth": settings.market_depth_interval,
            "floorsheet_analysis": settings.floorsheet_analysis_interval,
            "signal_generation": settings.signal_generation_interval
        }
    }


# Unified HTTPException handler — respects the `detail` message set by routes
# (e.g. "No market depth data found for NABIL") and only substitutes a generic
# "Endpoint not found" message when FastAPI itself raises 404 for an unmatched
# route (which has detail == "Not Found").
@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request, exc: StarletteHTTPException):
    detail = exc.detail
    is_default_not_found = exc.status_code == 404 and detail == "Not Found"

    if is_default_not_found:
        payload = {
            "status": "error",
            "message": "Endpoint not found",
            "path": str(request.url),
        }
    elif isinstance(detail, dict):
        payload = {"status": "error", **detail}
    else:
        payload = {
            "status": "error",
            "message": str(detail) if detail is not None else "Request failed",
        }

    return JSONResponse(status_code=exc.status_code, content=payload)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc: RequestValidationError):
    return JSONResponse(
        status_code=422,
        content={
            "status": "error",
            "message": "Validation failed",
            "errors": exc.errors(),
        },
    )


# Error handler for 500
@app.exception_handler(500)
async def internal_error_handler(request, exc):
    """Handle 500 errors"""
    logger.error(f"Internal server error: {exc}")
    return JSONResponse(
        status_code=500,
        content={
            "status": "error",
            "message": "Internal server error"
        }
    )


# Test NEPSE Live endpoint
@app.get("/test-nepse-live", tags=["API"])
async def test_nepse_live():
    """
    Test NEPSE Live Data endpoint

    Directly calls the unofficial NEPSE API at nepseapi.surajrimal.dev
    and returns raw live data. Useful for verifying API connectivity.

    Returns:
        - health: API health status
        - today_prices: Sample of today's stock prices (first 5 records)
        - indices: Current NEPSE index data
        - summary: Market summary
        - errors: Any errors encountered per call
    """
    import requests as req_lib
    from datetime import datetime

    BASE = "https://nepseapi.surajrimal.dev"
    TIMEOUT = 20

    results = {
        "timestamp": datetime.now().isoformat(),
        "api_base": BASE,
        "health": None,
        "today_prices": None,
        "indices": None,
        "summary": None,
        "errors": {}
    }

    session = req_lib.Session()
    session.headers.update({"Accept": "application/json"})

    def safe_get(endpoint, label):
        try:
            r = session.get(f"{BASE}{endpoint}", timeout=TIMEOUT)
            r.raise_for_status()
            return r.json()
        except req_lib.exceptions.Timeout:
            results["errors"][label] = f"Timeout after {TIMEOUT}s"
            logger.warning(f"/test-nepse-live: {label} timed out")
            return None
        except Exception as e:
            results["errors"][label] = str(e)
            logger.warning(f"/test-nepse-live: {label} error: {e}")
            return None

    # 1. Health check
    health_data = safe_get("/health", "health")
    if health_data:
        results["health"] = health_data
        logger.info(f"/test-nepse-live: health={health_data}")

    # 2. Market summary
    summary_data = safe_get("/Summary", "summary")
    if summary_data:
        results["summary"] = summary_data
        logger.info(f"/test-nepse-live: summary fetched")

    # 3. Today's prices (LiveMarket)
    prices_data = safe_get("/LiveMarket", "today_prices")
    if prices_data is not None:
        if isinstance(prices_data, list):
            results["today_prices"] = {
                "total_records": len(prices_data),
                "sample": prices_data[:5]
            }
        else:
            results["today_prices"] = prices_data
        logger.info(f"/test-nepse-live: LiveMarket returned data")

    # 4. NEPSE indices
    indices_data = safe_get("/NepseIndex", "indices")
    if indices_data is not None:
        if isinstance(indices_data, list):
            results["indices"] = {
                "total_records": len(indices_data),
                "sample": indices_data[:5]
            }
        else:
            results["indices"] = indices_data
        logger.info(f"/test-nepse-live: NepseIndex returned data")

    session.close()

    has_data = any(v is not None for k, v in results.items()
                   if k not in ("timestamp", "api_base", "errors"))
    has_errors = bool(results["errors"])

    return {
        "status": "success" if has_data and not has_errors else (
            "partial" if has_data else "no_data"
        ),
        "data": results
    }


# Include API routers
from app.api.v1 import router as api_v1_router
app.include_router(api_v1_router, prefix="/api/v1")


if __name__ == "__main__":
    import uvicorn
    
    # Run the application
    uvicorn.run(
        "app.main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.debug,
        log_level=settings.log_level.lower()
    )
