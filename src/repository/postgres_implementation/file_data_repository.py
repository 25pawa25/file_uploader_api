import uuid
from datetime import datetime
from typing import Optional, Iterable

from loguru import logger
from sqlalchemy import desc, select, delete

from common.exceptions.file import FileNotExists
from db.postgres.models.file_data import FileData
from repository.interfaces.entity.abc_file_data_repository import AbstractFileDataRepository
from repository.postgres_implementation.base_repository import SQLRepository
from schemas.entities.file_data_entity import FileDataEntity


class SQLFileDataRepository(SQLRepository, AbstractFileDataRepository):
    class_model = FileData
    entity_class = FileDataEntity

    async def add_file_data(self, **fields) -> FileDataEntity:
        """
        Add a file data
        Args:
            **fields: fields of the file data
        """
        return await self.add(self.entity_class(**fields))

    async def get_file_data(self, file_id: uuid.UUID, raise_if_notfound: bool = True) -> FileDataEntity:
        """
        Get a file data by id
        Args:
            file_id: id of the file
        """
        result = await self.session.execute(select(self.class_model).where(self.class_model.id==file_id))
        instance = result.scalar_one_or_none()
        if instance:
            return self.to_entity(instance)
        if raise_if_notfound:
            raise FileNotExists(f"No file found with ID: {file_id}")

    async def get_file_data_to_delete(self) -> Iterable[FileDataEntity]:
        """
        Get a file data to delete
        Returns:
            list of file data to delete
        """
        result = await self.session.execute(select(self.class_model).where(self.class_model.will_be_deleted==True))
        return [self.to_entity(instance) for instance in result.scalars().all()]

    async def update_file_data(self, file_id: uuid.UUID, **fields) -> FileDataEntity:
        """
        Update a file data by id
        Args:
            file_id: id of the file
            **fields: fields of the file data
        """
        return await self.update(self_id=file_id, **fields)

    async def delete_file_data(self, file_id: uuid.UUID):
        """
        Deleting a file data
        Args:
            file_id: id of the file
        """
        stmt = delete(self.class_model).where(self.class_model.id == file_id)
        await self.session.execute(stmt)
        await self.session.commit()
