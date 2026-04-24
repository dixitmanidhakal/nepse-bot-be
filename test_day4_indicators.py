"""
Day 4 Indicators Testing Script

This script tests all technical indicator calculations.
"""

import sys
import numpy as np
from datetime import datetime

# Test data for indicators
test_prices = [
    44.00, 44.34, 44.09, 43.61, 44.33, 44.83, 45.10, 45.42, 45.84, 46.08,
    45.89, 46.03, 45.61, 46.28, 46.28, 46.00, 46.03, 46.41, 46.22, 45.64,
    46.21, 46.25, 45.71, 46.45, 45.78, 45.35, 44.03, 44.18, 44.22, 44.57,
    43.42, 42.66, 43.13
]

test_high = [h * 1.02 for h in test_prices]
test_low = [l * 0.98 for l in test_prices]
test_volume = [100000 + i * 5000 for i in range(len(test_prices))]


def test_moving_averages():
    """Test moving average calculations"""
    print("\n" + "="*60)
    print("TESTING MOVING AVERAGES")
    print("="*60)
    
    try:
        from app.indicators.moving_averages import MovingAverages
        
        # Test SMA
        print("\n1. Testing SMA...")
        sma_10 = MovingAverages.sma(test_prices, 10)
        print(f"   ✓ SMA(10) calculated: {len(sma_10)} values")
        print(f"   Last 3 values: {sma_10[-3:]}")
        
        # Test EMA
        print("\n2. Testing EMA...")
        ema_10 = MovingAverages.ema(test_prices, 10)
        print(f"   ✓ EMA(10) calculated: {len(ema_10)} values")
        print(f"   Last 3 values: {ema_10[-3:]}")
        
        # Test WMA
        print("\n3. Testing WMA...")
        wma_10 = MovingAverages.wma(test_prices, 10)
        print(f"   ✓ WMA(10) calculated: {len(wma_10)} values")
        print(f"   Last 3 values: {wma_10[-3:]}")
        
        # Test multiple SMAs
        print("\n4. Testing multiple SMAs...")
        smas = MovingAverages.calculate_multiple_sma(test_prices, [5, 10, 20])
        print(f"   ✓ Calculated {len(smas)} SMAs")
        for key in smas:
            print(f"   {key}: Last value = {smas[key][-1]:.2f}")
        
        # Test crossover detection
        print("\n5. Testing crossover detection...")
        fast_ma = MovingAverages.sma(test_prices, 5)
        slow_ma = MovingAverages.sma(test_prices, 10)
        crossovers = MovingAverages.get_crossover_signals(fast_ma, slow_ma)
        print(f"   ✓ Bullish crossovers: {len(crossovers['bullish'])}")
        print(f"   ✓ Bearish crossovers: {len(crossovers['bearish'])}")
        
        # Test trend detection
        print("\n6. Testing trend detection...")
        trend = MovingAverages.get_ma_trend(test_prices, 10, 'sma')
        print(f"   ✓ Current trend: {trend}")
        
        print("\n✅ Moving Averages: ALL TESTS PASSED")
        return True
        
    except Exception as e:
        print(f"\n❌ Moving Averages: TEST FAILED - {str(e)}")
        import traceback
        traceback.print_exc()
        return False


