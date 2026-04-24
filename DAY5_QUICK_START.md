# 🚀 DAY 5 QUICK START: Sector Analysis & Stock Screening

## Quick Overview

Day 5 implements sector analysis and stock screening components with 14 API endpoints.

---

## 🎯 What's Available

### Components

1. **Sector Analyzer** - Analyze sector performance and rotation
2. **Stock Screener** - Multi-criteria stock filtering
3. **Beta Calculator** - Calculate systematic risk

### API Endpoints

- **7 Sector Analysis endpoints**
- **7 Stock Screening endpoints**

---

## 🚀 Quick Start

### 1. Run Tests

```bash
# Run all Day 5 tests
python run_day5_tests.py

# Or run directly
python test_day5_components.py
```

### 2. Start the Server

```bash
# Activate virtual environment
source venv/bin/activate  # On macOS/Linux
# or
venv\Scripts\activate  # On Windows

# Start server
uvicorn app.main:app --reload
```

### 3. Access API Documentation

Open in browser:

- **Swagger UI:** http://localhost:8000/docs
- **ReDoc:** http://localhost:8000/redoc

---

## 📡 API Endpoints

### Sector Analysis

```bash
# Get all sectors
GET /api/v1/sectors/

# Get sector details
GET /api/v1/sectors/{sector_id}

# Get stocks in sector
GET /api/v1/sectors/{sector_id}/stocks

# Get top performers
GET /api/v1/sectors/top-performers?limit=5

# Get complete analysis
GET /api/v1/sectors/analysis/complete

# Get sector rotation
GET /api/v1/sectors/analysis/rotation

# Get bullish sectors
GET /api/v1/sectors/analysis/bullish?min_momentum=5.0
```

### Stock Screening

```bash
# Custom screening
POST /api/v1/stocks/screen
{
  "min_volume_ratio": 1.5,
  "max_beta": 1.5,
  "min_rsi": 30,
  "max_rsi": 70,
  "price_above_sma20": true,
  "limit": 20
}

# High volume stocks
GET /api/v1/stocks/screen/high-volume?min_volume_ratio=2.0&limit=20

# Momentum stocks
GET /api/v1/stocks/screen/momentum?limit=20

# Value stocks
GET /api/v1/stocks/screen/value?limit=20

# Defensive stocks
GET /api/v1/stocks/screen/defensive?limit=20

# Growth stocks
GET /api/v1/stocks/screen/growth?limit=20

# Oversold stocks
GET /api/v1/stocks/screen/oversold?limit=20
```

### Beta Calculation

```bash
# Calculate stock beta
GET /api/v1/stocks/{symbol}/beta?days=90

# High beta stocks
GET /api/v1/stocks/beta/high?min_beta=1.2&limit=20

# Low beta stocks
GET /api/v1/stocks/beta/low?max_beta=0.8&limit=20
```

---

## 💻 Python Usage

### Sector Analysis

```python
from app.database import SessionLocal
from app.components.sector_analyzer import SectorAnalyzer

db = SessionLocal()
analyzer = SectorAnalyzer(db)

# Analyze all sectors
result = analyzer.analyze_all_sectors()
print(f"Total sectors: {result['total_sectors']}")
print(f"Bullish sectors: {result['bullish_sectors']}")

# Get top performers
top = analyzer.get_top_sectors(limit=5)
for sector in top['sectors']:
    print(f"{sector['sector_name']}: {sector['momentum_30d']}%")

# Calculate sector rotation
rotation = analyzer.calculate_sector_rotation()
print(f"Rotation opportunities: {rotation['rotation_opportunities']}")

db.close()
```

### Stock Screening

```python
from app.database import SessionLocal
from app.components.stock_screener import StockScreener

db = SessionLocal()
screener = StockScreener(db)

# Custom screening
criteria = {
    'min_volume_ratio': 1.5,
    'max_beta': 1.5,
    'min_rsi': 30,
    'max_rsi': 70,
    'price_above_sma20': True,
    'limit': 20
}
result = screener.screen_stocks(criteria)

for stock in result['stocks']:
    print(f"{stock['symbol']}: Score {stock['score']}")

# Pre-built strategies
momentum = screener.get_momentum_stocks(limit=10)
value = screener.get_value_stocks(limit=10)
defensive = screener.get_defensive_stocks(limit=10)

db.close()
```

### Beta Calculation

```python
from app.database import SessionLocal
from app.components.beta_calculator import BetaCalculator

db = SessionLocal()
calculator = BetaCalculator(db)

# Calculate stock beta
result = calculator.calculate_stock_beta('NABIL', days=90)
if result['success']:
    print(f"Beta: {result['beta']:.4f}")
    print(f"Classification: {result['classification']}")
    print(f"Correlation: {result['correlation']:.4f}")

# Get high beta stocks
high_beta = calculator.get_high_beta_stocks(min_beta=1.2, limit=10)
for stock in high_beta['stocks']:
    print(f"{stock['symbol']}: Beta {stock['beta']:.4f}")

db.close()
```

