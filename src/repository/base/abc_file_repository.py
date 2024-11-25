from abc import abstractmethod, ABC

from fastapi import UploadFile


class AbstractFileRepository(ABC):
    @abstractmethod
    async def add_file(self, file: UploadFile, file_name: str) -> int:
        pass

    @abstractmethod
    def delete_file(self, file_name: str):
        pass
