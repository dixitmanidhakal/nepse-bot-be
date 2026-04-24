"""
Data API Routes

This module defines API endpoints for data fetching operations.
"""

import logging
from typing import Optional
from datetime import date
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.services.data import DataFetcherService

logger = logging.getLogger(__name__)

# Create router
router = APIRouter(prefix="/data", tags=["Data Fetching"])


@router.post("/fetch-market")
async def fetch_market_data(db: Session = Depends(get_db)):
    """
    Fetch market indices and sector data from NEPSE API
    
    This endpoint:
    - Fetches NEPSE index
    - Fetches all sector indices
    - Updates database with latest data
    
    Returns:
        Dictionary with operation results
    """
    try:
        logger.info("API: Fetching market data...")
        service = DataFetcherService(db)
        result = service.fetch_market_data_only()
        return result
    except Exception as e:
        logger.error(f"Error in fetch_market_data endpoint: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/fetch-stocks")
async def fetch_stock_list(db: Session = Depends(get_db)):
    """
    Fetch stock list from NEPSE API
    
    This endpoint:
    - Fetches all listed stocks
    - Updates stock information
    - Links stocks to sectors
    
    Returns:
        Dictionary with operation results
    """
    try:
        logger.info("API: Fetching stock list...")
        service = DataFetcherService(db)
        result = service.fetch_stock_data_only()
        return result
    except Exception as e:
        logger.error(f"Error in fetch_stock_list endpoint: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/fetch-ohlcv/{symbol}")
async def fetch_ohlcv_data(
    symbol: str,
    days: int = Query(default=30, ge=1, le=365, description="Number of days to fetch"),
    db: Session = Depends(get_db)
):
    """
    Fetch OHLCV (Open, High, Low, Close, Volume) data for a stock
    
    Args:
        symbol: Stock symbol (e.g., NABIL)
        days: Number of days of historical data to fetch (1-365)
    
    Returns:
        Dictionary with operation results
    """
    try:
        logger.info(f"API: Fetching OHLCV for {symbol}...")
        service = DataFetcherService(db)
        result = service.fetch_ohlcv_for_symbol(symbol=symbol.upper(), days=days)
        return result
    except Exception as e:
        logger.error(f"Error in fetch_ohlcv_data endpoint: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/fetch-market-depth/{symbol}")
async def fetch_market_depth(
    symbol: str,
    db: Session = Depends(get_db)
):
    """
    Fetch market depth (order book) data for a stock
    
    Args:
        symbol: Stock symbol (e.g., NABIL)
    
    Returns:
        Dictionary with operation results including buy/sell orders
    """
    try:
        logger.info(f"API: Fetching market depth for {symbol}...")
        service = DataFetcherService(db)
        result = service.fetch_market_depth_for_symbol(symbol=symbol.upper())
        return result
    except Exception as e:
        logger.error(f"Error in fetch_market_depth endpoint: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/fetch-floorsheet")
async def fetch_floorsheet_data(
    symbol: Optional[str] = Query(None, description="Stock symbol (optional, fetch all if not provided)"),
    trade_date: Optional[date] = Query(None, description="Trade date (optional, fetch today if not provided)"),
    db: Session = Depends(get_db)
):
    """
    Fetch floorsheet (trade details) data
    
    Args:
        symbol: Stock symbol (optional, fetches all stocks if not provided)
        trade_date: Trade date (optional, fetches today's data if not provided)
    
    Returns:
        Dictionary with operation results including trade details
    """
    try:
        if symbol:
            logger.info(f"API: Fetching floorsheet for {symbol}...")
            symbol = symbol.upper()
        else:
            logger.info("API: Fetching floorsheet for all stocks...")
        
        service = DataFetcherService(db)
        result = service.fetch_floorsheet_for_symbol(symbol=symbol, trade_date=trade_date)
        return result
    except Exception as e:
        logger.error(f"Error in fetch_floorsheet_data endpoint: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/fetch-all")
async def fetch_all_data(
    include_ohlcv: bool = Query(default=True, description="Include OHLCV data"),
    include_depth: bool = Query(default=True, description="Include market depth data"),
    include_floorsheet: bool = Query(default=True, description="Include floorsheet data"),
    ohlcv_days: int = Query(default=30, ge=1, le=365, description="Number of days of OHLCV data"),
    db: Session = Depends(get_db)
):
    """
    Fetch all data from NEPSE API (orchestrated operation)
    
    This endpoint performs a complete data fetch:
    1. Market indices and sectors
    2. Stock list
    3. OHLCV data (optional)
    4. Market depth (optional)
    5. Floorsheet (optional)
    
    Args:
        include_ohlcv: Whether to fetch OHLCV data
        include_depth: Whether to fetch market depth
        include_floorsheet: Whether to fetch floorsheet
        ohlcv_days: Number of days of OHLCV data to fetch
    
    Returns:
        Dictionary with comprehensive operation results
        
    Note: This operation may take several minutes to complete
    """
    try:
        logger.info("API: Starting full data fetch operation...")
        service = DataFetcherService(db)
        result = service.fetch_all_data(
            include_ohlcv=include_ohlcv,
            include_depth=include_depth,
            include_floorsheet=include_floorsheet,
            ohlcv_days=ohlcv_days
        )
        return result
    except Exception as e:
        logger.error(f"Error in fetch_all_data endpoint: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/status")
async def get_data_status(db: Session = Depends(get_db)):
    """
    Get status of data in database
    
    Returns statistics about:
    - Number of sectors
    - Number of stocks
    - Latest OHLCV date
    - Database connection status
    
    Returns:
        Dictionary with data statistics
    """
    try:
        logger.info("API: Getting data status...")
        service = DataFetcherService(db)
        result = service.get_data_status()
        return result
    except Exception as e:
        logger.error(f"Error in get_data_status endpoint: {e}")
        raise HTTPException(status_code=500, detail=str(e))
