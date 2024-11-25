from typing import Optional

from schemas.entities.base_entity import BaseEntity


class FileDataEntity(BaseEntity):
    size: int
    format: str
    name: str
    extension: str
    will_be_deleted: Optional[bool]

    class Config:
        orm_mode = True
