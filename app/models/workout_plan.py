from sqlalchemy import Column, Integer, Boolean, DateTime, Enum, ForeignKey
from sqlalchemy.sql import func
from app.database import Base

class WorkoutPlan(Base):
    __tablename__ = "workout_plans"

    id           = Column(Integer, primary_key=True, index=True)
    user_id      = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    week_number  = Column(Integer, default=1)
    workout_type = Column(
        Enum("Full Body", "Upper Body", "Lower Body", "Core"), nullable=False
    )
    difficulty   = Column(
        Enum("Beginner", "Intermediate", "Advanced"), nullable=False
    )
    is_active    = Column(Boolean, default=True)
    created_at   = Column(DateTime, server_default=func.now())
