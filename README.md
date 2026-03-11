# Calisthenics Planner — Backend (FastAPI)

## Setup

```bash
# 1. Create virtual environment
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Copy and edit .env
cp .env.example .env
# Edit .env with your MySQL credentials

# 4. Create the database in MySQL Workbench
#    Run the contents of schema.sql

# 5. Seed exercise data
python seeds/seed_exercises.py

# 6. Start the server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## API Docs
- Swagger UI: http://localhost:8000/docs
- ReDoc:       http://localhost:8000/redoc

## Endpoints
| Method | Endpoint                    | Auth | Description                        |
|--------|-----------------------------|------|------------------------------------|
| POST   | /api/auth/register          | No   | Register new user                  |
| POST   | /api/auth/login             | No   | Login and get JWT                  |
| GET    | /api/auth/me                | Yes  | Get current user profile           |
| GET    | /api/exercises              | Yes  | List all exercises                 |
| GET    | /api/exercises/{id}         | Yes  | Get single exercise detail         |
| POST   | /api/workout/generate-plan  | Yes  | Create a new workout plan          |
| GET    | /api/workout/today          | Yes  | Get today's workout with overload  |
| POST   | /api/workout/complete       | Yes  | Log workout completion             |
| GET    | /api/workout/history        | Yes  | Past 30 sessions                   |
| GET    | /api/progress               | Yes  | Streak, totals, weekly %           |
| GET    | /api/progress/weekly        | Yes  | Day-by-day weekly breakdown        |
