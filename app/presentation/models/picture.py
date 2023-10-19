from sqlalchemy import Column, Unicode, BigInteger, Boolean, ForeignKey, DateTime
from sqlalchemy.orm import relationship
import uuid
from sqlalchemy.dialects.postgresql import UUID

from core.db import Base
from core.db.mixins import TimestampMixin


class Picture(Base):
    __tablename__ = "picture"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    source = Column(Unicode(255), nullable=True)
    prompt = Column(Unicode(1024), nullable=False)
    resolution = Column(Unicode(255), nullable=False)
    type = Column(Unicode(255), nullable=False)
    path = Column(Unicode(255), nullable=False)
    create_at = Column(DateTime, nullable=False)

    user_id = Column(BigInteger, ForeignKey('users.id'))

