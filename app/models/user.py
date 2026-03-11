from sqlalchemy import Column, Integer, String, DateTime, Time, Enum
from sqlalchemy.sql import func
from app.database import Base

class User(Base):
    __tablename__ = "users"

    id                = Column(Integer, primary_key=True, index=True)
    username          = Column(String(50), unique=True, nullable=False)
    email             = Column(String(100), unique=True, nullable=False, index=True)
    password_hash     = Column(String(255), nullable=False)
    fitness_level     = Column(
        Enum("Beginner", "Intermediate", "Advanced"),
        default="Beginner", nullable=False
    )
    notification_time = Column(Time, nullable=True)
    created_at        = Column(DateTime, server_default=func.now())
