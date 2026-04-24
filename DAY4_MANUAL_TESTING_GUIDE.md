# Day 4 Manual Testing Guide: Technical Indicators

This guide provides step-by-step instructions for manually testing the technical indicator functionality.

---

## Prerequisites

1. **Server Running:**

   ```bash
   python app/main.py
   ```

2. **Database with OHLCV Data:**
   - You need stock OHLCV data in the database
   - If you don't have data, run Day 3 data fetching first:

     ```bash
     # Fetch market data and stocks
     curl -X POST http://localhost:8000/api/v1/data/fetch-market
     curl -X POST http://localhost:8000/api/v1/data/fetch-stocks

     # Fetch OHLCV for a stock (e.g., NABIL)
     curl -X POST http://localhost:8000/api/v1/data/fetch-ohlcv/NABIL?days=200
     ```

---

## Testing via Swagger UI

### Step 1: Access Swagger UI

1. Open browser: `http://localhost:8000/docs`
2. You should see the API documentation with a new "Indicators" section

### Step 2: Test Get All Indicators

1. **Expand:** `GET /api/v1/indicators/{symbol}`
2. **Click:** "Try it out"
3. **Enter:**
   - symbol: `NABIL` (or any stock with OHLCV data)
   - days: `200`
4. **Click:** "Execute"

**Expected Response:**

```json
{
  "success": true,
  "symbol": "NABIL",
  "data_points": 200,
  "date_range": {
    "start": "2024-06-01",
    "end": "2024-12-28"
  },
  "current_price": 1234.56,
  "indicators": {
    "moving_averages": {
      "sma": {
        "sma_5": { "current": 1230.45, "values": [...] },
        "sma_10": { "current": 1225.30, "values": [...] },
        ...
      },
      "ema": {...},
      "wma": {...},
      "crossovers": {...},
      "trends": {...}
    },
    "momentum": {
      "rsi": {
        "current": 55.23,
        "values": [...],
        "signals": {
          "current_rsi": 55.23,
          "condition": "neutral"
        }
      },
      "macd": {...},
      "stochastic": {...},
      "roc": {...},
      "cci": {...}
    },
    "volatility": {
      "atr": {...},
      "bollinger_bands": {...},
      "std_dev": {...},
      "historical_volatility": {...}
    },
    "volume": {
      "obv": {...},
      "volume_sma": {...},
      "mfi": {...},
      ...
    }
  },
  "calculated_at": "2024-12-28T13:00:00"
}
```

### Step 3: Test Indicator Summary

1. **Expand:** `GET /api/v1/indicators/{symbol}/summary`
2. **Click:** "Try it out"
3. **Enter:** symbol: `NABIL`
4. **Click:** "Execute"

**Expected Response:**

```json
{
  "success": true,
  "symbol": "NABIL",
  "current_price": 1234.56,
  "date": "2024-12-28",
  "trend": {
    "sma_20": 1225.3,
    "sma_50": 1210.45,
    "ema_20": 1228.9,
    "price_vs_sma20": "above",
    "price_vs_sma50": "above"
  },
  "momentum": {
    "rsi_14": 55.23,
    "rsi_signal": "neutral",
    "macd": 5.67,
    "macd_signal": 4.23,
    "macd_histogram": 1.44
  },
  "volatility": {
    "atr_14": 45.67,
    "bb_upper": 1280.5,
    "bb_middle": 1225.3,
    "bb_lower": 1170.1,
    "bb_position": "within_bands"
  },
  "volume": {
    "current": 150000,
    "average_20": 120000,
    "volume_ratio": 1.25
  }
}
```

### Step 4: Test Moving Averages Only

1. **Expand:** `GET /api/v1/indicators/{symbol}/moving-averages`
2. **Click:** "Try it out"
3. **Enter:**
   - symbol: `NABIL`
   - days: `100`
   - sma_periods: `10,20,50`
   - ema_periods: `10,20,50`
