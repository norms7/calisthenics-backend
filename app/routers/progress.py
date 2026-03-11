from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from datetime import date, timedelta
from app.database import get_db
from app.models.user import User
from app.models.workout_session import WorkoutSession
from app.services.progress_service import get_or_create_stats
from app.dependencies import get_current_user

router = APIRouter(prefix="/progress", tags=["Progress"])

@router.get("")
def get_progress(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    stats = get_or_create_stats(current_user.id, db)
    return {
        "total_workouts": stats.total_workouts,
        "current_streak": stats.current_streak,
        "longest_streak": stats.longest_streak,
        "total_exercises": stats.total_exercises,
        "weekly_completion_pct": float(stats.weekly_completion_pct),
        "last_workout_date": str(stats.last_workout_date) if stats.last_workout_date else None,
    }

@router.get("/weekly")
def get_weekly(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    today = date.today()
    week_start = today - timedelta(days=today.weekday())
    week_days = [week_start + timedelta(days=i) for i in range(7)]

    completed = {
        s.session_date for s in db.query(WorkoutSession).filter(
            WorkoutSession.user_id == current_user.id,
            WorkoutSession.session_date >= week_start,
            WorkoutSession.status == "completed",
        ).all()
    }

    days = [{"date": str(d), "completed": d in completed} for d in week_days]
    done = len(completed)
    return {
        "days": days,
        "completed_this_week": done,
        "total_this_week": 7,
        "completion_pct": round(done / 7 * 100, 1),
    }
