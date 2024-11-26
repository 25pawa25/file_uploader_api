from typing import AsyncGenerator

from repository.interfaces.file.abc_local_storage_repository import AbstractLocalStorageRepository
from services.file.adc_file import AbstractFileService


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
