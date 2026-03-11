from sqlalchemy import Column, Integer, Date, DateTime, Numeric, ForeignKey
from sqlalchemy.sql import func
from app.database import Base

class ProgressStat(Base):
    __tablename__ = "progress_stats"

    id                    = Column(Integer, primary_key=True, index=True)
    user_id               = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), unique=True)
    total_workouts        = Column(Integer, default=0)
    current_streak        = Column(Integer, default=0)
    longest_streak        = Column(Integer, default=0)
    total_exercises       = Column(Integer, default=0)
    weekly_completion_pct = Column(Numeric(5, 2), default=0.00)
    last_workout_date     = Column(Date, nullable=True)
    updated_at            = Column(DateTime, onupdate=func.now(), server_default=func.now())
