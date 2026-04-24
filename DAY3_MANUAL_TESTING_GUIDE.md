# Day 3 Manual Testing Guide

This guide will help you manually test all Day 3 features through the FastAPI Swagger UI.

## Prerequisites

1. ✅ Database is running (PostgreSQL)
2. ✅ Virtual environment is activated
3. ✅ All dependencies are installed
4. ✅ Database migrations are applied (Day 2)

## Step 1: Start the FastAPI Server

```bash
# Make sure you're in the project directory
cd /Users/dixitmanidhakal/Documents/nepse-bot/nepse-bot-be

# Activate virtual environment (if not already activated)
source venv/bin/activate

# Start the server
python app/main.py
```

The server should start at: `http://localhost:8000`

You should see output like:

```
INFO:     Started server process
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8000
```

## Step 2: Open Swagger UI

Open your browser and navigate to:

```
http://localhost:8000/docs
```

You should see the FastAPI interactive documentation with all endpoints.

## Step 3: Test Each Endpoint

### 3.1 Test Data Status Endpoint

**Endpoint:** `GET /api/v1/data/status`

1. Find the endpoint in Swagger UI
2. Click "Try it out"
3. Click "Execute"
4. Check the response:
   - Should show current data statistics
   - Sectors count
   - Stocks count
   - Latest OHLCV date
   - Database connection status

**Expected Response:**

```json
{
  "status": "success",
  "data_status": {
    "sectors_count": 0,
    "stocks_count": 0,
    "latest_ohlcv_date": null,
    "database_connected": true
  },
  "timestamp": "2024-01-15T10:30:00"
}
```

### 3.2 Test Market Data Fetch

**Endpoint:** `POST /api/v1/data/fetch-market`

1. Find the endpoint in Swagger UI
2. Click "Try it out"
3. Click "Execute"
4. Wait for the response (may take a few seconds)
5. Check the response:
   - Status should be "success" or "partial_success"
   - NEPSE index value
   - Number of sectors updated

**Expected Response:**

```json
{
  "status": "success",
  "message": "Market data fetched. X sectors updated.",
  "nepse_index": 2100.5,
  "sectors_updated": 12,
  "errors": []
}
```

**Note:** Since the NEPSE API client has placeholder implementations, you might see:

- `nepse_index: 0`
- `sectors_updated: 0`
- This is expected! The infrastructure is working, just waiting for real API endpoints.

### 3.3 Test Stock List Fetch

**Endpoint:** `POST /api/v1/data/fetch-stocks`

1. Find the endpoint in Swagger UI
2. Click "Try it out"
3. Click "Execute"
4. Wait for the response
5. Check the response:
   - Number of stocks added
   - Number of stocks updated

**Expected Response:**

```json
{
  "status": "success",
  "message": "Stock data fetched. Added: X, Updated: Y",
  "stocks_added": 10,
  "stocks_updated": 240,
  "errors": []
}
```

### 3.4 Test OHLCV Data Fetch

**Endpoint:** `POST /api/v1/data/fetch-ohlcv/{symbol}`

1. Find the endpoint in Swagger UI
2. Click "Try it out"
3. Enter a stock symbol (e.g., "NABIL")
4. Optionally change the `days` parameter (default: 30)
5. Click "Execute"
6. Check the response:
   - Number of records added
   - Number of records updated
   - Date range

**Parameters:**

- `symbol`: NABIL (or any stock symbol)
- `days`: 30 (number of days to fetch)

**Expected Response:**

```json
{
  "status": "success",
  "message": "OHLCV data fetched for NABIL",
  "symbol": "NABIL",
  "records_added": 30,
  "records_updated": 0,
  "errors": []
}
```

### 3.5 Test Market Depth Fetch

**Endpoint:** `POST /api/v1/data/fetch-market-depth/{symbol}`

1. Find the endpoint in Swagger UI
2. Click "Try it out"
3. Enter a stock symbol (e.g., "NABIL")
4. Click "Execute"
5. Check the response:
   - Market depth data
   - Buy/sell orders
   - Bid-ask spread

**Parameters:**

- `symbol`: NABIL

**Expected Response:**

```json
{
  "status": "success",
  "message": "Market depth fetched for NABIL",
  "symbol": "NABIL",
  "errors": []
}
```

### 3.6 Test Floorsheet Fetch

**Endpoint:** `POST /api/v1/data/fetch-floorsheet`

1. Find the endpoint in Swagger UI
2. Click "Try it out"
3. Optionally enter:
   - `symbol`: Leave empty to fetch all stocks
   - `trade_date`: Leave empty to fetch today's data
4. Click "Execute"
5. Check the response:
   - Number of trades added
   - Total volume
   - Total amount

**Parameters:**

- `symbol`: (optional) NABIL
- `trade_date`: (optional) 2024-01-15

