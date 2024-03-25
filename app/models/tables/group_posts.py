from app.extensions import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, ForeignKey
from uuid import uuid4, UUID


class GroupPosts(Base):
  id: Mapped[UUID] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid4()))
  post_id: Mapped[UUID] = mapped_column(String(36), ForeignKey("post.id"), unique=False, nullable=False)
  group_holder_id: Mapped[UUID] = mapped_column(String(36), ForeignKey("group.id"), unique=False, nullable=False)
  
  def __init__(self, post_id: UUID, group_holder_id: UUID):
    self.post_id = post_id
    self.group_holder_id = group_holder_id