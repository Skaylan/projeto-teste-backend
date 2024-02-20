from app.extensions import Base, db
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, ForeignKey
from uuid import uuid4, UUID


class Reply(Base):
    id = db.Column(String(36), primary_key=True, default=lambda: str(uuid4()))
    comment: Mapped[str] = mapped_column(String(240), unique=False, nullable=False)
    post_id: Mapped[UUID] = mapped_column(String(36), ForeignKey('post.id'), unique=False, nullable=False)
    owner_id: Mapped[UUID] = mapped_column(String(36), ForeignKey('user.id'), unique=False, nullable=False)
    parent_comment_id: Mapped[UUID] = mapped_column(String(36), ForeignKey('comment.id'), unique=False, nullable=False)


    def __init__(self, comment: str, owner_id: UUID, parent_comment_id: UUID, post_id: UUID):
        self.comment = comment
        self.owner_id = owner_id
        self.parent_comment_id = parent_comment_id
        self.post_id = post_id