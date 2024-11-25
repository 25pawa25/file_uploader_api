from abc import ABC

from repository.base.abc_file_repository import AbstractFileRepository


class AbstractS3Repository(AbstractFileRepository, ABC):
    ...