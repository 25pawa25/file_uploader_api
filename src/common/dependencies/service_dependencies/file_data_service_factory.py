import aioboto3
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from common.dependencies.registrator import add_factory_to_mapper
from db.postgres.connection import get_async_session
from db.s3.connection import get_async_s3_client
from repository.local_storage_implementation.file_repository import FileRepository
from repository.postgres_implementation.file_data_repository import SQLFileDataRepository
from repository.s3_implementation.s3_repository import S3FileRepository
from services import FileDataService
from services.file_data.abc_file_data import AbstractFileDataService


@add_factory_to_mapper(AbstractFileDataService)
def create_file_data_service(
        session: AsyncSession = Depends(get_async_session),
        s3_client: aioboto3.session.Session = Depends(get_async_s3_client),
):
    return FileDataService(
        file_data_repository=SQLFileDataRepository(session=session),
        file_repository=FileRepository(),
        s3_repository=S3FileRepository(s3_client),
    )
