from abc import ABC, abstractmethod
from typing import AsyncGenerator

from fastapi import UploadFile

from schemas.request.file_data import FileDataSchema
from schemas.response.file_data import FileDataResponse


class AbstractFileService(ABC):
    @abstractmethod
    def get_file(self, file_name: str) -> AsyncGenerator[bytes, None]:
        ...
