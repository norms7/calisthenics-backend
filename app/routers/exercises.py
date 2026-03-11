from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from typing import Optional
from app.database import get_db
from app.models.exercise import Exercise
from app.dependencies import get_current_user

router = APIRouter(prefix="/exercises", tags=["Exercises"])

def _to_dict(e: Exercise) -> dict:
    return {
        "id": e.id, "name": e.name, "muscle_groups": e.muscle_groups,
        "description": e.description, "instructions": e.instructions,
        "common_mistakes": e.common_mistakes, "difficulty": e.difficulty,
        "base_sets": e.base_sets, "base_reps": e.base_reps,
        "rest_seconds": e.rest_seconds, "workout_type": e.workout_type,
        "image_url": e.image_url,
    }

@router.get("")
def list_exercises(
    workout_type: Optional[str] = Query(None),
    difficulty: Optional[str] = Query(None),
    db: Session = Depends(get_db),
    _=Depends(get_current_user),
):
    q = db.query(Exercise)
    if workout_type:
        q = q.filter(Exercise.workout_type == workout_type)
    if difficulty:
        q = q.filter(Exercise.difficulty == difficulty)
    return [_to_dict(e) for e in q.order_by(Exercise.name).all()]

@router.get("/{exercise_id}")
def get_exercise(exercise_id: int, db: Session = Depends(get_db), _=Depends(get_current_user)):
    ex = db.query(Exercise).filter(Exercise.id == exercise_id).first()
    if not ex:
        raise HTTPException(404, "Exercise not found")
    return _to_dict(ex)
