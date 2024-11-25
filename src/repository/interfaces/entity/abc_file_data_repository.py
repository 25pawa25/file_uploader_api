import uuid
from abc import abstractmethod
from typing import Iterable

from repository.base.abc_entity_repository import BaseRepository
from schemas.entities.base_entity import BaseEntity
from schemas.entities.file_data_entity import FileDataEntity


class AbstractFileDataRepository(BaseRepository):
    @abstractmethod
    async def add_file_data(self, **fields) -> BaseEntity:
        pass

    @abstractmethod
    async def get_file_data(self, file_id: uuid.UUID, raise_if_notfound: bool = True) -> BaseEntity:
        pass

    @abstractmethod
    async def get_file_data_to_delete(self) -> Iterable[FileDataEntity]:
        ...

    @abstractmethod
    async def update_file_data(self, file_id: uuid.UUID, **fields) -> BaseEntity:
        pass

    @abstractmethod
    async def delete_file_data(self, file_id: uuid.UUID):
        pass
