from app.config.app_config import *
from app.config.db_config import *
from sqlalchemy.orm import Mapped, mapped_column, relationship, backref
from sqlalchemy import String, Text
from uuid import uuid4, UUID
from datetime import datetime


class UserType(Base):
    id = db.Column(String(36), primary_key=True, default=lambda: str(uuid4()))
    descr: Mapped[str] = mapped_column(String(45), unique=False, nullable=False)
    owner_id = relationship('User', backref='user_type')
    
    
    def __init__(self, descr: str):
        self.descr = descr