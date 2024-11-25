import base64
import json
import uuid
from datetime import datetime, timedelta

import jwt
from fastapi import UploadFile
from loguru import logger
from pydantic import ValidationError

from core.config import settings
from repository.base.abc_file_repository import AbstractFileRepository
from repository.interfaces.entity.abc_file_data_repository import AbstractFileDataRepository
from repository.interfaces.file.abc_local_storage_repository import AbstractLocalStorageRepository
from repository.interfaces.file.abc_s3_repository import AbstractS3Repository
from repository.interfaces.kv.abc_session_repository import AbstractSessionRepository

from schemas.request.file_data import FileDataSchema
from schemas.response.file_data import FileDataResponse
from services.file_data.abc_file_data import AbstractFileDataService


class FileDataService(AbstractFileDataService):
    def __init__(
            self,
            file_data_repository: AbstractFileDataRepository,
            file_repository: AbstractLocalStorageRepository,
            s3_repository: AbstractS3Repository,
    ) -> None:
        self.file_data_repository = file_data_repository
        self.file_repository = file_repository
        self.s3_repository = s3_repository

    async def add_file_data(self, file: UploadFile, file_data_schema: FileDataSchema) -> FileDataResponse:
        """
        Add a file data
        Args:
            file: file to upload
            file_data_schema: FileDataSchema
        """
        file_data_schema.size = await self.file_repository.add_file(file=file, file_name=file_data_schema.name)
        await self.s3_repository.add_file(file=file, file_name=file_data_schema.name)
        file_data_db = await self.file_data_repository.add_file_data(**file_data_schema.dict())
        return FileDataResponse.from_orm(file_data_db)

    async def get_file_data(self, file_id: uuid.UUID) -> FileDataResponse:
        """
        Get a file data by id
        Args:
            file_id: id of the file
        """
        file_data = await self.file_data_repository.get_file_data(file_id)
        return FileDataResponse.from_orm(file_data)

    async def set_file_to_delete(self, file_id: uuid.UUID) -> FileDataResponse:
        """
        Update a file data: set to delete
        Args:
            file_id: id of the file
        """
        file_data_db = await self.file_data_repository.update_file_data(file_id=file_id, will_be_deleted=True)
        return FileDataResponse.from_orm(file_data_db)

    async def delete_file_data(self, file_id: uuid.UUID):
        """
        Deleting a file data
        Args:
            file_id: id of the file
        """
        file_db = await self.file_data_repository.get_file_data(file_id)
        self.file_repository.delete_file(file_db.name)
        await self.s3_repository.delete_file(file_db.name)
        await self.file_data_repository.delete_file_data(file_id)