**Expected Response:**

```json
{
  "status": "success",
  "message": "Floorsheet data fetched",
  "symbol": null,
  "trades_added": 150,
  "trades_updated": 0,
  "total_volume": 50000,
  "total_amount": 60000000.0,
  "errors": []
}
```

### 3.7 Test Full Data Fetch (Orchestrated)

**Endpoint:** `POST /api/v1/data/fetch-all`

⚠️ **Warning:** This endpoint may take several minutes to complete!

1. Find the endpoint in Swagger UI
2. Click "Try it out"
3. Configure parameters:
   - `include_ohlcv`: true/false
   - `include_depth`: true/false
   - `include_floorsheet`: true/false
   - `ohlcv_days`: 30
4. Click "Execute"
5. Wait for the response (may take 5-10 minutes)
6. Check the comprehensive response

**Parameters:**

- `include_ohlcv`: true
- `include_depth`: true
- `include_floorsheet`: true
- `ohlcv_days`: 30

**Expected Response:**

```json
{
  "status": "success",
  "start_time": "2024-01-15T10:00:00",
  "end_time": "2024-01-15T10:05:00",
  "duration_seconds": 300,
  "operations": {
    "market_data": {
      "status": "success",
      "nepse_index": 2100.5,
      "sectors_updated": 12
    },
    "stock_data": {
      "status": "success",
      "stocks_added": 10,
      "stocks_updated": 240
    },
    "ohlcv_data": {
      "status": "success",
      "successful": 45,
      "failed": 5
    },
    "market_depth": {
      "status": "success",
      "successful": 48,
      "failed": 2
    },
    "floorsheet": {
      "status": "success",
      "trades_added": 150
    }
  },
  "errors": []
}
```

## Step 4: Verify Data in Database

After testing the endpoints, verify the data was stored correctly:

### Using DBeaver or psql:

```sql
-- Check sectors
SELECT COUNT(*) FROM sectors;
SELECT * FROM sectors LIMIT 5;

-- Check stocks
SELECT COUNT(*) FROM stocks;
SELECT symbol, name, ltp FROM stocks LIMIT 10;

-- Check OHLCV data
SELECT COUNT(*) FROM stock_ohlcv;
SELECT * FROM stock_ohlcv ORDER BY date DESC LIMIT 10;

-- Check market depth
SELECT COUNT(*) FROM market_depth;
SELECT * FROM market_depth ORDER BY timestamp DESC LIMIT 5;

-- Check floorsheet
SELECT COUNT(*) FROM floorsheet;
SELECT * FROM floorsheet ORDER BY trade_time DESC LIMIT 10;
```

## Step 5: Test Error Handling

### Test with Invalid Stock Symbol

1. Try fetching OHLCV for a non-existent stock:
   - Endpoint: `POST /api/v1/data/fetch-ohlcv/INVALID`
   - Should return an error message

### Test with Invalid Parameters

1. Try fetching OHLCV with invalid days:
   - Endpoint: `POST /api/v1/data/fetch-ohlcv/NABIL?days=1000`
   - Should return validation error (max 365 days)

## Step 6: Monitor Logs

While testing, monitor the server logs in the terminal:

```bash
# You should see logs like:
INFO:app.services.data.market_data_service:Fetching market indices from NEPSE API...
INFO:app.services.data.stock_data_service:Fetching stock list from NEPSE API...
INFO:app.api.v1.data_routes:API: Fetching market data...
```

## Step 7: Test ReDoc Documentation

Open alternative documentation:

```
http://localhost:8000/redoc
```

This provides a different view of the API documentation.

## Common Issues and Solutions

### Issue 1: Server won't start

**Solution:** Check if port 8000 is already in use

```bash
lsof -i :8000
# Kill the process if needed
kill -9 <PID>
```

### Issue 2: Database connection error

**Solution:** Verify PostgreSQL is running

```bash
pg_isready
# Or check the service
brew services list | grep postgresql
```

### Issue 3: Import errors

**Solution:** Reinstall dependencies

```bash
pip install -r requirements.txt
```

### Issue 4: No data returned

**Solution:** This is expected! The NEPSE API client has placeholder implementations. The infrastructure is working correctly.

## Success Criteria

✅ All endpoints are accessible  
✅ Swagger UI loads correctly  
✅ Each endpoint returns a response (even if with placeholder data)  
✅ No server crashes or errors  
✅ Database connections work  
✅ Logs show proper execution flow

## Next Steps

After manual testing:

1. Run automated tests:

   ```bash
   python test_day3_services.py
   ```

2. Check the completion report:

   ```bash
   cat DAY3_COMPLETION_REPORT.md
   ```

3. Update TODO.md to mark Day 3 as complete

---

**Happy Testing! 🚀**

If you encounter any issues, check the logs and refer to the troubleshooting section above.
