"""
Stock Data Service

This service handles fetching and storing stock list and fundamental data.
"""

import logging
from typing import List, Optional, Dict, Any
from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

from app.services.nepse_api_client import create_api_client
from app.models.stock import Stock
from app.models.sector import Sector
from app.validators.stock_validators import (
    StockDataSchema,
    FundamentalDataSchema,
    StockDataResponse
)

logger = logging.getLogger(__name__)


class StockDataService:
    """
    Service for fetching and storing stock data
    
    This service:
    1. Fetches stock list from NEPSE API
    2. Validates the data
    3. Stores/updates in database
    4. Handles fundamental data
    """
    
    def __init__(self, db: Session):
        """
        Initialize stock data service
        
        Args:
            db: Database session
        """
        self.db = db
        self.api_client = create_api_client("nepse")
        logger.info("StockDataService initialized")
    
    def fetch_and_store_stock_list(self) -> StockDataResponse:
        """
        Fetch stock list and store in database
        
        Returns:
            StockDataResponse with operation results
        """
        try:
            logger.info("Fetching stock list from NEPSE API...")
            
            # Fetch data from API
            stocks_data = self.api_client.fetch_stock_list()
            
            if not stocks_data:
                logger.warning("No stock data received from API")
                return StockDataResponse(
                    status="warning",
                    message="No stock data received from API",
                    stocks_added=0,
                    stocks_updated=0,
                    errors=["No data received"]
                )
            
            logger.info(f"Received {len(stocks_data)} stocks from API")
            
            # Process stocks
            stocks_added = 0
            stocks_updated = 0
            errors = []
            
            for stock_data in stocks_data:
                try:
                    # Validate stock data
                    validated_data = self._validate_stock_data(stock_data)
                    
                    if validated_data:
                        # Store or update stock
                        is_new = self._store_stock(validated_data)
                        if is_new:
                            stocks_added += 1
                        else:
                            stocks_updated += 1
                            
                except Exception as e:
                    symbol = stock_data.get("symbol", "UNKNOWN")
                    error_msg = f"Error processing stock {symbol}: {str(e)}"
                    logger.error(error_msg)
                    errors.append(error_msg)
            
            # Commit changes
            self.db.commit()
            
            logger.info(f"Stock data processed. Added: {stocks_added}, Updated: {stocks_updated}")
            
            return StockDataResponse(
                status="success" if not errors else "partial_success",
                message=f"Stock data fetched. Added: {stocks_added}, Updated: {stocks_updated}",
                stocks_added=stocks_added,
                stocks_updated=stocks_updated,
                errors=errors
            )
            
        except Exception as e:
            logger.error(f"Error in fetch_and_store_stock_list: {e}")
            self.db.rollback()
            return StockDataResponse(
                status="error",
                message=f"Failed to fetch stock data: {str(e)}",
                stocks_added=0,
                stocks_updated=0,
                errors=[str(e)]
            )
        finally:
            self.api_client.close()
    
    def _validate_stock_data(self, data: Dict[str, Any]) -> Optional[StockDataSchema]:
        """
        Validate stock data using Pydantic schema
        
        Args:
            data: Raw stock data from API
            
        Returns:
            Validated StockDataSchema or None if validation fails
        """
        try:
            # Map API data to schema
            stock_data = {
                "symbol": data.get("symbol", ""),
                "name": data.get("name", data.get("securityName", "")),
                "sector_name": data.get("sector", data.get("sectorName")),
                "ltp": data.get("ltp", data.get("lastTradedPrice")),
                "open_price": data.get("open", data.get("openPrice")),
                "high_price": data.get("high", data.get("highPrice")),
                "low_price": data.get("low", data.get("lowPrice")),
                "close_price": data.get("close", data.get("closePrice")),
                "previous_close": data.get("previous_close", data.get("previousClose")),
                "volume": data.get("volume", data.get("totalTradeQuantity")),
                "turnover": data.get("turnover", data.get("totalTurnover")),
                "change": data.get("change"),
                "change_percent": data.get("change_percent", data.get("changePercent")),
                "total_trades": data.get("total_trades", data.get("totalTrades")),
                "fifty_two_week_high": data.get("fifty_two_week_high", data.get("52WeekHigh")),
                "fifty_two_week_low": data.get("fifty_two_week_low", data.get("52WeekLow")),
                "market_cap": data.get("market_cap", data.get("marketCap"))
            }
            
            # Validate using Pydantic
            validated = StockDataSchema(**stock_data)
            return validated
            
        except Exception as e:
            logger.error(f"Validation error for stock: {e}")
            return None
    
    def _store_stock(self, stock_data: StockDataSchema) -> bool:
        """
        Store or update stock in database
        
        Args:
            stock_data: Validated stock data
            
        Returns:
            True if new stock created, False if updated
        """
        try:
            # Get sector ID if sector name provided
            sector_id = None
            if stock_data.sector_name:
                sector = self.db.query(Sector).filter_by(name=stock_data.sector_name).first()
                if sector:
                    sector_id = sector.id
            
            # Check if stock exists
            stock = self.db.query(Stock).filter_by(symbol=stock_data.symbol).first()
            
            if stock:
                # Update existing stock
                stock.name = stock_data.name
                stock.sector_id = sector_id
                stock.ltp = stock_data.ltp
                stock.open_price = stock_data.open_price
                stock.high_price = stock_data.high_price
                stock.low_price = stock_data.low_price
                stock.close_price = stock_data.close_price
                stock.previous_close = stock_data.previous_close
                stock.volume = stock_data.volume
                stock.turnover = stock_data.turnover
                stock.change = stock_data.change
                stock.change_percent = stock_data.change_percent
                stock.total_trades = stock_data.total_trades
                stock.fifty_two_week_high = stock_data.fifty_two_week_high
                stock.fifty_two_week_low = stock_data.fifty_two_week_low
                stock.market_cap = stock_data.market_cap
                stock.last_updated = datetime.now()
                
                logger.debug(f"Updated stock: {stock_data.symbol}")
                return False
            else:
                # Create new stock
                stock = Stock(
                    symbol=stock_data.symbol,
                    name=stock_data.name,
                    sector_id=sector_id,
                    ltp=stock_data.ltp,
                    open_price=stock_data.open_price,
                    high_price=stock_data.high_price,
                    low_price=stock_data.low_price,
                    close_price=stock_data.close_price,
                    previous_close=stock_data.previous_close,
                    volume=stock_data.volume,
                    turnover=stock_data.turnover,
                    change=stock_data.change,
                    change_percent=stock_data.change_percent,
                    total_trades=stock_data.total_trades,
                    fifty_two_week_high=stock_data.fifty_two_week_high,
                    fifty_two_week_low=stock_data.fifty_two_week_low,
                    market_cap=stock_data.market_cap
                )
                self.db.add(stock)
                
                logger.debug(f"Created new stock: {stock_data.symbol}")
                return True
                
        except SQLAlchemyError as e:
            logger.error(f"Database error storing stock {stock_data.symbol}: {e}")
            raise
    
    def fetch_and_store_fundamentals(self, symbol: str) -> Dict[str, Any]:
        """
        Fetch and store fundamental data for a stock
        
        Args:
            symbol: Stock symbol
            
        Returns:
            Dictionary with operation results
        """
        try:
            logger.info(f"Fetching fundamentals for {symbol}...")
            
            # Fetch data from API
            fundamentals = self.api_client.fetch_stock_fundamentals(symbol)
            
            if "error" in fundamentals:
                logger.error(f"Error fetching fundamentals: {fundamentals['error']}")
                return {
                    "status": "error",
                    "message": f"Failed to fetch fundamentals: {fundamentals['error']}",
                    "symbol": symbol
                }
            
            # Validate fundamental data
            validated_data = self._validate_fundamental_data(fundamentals)
            
            if not validated_data:
                return {
                    "status": "error",
                    "message": "Failed to validate fundamental data",
                    "symbol": symbol
                }
            
            # Update stock with fundamental data
            self._update_stock_fundamentals(validated_data)
            
            # Commit changes
            self.db.commit()
            
            logger.info(f"Fundamentals updated for {symbol}")
            
            return {
                "status": "success",
                "message": f"Fundamentals updated for {symbol}",
                "symbol": symbol,
                "data": validated_data.dict()
            }
            
        except Exception as e:
            logger.error(f"Error in fetch_and_store_fundamentals: {e}")
            self.db.rollback()
            return {
                "status": "error",
                "message": f"Failed to fetch fundamentals: {str(e)}",
                "symbol": symbol
            }
        finally:
            self.api_client.close()
    
    def _validate_fundamental_data(self, data: Dict[str, Any]) -> Optional[FundamentalDataSchema]:
        """
        Validate fundamental data using Pydantic schema
        
        Args:
            data: Raw fundamental data from API
            
        Returns:
            Validated FundamentalDataSchema or None if validation fails
        """
        try:
            validated = FundamentalDataSchema(**data)
            return validated
        except Exception as e:
            logger.error(f"Validation error for fundamental data: {e}")
            return None
    
    def _update_stock_fundamentals(self, fundamental_data: FundamentalDataSchema) -> None:
        """
        Update stock with fundamental data
        
        Args:
            fundamental_data: Validated fundamental data
        """
        try:
            stock = self.db.query(Stock).filter_by(symbol=fundamental_data.symbol).first()
            
            if stock:
                stock.eps = fundamental_data.eps
                stock.pe_ratio = fundamental_data.pe_ratio
                stock.book_value = fundamental_data.book_value
                stock.pb_ratio = fundamental_data.pb_ratio
                stock.roe = fundamental_data.roe
                stock.roa = fundamental_data.roa
                stock.net_profit_margin = fundamental_data.net_profit_margin
                stock.debt_to_equity = fundamental_data.debt_to_equity
                stock.current_ratio = fundamental_data.current_ratio
                stock.dividend_yield = fundamental_data.dividend_yield
                stock.dividend_per_share = fundamental_data.dividend_per_share
                stock.market_cap = fundamental_data.market_cap
                stock.shares_outstanding = fundamental_data.shares_outstanding
                stock.last_updated = datetime.now()
                
                logger.debug(f"Updated fundamentals for: {fundamental_data.symbol}")
            else:
                logger.warning(f"Stock not found: {fundamental_data.symbol}")
                
        except SQLAlchemyError as e:
            logger.error(f"Database error updating fundamentals: {e}")
            raise
    
    def get_all_stocks(self, limit: Optional[int] = None) -> List[Stock]:
        """
        Get all stocks from database
        
        Args:
            limit: Optional limit on number of stocks
            
        Returns:
            List of Stock objects
        """
        try:
            query = self.db.query(Stock).order_by(Stock.symbol)
            if limit:
                query = query.limit(limit)
            stocks = query.all()
            logger.info(f"Retrieved {len(stocks)} stocks from database")
            return stocks
        except SQLAlchemyError as e:
            logger.error(f"Error retrieving stocks: {e}")
            return []
    
    def get_stock_by_symbol(self, symbol: str) -> Optional[Stock]:
        """
        Get stock by symbol
        
        Args:
            symbol: Stock symbol
            
        Returns:
            Stock object or None
        """
        try:
            stock = self.db.query(Stock).filter_by(symbol=symbol.upper()).first()
            if stock:
                logger.debug(f"Retrieved stock: {symbol}")
            else:
                logger.warning(f"Stock not found: {symbol}")
            return stock
        except SQLAlchemyError as e:
            logger.error(f"Error retrieving stock {symbol}: {e}")
            return None
    
    def get_stocks_by_sector(self, sector_id: int) -> List[Stock]:
        """
        Get stocks by sector
        
        Args:
            sector_id: Sector ID
            
        Returns:
            List of Stock objects
        """
        try:
            stocks = self.db.query(Stock).filter_by(sector_id=sector_id).all()
            logger.info(f"Retrieved {len(stocks)} stocks for sector {sector_id}")
            return stocks
        except SQLAlchemyError as e:
            logger.error(f"Error retrieving stocks for sector {sector_id}: {e}")
            return []
