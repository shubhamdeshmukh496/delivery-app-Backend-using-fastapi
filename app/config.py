from pydantic_settings import BaseSettings, SettingsConfigDict

_base_config = SettingsConfigDict(
    env_file="./app/.env",
    env_ignore_empty=True,
    extra="ignore",
)

class DatabaseSettings(BaseSettings):
    POSTGRES_SERVER: str
    POSTGRES_PORT: int
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str

    REDIS_HOST: str
    REDIS_PORT: str

    model_config = _base_config

    @property
    def POSTGRES_url(self):
        return f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_SERVER}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
    @property
    def REDIS_url(self):
        return f"redis://{self.REDIS_HOST}:{self.REDIS_PORT}"

class SecuritySettings(BaseSettings):
    JWT_SECRET : str
    JWT_ALGORITHM: str
    model_config = _base_config

db_settings = DatabaseSettings()
security_settings = SecuritySettings()