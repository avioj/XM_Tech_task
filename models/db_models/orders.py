import enum
import uuid

from sqlalchemy import Enum, Column, String
from sqlalchemy.dialects.postgresql import UUID, DOUBLE_PRECISION

from . import Base


class StatusEnum(enum.Enum):
    pending = 1
    executed = 2
    canceled = 3

    def __str__(self):
        return self.name


class Order(Base):
    __tablename__ = 'orders'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    quantity = Column(DOUBLE_PRECISION)
    stocks = Column(String)
    status = Column(Enum(StatusEnum))
