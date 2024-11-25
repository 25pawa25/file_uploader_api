from abc import ABC, abstractmethod
from typing import AsyncGenerator

from repository.base.abc_file_repository import AbstractFileRepository


class AbstractLocalStorageRepository(AbstractFileRepository, ABC):
    @abstractmethod
    async def get_file(self, file_name: str) -> AsyncGenerator[bytes, None]:
        ...