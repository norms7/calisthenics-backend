from datetime import date, timedelta
from sqlalchemy.orm import Session
from app.models.progress_stat import ProgressStat
from app.models.workout_session import WorkoutSession

def get_or_create_stats(user_id: int, db: Session) -> ProgressStat:
    stats = db.query(ProgressStat).filter_by(user_id=user_id).first()
    if not stats:
        stats = ProgressStat(user_id=user_id)
        db.add(stats)
        db.commit()
        db.refresh(stats)
    return stats

def update_stats_after_workout(user_id: int, exercise_count: int, db: Session) -> ProgressStat:
    stats = get_or_create_stats(user_id, db)
    today = date.today()

    if stats.last_workout_date == today:
        pass  # already counted today
    elif stats.last_workout_date == today - timedelta(days=1):
        stats.current_streak += 1
    else:
        stats.current_streak = 1  # streak reset

    if stats.current_streak > stats.longest_streak:
        stats.longest_streak = stats.current_streak

    stats.total_workouts  += 1
    stats.total_exercises += exercise_count
    stats.last_workout_date = today

    # Weekly completion %
    week_start = today - timedelta(days=today.weekday())
    completed_this_week = db.query(WorkoutSession).filter(
        WorkoutSession.user_id == user_id,
        WorkoutSession.session_date >= week_start,
        WorkoutSession.status == "completed",
    ).count()
    stats.weekly_completion_pct = round(min(completed_this_week / 7 * 100, 100), 2)

    db.commit()
    db.refresh(stats)
    return stats