---

## 🎯 Common Use Cases

### 1. Find Stocks in Bullish Sectors

```python
# Get bullish sectors
bullish = analyzer.get_bullish_sectors(min_momentum=5.0)

# Screen stocks in those sectors
sector_ids = [s['sector_id'] for s in bullish['sectors']]
criteria = {
    'sector_ids': sector_ids,
    'min_volume_ratio': 1.5,
    'price_above_sma20': True,
    'limit': 20
}
stocks = screener.screen_stocks(criteria)
```

### 2. Find Momentum Stocks with Low Risk

```python
criteria = {
    'price_above_sma20': True,
    'price_above_sma50': True,
    'min_rsi': 50,
    'max_rsi': 70,
    'macd_bullish': True,
    'max_beta': 1.2,  # Lower risk
    'limit': 20
}
stocks = screener.screen_stocks(criteria)
```

### 3. Identify Sector Rotation

```python
rotation = analyzer.calculate_sector_rotation()

# Sectors gaining momentum (buy)
for sector in rotation['gaining_momentum'][:5]:
    print(f"BUY: {sector['sector_name']} (+{sector['momentum_change']:.2f}%)")

# Sectors losing momentum (sell)
for sector in rotation['losing_momentum'][:5]:
    print(f"SELL: {sector['sector_name']} ({sector['momentum_change']:.2f}%)")
```

### 4. Find Defensive Stocks for Bear Market

```python
# Low beta + dividend yield
criteria = {
    'max_beta': 0.8,
    'min_dividend_yield': 2.0,
    'min_roe': 10,
    'limit': 20
}
defensive = screener.screen_stocks(criteria)
```

---

## 📊 Screening Criteria Reference

### Volume Filters

- `min_volume_ratio`: Minimum volume/avg volume ratio
- Example: `1.5` = 50% above average

### Beta Filters

- `min_beta`: Minimum beta (e.g., 0.5)
- `max_beta`: Maximum beta (e.g., 1.5)

### Sector Filters

- `bullish_sector_only`: Only stocks in bullish sectors
- `sector_ids`: List of specific sector IDs

### Technical Filters

- `min_rsi`: Minimum RSI (e.g., 30)
- `max_rsi`: Maximum RSI (e.g., 70)
- `price_above_sma20`: Price above 20-day SMA
- `price_above_sma50`: Price above 50-day SMA
- `macd_bullish`: MACD above signal line

### Fundamental Filters

- `min_pe_ratio`: Minimum P/E ratio
- `max_pe_ratio`: Maximum P/E ratio
- `min_roe`: Minimum ROE percentage
- `min_dividend_yield`: Minimum dividend yield

### Price Filters

- `min_price`: Minimum stock price
- `max_price`: Maximum stock price

### Other

- `limit`: Maximum number of results

---

## 🎯 Pre-built Screening Strategies

### 1. High Volume (Liquidity Hunters)

- Volume ratio > 2.0
- Good for day trading

### 2. Momentum Stocks

- Price > SMA20 and SMA50
- RSI 50-70
- MACD bullish
- Volume > average

### 3. Value Stocks

- P/E < 20
- ROE > 15%
- Dividend yield > 2%

### 4. Defensive Stocks

- Beta < 0.8
- Dividend yield > 1%
- Low volatility

### 5. Growth Stocks

- ROE > 20%
- In bullish sector
- Strong momentum

### 6. Oversold Stocks

- RSI < 30
- In bullish sector
- Above average volume

---

## 🔍 Response Format

### Sector Analysis Response

```json
{
  "success": true,
  "total_sectors": 10,
  "bullish_sectors": 6,
  "bearish_sectors": 2,
  "sectors": [...],
  "top_performers": [...],
  "worst_performers": [...]
}
```

### Stock Screening Response

```json
{
  "success": true,
  "filters_applied": ["volume_ratio >= 1.5", "beta <= 1.5"],
  "total_results": 15,
  "stocks": [
    {
      "symbol": "NABIL",
      "name": "Nabil Bank Limited",
      "sector": "Banking",
      "ltp": 850.0,
      "change_percent": 2.5,
      "volume_ratio": 1.8,
      "beta": 1.2,
      "rsi_14": 55.0,
      "score": 75.5
    }
  ]
}
```

### Beta Calculation Response

```json
{
  "success": true,
  "symbol": "NABIL",
  "beta": 1.15,
  "correlation": 0.85,
  "r_squared": 0.72,
  "alpha": 0.02,
  "classification": "neutral",
  "stock_volatility": 25.5,
  "market_volatility": 22.0,
  "data_points": 90
}
```

---

## 🎉 Summary

Day 5 provides powerful tools for:

- ✅ Sector analysis and rotation detection
- ✅ Multi-criteria stock screening
- ✅ Risk assessment via beta calculation
- ✅ Pre-built screening strategies
- ✅ Flexible filtering and scoring

**Ready to use for stock selection and portfolio management!**

---

For detailed documentation, see `DAY5_COMPLETION_REPORT.md`
