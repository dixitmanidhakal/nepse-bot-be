"""
Day 3 Testing Script

This script tests all Day 3 data fetching services.
"""

import sys
import logging
from datetime import datetime, timedelta

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Add app to path
sys.path.insert(0, '.')

from app.database import SessionLocal
from app.services.data import (
    MarketDataService,
    StockDataService,
    OHLCVService,
    MarketDepthService,
    FloorsheetService,
    DataFetcherService
)


def test_market_data_service():
    """Test MarketDataService"""
    print("\n" + "="*60)
    print("TEST 1: Market Data Service")
    print("="*60)
    
    db = SessionLocal()
    try:
        service = MarketDataService(db)
        
        # Test fetching market data
        print("\n📊 Fetching market indices and sectors...")
        response = service.fetch_and_store_market_indices()
        
        print(f"Status: {response.status}")
        print(f"Message: {response.message}")
        print(f"NEPSE Index: {response.nepse_index}")
        print(f"Sectors Updated: {response.sectors_updated}")
        
        if response.errors:
            print(f"Errors: {response.errors}")
        
        # Test getting sectors
        print("\n📋 Getting all sectors...")
        sectors = service.get_all_sectors()
        print(f"Total sectors in database: {len(sectors)}")
        
        if sectors:
            print("\nSample sector:")
            sector = sectors[0]
            print(f"  Name: {sector.name}")
            print(f"  Symbol: {sector.symbol}")
            print(f"  Current Index: {sector.current_index}")
            print(f"  Change: {sector.change}")
        
        print("\n✅ Market Data Service test completed")
        return True
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        return False
    finally:
        db.close()


def test_stock_data_service():
    """Test StockDataService"""
    print("\n" + "="*60)
    print("TEST 2: Stock Data Service")
    print("="*60)
    
    db = SessionLocal()
    try:
        service = StockDataService(db)
        
        # Test fetching stock list
        print("\n📈 Fetching stock list...")
        response = service.fetch_and_store_stock_list()
        
        print(f"Status: {response.status}")
        print(f"Message: {response.message}")
        print(f"Stocks Added: {response.stocks_added}")
        print(f"Stocks Updated: {response.stocks_updated}")
        
        if response.errors:
            print(f"Errors: {response.errors[:5]}")  # Show first 5 errors
        
        # Test getting stocks
        print("\n📋 Getting all stocks...")
        stocks = service.get_all_stocks(limit=10)
        print(f"Sample stocks (first 10):")
        
        for stock in stocks:
            print(f"  {stock.symbol}: {stock.name} - LTP: {stock.ltp}")
        
        print("\n✅ Stock Data Service test completed")
        return True
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        return False
    finally:
        db.close()


def test_ohlcv_service():
    """Test OHLCVService"""
    print("\n" + "="*60)
    print("TEST 3: OHLCV Service")
    print("="*60)
    
    db = SessionLocal()
    try:
        service = OHLCVService(db)
        
        # Get a sample stock
        from app.models.stock import Stock
        stock = db.query(Stock).first()
        
        if not stock:
            print("⚠️  No stocks in database. Run test_stock_data_service first.")
            return False
        
        # Test fetching OHLCV
        print(f"\n📊 Fetching OHLCV for {stock.symbol}...")
        response = service.fetch_and_store_ohlcv(
            symbol=stock.symbol,
            days=10
        )
        
        print(f"Status: {response.status}")
        print(f"Message: {response.message}")
        print(f"Records Added: {response.records_added}")
        print(f"Records Updated: {response.records_updated}")
        
        if response.errors:
            print(f"Errors: {response.errors}")
        
        # Test getting OHLCV
        print(f"\n📋 Getting OHLCV data for {stock.symbol}...")
        ohlcv_data = service.get_ohlcv_by_symbol(stock.symbol, limit=5)
        print(f"OHLCV records (last 5 days):")
        
        for ohlcv in ohlcv_data:
            print(f"  {ohlcv.date}: O:{ohlcv.open} H:{ohlcv.high} L:{ohlcv.low} C:{ohlcv.close} V:{ohlcv.volume}")
        
        print("\n✅ OHLCV Service test completed")
        return True
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        return False
    finally:
        db.close()


