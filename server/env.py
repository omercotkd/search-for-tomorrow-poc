from pydantic_settings import BaseSettings
from enum import Enum


class Environment(str, Enum):
    LOCAL = "local"
    DEV = "dev"
    PROD = "prod"

    def is_local(self) -> bool:
        return self == Environment.LOCAL

    def is_dev(self) -> bool:
        return self == Environment.DEV

    def is_prod(self) -> bool:
        return self == Environment.PROD


class EnvVariables(BaseSettings):
    ENVIRONMENT: Environment = Environment.LOCAL
    MONGO_URI: str = "mongodb://root:example@localhost:27017/documents?authSource=admin"
    DB_NAME: str = "search_engine"
    REDIS_URI: str = 'redis://localhost:6379'


ENV_VARIABLES = EnvVariables(_env_file=".env", _env_file_encoding="utf-8")
