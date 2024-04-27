import os
from enum import Enum

from pydantic_settings import BaseSettings
from starlette.config import Config

from google.cloud import secretmanager
import json

project_id = '522840570394'
secret_name = 'alpha-eye-be-v2-env'
client_sm = secretmanager.SecretManagerServiceClient()
credential_path="C:\\Users\\HP\\AppData\\Roaming\\gcloud\\application_default_credentials.json"
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = credential_path
# Access the secret
name = f"projects/{project_id}/secrets/{secret_name}/versions/latest"
response = client_sm.access_secret_version(request={"name": name})

# Extract the secret value (JSON string)
secret_value_json = response.payload.data.decode("UTF-8")


def parse_env_file(env_content):
    env_vars = {}
    for line in env_content.splitlines():
        if line.strip() and not line.startswith("#"):
            key, value = line.strip().split("=", 1)
            env_vars[key.strip()] = value.strip()
    return env_vars


env_vars = parse_env_file(secret_value_json)

env_list = []

for key, value in env_vars.items():
    env_list.append({f"{key}": f"{value}"})

keys_to_access = set().union(*(d.keys() for d in env_list))

# Create a new dictionary with values associated with the specified keys
result_dict = {key: next((d[key] for d in env_list if key in d), None)
               for key in keys_to_access}

# print(result_dict)

current_file_dir = os.path.dirname(os.path.realpath(__file__))
env_path = os.path.join(current_file_dir, "..", "..", "..", ".env")
config = Config(env_path)


class AppSettings(BaseSettings):
    APP_NAME: str = config("APP_NAME", default="FastAPI app")
    APP_DESCRIPTION: str | None = config("APP_DESCRIPTION", default=None)
    APP_VERSION: str | None = config("APP_VERSION", default=None)
    LICENSE_NAME: str | None = config("LICENSE", default=None)
    CONTACT_NAME: str | None = config("CONTACT_NAME", default=None)
    CONTACT_EMAIL: str | None = config("CONTACT_EMAIL", default=None)


class CryptSettings(BaseSettings):
    SECRET_KEY: str = result_dict["SECRET_KEY"]
    ALGORITHM: str = result_dict["ALGORITHM"]
    ACCESS_TOKEN_EXPIRE_MINUTES: int = result_dict["ACCESS_TOKEN_EXPIRE_MINUTES"]
    REFRESH_TOKEN_EXPIRE_DAYS: int = result_dict["REFRESH_TOKEN_EXPIRE_DAYS"]


class DatabaseSettings(BaseSettings):
    pass


class CloudinaryConfigSettings(BaseSettings):
    CLOUDINARY_CLOUD_NAME: str = result_dict["CLOUDINARY_CLOUD_NAME"]
    CLOUDINARY_API_KEY: str = result_dict["CLOUDINARY_API_KEY"]
    CLOUDINARY_API_SECRET: str = result_dict["CLOUDINARY_API_SECRET"]

# class SQLiteSettings(DatabaseSettings):
#     SQLITE_URI: str = config("SQLITE_URI", default="./sql_app.db")
#     SQLITE_SYNC_PREFIX: str = config("SQLITE_SYNC_PREFIX", default="sqlite:///")
#     SQLITE_ASYNC_PREFIX: str = config("SQLITE_ASYNC_PREFIX", default="sqlite+aiosqlite:///")


# class MySQLSettings(DatabaseSettings):
#     MYSQL_USER: str = config("MYSQL_USER", default="username")
#     MYSQL_PASSWORD: str = config("MYSQL_PASSWORD", default="password")
#     MYSQL_SERVER: str = config("MYSQL_SERVER", default="localhost")
#     MYSQL_PORT: int = config("MYSQL_PORT", default=5432)
#     MYSQL_DB: str = config("MYSQL_DB", default="dbname")
#     MYSQL_URI: str = f"{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_SERVER}:{MYSQL_PORT}/{MYSQL_DB}"
#     MYSQL_SYNC_PREFIX: str = config("MYSQL_SYNC_PREFIX", default="mysql://")
#     MYSQL_ASYNC_PREFIX: str = config("MYSQL_ASYNC_PREFIX", default="mysql+aiomysql://")
#     MYSQL_URL: str = config("MYSQL_URL", default=None)


