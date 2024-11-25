from common.dependencies.registrator import add_factory_to_mapper
from db.postgres.connection import get_async_session
from fastapi import Depends

from db.s3.connection import get_async_s3_client
from repository.local_storage_implementation.file_repository import FileRepository
from repository.postgres_implementation.file_data_repository import SQLFileDataRepository
from repository.s3_implementation.s3_repository import S3FileRepository
from services import FileDataService
from services.file.adc_file import AbstractFileService
from services.file.file import FileService
from services.file_data.abc_file_data import AbstractFileDataService
from sqlalchemy.ext.asyncio import AsyncSession


@add_factory_to_mapper(AbstractFileService)
def create_file_service():
    return FileService(file_repository=FileRepository(),)
