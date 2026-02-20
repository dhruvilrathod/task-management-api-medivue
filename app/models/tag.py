from sqlalchemy import Column, Integer, String, UniqueConstraint
from sqlalchemy.orm import relationship

from app.models.base import Base


class Tag(Base):
    __tablename__ = "tags"

    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False, unique=True, index=True)

    tasks = relationship(
        "Task",
        secondary="task_tags",
        back_populates="tags",
        lazy="selectin",
    )

    __table_args__ = (
        UniqueConstraint("name", name="uq_tag_name"),
    )