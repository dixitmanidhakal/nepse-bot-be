# Day 3 Quick Start Guide

## 🚀 Start Testing in 3 Steps

### Step 1: Start the Server

```bash
# Make sure you're in the project directory
cd /Users/dixitmanidhakal/Documents/nepse-bot/nepse-bot-be

# Activate virtual environment
source venv/bin/activate

# Start the FastAPI server
python app/main.py
```

**Expected Output:**

```
============================================================
Starting NEPSE Trading Bot v1.0.0
Environment: development
============================================================
INFO:     Started server process
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8000
```

### Step 2: Open Swagger UI

Open your browser and go to:

```
http://localhost:8000/docs
```

You should see the interactive API documentation with all endpoints.

### Step 3: Test the Endpoints

#### Quick Test 1: Check Data Status

1. Find `GET /api/v1/data/status`
2. Click "Try it out"
3. Click "Execute"
4. You should see database statistics

#### Quick Test 2: Fetch Market Data

1. Find `POST /api/v1/data/fetch-market`
2. Click "Try it out"
3. Click "Execute"
4. You should see a success response

#### Quick Test 3: Fetch Stock List

1. Find `POST /api/v1/data/fetch-stocks`
2. Click "Try it out"
3. Click "Execute"
4. You should see stocks added/updated count

---

## 📊 What to Expect

### ⚠️ Important Note

The NEPSE API client currently has **placeholder implementations**, so:

- You'll see responses with `0` or empty data
- This is **EXPECTED** and **CORRECT**
- The infrastructure is working perfectly
- Real API endpoints will be added later

### ✅ What Should Work

- All endpoints are accessible
- Requests are processed
- Responses are returned
- No server crashes
- Database connections work
- Validation works

### 🔍 Verify in Database

After testing, check the database:

```sql
-- Check if tables exist
SELECT table_name FROM information_schema.tables
WHERE table_schema = 'public';

-- Check data counts
SELECT 'sectors' as table_name, COUNT(*) as count FROM sectors
UNION ALL
SELECT 'stocks', COUNT(*) FROM stocks
UNION ALL
SELECT 'stock_ohlcv', COUNT(*) FROM stock_ohlcv;
```

---

## 🧪 Run Automated Tests

```bash
# Run Day 3 tests
python test_day3_services.py

# Or use the runner
python run_day3_tests.py
```

---

## 📚 Full Documentation

For detailed testing instructions, see:

- `DAY3_MANUAL_TESTING_GUIDE.md` - Complete testing guide
- `DAY3_COMPLETION_REPORT.md` - Implementation details
- `http://localhost:8000/docs` - Interactive API docs

---

## 🆘 Troubleshooting

### Server won't start?

```bash
# Check if port 8000 is in use
lsof -i :8000

# Kill the process if needed
kill -9 <PID>
```

### Database connection error?

```bash
# Check PostgreSQL is running
pg_isready

# Or check the service
brew services list | grep postgresql
```

### Import errors?

```bash
# Reinstall dependencies
pip install -r requirements.txt
```

---

## ✅ Success Checklist

- [ ] Server starts without errors
- [ ] Swagger UI loads at http://localhost:8000/docs
- [ ] All 7 endpoints are visible
- [ ] Can execute GET /api/v1/data/status
- [ ] Can execute POST /api/v1/data/fetch-market
- [ ] No server crashes
- [ ] Database connection works

---

**You're all set! Happy testing! 🎉**