class PostgresSettings(DatabaseSettings):
    POSTGRES_USER: str = result_dict["POSTGRES_USER"].strip('""')
    POSTGRES_PASSWORD: str = result_dict["POSTGRES_PASSWORD"].strip('""')
    POSTGRES_SERVER: str = result_dict["POSTGRES_SERVER"].strip('""')
    POSTGRES_PORT: int = result_dict["POSTGRES_PORT"].strip('""')
    POSTGRES_DB: str = result_dict["POSTGRES_DB"].strip('""')
    POSTGRES_SYNC_PREFIX: str = "postgresql://"
    POSTGRES_ASYNC_PREFIX: str = "postgresql+asyncpg://"
    POSTGRES_URI: str = f"{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_SERVER}:{POSTGRES_PORT}/{POSTGRES_DB}"
    POSTGRES_URL: str | None = f"{POSTGRES_URI}"


# class FirstUserSettings(BaseSettings):
#     ADMIN_NAME: str = config("ADMIN_NAME", default="admin")
#     ADMIN_EMAIL: str = config("ADMIN_EMAIL", default="admin@admin.com")
#     ADMIN_USERNAME: str = config("ADMIN_USERNAME", default="admin")
#     ADMIN_PASSWORD: str = config("ADMIN_PASSWORD", default="!Ch4ng3Th1sP4ssW0rd!")


# class TestSettings(BaseSettings):
#     TEST_NAME: str = config("TEST_NAME", default="Tester User")
#     TEST_EMAIL: str = config("TEST_EMAIL", default="test@tester.com")
#     TEST_USERNAME: str = config("TEST_USERNAME", default="testeruser")
#     TEST_PASSWORD: str = config("TEST_PASSWORD", default="Str1ng$t")


class RedisCacheSettings(BaseSettings):
    REDIS_CACHE_HOST: str = result_dict["REDIS_CACHE_HOST"]
    REDIS_CACHE_PORT: int = result_dict["REDIS_CACHE_PORT"]
    REDIS_CACHE_PASSWORD: str = result_dict["REDIS_CACHE_PASSWORD"]
    REDIS_CACHE_URL: str = f"redis://:{REDIS_CACHE_PASSWORD}@{REDIS_CACHE_HOST}:{REDIS_CACHE_PORT}"


class ClientSideCacheSettings(BaseSettings):
    CLIENT_CACHE_MAX_AGE: int = config("CLIENT_CACHE_MAX_AGE", default=60)


# class RedisQueueSettings(BaseSettings):
#     REDIS_QUEUE_HOST: str = config("REDIS_QUEUE_HOST", default="localhost")
#     REDIS_QUEUE_PORT: int = config("REDIS_QUEUE_PORT", default=6379)


# class RedisRateLimiterSettings(BaseSettings):
#     REDIS_RATE_LIMIT_HOST: str = config("REDIS_RATE_LIMIT_HOST", default="localhost")
#     REDIS_RATE_LIMIT_PORT: int = config("REDIS_RATE_LIMIT_PORT", default=6379)
#     REDIS_RATE_LIMIT_URL: str = f"redis://{REDIS_RATE_LIMIT_HOST}:{REDIS_RATE_LIMIT_PORT}"


# class DefaultRateLimitSettings(BaseSettings):
#     DEFAULT_RATE_LIMIT_LIMIT: int = config("DEFAULT_RATE_LIMIT_LIMIT", default=10)
#     DEFAULT_RATE_LIMIT_PERIOD: int = config("DEFAULT_RATE_LIMIT_PERIOD", default=3600)


class EnvironmentOption(Enum):
    LOCAL = "local"
    STAGING = "staging"
    PRODUCTION = "production"


class EnvironmentSettings(BaseSettings):
    ENVIRONMENT: EnvironmentOption = config("ENVIRONMENT", default="local")


class Settings(
    AppSettings,
    PostgresSettings,
    CryptSettings,
    CloudinaryConfigSettings,
    # FirstUserSettings,
    # TestSettings,
    RedisCacheSettings,
    ClientSideCacheSettings,
    # RedisQueueSettings,
    # RedisRateLimiterSettings,
    # DefaultRateLimitSettings,
    EnvironmentSettings,
):
    pass


settings = Settings()
