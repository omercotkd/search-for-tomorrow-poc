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
    MONGO_URI: str = "mongodb://localhost:27017"


ENV_VARIABLES = EnvVariables(_env_file=".env", _env_file_encoding="utf-8")
