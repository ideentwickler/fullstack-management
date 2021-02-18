import enum
from typing import TYPE_CHECKING

from sqlalchemy import Column, ForeignKey, Integer, String, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from app.db.session import SessionLocal
from app.db.base_class import Base

db = SessionLocal()

if TYPE_CHECKING:
    from .user import User  # noqa: F401


class MediaType(enum.Enum):
    REPORTING = 'REPORTING'
    PICTURE = 'PICTURE'
    IMPORT = 'IMPORT'
    OTHER = 'OTHER'


class Media(Base):
    id = Column(UUID(as_uuid=True), primary_key=True, index=True)
    type = Column(Enum(MediaType), default=MediaType.OTHER)
    filename = Column(String, unique=True, index=True)

    owner_id = Column(Integer, ForeignKey("user.id"))
    owner = relationship("User", back_populates="claims")


