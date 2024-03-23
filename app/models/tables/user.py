from app.extensions import Base, db
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, ForeignKey, Integer
from .comment import Comment
from .user_data import UserData
from .reply import Reply
from uuid import uuid4, UUID


class User(Base):
    id = db.Column(String(36), primary_key=True, default=lambda: str(uuid4()))
    name: Mapped[str] = mapped_column(String(45), unique=False, nullable=False)
    email: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(String(256), unique=False, nullable=False)
    user_type_id: Mapped[int] = mapped_column(Integer, ForeignKey('user_type.id'), unique=False, nullable=False)
    comments = relationship(Comment, backref='owner', lazy='dynamic', foreign_keys=[Comment.owner_id])
    replies = relationship('Reply', backref='reply_owner', lazy='dynamic', foreign_keys=[Reply.owner_id])
    user_data = relationship("UserData", backref='user', uselist=False, foreign_keys=[UserData.user_id], lazy=True)
    
    
    def __init__(self, name: str, email:str, password_hash: str, user_type_id: UUID):
        self.name = name
        self.email = email
        self.password_hash = password_hash
        self.user_type_id = user_type_id