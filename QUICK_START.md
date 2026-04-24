# 🚀 NEPSE Trading Bot - Quick Start Guide

## ⚡ Get Started in 3 Steps

### 1️⃣ Activate Virtual Environment

```bash
source venv/bin/activate
```

### 2️⃣ Start the Server

```bash
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

### 3️⃣ Access the Application

- **API:** http://localhost:8000
- **Docs:** http://localhost:8000/docs
- **Health:** http://localhost:8000/health

---

## 📋 Common Commands

### Application

```bash
# Start server
python -m uvicorn app.main:app --reload

# Test database connection
python test_connection.py

# Run tests (when available)
pytest

# Check installed packages
pip list
```

### Database

```bash
# Connect to database
psql nepse_bot

# List tables
psql nepse_bot -c "\dt"

# Run query
psql nepse_bot -c "SELECT * FROM table_name;"

# Backup database
pg_dump nepse_bot > backup.sql
```

### API Testing

```bash
# Root endpoint
curl http://localhost:8000/

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

## 📁 Project Structure

```
nepse-bot-be/
├── app/                    # Main application
│   ├── main.py            # FastAPI app
│   ├── config.py          # Configuration
│   ├── database.py        # Database connection
│   ├── models/            # SQLAlchemy models
│   ├── api/               # API routes
│   ├── services/          # Business logic
│   ├── components/        # Strategy components
│   ├── indicators/        # Technical indicators
│   └── utils/             # Utilities
├── tests/                 # Test files
├── venv/                  # Virtual environment
├── .env                   # Environment variables
└── requirements.txt       # Dependencies
```

---

## 🔧 Configuration

Edit `.env` file to change settings:

```bash
# Database
DATABASE_URL=postgresql://user:pass@localhost:5432/nepse_bot

# API
NEPSE_API_BASE_URL=https://www.nepalstock.com.np/api

# Server
PORT=8000
DEBUG=True
```

---

## 📚 Documentation

- **README.md** - Project overview
- **SETUP_GUIDE.md** - Detailed setup
- **ARCHITECTURE.md** - System design
- **DATABASE_BROWSING_GUIDE.md** - Database access
- **DAY1_COMPLETION_REPORT.md** - Day 1 summary

---

## 🆘 Troubleshooting

### Server won't start

```bash
# Check if port is in use
lsof -i :8000

# Kill process if needed
kill -9 <PID>
```

### Database connection fails

```bash
# Check PostgreSQL is running
brew services list

# Start PostgreSQL
brew services start postgresql@14

# Test connection
psql nepse_bot
```

### Import errors

```bash
# Reinstall dependencies
pip install -r requirements.txt

# Check virtual environment
which python  # Should show venv path
```

---

## ✅ Day 1 Complete!

All systems are ready:

- ✅ Python 3.13.2
- ✅ PostgreSQL 14
- ✅ Virtual environment
- ✅ 45 packages installed
- ✅ Database connected
- ✅ FastAPI running

**Ready for Day 2! 🎉**
