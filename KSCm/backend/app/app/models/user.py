from typing import TYPE_CHECKING

from sqlalchemy import Boolean, Column, Integer, String
from sqlalchemy.orm import relationship

from app.db.base_class import Base

if TYPE_CHECKING:
    from .ticket import Ticket  # noqa: F401
    from .item import Item  # noqa: F401
    from .claim import Claim  # noqa: F401
    from .media import Media  # noqa: F401


class User(Base):
    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String, index=True)
    last_name = Column(String, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean(), default=True)
    is_superuser = Column(Boolean(), default=False)

    tickets = relationship("Ticket", back_populates="owner")
    items = relationship("Item", back_populates="owner")
    claims = relationship("Claim", back_populates="owner")
    media = relationship("Media", back_populates="owner")
