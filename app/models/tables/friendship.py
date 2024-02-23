from app.extensions import Base, db
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, ForeignKey
from uuid import uuid4, UUID



class Friendship(Base):
    id = db.Column(String(36), primary_key=True, default=lambda: str(uuid4()))
    user_id: Mapped[UUID] = mapped_column(String(36), ForeignKey('user.id'), unique=False, nullable=False)
    friend_id: Mapped[UUID] = mapped_column(String(36), ForeignKey('user.id'), unique=False, nullable=False)
    friend = relationship('User', backref='friend', foreign_keys=[friend_id])
    def __init__(self, user_id: UUID, friend_id: UUID):
        self.user_id = user_id
        self.friend_id = friend_id