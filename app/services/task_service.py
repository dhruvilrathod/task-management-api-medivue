from typing import List, Optional

from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import asc, desc, select, func

from app.models.task import Task
from app.models.tag import Tag
from app.schemas.tasks import TaskCreate


def create_task(db: Session, payload: TaskCreate) -> Task:
    task = Task(
        title=payload.title,
        description=payload.description,
        priority=payload.priority,
        due_date=payload.due_date,
    )

    if payload.tags:
        tags = []
        for tag_name in payload.tags:
            tag_name = tag_name.strip().lower()
            tag = db.execute(
                select(Tag).where(Tag.name == tag_name)
            ).scalar_one_or_none()

            if not tag:
                tag = Tag(name=tag_name)
                db.add(tag)

            tags.append(tag)

        task.tags = tags

    db.add(task)
    db.commit()
    db.refresh(task)

    return task


def list_tasks(
    db,
    *,
    completed: Optional[bool] = None,
    priority: Optional[int] = None,
    tags: Optional[List[str]] = None,
    sort_by: str = "created_at",
    order: str = "desc",
    limit: int = 10,
    offset: int = 0,
):
    
    query = select(Task).where(Task.is_deleted == False)

    if completed is not None:
        query = query.where(Task.completed == completed)

    if priority is not None:
        query = query.where(Task.priority == priority)

    if tags:
        normalized_tags = [t.lower() for t in tags]
        query = (
            query.join(Task.tags)
            .where(func.lower(Tag.name).in_(normalized_tags))
            .distinct()
        )

    sort_map = {
        "created_at": Task.created_at,
        "due_date": Task.due_date,
        "priority": Task.priority,
    }

    sort_column = sort_map.get(sort_by, Task.created_at)

    if order == "asc":
        query = query.order_by(asc(sort_column))
    else:
        query = query.order_by(desc(sort_column))

    count_query = select(func.count()).select_from(
        query.subquery()
    )

    total = db.execute(count_query).scalar_one()

    tasks = db.execute(
        query.limit(limit).offset(offset)
    ).scalars().all()

    return total, tasks


def get_task(db, task_id: int) -> Optional[Task]:
    print("Fetching task with ID:", task_id)  # Debug statement
    return db.execute(
        select(Task).where(
            Task.id == task_id,
            Task.is_deleted == False,
        )
    ).scalar_one_or_none()



def update_task(db, task_id: int, data):
    task = get_task_or_404(db, task_id)

    update_data = data.model_dump(exclude_unset=True)

    if "tags" in update_data:
        tags = update_data.pop("tags")
        task.tags.clear()

        if tags:
            normalized = {t.lower() for t in tags}

            existing_tags = db.execute(
                select(Tag).where(Tag.name.in_(normalized))
            ).scalars().all()

            existing_map = {t.name: t for t in existing_tags}

            for tag_name in normalized:
                tag = existing_map.get(tag_name)
                if not tag:
                    tag = Tag(name=tag_name)
                    db.add(tag)
                task.tags.append(tag)

    for field, value in update_data.items():
        setattr(task, field, value)

    db.commit()
    db.refresh(task)

    return task


def delete_task(db, task_id: int):
    task = get_task_or_404(db, task_id)

    task.is_deleted = True
    db.commit()

    return



def get_task_or_404(db, task_id: int) -> Task:
    task = db.execute(
        select(Task).where(
            Task.id == task_id,
            Task.is_deleted == False,
        )
    ).scalar_one_or_none()

    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found",
        )

    return task