import uuid
from sqlalchemy import Column, Unicode, BigInteger, Boolean, PickleType, Float, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from core.db import Base
from core.db.mixins import TimestampMixin


class Referral(Base, TimestampMixin):
    __tablename__ = "referral"

    referral_id = Column(UUID(as_uuid=True), primary_key=True, nullable=False, default=uuid.uuid4)
    count_referral = Column(BigInteger, nullable=False, default=0)
    user_id = Column(BigInteger, ForeignKey('users.id'))

    user = relationship("User", back_populates="referral")