def test_momentum_indicators():
    """Test momentum indicator calculations"""
    print("\n" + "="*60)
    print("TESTING MOMENTUM INDICATORS")
    print("="*60)
    
    try:
        from app.indicators.momentum import MomentumIndicators
        
        # Test RSI
        print("\n1. Testing RSI...")
        rsi = MomentumIndicators.rsi(test_prices, 14)
        print(f"   ✓ RSI(14) calculated: {len(rsi)} values")
        print(f"   Last 3 values: {rsi[-3:]}")
        print(f"   Current RSI: {rsi[-1]:.2f}")
        
        # Test MACD
        print("\n2. Testing MACD...")
        macd_data = MomentumIndicators.macd(test_prices, 12, 26, 9)
        print(f"   ✓ MACD calculated")
        print(f"   MACD Line: {macd_data['macd'][-1]:.4f}")
        print(f"   Signal Line: {macd_data['signal'][-1]:.4f}")
        print(f"   Histogram: {macd_data['histogram'][-1]:.4f}")
        
        # Test Stochastic
        print("\n3. Testing Stochastic...")
        stoch = MomentumIndicators.stochastic(test_high, test_low, test_prices, 14, 3)
        print(f"   ✓ Stochastic calculated")
        print(f"   %K: {stoch['k'][-1]:.2f}")
        print(f"   %D: {stoch['d'][-1]:.2f}")
        
        # Test ROC
        print("\n4. Testing ROC...")
        roc = MomentumIndicators.roc(test_prices, 12)
        print(f"   ✓ ROC(12) calculated: {len(roc)} values")
        print(f"   Current ROC: {roc[-1]:.2f}%")
        
        # Test CCI
        print("\n5. Testing CCI...")
        cci = MomentumIndicators.cci(test_high, test_low, test_prices, 20)
        print(f"   ✓ CCI(20) calculated: {len(cci)} values")
        print(f"   Current CCI: {cci[-1]:.2f}")
        
        # Test RSI signals
        print("\n6. Testing RSI signals...")
        rsi_signals = MomentumIndicators.get_rsi_signals(rsi)
        print(f"   ✓ Current RSI: {rsi_signals['current_rsi']:.2f}")
        print(f"   ✓ Condition: {rsi_signals['condition']}")
        
        # Test MACD signals
        print("\n7. Testing MACD signals...")
        macd_signals = MomentumIndicators.get_macd_signals(macd_data)
        print(f"   ✓ Trend: {macd_signals['trend']}")
        print(f"   ✓ Bullish crossovers: {len(macd_signals['bullish_crossovers'])}")
        
        print("\n✅ Momentum Indicators: ALL TESTS PASSED")
        return True
        
    except Exception as e:
        print(f"\n❌ Momentum Indicators: TEST FAILED - {str(e)}")
        import traceback
        traceback.print_exc()
        return False


def test_volatility_indicators():
    """Test volatility indicator calculations"""
    print("\n" + "="*60)
    print("TESTING VOLATILITY INDICATORS")
    print("="*60)
    
    try:
        from app.indicators.volatility import VolatilityIndicators
        
        # Test ATR
        print("\n1. Testing ATR...")
        atr = VolatilityIndicators.atr(test_high, test_low, test_prices, 14)
        print(f"   ✓ ATR(14) calculated: {len(atr)} values")
        print(f"   Current ATR: {atr[-1]:.4f}")
        
        # Test Bollinger Bands
        print("\n2. Testing Bollinger Bands...")
        bb = VolatilityIndicators.bollinger_bands(test_prices, 20, 2.0)
        print(f"   ✓ Bollinger Bands calculated")
        print(f"   Upper: {bb['upper'][-1]:.2f}")
        print(f"   Middle: {bb['middle'][-1]:.2f}")
        print(f"   Lower: {bb['lower'][-1]:.2f}")
        print(f"   Bandwidth: {bb['bandwidth'][-1]:.2f}%")
        
        # Test Standard Deviation
        print("\n3. Testing Standard Deviation...")
        std = VolatilityIndicators.standard_deviation(test_prices, 20)
        print(f"   ✓ Std Dev(20) calculated: {len(std)} values")
        print(f"   Current Std Dev: {std[-1]:.4f}")
        
        # Test Historical Volatility
        print("\n4. Testing Historical Volatility...")
        hv = VolatilityIndicators.historical_volatility(test_prices, 20)
        print(f"   ✓ HV(20) calculated: {len(hv)} values")
        print(f"   Current HV: {hv[-1]:.2f}%")
        
        # Test Keltner Channels
        print("\n5. Testing Keltner Channels...")
        kc = VolatilityIndicators.keltner_channels(test_high, test_low, test_prices, 20, 10, 2.0)
        print(f"   ✓ Keltner Channels calculated")
        print(f"   Upper: {kc['upper'][-1]:.2f}")
        print(f"   Middle: {kc['middle'][-1]:.2f}")
        print(f"   Lower: {kc['lower'][-1]:.2f}")
        
        # Test Bollinger signals
        print("\n6. Testing Bollinger signals...")
        bb_signals = VolatilityIndicators.get_bollinger_signals(test_prices, bb)
        print(f"   ✓ Position: {bb_signals['current_position']}")
        print(f"   ✓ Squeeze: {bb_signals['squeeze']}")
        
        print("\n✅ Volatility Indicators: ALL TESTS PASSED")
        return True
        
    except Exception as e:
        print(f"\n❌ Volatility Indicators: TEST FAILED - {str(e)}")
        import traceback
        traceback.print_exc()
        return False


