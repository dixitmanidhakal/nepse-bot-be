"""
Floorsheet Service

This service handles fetching and storing floorsheet (trade details) data.
"""

import logging
from typing import Optional, Dict, Any, List
from datetime import datetime, date
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from collections import defaultdict

from app.services.nepse_api_client import create_api_client
from app.models.stock import Stock
from app.models.floorsheet import Floorsheet
from app.validators.floorsheet_validators import (
    FloorsheetTradeSchema,
    FloorsheetResponse,
    BrokerActivitySchema
)

logger = logging.getLogger(__name__)


class FloorsheetService:
    """
    Service for fetching and storing floorsheet data
    
    This service:
    1. Fetches floorsheet from NEPSE API
    2. Validates the data
    3. Stores/updates in database
    4. Analyzes broker activity
    """
    
    def __init__(self, db: Session):
        """
        Initialize floorsheet service
        
        Args:
            db: Database session
        """
        self.db = db
        self.api_client = create_api_client("nepse")
        logger.info("FloorsheetService initialized")
    
    def fetch_and_store_floorsheet(
        self,
        symbol: Optional[str] = None,
        trade_date: Optional[date] = None
    ) -> FloorsheetResponse:
        """
        Fetch floorsheet and store in database
        
        Args:
            symbol: Stock symbol (optional, fetch all if None)
            trade_date: Trade date (optional, fetch today if None)
            
        Returns:
            FloorsheetResponse with operation results
        """
        try:
            if symbol:
                logger.info(f"Fetching floorsheet for {symbol}...")
            else:
                logger.info("Fetching floorsheet for all stocks...")
            
            # Verify stock exists if symbol provided
            stock_id = None
            if symbol:
                stock = self.db.query(Stock).filter_by(symbol=symbol.upper()).first()
                if not stock:
                    logger.error(f"Stock not found: {symbol}")
                    return FloorsheetResponse(
                        status="error",
                        message=f"Stock not found: {symbol}",
                        symbol=symbol,
                        trades_added=0,
                        trades_updated=0,
                        errors=[f"Stock not found: {symbol}"]
                    )
                stock_id = stock.id
            
            # Convert date to datetime if provided
            trade_datetime = None
            if trade_date:
                trade_datetime = datetime.combine(trade_date, datetime.min.time())
            
            # Fetch data from API
            floorsheet_data = self.api_client.fetch_floorsheet(
                symbol=symbol,
                date=trade_datetime
            )
            
            if not floorsheet_data:
                logger.warning("No floorsheet data received")
                return FloorsheetResponse(
                    status="warning",
                    message="No floorsheet data received",
                    symbol=symbol,
                    trades_added=0,
                    trades_updated=0,
                    errors=["No data received"]
                )
            
            logger.info(f"Received {len(floorsheet_data)} floorsheet records")
            
            # Process floorsheet data
            trades_added = 0
            trades_updated = 0
            total_volume = 0
            total_amount = 0.0
            errors = []
            
            for trade_data in floorsheet_data:
                try:
                    # Validate trade data
                    validated_data = self._validate_floorsheet_trade(trade_data)
                    
                    if validated_data:
                        # Get stock_id for this trade
                        trade_stock = self.db.query(Stock).filter_by(
                            symbol=validated_data.symbol
                        ).first()
                        
                        if trade_stock:
                            # Store trade
                            is_new = self._store_floorsheet_trade(trade_stock.id, validated_data)
                            if is_new:
                                trades_added += 1
                            else:
                                trades_updated += 1
                            
                            total_volume += validated_data.quantity
                            total_amount += validated_data.amount
                        else:
                            logger.warning(f"Stock not found for trade: {validated_data.symbol}")
                            
                except Exception as e:
                    error_msg = f"Error processing trade: {str(e)}"
                    logger.error(error_msg)
                    errors.append(error_msg)
            
            # Commit changes
            self.db.commit()
            
            logger.info(f"Floorsheet processed. Added: {trades_added}, Updated: {trades_updated}")
            
            return FloorsheetResponse(
                status="success" if not errors else "partial_success",
                message=f"Floorsheet data fetched",
                symbol=symbol,
                trades_added=trades_added,
                trades_updated=trades_updated,
                total_volume=total_volume,
                total_amount=total_amount,
                date=trade_date,
                errors=errors
            )
            
        except Exception as e:
            logger.error(f"Error in fetch_and_store_floorsheet: {e}")
            self.db.rollback()
            return FloorsheetResponse(
                status="error",
                message=f"Failed to fetch floorsheet: {str(e)}",
                symbol=symbol,
                trades_added=0,
                trades_updated=0,
                errors=[str(e)]
            )
        finally:
            self.api_client.close()
    
    def _validate_floorsheet_trade(self, data: Dict[str, Any]) -> Optional[FloorsheetTradeSchema]:
        """
        Validate floorsheet trade data using Pydantic schema
        
        Args:
            data: Raw trade data from API
            
        Returns:
            Validated FloorsheetTradeSchema or None if validation fails
        """
        try:
            # Parse dates
            trade_time = data.get("trade_time", data.get("tradeTime"))
            if isinstance(trade_time, str):
                try:
                    trade_time = datetime.fromisoformat(trade_time)
                except:
                    trade_time = None
            
            trade_date = data.get("trade_date", data.get("tradeDate"))
            if isinstance(trade_date, str):
                try:
                    trade_date = datetime.strptime(trade_date, "%Y-%m-%d").date()
                except:
                    trade_date = None
            
            # Map API data to schema
            trade_data = {
                "symbol": data.get("symbol", ""),
                "contract_id": data.get("contract_id", data.get("contractId", "")),
                "buyer_broker_no": data.get("buyer_broker", data.get("buyerBrokerNo", 0)),
                "buyer_broker_name": data.get("buyer_broker_name", data.get("buyerBrokerName")),
                "seller_broker_no": data.get("seller_broker", data.get("sellerBrokerNo", 0)),
                "seller_broker_name": data.get("seller_broker_name", data.get("sellerBrokerName")),
                "quantity": data.get("quantity", data.get("contractQuantity", 0)),
                "rate": data.get("rate", data.get("contractRate", 0)),
                "amount": data.get("amount", data.get("contractAmount", 0)),
                "trade_time": trade_time,
                "trade_date": trade_date,
                "is_institutional": data.get("is_institutional", False),
                "is_cross_trade": data.get("is_cross_trade", False)
            }
            
            # Validate using Pydantic
            validated = FloorsheetTradeSchema(**trade_data)
            return validated
            
        except Exception as e:
            logger.error(f"Validation error for floorsheet trade: {e}")
            return None
    
    def _store_floorsheet_trade(self, stock_id: int, trade_data: FloorsheetTradeSchema) -> bool:
        """
        Store floorsheet trade in database
        
        Args:
            stock_id: Stock ID
            trade_data: Validated trade data
            
        Returns:
            True if new trade created, False if updated
        """
        try:
            # Check if trade exists (by contract_id)
            trade = self.db.query(Floorsheet).filter_by(
                contract_id=trade_data.contract_id
            ).first()
            
            if trade:
                # Update existing trade (rare case)
                trade.buyer_broker_no = trade_data.buyer_broker_no
                trade.buyer_broker_name = trade_data.buyer_broker_name
                trade.seller_broker_no = trade_data.seller_broker_no
                trade.seller_broker_name = trade_data.seller_broker_name
                trade.quantity = trade_data.quantity
                trade.rate = trade_data.rate
                trade.amount = trade_data.amount
                trade.trade_time = trade_data.trade_time
                trade.trade_date = trade_data.trade_date
                trade.is_institutional = trade_data.is_institutional
                trade.is_cross_trade = trade_data.is_cross_trade
                
                logger.debug(f"Updated trade: {trade_data.contract_id}")
                return False
            else:
                # Create new trade
                trade = Floorsheet(
                    stock_id=stock_id,
                    contract_id=trade_data.contract_id,
                    buyer_broker_no=trade_data.buyer_broker_no,
                    buyer_broker_name=trade_data.buyer_broker_name,
                    seller_broker_no=trade_data.seller_broker_no,
                    seller_broker_name=trade_data.seller_broker_name,
                    quantity=trade_data.quantity,
                    rate=trade_data.rate,
                    amount=trade_data.amount,
                    trade_time=trade_data.trade_time,
                    trade_date=trade_data.trade_date,
                    is_institutional=trade_data.is_institutional,
                    is_cross_trade=trade_data.is_cross_trade
                )
                
                self.db.add(trade)
                logger.debug(f"Created new trade: {trade_data.contract_id}")
                return True
                
        except SQLAlchemyError as e:
            logger.error(f"Database error storing floorsheet trade: {e}")
            raise
    
    def get_floorsheet_by_symbol(
        self,
        symbol: str,
        trade_date: Optional[date] = None,
        limit: int = 100
    ) -> List[Floorsheet]:
        """
        Get floorsheet data for a stock
        
        Args:
            symbol: Stock symbol
            trade_date: Trade date filter
            limit: Maximum number of records
            
        Returns:
            List of Floorsheet objects
        """
        try:
            stock = self.db.query(Stock).filter_by(symbol=symbol.upper()).first()
            if not stock:
                return []
            
            query = self.db.query(Floorsheet).filter_by(stock_id=stock.id)
            
            if trade_date:
                query = query.filter(Floorsheet.trade_date == trade_date)
            
            trades = query.order_by(Floorsheet.trade_time.desc()).limit(limit).all()
            
            logger.info(f"Retrieved {len(trades)} floorsheet records for {symbol}")
            return trades
            
        except SQLAlchemyError as e:
            logger.error(f"Error retrieving floorsheet for {symbol}: {e}")
            return []
    
    def analyze_broker_activity(
        self,
        symbol: str,
        trade_date: date
    ) -> Dict[str, Any]:
        """
        Analyze broker activity for a stock on a specific date
        
        Args:
            symbol: Stock symbol
            trade_date: Trade date
            
        Returns:
            Dictionary with broker activity analysis
        """
        try:
            # Get floorsheet data
            trades = self.get_floorsheet_by_symbol(symbol, trade_date, limit=10000)
            
            if not trades:
                return {
                    "status": "error",
                    "message": "No trades found",
                    "symbol": symbol,
                    "date": trade_date
                }
            
            # Analyze broker activity
            broker_activity = defaultdict(lambda: {
                "buy_quantity": 0,
                "buy_amount": 0.0,
                "buy_trades": 0,
                "sell_quantity": 0,
                "sell_amount": 0.0,
                "sell_trades": 0
            })
            
            for trade in trades:
                # Buyer activity
                broker_activity[trade.buyer_broker_no]["buy_quantity"] += trade.quantity
                broker_activity[trade.buyer_broker_no]["buy_amount"] += trade.amount
                broker_activity[trade.buyer_broker_no]["buy_trades"] += 1
                
                # Seller activity
                broker_activity[trade.seller_broker_no]["sell_quantity"] += trade.quantity
                broker_activity[trade.seller_broker_no]["sell_amount"] += trade.amount
                broker_activity[trade.seller_broker_no]["sell_trades"] += 1
            
            # Convert to list and calculate net activity
            broker_list = []
            for broker_no, activity in broker_activity.items():
                net_quantity = activity["buy_quantity"] - activity["sell_quantity"]
                net_amount = activity["buy_amount"] - activity["sell_amount"]
                
                broker_list.append({
                    "broker_no": broker_no,
                    "buy_quantity": activity["buy_quantity"],
                    "buy_amount": activity["buy_amount"],
                    "buy_trades": activity["buy_trades"],
                    "sell_quantity": activity["sell_quantity"],
                    "sell_amount": activity["sell_amount"],
                    "sell_trades": activity["sell_trades"],
                    "net_quantity": net_quantity,
                    "net_amount": net_amount,
                    "is_net_buyer": net_quantity > 0,
                    "is_net_seller": net_quantity < 0
                })
            
            # Sort by net quantity
            top_buyers = sorted(
                [b for b in broker_list if b["is_net_buyer"]],
                key=lambda x: x["net_quantity"],
                reverse=True
            )[:10]
            
            top_sellers = sorted(
                [b for b in broker_list if b["is_net_seller"]],
                key=lambda x: abs(x["net_quantity"]),
                reverse=True
            )[:10]
            
            return {
                "status": "success",
                "symbol": symbol,
                "date": trade_date,
                "total_trades": len(trades),
                "total_volume": sum(t.quantity for t in trades),
                "total_amount": sum(t.amount for t in trades),
                "top_buyers": top_buyers,
                "top_sellers": top_sellers,
                "unique_brokers": len(broker_activity)
            }
            
        except Exception as e:
            logger.error(f"Error analyzing broker activity: {e}")
            return {
                "status": "error",
                "message": str(e),
                "symbol": symbol,
                "date": trade_date
            }
