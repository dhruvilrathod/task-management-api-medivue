from datetime import date, datetime
from typing import List, Optional

from pydantic import BaseModel, Field, field_validator


class TaskBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = None
    priority: int = Field(ge=1, le=5)
    due_date: date
    tags: Optional[List[str]] = []

    @field_validator("due_date")
    @classmethod
    def due_date_not_in_past(cls, v: date):
        if v < date.today():
            raise ValueError("due_date cannot be in the past")
        return v

class TaskCreate(TaskBase):
    pass


class TaskUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = None
    priority: Optional[int] = Field(None, ge=1, le=5)
    completed: Optional[bool] = None
    due_date: Optional[date] = None
    tags: Optional[List[str]] = None

    @field_validator("due_date")
    @classmethod
    def due_date_not_in_past(cls, v: Optional[date]):
        if v and v < date.today():
            raise ValueError("due_date cannot be in the past")
        return v


class TaskResponse(BaseModel):
    id: int
    title: str
    description: Optional[str]
    priority: int
    completed: bool
    due_date: date
    tags: List[str]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class PaginatedTasks(BaseModel):
    total: int
    limit: int
    offset: int
    items: List[TaskResponse]