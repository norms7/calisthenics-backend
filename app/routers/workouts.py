from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import date, datetime, timezone
from app.database import get_db
from app.models.user import User
from app.models.exercise import Exercise
from app.models.workout_plan import WorkoutPlan
from app.models.workout_session import WorkoutSession
from app.models.exercise_log import ExerciseLog
from app.services.overload_service import get_current_week, apply_overload
from app.services.progress_service import update_stats_after_workout
from app.dependencies import get_current_user

router = APIRouter(prefix="/workout", tags=["Workouts"])

@router.post("/generate-plan")
def generate_plan(body: dict, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    # Deactivate any existing plan
    db.query(WorkoutPlan).filter(
        WorkoutPlan.user_id == current_user.id,
        WorkoutPlan.is_active == True
    ).update({"is_active": False})
    plan = WorkoutPlan(
        user_id=current_user.id,
        workout_type=body["workout_type"],
        difficulty=body["difficulty"],
        week_number=1,
        is_active=True,
    )
    db.add(plan)
    db.commit()
    db.refresh(plan)
    return {"message": "Plan generated", "plan_id": plan.id}

@router.get("/today")
def get_today(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    plan = db.query(WorkoutPlan).filter(
        WorkoutPlan.user_id == current_user.id,
        WorkoutPlan.is_active == True
    ).first()
    if not plan:
        raise HTTPException(404, "No active plan. Call POST /workout/generate-plan first.")

    week = get_current_week(plan.created_at.date(), date.today())

    exercises = db.query(Exercise).filter(
        Exercise.difficulty == plan.difficulty,
    ).limit(6).all()

    # Create today's session if it doesn't exist
    session = db.query(WorkoutSession).filter(
        WorkoutSession.user_id == current_user.id,
        WorkoutSession.session_date == date.today(),
    ).first()
    if not session:
        session = WorkoutSession(
            user_id=current_user.id,
            plan_id=plan.id,
            session_date=date.today(),
            status="pending",
        )
        db.add(session)
        db.commit()
        db.refresh(session)

    result = []
    for ex in exercises:
        sets, reps = apply_overload(ex.base_sets, ex.base_reps, week)
        result.append({
            "exercise_id": ex.id, "name": ex.name,
            "sets": sets, "reps": reps,
            "rest_seconds": ex.rest_seconds,
            "muscle_groups": ex.muscle_groups,
            "image_url": ex.image_url, "is_completed": False,
        })

    return {
        "session_id": session.id, "date": str(date.today()),
        "week_number": week, "workout_type": plan.workout_type,
        "exercises": result,
    }

@router.post("/complete")
def complete_workout(body: dict, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    session = db.query(WorkoutSession).filter(
        WorkoutSession.id == body["session_id"],
        WorkoutSession.user_id == current_user.id,
    ).first()
    if not session:
        raise HTTPException(404, "Session not found")

    for log in body.get("exercise_logs", []):
        db.add(ExerciseLog(
            session_id=session.id,
            exercise_id=log["exercise_id"],
            sets_completed=log["sets_completed"],
            reps_completed=log["reps_completed"],
            is_completed=True,
        ))

    session.status = "completed"
    session.duration_minutes = body.get("duration_minutes")
    session.completed_at = datetime.now(timezone.utc)
    db.commit()

    stats = update_stats_after_workout(current_user.id, len(body.get("exercise_logs", [])), db)
    return {
        "message": "Workout completed!",
        "current_streak": stats.current_streak,
        "total_workouts": stats.total_workouts,
    }

@router.get("/history")
def get_history(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    sessions = db.query(WorkoutSession).filter(
        WorkoutSession.user_id == current_user.id
    ).order_by(WorkoutSession.session_date.desc()).limit(30).all()
    return [{"date": str(s.session_date), "status": s.status, "duration_minutes": s.duration_minutes}
            for s in sessions]
