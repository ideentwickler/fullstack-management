import enum
from typing import TYPE_CHECKING

from sqlalchemy import Column, Integer, String, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.ext.hybrid import hybrid_method, hybrid_property

from app.db.base_class import Base

if TYPE_CHECKING:
    from .ticket import Ticket  # noqa
    from .claim import Claim  # noqa


class StoreSupport(enum.Enum):
    DISABLED = 0
    CLAIMS = 1
    FULL = 2


class Store(Base):
    id = Column(Integer, primary_key=True, index=True)
    internal_id = Column(Integer, unique=True, index=True)
    name = Column(String, index=True)
    support = Column(Enum(StoreSupport), default=StoreSupport.DISABLED)

    tickets = relationship("Ticket", backref="store", lazy="dynamic")
    claims = relationship("Claim", backref="claims", lazy="dynamic")

    # https://stackoverflow.com/questions/14361264/the-default-sorting-criteria-of-sqlalchemy
    __mapper_args__ = {
        "order_by": name
    }

    def __repr__(self):
        return f"<{self.__tablename__.upper()} # {self.internal_id} - {self.name}>"



