from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "Server Monitoring Tool"
    DB_USER: str
    DB_PASSWORD: str
    DB_HOST: str
    DB_PORT: int
    DB_SERVICE_NAME: str
    DB_MIN_POOL: int = 1
    DB_MAX_POOL: int = 4
    DB_INCREMENT_POOL: int = 1
    DB_THICK_MODE: bool
    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str
    ORACLEDB_LIB_DIR: str

    

    class Config:
        env_file = ".env"

settings = Settings()