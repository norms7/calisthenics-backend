import logging
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.user import User
from app.services.auth_service import hash_password, verify_password, create_access_token
from app.services.progress_service import get_or_create_stats
from app.dependencies import get_current_user

# Add logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/register", status_code=201)
def register(body: dict, db: Session = Depends(get_db)):
    if db.query(User).filter(User.email == body["email"]).first():
        raise HTTPException(400, "Email already registered")
    if db.query(User).filter(User.username == body["username"]).first():
        raise HTTPException(400, "Username already taken")
    user = User(
        username=body["username"],
        email=body["email"],
        password_hash=hash_password(body["password"]),
        fitness_level=body.get("fitness_level", "Beginner"),
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    get_or_create_stats(user.id, db)
    token = create_access_token({"sub": str(user.id)})
    return {
        "access_token": token,
        "token_type": "bearer",
        "user": {"id": user.id, "username": user.username,
                 "email": user.email, "fitness_level": user.fitness_level},
    }


@router.post("/login")
def login(body: dict, db: Session = Depends(get_db)):
    try:
        logger.info(f"Login attempt for email: {body.get('email')}")

        # Check if email exists in request
        if "email" not in body:
            raise HTTPException(400, "Email is required")
        if "password" not in body:
            raise HTTPException(400, "Password is required")

        user = db.query(User).filter(User.email == body["email"]).first()

        if not user:
            logger.warning(f"User not found for email: {body['email']}")
            raise HTTPException(401, "Invalid email or password")

        # Debug: Check password verification
        logger.info(f"User found: {user.username}")

        if not verify_password(body["password"], user.password_hash):
            logger.warning("Password verification failed")
            raise HTTPException(401, "Invalid email or password")

        token = create_access_token({"sub": str(user.id)})

        return {
            "access_token": token,
            "token_type": "bearer",
            "user": {
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "fitness_level": user.fitness_level
            },
        }
    except HTTPException:
        # Re-raise HTTP exceptions
        raise
    except Exception as e:
        logger.error(f"Unexpected error in login: {str(e)}", exc_info=True)
        raise HTTPException(500, f"Internal server error: {str(e)}")

@router.get("/me")
def get_me(current_user: User = Depends(get_current_user)):
    return {
        "id": current_user.id,
        "username": current_user.username,
        "email": current_user.email,
        "fitness_level": current_user.fitness_level,
        "notification_time": str(current_user.notification_time) if current_user.notification_time else None,
    }

@router.put("/me/notifications")
def update_notifications(body: dict, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    current_user.notification_time = body.get("notification_time")
    db.commit()
    return {"message": "Notification time updated"}