4. **Click:** "Execute"

**Expected Response:**

```json
{
  "success": true,
  "symbol": "NABIL",
  "data_points": 100,
  "indicators": {
    "sma": {
      "sma_10": { "current": 1230.45, "values": [...] },
      "sma_20": { "current": 1225.30, "values": [...] },
      "sma_50": { "current": 1210.45, "values": [...] }
    },
    "ema": {
      "ema_10": { "current": 1232.10, "values": [...] },
      "ema_20": { "current": 1228.90, "values": [...] },
      "ema_50": { "current": 1215.20, "values": [...] }
    },
    "crossovers": {...},
    "trends": {...}
  }
}
```

### Step 5: Test Momentum Indicators

1. **Expand:** `GET /api/v1/indicators/{symbol}/momentum`
2. **Click:** "Try it out"
3. **Enter:**
   - symbol: `NABIL`
   - days: `100`
   - rsi_period: `14`
   - macd_fast: `12`
   - macd_slow: `26`
4. **Click:** "Execute"

### Step 6: Test Volatility Indicators

1. **Expand:** `GET /api/v1/indicators/{symbol}/volatility`
2. **Click:** "Try it out"
3. **Enter:**
   - symbol: `NABIL`
   - days: `100`
   - atr_period: `14`
   - bb_period: `20`
   - bb_std: `2.0`
4. **Click:** "Execute"

### Step 7: Test Volume Indicators

1. **Expand:** `GET /api/v1/indicators/{symbol}/volume`
2. **Click:** "Try it out"
3. **Enter:**
   - symbol: `NABIL`
   - days: `100`
   - vol_sma_period: `20`
   - mfi_period: `14`
4. **Click:** "Execute"

---

## Testing via cURL

### Get All Indicators

```bash
curl -X GET "http://localhost:8000/api/v1/indicators/NABIL?days=200"
```

### Get Indicator Summary

```bash
curl -X GET "http://localhost:8000/api/v1/indicators/NABIL/summary"
```

### Get Moving Averages

```bash
curl -X GET "http://localhost:8000/api/v1/indicators/NABIL/moving-averages?days=100&sma_periods=10,20,50"
```

### Get Momentum Indicators

```bash
curl -X GET "http://localhost:8000/api/v1/indicators/NABIL/momentum?days=100&rsi_period=14"
```

### Get Volatility Indicators

```bash
curl -X GET "http://localhost:8000/api/v1/indicators/NABIL/volatility?days=100&atr_period=14"
```

### Get Volume Indicators

```bash
curl -X GET "http://localhost:8000/api/v1/indicators/NABIL/volume?days=100&mfi_period=14"
```

---

## Testing via Python

```python
import requests

# Base URL
base_url = "http://localhost:8000/api/v1/indicators"

# Test 1: Get all indicators
response = requests.get(f"{base_url}/NABIL?days=200")
print("All Indicators:", response.json())

# Test 2: Get summary
response = requests.get(f"{base_url}/NABIL/summary")
print("Summary:", response.json())

# Test 3: Get moving averages
response = requests.get(
    f"{base_url}/NABIL/moving-averages",
    params={"days": 100, "sma_periods": "10,20,50"}
)
print("Moving Averages:", response.json())

# Test 4: Get momentum indicators
response = requests.get(
    f"{base_url}/NABIL/momentum",
    params={"days": 100, "rsi_period": 14}
)
print("Momentum:", response.json())
```

---

## Verification Checklist

### ✅ Indicator Calculations

- [ ] **SMA:** Values are correct (simple average)
- [ ] **EMA:** Values show exponential weighting
- [ ] **RSI:** Values between 0-100
- [ ] **MACD:** Has macd, signal, and histogram
- [ ] **Bollinger Bands:** Has upper, middle, lower bands
- [ ] **ATR:** Positive values representing volatility
- [ ] **OBV:** Cumulative volume indicator
- [ ] **MFI:** Values between 0-100

### ✅ API Responses

