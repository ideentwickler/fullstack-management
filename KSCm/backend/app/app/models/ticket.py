import enum
from typing import TYPE_CHECKING

from sqlalchemy import Column, ForeignKey, Integer, String, Enum, desc
from sqlalchemy.orm import relationship
from sqlalchemy.ext.hybrid import hybrid_method, hybrid_property
from app.db.session import SessionLocal
from app.db.base_class import Base

db = SessionLocal()

if TYPE_CHECKING:
    from .user import User  # noqa: F401
    from .store import Store  # noqa: F401


class TicketStatus(enum.Enum):
    NEW = '1-NEU'
    OPEN_QUESTION = '3-KL'
    ANSWERED_QUESTION = '5-BEANT'
    IN_PROGRESS = '8-BEAR'
    ORDERED = '9-ABNA'
    CLOSED = 'GESCHLOSSEN'


class TicketKind(enum.Enum):
    IMPORTED = 'IMPORTIERT'
    COMMISSION = 'KOMMISSION'
    CLAIM = 'REKLAMATION'
    CONNECTED = 'VERKNUEPFT'
    INCOMPLETE = 'UNVOLLSTAENDIG'


class Ticket(Base):
    id = Column(Integer, primary_key=True, index=True)
    ticket_id = Column(Integer, unique=True, index=True)
    contract_nr = Column(Integer, unique=False, index=True)
    customer_name = Column(String, index=True)
    status = Column(Enum(TicketStatus), default=TicketStatus.NEW)
    kind = Column(Enum(TicketKind), default=TicketKind.INCOMPLETE)

    owner_id = Column(Integer, ForeignKey("user.id"))
    owner = relationship("User", back_populates="tickets")

    store_internal_id = Column(Integer, ForeignKey("store.internal_id"))

    claims = relationship("Claim", back_populates="ticket")
