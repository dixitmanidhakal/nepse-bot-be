"""
Market Depth API Routes

This module provides REST API endpoints for market depth analysis:
- Current order book
- Order imbalance analysis
- Bid/Ask wall detection
- Liquidity analysis
- Spread analysis
- Price pressure
- Historical depth data
"""

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Optional
import logging

from app.database import get_db
from app.components.market_depth_analyzer import MarketDepthAnalyzer

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/depth", tags=["Market Depth"])


@router.get("/{symbol}/current")
async def get_current_depth(
    symbol: str,
    db: Session = Depends(get_db)
):
    """
    Get current market depth (order book) for a stock
    
    Returns the latest order book data including:
    - Top 5 buy orders
    - Top 5 sell orders
    - Order imbalance
    - Bid-ask spread
    - Liquidity metrics
    """
    try:
        analyzer = MarketDepthAnalyzer(db)
        result = analyzer.get_current_depth(symbol)
        
        if result is None:
            raise HTTPException(
                status_code=404,
                detail=f"No market depth data found for {symbol}"
            )
        
        return {
            "success": True,
            "data": result
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting current depth for {symbol}: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{symbol}/analysis")
async def get_depth_analysis(
    symbol: str,
    db: Session = Depends(get_db)
):
    """
    Get comprehensive market depth analysis
    
    Includes:
    - Order imbalance
    - Bid/Ask walls
    - Liquidity analysis
    - Price pressure
    - Support/Resistance from order book
    """
    try:
        analyzer = MarketDepthAnalyzer(db)
        
        result = {
            "symbol": symbol,
            "imbalance": analyzer.analyze_order_imbalance(symbol),
            "walls": analyzer.detect_walls(symbol),
            "liquidity": analyzer.analyze_liquidity(symbol),
            "pressure": analyzer.calculate_price_pressure(symbol),
            "support_resistance": analyzer.get_support_resistance_from_depth(symbol)
        }
        
        return {
            "success": True,
            "data": result
        }
        
    except Exception as e:
        logger.error(f"Error analyzing depth for {symbol}: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{symbol}/imbalance")
async def get_order_imbalance(
    symbol: str,
    db: Session = Depends(get_db)
):
    """
    Analyze order book imbalance
    
    Order imbalance indicates buying or selling pressure:
    - Positive imbalance = More buying pressure
    - Negative imbalance = More selling pressure
    """
    try:
        analyzer = MarketDepthAnalyzer(db)
        result = analyzer.analyze_order_imbalance(symbol)
        
        if not result.get('success'):
            raise HTTPException(
                status_code=404,
                detail=result.get('error', 'Analysis failed')
            )
        
        return result
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error analyzing imbalance for {symbol}: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{symbol}/walls")
async def detect_walls(
    symbol: str,
    wall_threshold: float = Query(2.0, description="Multiplier of average order size to consider as wall"),
    db: Session = Depends(get_db)
):
    """
    Detect bid/ask walls (large orders)
    
    Walls are large orders that can act as support/resistance levels.
    They indicate strong buying or selling interest at specific price levels.
    """
    try:
        analyzer = MarketDepthAnalyzer(db)
        result = analyzer.detect_walls(symbol, wall_threshold)
        
        if not result.get('success'):
            raise HTTPException(
                status_code=404,
                detail=result.get('error', 'Detection failed')
            )
        
        return result
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error detecting walls for {symbol}: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{symbol}/liquidity")
async def analyze_liquidity(
    symbol: str,
    db: Session = Depends(get_db)
):
    """
    Analyze market liquidity
    
    Liquidity indicates how easily a stock can be bought/sold:
    - High liquidity = Tight spreads, deep order book
    - Low liquidity = Wide spreads, thin order book
    """
    try:
        analyzer = MarketDepthAnalyzer(db)
        result = analyzer.analyze_liquidity(symbol)
        
        if not result.get('success'):
            raise HTTPException(
                status_code=404,
                detail=result.get('error', 'Analysis failed')
            )
        
        return result
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error analyzing liquidity for {symbol}: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{symbol}/spread")
async def analyze_spread(
    symbol: str,
    db: Session = Depends(get_db)
):
    """
    Analyze bid-ask spread
    
    Spread indicates transaction cost and liquidity:
    - Tight spread = High liquidity, low cost
    - Wide spread = Low liquidity, high cost
    """
    try:
        analyzer = MarketDepthAnalyzer(db)
        result = analyzer.analyze_spread(symbol)
        
        if not result.get('success'):
            raise HTTPException(
                status_code=404,
                detail=result.get('error', 'Analysis failed')
            )
        
        return result
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error analyzing spread for {symbol}: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{symbol}/pressure")
async def calculate_price_pressure(
    symbol: str,
    db: Session = Depends(get_db)
):
    """
    Calculate price pressure from order book
    
    Price pressure indicates likely direction of next price movement:
    - Positive pressure = Upward price movement likely
    - Negative pressure = Downward price movement likely
    """
    try:
        analyzer = MarketDepthAnalyzer(db)
        result = analyzer.calculate_price_pressure(symbol)
        
        if not result.get('success'):
            raise HTTPException(
                status_code=404,
                detail=result.get('error', 'Calculation failed')
            )
        
        return result
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error calculating pressure for {symbol}: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{symbol}/history")
async def get_depth_history(
    symbol: str,
    hours: int = Query(24, description="Number of hours of history", ge=1, le=168),
    db: Session = Depends(get_db)
):
    """
    Get historical market depth data
    
    Returns historical order book snapshots for trend analysis.
    """
    try:
        analyzer = MarketDepthAnalyzer(db)
        result = analyzer.get_depth_history(symbol, hours)
        
        if not result.get('success'):
            raise HTTPException(
                status_code=404,
                detail=result.get('error', 'No historical data found')
            )
        
        return result
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting depth history for {symbol}: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{symbol}/support-resistance")
async def get_support_resistance(
    symbol: str,
    db: Session = Depends(get_db)
):
    """
    Get support/resistance levels from order book
    
    Large orders in the order book can act as support/resistance levels.
    """
    try:
        analyzer = MarketDepthAnalyzer(db)
        result = analyzer.get_support_resistance_from_depth(symbol)
        
        if not result.get('success'):
            raise HTTPException(
                status_code=404,
                detail=result.get('error', 'Analysis failed')
            )
        
        return result
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting support/resistance for {symbol}: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
