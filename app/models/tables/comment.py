from app.config.app_config import *
from app.config.db_config import *
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, ForeignKey, Text
from uuid import uuid4, UUID
from datetime import datetime



class Comment(Base):
    id = db.Column(String(36), primary_key=True, default=lambda: str(uuid4()))
    comment: Mapped[str] = mapped_column(String(240), unique=False, nullable=False)
    post_id: Mapped[UUID] = mapped_column(String(36), ForeignKey('post.id'), unique=False, nullable=False)
    reply_id: Mapped[UUID] = mapped_column(String(36), ForeignKey('post.id'), unique=False, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


    def __init__(self, comment: str, post_id: UUID, reply_id: UUID):
        self.comment = comment
        self.post_id = post_id
        self.reply_id = reply_id