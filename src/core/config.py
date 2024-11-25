import os
from functools import lru_cache

from aiocache import Cache
from aiocache.serializers import PickleSerializer
from pydantic import BaseSettings, Field


class PostgresConfig(BaseSettings):
    echo_log: bool = Field(default=False, env="DB_ECHO_LOG")
    host: str = Field(default="127.0.0.1", env="DB_HOST")
    port: str = Field(default="15432", env="DB_PORT")
    database: str = Field(default="file_uploader_database", env="DB_NAME")
    user: str = Field(default="user", env="DB_USERNAME")
    password: str = Field(default="changeme", env="DB_PASSWORD")

    @property
    def database_url(self):
        return f"postgresql+asyncpg://{self.user}:{self.password}@{self.host}:{self.port}/{self.database}"

    @property
    def migration_database_url(self):
        return f"postgresql://{self.user}:{self.password}@{self.host}:{self.port}/{self.database}"


class ProjectConfig(BaseSettings):
    name: str = Field("file_uploader", env="PROJECT_NAME")
    api_host: str = Field(default="127.0.0.1", env="API_HOST")
    api_port: int = Field(default=8000, env="API_PORT")
    debug: bool = Field(default=False, env="DEBUG")
    base_dir: str = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    upload_chunk_size: int = Field(default=1024, env="UPLOAD_CHUNK_SIZE")
    frequency_of_files_deleting: int = Field(default=720, env="FREQUENCY_OF_FILES_DELETING")

    @property
    def upload_file_path(self):
        return self.base_dir + "/uploads"


class S3StorageConfig(BaseSettings):
    access_key: str = Field(default="access_key", env="AWS_ACCESS_KEY_ID")
    secret_key: str = Field(default="secret_key", env="AWS_SECRET_ACCESS_KEY")
    region: str = Field(default="ru", env="AWS_DEFAULT_REGION")
    bucket: str = Field(default="file_uploader", env="S3_BUCKET_NAME")


class RedisConfig(BaseSettings):
    port: int = Field(default=6379, env="REDIS_PORT")
    host: str = Field(default="127.0.0.1", env="REDIS_HOST")

    @property
    def cache_params(self):
        return {
            "timeout": 10,
            "cache": Cache.REDIS,
            "serializer": PickleSerializer(),
            "port": self.port,
            "endpoint": self.host,
            "namespace": "main",
        }

    @property
    def broker_url(self):
        return f"redis://{self.host}:{self.port}"


class Settings(BaseSettings):
    project: ProjectConfig = ProjectConfig()
    s3: S3StorageConfig = S3StorageConfig()
    redis: RedisConfig = RedisConfig()
    postgres: PostgresConfig = PostgresConfig()


@lru_cache()
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
