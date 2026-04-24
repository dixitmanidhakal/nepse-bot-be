"""
Day 2 Testing Script

This script tests the database models and CRUD operations.
"""

import sys
from datetime import datetime, date
from sqlalchemy.orm import Session

from app.database import SessionLocal, test_connection
from app.models import (
    BotConfiguration,
    Sector,
    Stock,
    StockOHLCV,
    MarketDepth,
    Floorsheet,
    Signal,
    SignalType,
    SignalStatus,
    Pattern,
    PatternType,
    PatternStatus,
)


def test_database_connection():
    """Test database connection"""
    print("\n" + "="*60)
    print("Testing Database Connection...")
    print("="*60)
    
    if test_connection():
        print("✅ Database connection successful!")
        return True
    else:
        print("❌ Database connection failed!")
        return False


def test_bot_configuration_crud():
    """Test BotConfiguration CRUD operations"""
    print("\n" + "="*60)
    print("Testing BotConfiguration Model...")
    print("="*60)
    
    db = SessionLocal()
    
    try:
        # Create
        print("\n1. Creating bot configuration...")
        bot_config = BotConfiguration(
            name="Test Bot Config",
            description="Test configuration for Day 2",
            is_active=True,
            sector_identifier_enabled=True,
            liquidity_hunter_enabled=True,
            market_depth_enabled=True,
            floorsheet_enabled=True,
            sector_comparison_days=30,
            volume_days=10,
            min_beta=0.8,
            max_beta=1.5,
            risk_per_trade=1.0,
            reward_risk_ratio=2.0
        )
        db.add(bot_config)
        db.commit()
        db.refresh(bot_config)
        print(f"✅ Created: {bot_config}")
        
        # Read
        print("\n2. Reading bot configuration...")
        config = db.query(BotConfiguration).filter_by(name="Test Bot Config").first()
        print(f"✅ Read: {config}")
        
        # Update
        print("\n3. Updating bot configuration...")
        config.risk_per_trade = 1.5
        db.commit()
        print(f"✅ Updated risk_per_trade to {config.risk_per_trade}")
        
        # Delete
        print("\n4. Deleting bot configuration...")
        db.delete(config)
        db.commit()
        print("✅ Deleted successfully")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        db.rollback()
        return False
    finally:
        db.close()


def test_sector_crud():
    """Test Sector CRUD operations"""
    print("\n" + "="*60)
    print("Testing Sector Model...")
    print("="*60)
    
    db = SessionLocal()
    
    try:
        # Create
        print("\n1. Creating sector...")
        sector = Sector(
            name="Banking",
            code="BANK",
            description="Banking sector",
            current_index=1500.0,
            previous_close=1480.0,
            change=20.0,
            change_percent=1.35,
            momentum_30d=5.5,
            total_stocks=25
        )
        db.add(sector)
        db.commit()
        db.refresh(sector)
        print(f"✅ Created: {sector}")
        
        # Read
        print("\n2. Reading sector...")
        sector_read = db.query(Sector).filter_by(code="BANK").first()
        print(f"✅ Read: {sector_read}")
        print(f"   Momentum: {sector_read.momentum_30d}%")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        db.rollback()
        return False
    finally:
        db.close()


