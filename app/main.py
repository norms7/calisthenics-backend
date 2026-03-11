from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import engine, Base
from app.routers import auth, exercises, workouts, progress

# Auto-create tables on startup
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Calisthenics Planner API",
    version="1.0.0",
    description="REST API for the Calisthenics Home Workout Planner mobile app.",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router,      prefix="/api")
app.include_router(exercises.router,  prefix="/api")
app.include_router(workouts.router,   prefix="/api")
app.include_router(progress.router,   prefix="/api")

@app.get("/")
def root():
    return {"message": "Calisthenics Planner API is running!", "docs": "/docs"}
