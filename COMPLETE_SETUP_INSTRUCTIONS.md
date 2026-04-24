# 🚀 Complete Setup Instructions - Step by Step

## Current Status

✅ Python 3.13.2 - Installed
✅ Homebrew 4.4.21 - Installed
🔄 PostgreSQL 14 - Installing now...

---

## Step-by-Step Setup Guide

### Step 1: Wait for PostgreSQL Installation ⏳

The command `brew install postgresql@14` is currently running. Wait for it to complete.

**Expected output when done:**

```
==> Summary
🍺  /usr/local/Cellar/postgresql@14/14.x.x: xxx files, xxxMB
```

---

### Step 2: Start PostgreSQL Service

After installation completes, run:

```bash
brew services start postgresql@14
```

**Verify it's running:**

```bash
brew services list | grep postgresql
```

You should see: `postgresql@14  started`

---

### Step 3: Add PostgreSQL to PATH

```bash
echo 'export PATH="/usr/local/opt/postgresql@14/bin:$PATH"' >> ~/.zshrc
source ~/.zshrc
```

**Verify:**

```bash
psql --version
```

Should output: `psql (PostgreSQL) 14.x`

---

### Step 4: Create PostgreSQL Database

```bash
# Connect to PostgreSQL
psql postgres

# Inside psql, run these commands:
CREATE DATABASE nepse_bot;

# Create a user (optional, or use default 'postgres')
CREATE USER nepse_user WITH PASSWORD 'your_secure_password';

# Grant privileges
GRANT ALL PRIVILEGES ON DATABASE nepse_bot TO nepse_user;

# Exit psql
\q
```

**Alternative (one-liner):**

```bash
psql postgres -c "CREATE DATABASE nepse_bot;"
```

---

### Step 5: Set Up Python Virtual Environment

```bash
# Make sure you're in the project directory
cd /Users/dixitmanidhakal/Documents/nepse-bot/nepse-bot-be

# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# You should see (venv) in your terminal prompt
```

---

### Step 6: Upgrade pip

```bash
pip install --upgrade pip
```

---

### Step 7: Install Python Dependencies

```bash
pip install -r requirements.txt
```

**Note:** This will install all required packages. It may take 5-10 minutes.

**If TA-Lib fails to install:**

```bash
# Install TA-Lib system library first
brew install ta-lib

# Then try again
pip install TA-Lib
```

---

### Step 8: Configure Environment Variables

Edit the `.env` file with your database credentials:

```bash
# Open in your editor
nano .env
# or
code .env
```

**Update these lines:**

```bash
# If using default postgres user
DATABASE_URL=postgresql://postgres:@localhost:5432/nepse_bot
DB_USER=postgres
DB_PASSWORD=

# OR if you created nepse_user
DATABASE_URL=postgresql://nepse_user:your_secure_password@localhost:5432/nepse_bot
DB_USER=nepse_user
DB_PASSWORD=your_secure_password
```

**Save and close the file.**

---

### Step 9: Test Database Connection

```bash
# Make sure virtual environment is activated
source venv/bin/activate

# Run the test script
python test_connection.py
```

**Expected output:**

```
========================================
NEPSE Trading Bot - Database Connection Test
========================================

Configuration:
  Database: nepse_bot
  Host: localhost
  Port: 5432
  User: postgres
  Environment: development

----------------------------------------------------------

Testing database connection...

✅ SUCCESS: Database connection is working!

Database Information:
  Host: localhost
  Port: 5432
  Database: nepse_bot
  User: postgres
  Pool Size: 5
  Active Connections: 0
  Overflow: 0

========================================
You can now proceed with the application!
========================================
```

---

### Step 10: Run the FastAPI Application

```bash
# Make sure virtual environment is activated
source venv/bin/activate

# Run the application
python app/main.py
```

**Expected output:**

