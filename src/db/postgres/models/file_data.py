from sqlalchemy import Boolean, PrimaryKeyConstraint, String, BigInteger
from sqlalchemy.orm import Mapped

from db.postgres.models.base_model import BaseModel, Column
from db.postgres.models.mixins import IdMixin, TsMixinCreated


class FileData(BaseModel, IdMixin, TsMixinCreated):
    """Data model for file data table."""

    __tablename__ = "file_data"
    __table_args__ = (PrimaryKeyConstraint("id", name="file_data_pkey"),)

    size: Mapped[str] = Column(BigInteger, nullable=True)
    format: Mapped[str] = Column(String(127), nullable=True)
    name: Mapped[str] = Column(String(255), nullable=False)
    extension: Mapped[str] = Column(String(127), nullable=False)
    will_be_deleted: Mapped[bool] = Column(Boolean, default=False, nullable=False)

    def __repr__(self):
        return (
            f"FileData(id={self.id}, size={self.size}, format={self.format}, "
            f"name={self.name}, extension={self.extension}, will_be_deleted={self.will_be_deleted})"
        )
