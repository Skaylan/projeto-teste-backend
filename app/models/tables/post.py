from app.config.app_config import *
from app.config.db_config import *
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, ForeignKey, Text
from uuid import uuid4, UUID
from datetime import datetime

class Post(Base):
    id = db.Column(String(36), primary_key=True, default=lambda: str(uuid4()))
    content: Mapped[str] = mapped_column(String(240), unique=False, nullable=False)
    owner: Mapped[UUID] = mapped_column(String(36), ForeignKey('user.id'), unique=False, nullable=False)
    owner_info = relationship('User', backref='post')
    
    
    def __init__(self, content: str, owner: UUID):
        self.content = content
        self.owner = owner