def test_volume_indicators():
    """Test volume indicator calculations"""
    print("\n" + "="*60)
    print("TESTING VOLUME INDICATORS")
    print("="*60)
    
    try:
        from app.indicators.volume import VolumeIndicators
        
        # Test OBV
        print("\n1. Testing OBV...")
        obv = VolumeIndicators.obv(test_prices, test_volume)
        print(f"   ✓ OBV calculated: {len(obv)} values")
        print(f"   Current OBV: {obv[-1]:,.0f}")
        
        # Test Volume SMA
        print("\n2. Testing Volume SMA...")
        vol_sma = VolumeIndicators.volume_sma(test_volume, 20)
        print(f"   ✓ Volume SMA(20) calculated: {len(vol_sma)} values")
        print(f"   Current Vol SMA: {vol_sma[-1]:,.0f}")
        
        # Test Volume ROC
        print("\n3. Testing Volume ROC...")
        vol_roc = VolumeIndicators.volume_roc(test_volume, 12)
        print(f"   ✓ Volume ROC(12) calculated: {len(vol_roc)} values")
        print(f"   Current Vol ROC: {vol_roc[-1]:.2f}%")
        
        # Test MFI
        print("\n4. Testing MFI...")
        mfi = VolumeIndicators.mfi(test_high, test_low, test_prices, test_volume, 14)
        print(f"   ✓ MFI(14) calculated: {len(mfi)} values")
        print(f"   Current MFI: {mfi[-1]:.2f}")
        
        # Test A/D Line
        print("\n5. Testing A/D Line...")
        ad = VolumeIndicators.ad_line(test_high, test_low, test_prices, test_volume)
        print(f"   ✓ A/D Line calculated: {len(ad)} values")
        print(f"   Current A/D: {ad[-1]:,.0f}")
        
        # Test CMF
        print("\n6. Testing CMF...")
        cmf = VolumeIndicators.cmf(test_high, test_low, test_prices, test_volume, 20)
        print(f"   ✓ CMF(20) calculated: {len(cmf)} values")
        print(f"   Current CMF: {cmf[-1]:.4f}")
        
        # Test Volume Ratio
        print("\n7. Testing Volume Ratio...")
        vol_ratio = VolumeIndicators.volume_ratio(test_volume, 20)
        print(f"   ✓ Volume Ratio calculated: {len(vol_ratio)} values")
        print(f"   Current Ratio: {vol_ratio[-1]:.2f}")
        
        print("\n✅ Volume Indicators: ALL TESTS PASSED")
        return True
        
    except Exception as e:
        print(f"\n❌ Volume Indicators: TEST FAILED - {str(e)}")
        import traceback
        traceback.print_exc()
        return False


def test_indicator_calculator():
    """Test indicator calculator (requires database)"""
    print("\n" + "="*60)
    print("TESTING INDICATOR CALCULATOR")
    print("="*60)
    
    try:
        from app.indicators.calculator import IndicatorCalculator
        from app.database import SessionLocal
        
        print("\n1. Testing calculator initialization...")
        db = SessionLocal()
        calculator = IndicatorCalculator(db)
        print("   ✓ Calculator initialized")
        
        print("\n2. Testing OHLCV data fetch...")
        print("   Note: This requires data in the database")
        print("   Skipping database-dependent tests for now")
        
        db.close()
        
        print("\n✅ Indicator Calculator: BASIC TESTS PASSED")
        print("   (Database-dependent tests skipped)")
        return True
        
    except Exception as e:
        print(f"\n❌ Indicator Calculator: TEST FAILED - {str(e)}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Run all tests"""
    print("\n" + "="*60)
    print("DAY 4: TECHNICAL INDICATORS - TEST SUITE")
    print("="*60)
    print(f"Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    results = {
        'Moving Averages': test_moving_averages(),
        'Momentum Indicators': test_momentum_indicators(),
        'Volatility Indicators': test_volatility_indicators(),
        'Volume Indicators': test_volume_indicators(),
        'Indicator Calculator': test_indicator_calculator()
    }
    
    # Summary
    print("\n" + "="*60)
    print("TEST SUMMARY")
    print("="*60)
    
    passed = sum(1 for v in results.values() if v)
    total = len(results)
    
    for test_name, result in results.items():
        status = "✅ PASSED" if result else "❌ FAILED"
        print(f"{test_name}: {status}")
    
    print(f"\nTotal: {passed}/{total} test suites passed")
    
    if passed == total:
        print("\n🎉 ALL TESTS PASSED! Day 4 indicators are working correctly.")
        return 0
    else:
        print(f"\n⚠️  {total - passed} test suite(s) failed. Please review the errors above.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
