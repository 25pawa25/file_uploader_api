import os
from typing import AsyncGenerator

import aiofiles
from fastapi import UploadFile

from common.exceptions import FileNotExists
from core.config import settings
from repository.interfaces.file.abc_local_storage_repository import AbstractLocalStorageRepository


class FileRepository(AbstractLocalStorageRepository):
    def __init__(self):
        self.path = settings.project.upload_file_path
        self.upload_chunk_size = settings.project.upload_chunk_size

    def generate_file_name(self, file_name):
        return os.path.join(self.path, file_name)

    async def add_file(self, file: UploadFile, file_name: str) -> int:
        """
        Add a file to the local storage.
        Args:
            file (UploadFile): the file to add
            file_name: Name of the file to add
        Returns:
            size of the file
        """
        total_size = 0
        async with aiofiles.open(self.generate_file_name(file_name), "wb") as out_file:
            while chunk := await file.read(self.upload_chunk_size):
                await out_file.write(chunk)
                total_size += len(chunk)
        return total_size

    async def get_file(self, file_name: str) -> AsyncGenerator[bytes, None]:
        """
        Retrieve the content of a file as an async generator.
        Args:
            file_name: Name of the file to retrieve.
        Returns:
            Async generator yielding chunks of file content.
        """
        file_path = self.generate_file_name(file_name)
        async with aiofiles.open(file_path, mode="rb") as file:
            while chunk := await file.read(1024 * 1024):
                yield chunk


    def delete_file(self, file_name: str):
        """
        Delete a file from the local storage.
        Args:
            file_name: Name of the file to be deleted.
        """
        file_path = self.generate_file_name(file_name)
        if os.path.exists(file_path):
            os.remove(file_path)
