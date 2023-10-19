from sqlalchemy import Column, Unicode, BigInteger, Boolean, ForeignKey
from sqlalchemy.orm import relationship
import uuid
from sqlalchemy.dialects.postgresql import UUID

from core.db import Base
from core.db.mixins import TimestampMixin


class PromptHistory(Base, TimestampMixin):
    __tablename__ = "prompt_history"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    prompt = Column(Unicode(1024), nullable=False)

    user_id = Column(BigInteger, ForeignKey('users.id'))
    presentation_id = Column(UUID(as_uuid=True), ForeignKey('presentation.id'))

    presentation = relationship("Presentation", back_populates="prompt")

