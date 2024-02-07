from app.config.app_config import *
from app.config.db_config import *
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, ForeignKey, Text
from uuid import uuid4, UUID
from datetime import datetime

class Post(Base):
    id = db.Column(String(36), primary_key=True, default=lambda: str(uuid4()))
    title: Mapped[str] = mapped_column(String(45), unique=False, nullable=False)
    content: Mapped[str] = mapped_column(String(240), unique=False, nullable=False)
    owner: Mapped[UUID] = mapped_column(String(36), ForeignKey('user.id'), unique=False, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    
    def __init__(self, title: str, content: str, owner: UUID):
        self.title = title
        self.content = content
        self.owner = owner