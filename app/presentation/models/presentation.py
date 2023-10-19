from sqlalchemy import Column, Unicode, BigInteger, Boolean, ForeignKey
from sqlalchemy.orm import relationship
import uuid
from sqlalchemy.dialects.postgresql import UUID

from core.db import Base
from core.db.mixins import TimestampMixin


class Presentation(Base, TimestampMixin):
    __tablename__ = "presentation"

    id = Column(UUID(as_uuid=True), primary_key=True, nullable=False, default=uuid.uuid4)
    title = Column(Unicode(255), nullable=True)
    subject = Column(Unicode(255), nullable=True)
    user_id = Column(BigInteger, ForeignKey('users.id'))

    slides = relationship("Slide", back_populates="presentation")

    user = relationship("User", back_populates="presentations")
    prompt = relationship("PromptHistory", back_populates="presentation")
    