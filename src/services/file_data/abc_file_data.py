import uuid
from abc import ABC, abstractmethod

from fastapi import UploadFile

from schemas.request.file_data import FileDataSchema
from schemas.response.file_data import FileDataResponse


class AbstractFileDataService(ABC):
    @abstractmethod
    async def add_file_data(self, file: UploadFile, file_data: FileDataSchema) -> FileDataResponse:
        ...

    @abstractmethod
    async def get_file_data(self, file_id: uuid.UUID) -> FileDataResponse:
        ...

    @abstractmethod
    async def set_file_to_delete(self, file_id: uuid.UUID) -> FileDataResponse:
        ...

    @abstractmethod
    async def delete_file_data(self, file_id: uuid.UUID):
        ...
