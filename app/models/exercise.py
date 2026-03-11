from sqlalchemy import Column, Integer, String, Text, Enum
from app.database import Base

class Exercise(Base):
    __tablename__ = "exercises"

    id              = Column(Integer, primary_key=True, index=True)
    name            = Column(String(100), nullable=False)
    muscle_groups   = Column(String(255), nullable=False)
    description     = Column(Text, nullable=False)
    instructions    = Column(Text, nullable=False)
    common_mistakes = Column(Text)
    difficulty      = Column(Enum("Beginner", "Intermediate", "Advanced"), nullable=False)
    base_sets       = Column(Integer, default=3)
    base_reps       = Column(Integer, default=10)
    rest_seconds    = Column(Integer, default=60)
    workout_type    = Column(
        Enum("Full Body", "Upper Body", "Lower Body", "Core"), nullable=False
    )
    image_url       = Column(String(255), nullable=True)
