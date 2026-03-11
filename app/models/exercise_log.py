from sqlalchemy import Column, Integer, Boolean, ForeignKey
from app.database import Base

class ExerciseLog(Base):
    __tablename__ = "exercise_logs"

    id             = Column(Integer, primary_key=True, index=True)
    session_id     = Column(Integer, ForeignKey("workout_sessions.id", ondelete="CASCADE"))
    exercise_id    = Column(Integer, ForeignKey("exercises.id"))
    sets_completed = Column(Integer, nullable=False)
    reps_completed = Column(Integer, nullable=False)
    is_completed   = Column(Boolean, default=False)
