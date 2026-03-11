from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DB_HOST: str = "localhost"
    DB_PORT: int = 3306
    DB_USER: str = "root"
    DB_PASSWORD: str = "Admin123_"
    DB_NAME: str = "calisthenics_db"
    JWT_SECRET: str = "changeme-secret-key-32chars-minimum"
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRE_MINUTES: int = 10080

    class Config:
        env_file = ".env"

settings = Settings()