- [ ] All endpoints return 200 status
- [ ] Response includes `success: true`
- [ ] Current values are present
- [ ] Historical values arrays are included
- [ ] Signals and analysis are provided

### ✅ Error Handling

- [ ] Invalid symbol returns 404
- [ ] Insufficient data returns appropriate error
- [ ] Invalid parameters return 422

---

## Common Issues & Solutions

### Issue 1: "No OHLCV data found"

**Solution:** Fetch OHLCV data first:

```bash
curl -X POST "http://localhost:8000/api/v1/data/fetch-ohlcv/NABIL?days=200"
```

### Issue 2: "Insufficient data for calculation"

**Solution:** Fetch more historical data (at least 200 days recommended)

### Issue 3: Indicators return NaN values

**Cause:** Not enough data points for the indicator period
**Solution:** Ensure you have at least 200 days of OHLCV data

### Issue 4: Slow response time

**Cause:** Calculating many indicators on large datasets
**Solution:**

- Use the summary endpoint for quick analysis
- Reduce the `days` parameter
- Use specific indicator endpoints instead of "all"

---

## Performance Testing

### Test Response Times

```bash
# Time the all indicators endpoint
time curl -X GET "http://localhost:8000/api/v1/indicators/NABIL?days=200"

# Time the summary endpoint (should be faster)
time curl -X GET "http://localhost:8000/api/v1/indicators/NABIL/summary"
```

**Expected Times:**

- Summary: < 1 second
- All indicators (200 days): 1-3 seconds
- Specific indicator category: < 1 second

---

## Database Verification

### Check OHLCV Data

```sql
-- Check if stock exists
SELECT * FROM stocks WHERE symbol = 'NABIL';

-- Check OHLCV data count
SELECT COUNT(*) FROM stock_ohlcv
WHERE stock_id = (SELECT id FROM stocks WHERE symbol = 'NABIL');

-- Check date range
SELECT MIN(date), MAX(date) FROM stock_ohlcv
WHERE stock_id = (SELECT id FROM stocks WHERE symbol = 'NABIL');

-- View recent OHLCV data
SELECT date, open, high, low, close, volume
FROM stock_ohlcv
WHERE stock_id = (SELECT id FROM stocks WHERE symbol = 'NABIL')
ORDER BY date DESC
LIMIT 10;
```

---

## Advanced Testing

### Test Multiple Stocks

```bash
# Test with different stocks
for symbol in NABIL NICA ADBL GBIME; do
    echo "Testing $symbol..."
    curl -X GET "http://localhost:8000/api/v1/indicators/$symbol/summary"
    echo ""
done
```

### Test Different Periods

```bash
# Test with different day ranges
for days in 30 60 100 200; do
    echo "Testing with $days days..."
    curl -X GET "http://localhost:8000/api/v1/indicators/NABIL?days=$days"
    echo ""
done
```

### Test Custom Parameters

```bash
# Test custom RSI period
curl -X GET "http://localhost:8000/api/v1/indicators/NABIL/momentum?rsi_period=7"

# Test custom Bollinger Bands
curl -X GET "http://localhost:8000/api/v1/indicators/NABIL/volatility?bb_period=20&bb_std=3.0"

# Test custom moving averages
curl -X GET "http://localhost:8000/api/v1/indicators/NABIL/moving-averages?sma_periods=5,10,15,20,25"
```

---

## Success Criteria

✅ **All tests pass if:**

1. All 6 API endpoints return successful responses
2. Indicator values are within expected ranges
3. No NaN values in current indicators
4. Response times are acceptable (< 3 seconds)
5. Error handling works correctly
6. Different stocks can be queried
7. Custom parameters work as expected

---

## Next Steps

After successful testing:

1. ✅ Mark Day 4 as complete in TODO.md
2. ✅ Create Day 4 completion report
3. ✅ Proceed to Day 5: Sector Analysis Component

---

**Happy Testing! 🧪**
