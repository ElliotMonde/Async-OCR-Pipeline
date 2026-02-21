from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    DB_USER: str
    DB_PASSWORD: str
    DB_HOST: str
    DB_PORT: str
    DB_NAME: str
    REDIS_HOST: str
    REDIS_PORT: str

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

settings = Settings()
