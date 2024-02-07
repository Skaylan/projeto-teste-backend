from app.config.app_config import *
from app.config.db_config import *
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Text
from uuid import uuid4, UUID
from datetime import datetime


class UserType(Base):
    id = db.Column(String(36), primary_key=True, default=lambda: str(uuid4()))
    descr: Mapped[str] = mapped_column(String(45), unique=False, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    
    def __init__(self, descr: str):
        self.descr = descr