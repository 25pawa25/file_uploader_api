import base64
import json
from datetime import datetime, timedelta
from typing import AsyncGenerator

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
from services.file.adc_file import AbstractFileService
from services.file_data.abc_file_data import AbstractFileDataService


class FileService(AbstractFileService):
    def __init__(
            self,
            file_repository: AbstractLocalStorageRepository,
    ) -> None:
        self.file_repository = file_repository

    def get_file(self, file_name: str) -> AsyncGenerator[bytes, None]:
        """
        Get a file by name
        Args:
            file_name: name of the file
        """
        return self.file_repository.get_file(file_name)

