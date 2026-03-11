from sqlalchemy import Column, Integer, String, Date, DateTime, Enum, ForeignKey
from sqlalchemy.sql import func
from app.database import Base

class WorkoutSession(Base):
    __tablename__ = "workout_sessions"

    id               = Column(Integer, primary_key=True, index=True)
    user_id          = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    plan_id          = Column(Integer, ForeignKey("workout_plans.id"), nullable=True)
    session_date     = Column(Date, nullable=False)
    status           = Column(
        Enum("pending", "in_progress", "completed", "skipped"),
        default="pending"
    )
    duration_minutes = Column(Integer, nullable=True)
    completed_at     = Column(DateTime, nullable=True)
    created_at       = Column(DateTime, server_default=func.now())