```
============================================================
Starting NEPSE Trading Bot v1.0.0
Environment: development
============================================================
Testing database connection...
✅ Database connection successful
Connected to: nepse_bot at localhost:5432
✅ Database tables initialized
Testing NEPSE API connection...
⚠️  NEPSE API health check failed
============================================================
Application started successfully!
API Documentation: http://0.0.0.0:8000/docs
============================================================
INFO:     Started server process [xxxxx]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8000
```

**Note:** NEPSE API health check may fail because endpoints are placeholders. This is expected for Day 1.

---

### Step 11: Test the API

**Open your browser and visit:**

1. **Swagger UI (Interactive API Docs):**

   - http://localhost:8000/docs

2. **ReDoc (Alternative Docs):**

   - http://localhost:8000/redoc

3. **Health Check:**

   - http://localhost:8000/health

4. **Root Endpoint:**
   - http://localhost:8000/

**Or use curl:**

```bash
# Health check
curl http://localhost:8000/health

# Database info
curl http://localhost:8000/db-info

# Test database
curl http://localhost:8000/test-db

# Configuration
curl http://localhost:8000/config
```

---

## 🎉 Success Criteria

You've successfully completed Day 1 setup if:

- ✅ PostgreSQL is installed and running
- ✅ Database `nepse_bot` is created
- ✅ Virtual environment is created and activated
- ✅ All Python dependencies are installed
- ✅ `.env` file is configured with your credentials
- ✅ `python test_connection.py` shows success
- ✅ `python app/main.py` starts without errors
- ✅ You can access http://localhost:8000/docs

---

## 🐛 Troubleshooting

### Issue: PostgreSQL won't start

```bash
# Check status
brew services list

# Restart
brew services restart postgresql@14

# Check logs
tail -f /usr/local/var/log/postgresql@14.log
```

### Issue: Database connection failed

```bash
# Verify database exists
psql postgres -c "\l" | grep nepse_bot

# Verify PostgreSQL is accepting connections
psql postgres -c "SELECT 1;"

# Check .env file has correct credentials
cat .env | grep DATABASE_URL
```

### Issue: Virtual environment not activating

```bash
# Make sure you're in the project directory
pwd
# Should show: /Users/dixitmanidhakal/Documents/nepse-bot/nepse-bot-be

# Recreate virtual environment
rm -rf venv
python3 -m venv venv
source venv/bin/activate
```

### Issue: TA-Lib installation fails

```bash
# Install system library first
brew install ta-lib

# Then install Python package
pip install TA-Lib

# If still fails, skip it for now
pip install -r requirements.txt --no-deps
pip install TA-Lib || echo "TA-Lib skipped"
```

### Issue: Port 8000 already in use

```bash
# Find process using port 8000
lsof -i :8000

# Kill it
kill -9 <PID>

# Or use different port
uvicorn app.main:app --port 8001
```

---

## 📝 Quick Reference Commands

```bash
# Activate virtual environment
source venv/bin/activate

# Deactivate virtual environment
deactivate

# Start PostgreSQL
brew services start postgresql@14

# Stop PostgreSQL
brew services stop postgresql@14

# Run application
python app/main.py

# Run tests (future)
pytest

# Check database
psql nepse_bot

# View logs
tail -f logs/nepse_bot.log
```

---

## 🎯 What's Next?

After completing Day 1 setup, you're ready for:

### Day 2: Database Foundation

- Create SQLAlchemy models
- Set up Alembic migrations
- Create bot_configurations table
- Insert default configurations

### Day 3: Base Architecture

- Create BaseComponent class
- Set up API routes
- Create bot configuration endpoints

---

## 💡 Tips

1. **Always activate virtual environment** before running Python commands
2. **Keep PostgreSQL running** while developing
3. **Check logs** if something goes wrong
4. **Use the test utilities** (test_connection.py) to verify setup
5. **Read error messages carefully** - they usually tell you what's wrong

---

## 📞 Need Help?

- Check SETUP_GUIDE.md for detailed troubleshooting
- Review README.md for project overview
- Check ARCHITECTURE.md for design details
- Review logs in `logs/` directory

---

**You're doing great! Follow these steps and you'll have everything running smoothly! 🚀**