def test_market_depth_service():
    """Test MarketDepthService"""
    print("\n" + "="*60)
    print("TEST 4: Market Depth Service")
    print("="*60)
    
    db = SessionLocal()
    try:
        service = MarketDepthService(db)
        
        # Get a sample stock
        from app.models.stock import Stock
        stock = db.query(Stock).first()
        
        if not stock:
            print("⚠️  No stocks in database. Run test_stock_data_service first.")
            return False
        
        # Test fetching market depth
        print(f"\n📊 Fetching market depth for {stock.symbol}...")
        response = service.fetch_and_store_market_depth(symbol=stock.symbol)
        
        print(f"Status: {response.status}")
        print(f"Message: {response.message}")
        
        if response.errors:
            print(f"Errors: {response.errors}")
        
        # Test getting market depth
        print(f"\n📋 Getting latest market depth for {stock.symbol}...")
        depth = service.get_latest_market_depth(stock.symbol)
        
        if depth:
            print(f"Market Depth at {depth.timestamp}:")
            print(f"  Best Bid: {depth.buy_price_1} x {depth.buy_quantity_1}")
            print(f"  Best Ask: {depth.sell_price_1} x {depth.sell_quantity_1}")
            print(f"  Spread: {depth.bid_ask_spread}")
            print(f"  Order Imbalance: {depth.order_imbalance}")
        
        print("\n✅ Market Depth Service test completed")
        return True
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        return False
    finally:
        db.close()


def test_floorsheet_service():
    """Test FloorsheetService"""
    print("\n" + "="*60)
    print("TEST 5: Floorsheet Service")
    print("="*60)
    
    db = SessionLocal()
    try:
        service = FloorsheetService(db)
        
        # Get a sample stock
        from app.models.stock import Stock
        stock = db.query(Stock).first()
        
        if not stock:
            print("⚠️  No stocks in database. Run test_stock_data_service first.")
            return False
        
        # Test fetching floorsheet
        print(f"\n📊 Fetching floorsheet for {stock.symbol}...")
        response = service.fetch_and_store_floorsheet(symbol=stock.symbol)
        
        print(f"Status: {response.status}")
        print(f"Message: {response.message}")
        print(f"Trades Added: {response.trades_added}")
        print(f"Trades Updated: {response.trades_updated}")
        
        if response.errors:
            print(f"Errors: {response.errors[:5]}")  # Show first 5 errors
        
        # Test getting floorsheet
        print(f"\n📋 Getting floorsheet for {stock.symbol}...")
        trades = service.get_floorsheet_by_symbol(stock.symbol, limit=5)
        print(f"Recent trades (last 5):")
        
        for trade in trades:
            print(f"  Buyer:{trade.buyer_broker_no} -> Seller:{trade.seller_broker_no}")
            print(f"    Qty:{trade.quantity} @ {trade.rate} = {trade.amount}")
        
        print("\n✅ Floorsheet Service test completed")
        return True
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        return False
    finally:
        db.close()


def test_data_fetcher_service():
    """Test DataFetcherService (Orchestrator)"""
    print("\n" + "="*60)
    print("TEST 6: Data Fetcher Service (Orchestrator)")
    print("="*60)
    
    db = SessionLocal()
    try:
        service = DataFetcherService(db)
        
        # Test getting data status
        print("\n📊 Getting data status...")
        status = service.get_data_status()
        
        print(f"Status: {status['status']}")
        if 'data_status' in status:
            data_status = status['data_status']
            print(f"Sectors Count: {data_status.get('sectors_count', 0)}")
            print(f"Stocks Count: {data_status.get('stocks_count', 0)}")
            print(f"Latest OHLCV Date: {data_status.get('latest_ohlcv_date', 'N/A')}")
            print(f"Database Connected: {data_status.get('database_connected', False)}")
        
        print("\n✅ Data Fetcher Service test completed")
        return True
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        return False
    finally:
        db.close()


def main():
    """Run all tests"""
    print("\n" + "="*60)
    print("DAY 3 SERVICES TEST SUITE")
    print("="*60)
    print(f"Started at: {datetime.now()}")
    
    results = {
        "Market Data Service": test_market_data_service(),
        "Stock Data Service": test_stock_data_service(),
        "OHLCV Service": test_ohlcv_service(),
        "Market Depth Service": test_market_depth_service(),
        "Floorsheet Service": test_floorsheet_service(),
        "Data Fetcher Service": test_data_fetcher_service()
    }
    
    # Summary
    print("\n" + "="*60)
    print("TEST SUMMARY")
    print("="*60)
    
    passed = sum(1 for result in results.values() if result)
    total = len(results)
    
    for test_name, result in results.items():
        status = "✅ PASSED" if result else "❌ FAILED"
        print(f"{test_name}: {status}")
    
    print(f"\nTotal: {passed}/{total} tests passed")
    print(f"Completed at: {datetime.now()}")
    
    if passed == total:
        print("\n🎉 All tests passed!")
        return 0
    else:
        print(f"\n⚠️  {total - passed} test(s) failed")
        return 1


if __name__ == "__main__":
    sys.exit(main())
