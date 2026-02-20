from datetime import datetime
from sqlalchemy.orm import relationship
from app.configs.database import Base
from sqlalchemy import (
    Boolean,
    Column,
    CheckConstraint,
    Date,
    DateTime,
    ForeignKey,
    Index,
    Integer,
    String,
    Table,
)

task_tags = Table(
    "task_tags",
    Base.metadata,
    Column("task_id", ForeignKey("tasks.id", ondelete="CASCADE"), primary_key=True),
    Column("tag_id", ForeignKey("tags.id", ondelete="CASCADE"), primary_key=True),
)


class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True)
    title = Column(String(200), nullable=False)
    description = Column(String, nullable=True)
    priority = Column(Integer, nullable=False, default=3)
    completed = Column(Boolean, default=False, nullable=False)
    due_date = Column(Date, nullable=False)
    is_deleted = Column(Boolean, default=False, nullable=False)

    tags = relationship(
        "Tag",
        secondary=task_tags,
        back_populates="tasks",
        lazy="selectin",
    )

    created_at = Column(
        DateTime(timezone=True),
        nullable=False,
        default=datetime.utcnow,
    )
    updated_at = Column(
        DateTime(timezone=True),
        nullable=False,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
    )

    __table_args__ = (
        CheckConstraint("priority BETWEEN 1 AND 5", name="ck_priority_range"),
        Index("idx_tasks_priority", "priority"),
        Index("idx_tasks_completed", "completed"),
        Index("idx_tasks_due_date", "due_date"),
    )