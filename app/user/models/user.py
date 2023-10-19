from sqlalchemy import Column, Unicode, BigInteger, Boolean, PickleType, Float
from sqlalchemy.orm import relationship
from core.db import Base
from core.db.mixins import TimestampMixin


class User(Base, TimestampMixin):
    __tablename__ = "users"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    password = Column(Unicode(255), nullable=False)
    email = Column(Unicode(255), nullable=False, unique=True)
    username = Column(Unicode(255), nullable=False, unique=True)
    full_name = Column(Unicode(255), nullable=True, unique=False)
    is_admin = Column(Boolean, default=False)
    credits = Column(Float, default=400)

    presentations = relationship("Presentation", back_populates="user")
    referral = relationship("Referral", back_populates="user")
