from app.extensions import Base, db
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, ForeignKey
from uuid import uuid4, UUID

class Post(Base):
    id = db.Column(String(36), primary_key=True, default=lambda: str(uuid4()))
    content: Mapped[str] = mapped_column(String(240), unique=False, nullable=False)
    owner_id: Mapped[UUID] = mapped_column(String(36), ForeignKey('user.id'), unique=False, nullable=False)
    owner_info = relationship('User', backref='post')
    
    
    def __init__(self, content: str, owner_id: UUID):
        self.content = content
        self.owner_id = owner_id