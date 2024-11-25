from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel


class FileDataResponse(BaseModel):
    id: UUID
    size: str
    format: str
    name: str
    extension: str
    will_be_deleted: bool

    class Config:
        orm_mode = True
