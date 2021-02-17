import enum
from typing import TYPE_CHECKING

from sqlalchemy import Column, ForeignKey, Integer, String, Enum, Float, desc
from sqlalchemy.orm import relationship
from sqlalchemy.ext.hybrid import hybrid_method, hybrid_property
from app.db.session import SessionLocal
from app.db.base_class import Base

db = SessionLocal()

if TYPE_CHECKING:
    from .user import User  # noqa: F401
    from .store import Store  # noqa: F401
    from .ticket import Ticket  # noqa: F401


class ClaimKind(enum.Enum):
    WAREHOUSE = 'LAGER'
    SUPPLIER = 'LIEFERANT'
    ASSEMBLER = 'MONTEUR'
    SELLER = 'VERKÄUFER'
    CUSTOMER = 'KUNDE'


class Claim(Base):
    id = Column(Integer, primary_key=True, index=True)
    contract_nr = Column(Integer, nullable=False, index=True)
    bill = Column(Float, default=0.00, nullable=False)
    discharge = Column(Float, nullable=True)
    kind = Column(Enum(ClaimKind), default=ClaimKind.WAREHOUSE)

    ticket_id = Column(Integer, ForeignKey("ticket.ticket_id"))
    ticket = relationship("Ticket", back_populates="claims")

    owner_id = Column(Integer, ForeignKey("user.id"))
    owner = relationship("User", back_populates="claims")

    store_internal_id = Column(Integer, ForeignKey("store.internal_id"))
    store = relationship("Store", back_populates="claims")


