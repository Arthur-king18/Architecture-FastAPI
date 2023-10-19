from sqlalchemy import Column, Unicode, BigInteger, Boolean, Integer, ForeignKey, String
from sqlalchemy.orm import relationship
import uuid
from sqlalchemy.dialects.postgresql import UUID
from core.db import Base
from core.db.mixins import TimestampMixin


class Slide(Base, TimestampMixin):
    __tablename__ = "slide"

    id = Column(UUID(as_uuid=True), primary_key=True, nullable=False, default=uuid.uuid4)
    header = Column(Unicode(255), nullable=True)
    bgColor = Column(Unicode(255), nullable=True)
    paragraph = Column(Unicode(1024), nullable=True)
    order = Column(Integer, nullable=False, default=0)
    is_active = Column(Boolean, default=True)
    is_deleted = Column(Boolean, default=False)

    image_path = Column(Unicode(255), nullable=True, default=None)
    image_background_path = Column(Unicode(255), nullable=True, default=None)
    presentation_id = Column(UUID(as_uuid=True), ForeignKey('presentation.id'))
    
    presentation = relationship("Presentation", back_populates="slides")