# Day 4 Quick Start: Technical Indicators

Quick reference guide for using the technical indicators system.

---

## 🚀 Quick Start

### 1. Start the Server

```bash
python app/main.py
```

### 2. Access Swagger UI

```
http://localhost:8000/docs
```

### 3. Test an Endpoint

```bash
# Get indicator summary (fastest)
curl http://localhost:8000/api/v1/indicators/NABIL/summary

# Get all indicators
curl http://localhost:8000/api/v1/indicators/NABIL?days=200
```

---

## 📊 Available Indicators

### Moving Averages

- SMA (5, 10, 20, 50, 200)
- EMA (5, 10, 20, 50, 200)
- WMA (10, 20)

### Momentum

- RSI (14)
- MACD (12/26/9)
- Stochastic (14/3)
- ROC (12)
- CCI (20)

### Volatility

- ATR (14)
- Bollinger Bands (20, 2σ)
- Standard Deviation (20)
- Historical Volatility (20)
- Keltner Channels (20/10/2)

### Volume

- OBV
- Volume SMA (20)
- Volume ROC (12)
- MFI (14)
- A/D Line
- CMF (20)
- Volume Ratio (20)

---

## 🔗 API Endpoints

### 1. Get All Indicators

```bash
GET /api/v1/indicators/{symbol}?days=200
```

### 2. Get Summary (Recommended for Dashboards)

```bash
GET /api/v1/indicators/{symbol}/summary
```

### 3. Get Moving Averages Only

```bash
GET /api/v1/indicators/{symbol}/moving-averages?days=100
```

### 4. Get Momentum Indicators Only

```bash
GET /api/v1/indicators/{symbol}/momentum?days=100
```

### 5. Get Volatility Indicators Only

```bash
GET /api/v1/indicators/{symbol}/volatility?days=100
```

### 6. Get Volume Indicators Only

```bash
GET /api/v1/indicators/{symbol}/volume?days=100
```

---

## 💡 Usage Examples

### Python

```python
import requests

# Get summary
response = requests.get("http://localhost:8000/api/v1/indicators/NABIL/summary")
data = response.json()

print(f"Current Price: {data['current_price']}")
print(f"RSI: {data['momentum']['rsi_14']}")
print(f"Trend: {data['trend']['price_vs_sma20']}")
```

### JavaScript

```javascript
fetch("http://localhost:8000/api/v1/indicators/NABIL/summary")
  .then((response) => response.json())
  .then((data) => {
    console.log("Current Price:", data.current_price);
    console.log("RSI:", data.momentum.rsi_14);
    console.log("Trend:", data.trend.price_vs_sma20);
  });
```

### cURL

```bash
# Get summary
curl http://localhost:8000/api/v1/indicators/NABIL/summary | jq

# Get specific indicators
curl "http://localhost:8000/api/v1/indicators/NABIL/momentum?rsi_period=14" | jq
```

---

## 🧪 Testing

### Run Automated Tests

```bash
python run_day4_tests.py
```

### Expected Output

```
🎉 ALL TESTS PASSED! Day 4 indicators are working correctly.
```

---

## 📝 Common Use Cases

### 1. Dashboard Display

```bash
# Use summary endpoint for quick overview
curl http://localhost:8000/api/v1/indicators/NABIL/summary
```

### 2. Detailed Analysis

```bash
# Get all indicators with full history
curl http://localhost:8000/api/v1/indicators/NABIL?days=200
```

### 3. Custom Parameters

```bash
# Custom RSI period
curl "http://localhost:8000/api/v1/indicators/NABIL/momentum?rsi_period=7"

# Custom Bollinger Bands
curl "http://localhost:8000/api/v1/indicators/NABIL/volatility?bb_period=20&bb_std=3.0"
```

### 4. Multiple Stocks

```bash
# Loop through stocks
for symbol in NABIL NICA ADBL; do
    curl http://localhost:8000/api/v1/indicators/$symbol/summary
done
```

---

## ⚡ Performance Tips

1. **Use Summary Endpoint** for dashboards (< 1 second)
2. **Use Category Endpoints** for specific analysis
3. **Limit Days Parameter** for faster responses
4. **Cache Results** on client side if needed

---

## 🔍 Interpreting Indicators

### RSI (Relative Strength Index)

- **> 70:** Overbought (potential sell signal)
- **< 30:** Oversold (potential buy signal)
- **50:** Neutral

### MACD

- **Histogram > 0:** Bullish momentum
- **Histogram < 0:** Bearish momentum
- **Crossover:** Potential trend change

### Bollinger Bands

- **Price near upper band:** Overbought
- **Price near lower band:** Oversold
- **Bands squeeze:** Low volatility (breakout coming)

### Volume

- **Volume > Average:** Strong move
- **Volume < Average:** Weak move
- **OBV rising:** Accumulation

---

## 🐛 Troubleshooting

### "No OHLCV data found"

```bash
# Fetch data first
curl -X POST "http://localhost:8000/api/v1/data/fetch-ohlcv/NABIL?days=200"
```

### "Insufficient data for calculation"

- Ensure you have at least 200 days of OHLCV data
- Some indicators need more data (e.g., SMA 200)

### Slow Response

- Use summary endpoint instead of all indicators
- Reduce days parameter
- Use category-specific endpoints

---

## 📚 Documentation

- **Full Guide:** `DAY4_MANUAL_TESTING_GUIDE.md`
- **Completion Report:** `DAY4_COMPLETION_REPORT.md`
- **Swagger UI:** `http://localhost:8000/docs`
- **ReDoc:** `http://localhost:8000/redoc`

---

## ✅ Quick Checklist

- [ ] Server is running
- [ ] OHLCV data is available
- [ ] Can access Swagger UI
- [ ] Summary endpoint works
- [ ] All indicators calculate correctly

---

**Ready to analyze! 📊**
