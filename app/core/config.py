from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    MONGO_URL: str = "mongodb://localhost:27017"
    SECRET_KEY: str = "supersecretkey"

    class Config:
        env_file = ".env"

settings = Settings()
