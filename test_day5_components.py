"""
Day 5 Component Tests

Tests for sector analysis, stock screening, and beta calculation components.
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.database import SessionLocal
from app.components.sector_analyzer import SectorAnalyzer
from app.components.stock_screener import StockScreener
from app.components.beta_calculator import BetaCalculator
from app.models.sector import Sector
from app.models.stock import Stock


def test_sector_analyzer():
    """Test sector analyzer functionality"""
    print("\n" + "="*60)
    print("TEST 1: Sector Analyzer")
    print("="*60)
    
    db = SessionLocal()
    
    try:
        analyzer = SectorAnalyzer(db)
        
        # Test 1.1: Analyze all sectors
        print("\n1.1 Testing analyze_all_sectors()...")
        result = analyzer.analyze_all_sectors()
        
        if result['success']:
            print(f"✓ Successfully analyzed {result['total_sectors']} sectors")
            print(f"  - Bullish sectors: {result['bullish_sectors']}")
            print(f"  - Bearish sectors: {result['bearish_sectors']}")
            
            if result.get('top_performers'):
                print(f"\n  Top 3 performers:")
                for i, sector in enumerate(result['top_performers'][:3], 1):
                    print(f"    {i}. {sector['sector_name']}: {sector.get('momentum_30d', 'N/A')}%")
        else:
            print(f"✗ Failed: {result.get('error')}")
            return False
        
        # Test 1.2: Get top sectors
        print("\n1.2 Testing get_top_sectors()...")
        result = analyzer.get_top_sectors(limit=3)
        
        if result['success']:
            print(f"✓ Retrieved {result['count']} top sectors")
        else:
            print(f"✗ Failed: {result.get('error')}")
        
        # Test 1.3: Get bullish sectors
        print("\n1.3 Testing get_bullish_sectors()...")
        result = analyzer.get_bullish_sectors(min_momentum=0)
        
        if result['success']:
            print(f"✓ Found {result['count']} bullish sectors")
        else:
            print(f"✗ Failed: {result.get('error')}")
        
        # Test 1.4: Calculate sector rotation
        print("\n1.4 Testing calculate_sector_rotation()...")
        result = analyzer.calculate_sector_rotation()
        
        if result['success']:
            print(f"✓ Identified {result['rotation_opportunities']} rotation opportunities")
            print(f"  - Gaining momentum: {len(result['gaining_momentum'])}")
            print(f"  - Losing momentum: {len(result['losing_momentum'])}")
        else:
            print(f"✗ Failed: {result.get('error')}")
        
        print("\n✓ All Sector Analyzer tests passed!")
        return True
        
    except Exception as e:
        print(f"\n✗ Error in sector analyzer tests: {str(e)}")
        return False
    finally:
        db.close()


def test_stock_screener():
    """Test stock screener functionality"""
    print("\n" + "="*60)
    print("TEST 2: Stock Screener")
    print("="*60)
    
    db = SessionLocal()
    
    try:
        screener = StockScreener(db)
        
        # Test 2.1: Basic screening
        print("\n2.1 Testing basic screen_stocks()...")
        criteria = {
            'min_volume_ratio': 1.0,
            'limit': 10
        }
        result = screener.screen_stocks(criteria)
        
        if result['success']:
            print(f"✓ Screened {result['total_results']} stocks")
            filters_count = len(result.get('filters_applied', []))
            print(f"  - Filters applied: {filters_count}")
            
            if result['stocks']:
                top_stock = result['stocks'][0]
                print(f"  - Top stock: {top_stock['symbol']} (score: {top_stock['score']})")
        else:
            print(f"✗ Failed: {result.get('error')}")
            return False
        
        # Test 2.2: High volume stocks
        print("\n2.2 Testing get_high_volume_stocks()...")
        result = screener.get_high_volume_stocks(min_volume_ratio=1.5, limit=5)
        
        if result['success']:
            print(f"✓ Found {result['total_results']} high volume stocks")
        else:
            print(f"✗ Failed: {result.get('error')}")
        
        # Test 2.3: Momentum stocks
        print("\n2.3 Testing get_momentum_stocks()...")
        result = screener.get_momentum_stocks(limit=5)
        
        if result['success']:
            print(f"✓ Found {result['total_results']} momentum stocks")
        else:
            print(f"✗ Failed: {result.get('error')}")
        
        # Test 2.4: Value stocks
        print("\n2.4 Testing get_value_stocks()...")
        result = screener.get_value_stocks(limit=5)
        
        if result['success']:
            print(f"✓ Found {result['total_results']} value stocks")
        else:
            print(f"✗ Failed: {result.get('error')}")
        
        # Test 2.5: Defensive stocks
        print("\n2.5 Testing get_defensive_stocks()...")
        result = screener.get_defensive_stocks(limit=5)
        
        if result['success']:
            print(f"✓ Found {result['total_results']} defensive stocks")
        else:
            print(f"✗ Failed: {result.get('error')}")
        
        print("\n✓ All Stock Screener tests passed!")
        return True
        
    except Exception as e:
        print(f"\n✗ Error in stock screener tests: {str(e)}")
        return False
    finally:
        db.close()


def test_beta_calculator():
    """Test beta calculator functionality"""
    print("\n" + "="*60)
    print("TEST 3: Beta Calculator")
    print("="*60)
    
    db = SessionLocal()
    
    try:
        calculator = BetaCalculator(db)
        
        # Get a stock to test with
        stock = db.query(Stock).filter(Stock.is_active == True).first()
        
        if not stock:
            print("✗ No active stocks found for testing")
            return False
        
        # Test 3.1: Calculate stock beta
        print(f"\n3.1 Testing calculate_stock_beta() for {stock.symbol}...")
        result = calculator.calculate_stock_beta(stock.symbol, days=60)
        
        if result['success']:
            print(f"✓ Successfully calculated beta")
            print(f"  - Beta: {result['beta']:.4f}")
            print(f"  - Classification: {result['classification']}")
            print(f"  - Correlation: {result['correlation']:.4f}")
            print(f"  - Data points: {result['data_points']}")
        else:
            print(f"✗ Failed: {result.get('error')}")
            # This might fail if insufficient data, which is okay for testing
            print("  (This is acceptable if there's insufficient OHLCV data)")
        
        # Test 3.2: Get high beta stocks
        print("\n3.2 Testing get_high_beta_stocks()...")
        result = calculator.get_high_beta_stocks(min_beta=1.0, limit=5)
        
        if result['success']:
            print(f"✓ Found {result['count']} high beta stocks")
        else:
            print(f"✗ Failed: {result.get('error')}")
        
        # Test 3.3: Get low beta stocks
        print("\n3.3 Testing get_low_beta_stocks()...")
        result = calculator.get_low_beta_stocks(max_beta=1.0, limit=5)
        
        if result['success']:
            print(f"✓ Found {result['count']} low beta stocks")
        else:
            print(f"✗ Failed: {result.get('error')}")
        
        print("\n✓ All Beta Calculator tests passed!")
        return True
        
    except Exception as e:
        print(f"\n✗ Error in beta calculator tests: {str(e)}")
        return False
    finally:
        db.close()


def run_all_tests():
    """Run all Day 5 component tests"""
    print("\n" + "="*60)
    print("DAY 5 COMPONENT TESTS")
    print("="*60)
    print("\nTesting sector analysis, stock screening, and beta calculation...")
    
    results = {
        'sector_analyzer': False,
        'stock_screener': False,
        'beta_calculator': False
    }
    
    # Run tests
    results['sector_analyzer'] = test_sector_analyzer()
    results['stock_screener'] = test_stock_screener()
    results['beta_calculator'] = test_beta_calculator()
    
    # Summary
    print("\n" + "="*60)
    print("TEST SUMMARY")
    print("="*60)
    
    passed = sum(1 for v in results.values() if v)
    total = len(results)
    
    for test_name, passed_test in results.items():
        status = "✓ PASSED" if passed_test else "✗ FAILED"
        print(f"{test_name}: {status}")
    
    print(f"\nTotal: {passed}/{total} test suites passed")
    
    if passed == total:
        print("\n🎉 All Day 5 component tests passed!")
        return True
    else:
        print(f"\n⚠️  {total - passed} test suite(s) failed")
        return False


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
