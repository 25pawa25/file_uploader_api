from common.dependencies.registrator import add_factory_to_mapper

from repository.local_storage_implementation.file_repository import FileRepository
from services.file.adc_file import AbstractFileService
from services.file.file import FileService


@add_factory_to_mapper(AbstractFileService)
def create_file_service():
    return FileService(file_repository=FileRepository(), )