def test_stock_crud():
    """Test Stock CRUD operations"""
    print("\n" + "="*60)
    print("Testing Stock Model...")
    print("="*60)
    
    db = SessionLocal()
    
    try:
        # Get sector
        sector = db.query(Sector).filter_by(code="BANK").first()
        
        # Create
        print("\n1. Creating stock...")
        stock = Stock(
            symbol="NABIL",
            name="Nabil Bank Limited",
            sector_id=sector.id if sector else None,
            is_active=True,
            is_tradeable=True,
            ltp=1200.0,
            previous_close=1180.0,
            change=20.0,
            change_percent=1.69,
            volume=50000.0,
            beta=1.1,
            volatility=0.025
        )
        db.add(stock)
        db.commit()
        db.refresh(stock)
        print(f"✅ Created: {stock}")
        
        # Read with relationship
        print("\n2. Reading stock with sector...")
        stock_read = db.query(Stock).filter_by(symbol="NABIL").first()
        print(f"✅ Read: {stock_read}")
        if stock_read.sector:
            print(f"   Sector: {stock_read.sector.name}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        db.rollback()
        return False
    finally:
        db.close()


def test_stock_ohlcv_crud():
    """Test StockOHLCV CRUD operations"""
    print("\n" + "="*60)
    print("Testing StockOHLCV Model...")
    print("="*60)
    
    db = SessionLocal()
    
    try:
        # Get stock
        stock = db.query(Stock).filter_by(symbol="NABIL").first()
        
        # Create
        print("\n1. Creating OHLCV data...")
        ohlcv = StockOHLCV(
            stock_id=stock.id,
            date=date.today(),
            open=1180.0,
            high=1220.0,
            low=1175.0,
            close=1200.0,
            volume=50000.0,
            turnover=60000000.0,
            total_trades=500
        )
        db.add(ohlcv)
        db.commit()
        db.refresh(ohlcv)
        print(f"✅ Created: {ohlcv}")
        
        # Read
        print("\n2. Reading OHLCV data...")
        ohlcv_read = db.query(StockOHLCV).filter_by(stock_id=stock.id).first()
        print(f"✅ Read: OHLCV for {ohlcv_read.stock.symbol}")
        print(f"   O: {ohlcv_read.open}, H: {ohlcv_read.high}, L: {ohlcv_read.low}, C: {ohlcv_read.close}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        db.rollback()
        return False
    finally:
        db.close()


def test_signal_crud():
    """Test Signal CRUD operations"""
    print("\n" + "="*60)
    print("Testing Signal Model...")
    print("="*60)
    
    db = SessionLocal()
    
    try:
        # Get stock
        stock = db.query(Stock).filter_by(symbol="NABIL").first()
        
        # Create
        print("\n1. Creating signal...")
        signal = Signal(
            stock_id=stock.id,
            signal_type=SignalType.BUY,
            status=SignalStatus.ACTIVE,
            entry_price=1200.0,
            stop_loss=1140.0,
            take_profit_1=1260.0,
            take_profit_2=1320.0,
            confidence_score=0.75,
            sector_score=0.8,
            liquidity_score=0.7,
            signal_reason="Strong sector momentum with volume spike"
        )
        db.add(signal)
        db.commit()
        db.refresh(signal)
        print(f"✅ Created: {signal}")
        
        # Read
        print("\n2. Reading signal...")
        signal_read = db.query(Signal).filter_by(stock_id=stock.id).first()
        print(f"✅ Read: {signal_read.signal_type.value} signal for {signal_read.stock.symbol}")
        print(f"   Entry: {signal_read.entry_price}, SL: {signal_read.stop_loss}")
        print(f"   Confidence: {signal_read.confidence_score}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        db.rollback()
        return False
    finally:
        db.close()


def test_pattern_crud():
    """Test Pattern CRUD operations"""
    print("\n" + "="*60)
    print("Testing Pattern Model...")
    print("="*60)
    
    db = SessionLocal()
    
    try:
        # Get stock
        stock = db.query(Stock).filter_by(symbol="NABIL").first()
        
        # Create
        print("\n1. Creating pattern...")
        pattern = Pattern(
            stock_id=stock.id,
            pattern_type=PatternType.SUPPORT,
            status=PatternStatus.CONFIRMED,
            pattern_name="Support Level",
            description="Strong support at 1150",
            level_1=1150.0,
            strength=0.85,
            touches=5,
            duration_days=30,
            first_detected=date.today()
        )
        db.add(pattern)
        db.commit()
        db.refresh(pattern)
        print(f"✅ Created: {pattern}")
        
        # Read
        print("\n2. Reading pattern...")
        pattern_read = db.query(Pattern).filter_by(stock_id=stock.id).first()
        print(f"✅ Read: {pattern_read.pattern_type.value} for {pattern_read.stock.symbol}")
        print(f"   Level: {pattern_read.level_1}, Strength: {pattern_read.strength}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        db.rollback()
        return False
    finally:
        db.close()


def print_summary():
    """Print database summary"""
    print("\n" + "="*60)
    print("Database Summary")
    print("="*60)
    
    db = SessionLocal()
    
    try:
        bot_configs = db.query(BotConfiguration).count()
        sectors = db.query(Sector).count()
        stocks = db.query(Stock).count()
        ohlcv = db.query(StockOHLCV).count()
        signals = db.query(Signal).count()
        patterns = db.query(Pattern).count()
        
        print(f"\n📊 Record Counts:")
        print(f"   Bot Configurations: {bot_configs}")
        print(f"   Sectors: {sectors}")
        print(f"   Stocks: {stocks}")
        print(f"   OHLCV Records: {ohlcv}")
        print(f"   Signals: {signals}")
        print(f"   Patterns: {patterns}")
        
    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        db.close()


def main():
    """Run all tests"""
    print("\n" + "="*60)
    print("DAY 2: DATABASE MODELS & SCHEMA TESTING")
    print("="*60)
    
    tests = [
        ("Database Connection", test_database_connection),
        ("BotConfiguration CRUD", test_bot_configuration_crud),
        ("Sector CRUD", test_sector_crud),
        ("Stock CRUD", test_stock_crud),
        ("StockOHLCV CRUD", test_stock_ohlcv_crud),
        ("Signal CRUD", test_signal_crud),
        ("Pattern CRUD", test_pattern_crud),
    ]
    
    results = []
    
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"\n❌ {test_name} failed with error: {e}")
            results.append((test_name, False))
    
    # Print summary
    print_summary()
    
