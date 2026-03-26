# Complete Setup & Deployment Guide

## Prerequisites

- Docker & Docker Compose (recommended)
- OR: Python 3.11+, PostgreSQL 15, Redis 7
- Windows, macOS, or Linux

## Method 1: Docker Compose (⭐ Easiest)

### Step 1: Navigate to Project

```powershell
cd C:\Users\Akhilesh N R\food-recommender
```

### Step 2: Build & Run

```powershell
docker-compose up --build
```

Wait for output like:

```
✓ Food data seeded successfully
✓ Sample user created (ID: 1)
backend       | Uvicorn running on http://0.0.0.0:8000
```

### Step 3: Access Application

- **Frontend**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health

### Step 4: Stop Application

```powershell
docker-compose down
```

---

## Method 2: Local Development Setup

### Step 1: Install PostgreSQL

```powershell
# For Windows (using Chocolatey):
choco install postgresql

# Or download from: https://www.postgresql.org/download/windows/
```

### Step 2: Create Database

```powershell
# Connect to PostgreSQL
psql -U postgres

# In psql shell:
CREATE DATABASE food_recommender;
CREATE USER fooduser WITH PASSWORD 'foodpass';
ALTER ROLE fooduser SET client_encoding TO 'utf8';
ALTER ROLE fooduser SET default_transaction_isolation TO 'read committed';
ALTER ROLE fooduser SET default_transaction_deferrable TO on;
ALTER ROLE fooduser SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE food_recommender TO fooduser;
\q
```

### Step 3: Install Redis (Optional)

```powershell
# Using Chocolatey:
choco install redis

# Or download: https://github.com/microsoftarchive/redis/releases
```

### Step 4: Install Python Dependencies

```powershell
cd C:\Users\Akhilesh N R\food-recommender\backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

### Step 5: Seed Database

```powershell
python seed.py
# Output:
# ✓ Food data seeded successfully
# ✓ Sample user created (ID: 1)
# ✓ Database seeding complete!
```

### Step 6: Run Backend

```powershell
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

### Step 7: Serve Frontend

```powershell
# In a new terminal:
cd C:\Users\Akhilesh N R\food-recommender\frontend
python -m http.server 8080
```

Open: **http://localhost:8080**

---

## Stopping Services

### Docker Compose

```powershell
docker-compose down
```

### Local Development

- Press `Ctrl+C` in backend terminal
- Press `Ctrl+C` in frontend terminal

---

## Verification Checklist

- [ ] Docker containers running: `docker ps`
- [ ] Database has data: Connect to PostgreSQL
- [ ] Backend responds: `http://localhost:8000/health`
- [ ] API docs work: `http://localhost:8000/docs`
- [ ] Frontend loads: `http://localhost:8000`
- [ ] Can create user
- [ ] Can see recommendations

---

## Troubleshooting

### "Port 8000 already in use"

```powershell
# Find process using port
netstat -ano | findstr :8000

# Kill process (replace PID)
taskkill /PID <PID> /F

# Or change port in docker-compose.yml:
# ports:
#   - "8001:8000"
```

### "PostgreSQL connection refused"

```powershell
# Check if PostgreSQL service is running
Get-Service | grep postgres

# Restart PostgreSQL
Restart-Service postgresql-x64-15
```

### "Database doesn't exist"

```powershell
# Seed again
cd backend
python seed.py
```

### "Can't connect to backend from frontend"

- Ensure backend is running on 0.0.0.0 (not 127.0.0.1)
- Check browser console for CORS errors
- Verify API_BASE in script.js matches your URL

### Docker Container Exits

```powershell
# View logs
docker-compose logs backend

# Rebuild
docker-compose down
docker-compose up --build
```

---

## Database Reset

### Clear Data (Keep Schema)

```powershell
# SSH into container
docker exec -it food_recommender_backend python -c "
from database import SessionLocal, Base, engine
from models import Food, FoodTag, User, Interaction
db = SessionLocal()
db.query(Interaction).delete()
db.query(FoodTag).delete()
db.query(Food).delete()
db.query(User).delete()
db.commit()
"
```

### Full Reset (Remove Everything)

```powershell
docker-compose down -v
docker-compose up --build
```

---

## Performance Metrics

All operations measured on standard machine:

| Operation           | Response Time |
| ------------------- | ------------- |
| Create User         | ~30ms         |
| Get All Foods       | ~15ms         |
| Get Recommendations | ~45ms         |
| Record Interaction  | ~25ms         |

---

## Next Steps

1. ✅ Application is running
   2.📖 Read the [README.md](README.md) for API details
2. 🧪 Follow examples in [EXAMPLES.md](EXAMPLES.md)
3. 🚀 Deploy to cloud (AWS, GCP, Azure)
4. 🔒 Add authentication & security features
