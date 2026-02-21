from sqlalchemy import Column, Index, Integer, String, UniqueConstraint, func
from sqlalchemy.orm import relationship

from app.configs.database import Base


class Tag(Base):
    __tablename__ = "tags"

    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)

    tasks = relationship(
        "Task",
        secondary="task_tags",
        back_populates="tags",
        lazy="selectin",
    )

    __table_args__ = (
        Index(
            "uq_tags_name_lower",
            func.lower(name),
            unique=True,
        ),
    )