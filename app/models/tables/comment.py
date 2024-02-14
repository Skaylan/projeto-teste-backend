from app.config.app_config import *
from app.config.db_config import *
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, ForeignKey, Text
from uuid import uuid4, UUID
from datetime import datetime



class Comment(Base):
    id = db.Column(String(36), primary_key=True, default=lambda: str(uuid4()))
    comment: Mapped[str] = mapped_column(String(240), unique=False, nullable=False)
    owner_id: Mapped[UUID] = mapped_column(String(36), ForeignKey('user.id'), unique=False, nullable=False)
    post_id: Mapped[UUID] = mapped_column(String(36), ForeignKey('post.id'), unique=False, nullable=False)
    reply = relationship('Reply', backref='reply_comment')

    def __init__(self, comment: str, post_id: UUID, owner_id: str):
        self.comment = comment
        self.post_id = post_id
        self.owner_id = owner_id