from typing import Optional

from pydantic import BaseModel
from pydantic.fields import Field
from pydantic.networks import EmailStr


class FileDataSchema(BaseModel):
    size: Optional[int]
    format: str
    name: str
    extension: str
