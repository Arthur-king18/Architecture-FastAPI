import os

from pydantic import BaseModel
# from pydantic import BaseSettings
from dotenv import load_dotenv

load_dotenv()
WRITE_DB_URL = os.environ.get('WRITE_DB_URL')
READ_DB_URL = os.environ.get('READ_DB_URL')
WAITLIST = os.environ.get('WAITLIST')
EDEN_API = os.environ.get('EDEN_API')
DOMAIN = os.environ.get('DOMAIN')

class Config(BaseModel):
    ENV: str = "development"
    DEBUG: bool = True
    APP_HOST: str = "localhost"
    APP_PORT: int = 8000
    WRITER_DB_URL: str = WRITE_DB_URL
    READER_DB_URL: str = READ_DB_URL
    JWT_SECRET_KEY: str = "threhgrgerg"
    JWT_ALGORITHM: str = "HS256"
    SENTRY_SDN: str = None
    CELERY_BROKER_URL: str = "amqp://user:bitnami@localhost:5672/"
    CELERY_BACKEND_URL: str = "redis://:password123@localhost:6379/0"
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379


class DevelopmentConfig(Config):
    WRITER_DB_URL: str = WRITE_DB_URL
    READER_DB_URL: str = READ_DB_URL
    REDIS_HOST: str = "redis"
    REDIS_PORT: int = 6379


class LocalConfig(Config):
    WRITER_DB_URL: str = WRITE_DB_URL
    READER_DB_URL: str = READ_DB_URL


class ProductionConfig(Config):
    DEBUG: str = False
    WRITER_DB_URL: str = WRITE_DB_URL
    READER_DB_URL: str = READ_DB_URL


def get_config():
    env = os.getenv("ENV", "local")
    config_type = {
        "dev": DevelopmentConfig(),
        "local": LocalConfig(),
        "prod": ProductionConfig(),
    }
    return config_type[env]


config: Config = get_config()