from asgiref.sync import async_to_sync
from loguru import logger
from sqlalchemy import NullPool
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from celery_workers.celery_conf import app
from core.config import settings
from repository.local_storage_implementation.file_repository import FileRepository
from repository.postgres_implementation.file_data_repository import SQLFileDataRepository


class AsyncTaskManager:
    def __init__(self):
        self._url = settings.postgres.database_url
        self._engine = create_async_engine(self._url, echo=False, poolclass=NullPool)
        self._session = sessionmaker(self._engine, expire_on_commit=False, class_=AsyncSession)
        self.file_data_repository = SQLFileDataRepository(self._session())
        self.file_repository = FileRepository()

    async def delete_files(self):
        """
        Deleting files
        """
        files_data = await self.file_data_repository.get_file_data_to_delete()
        for file in files_data:
            self.file_repository.delete_file(file.name)


@app.task
def files_to_delete_checker():
    """
    Deleting files with the will_be_deleted = True field
    """
    try:
        logger.info("Starting to delete files")
        task_manager = AsyncTaskManager()
        async_to_sync(task_manager.delete_files)()
    except Exception as e:
        logger.error(f"An error has occurred: {str(e)}")
