from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from fastapi.responses import JSONResponse
from typing import Optional


from app.configs.database import get_db
from app.schemas.tasks import PaginatedTasks, TaskCreate, TaskResponse, TaskUpdate
from app.services.task_service import create_task, delete_task, list_tasks, update_task, get_task_or_404

router_v1 = APIRouter(prefix="/tasks")


@router_v1.get("", response_model=PaginatedTasks)
def get_tasks_endpoint(
    completed: Optional[bool] = None,
    priority: Optional[int] = None,
    tags: Optional[str] = Query(None, description="CSV list of tags"),
    sort_by: str = Query("created_at", pattern="^(created_at|due_date|priority)$"),
    order: str = Query("desc", pattern="^(asc|desc)$"),
    limit: int = Query(10, ge=1, le=100),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_db),
):
    tag_list = tags.split(",") if tags else None

    total, tasks = list_tasks(
            db,
            completed=completed,
            priority=priority,
            tags=tag_list,
            sort_by=sort_by,
            order=order,
            limit=limit,
            offset=offset,
        )

    return {
        "total": total,
        "limit": limit,
        "offset": offset,
        "items": [
            {
                "id": task.id,
                "title": task.title,
                "description": task.description,
                "priority": task.priority,
                "completed": task.completed,
                "due_date": task.due_date,
                "tags": [tag.name for tag in task.tags],
                "created_at": task.created_at,
                "updated_at": task.updated_at,
            }
            for task in tasks
        ]
    }



@router_v1.post(
    "",
    response_model=TaskResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_task_endpoint(
    payload: TaskCreate,
    db: Session = Depends(get_db),
):
    task = create_task(db, payload)

    return TaskResponse(
        id=task.id,
        title=task.title,
        description=task.description,
        priority=task.priority,
        completed=task.completed,
        due_date=task.due_date,
        tags=[tag.name for tag in task.tags],
        created_at=task.created_at,
        updated_at=task.updated_at,
    )



@router_v1.get("/{task_id}", response_model=TaskResponse)
def get_task_by_id_endpoint(task_id: int, db: Session = Depends(get_db)):
    task = get_task_or_404(db, int(task_id))
    print("task found: ", task)

    return TaskResponse(
        id=task.id,
        title=task.title,
        description=task.description,
        priority=task.priority,
        completed=task.completed,
        due_date=task.due_date,
        tags=[tag.name for tag in task.tags],
        created_at=task.created_at,
        updated_at=task.updated_at,
    )



@router_v1.patch(
    "/{task_id}", 
    response_model=TaskResponse
)
def patch_task_endpoint(
    task_id: int,
    payload: TaskUpdate,
    db: Session = Depends(get_db),
):
    task = update_task(db, task_id, payload)

    return {
        **task.__dict__,
        "tags": [t.name for t in task.tags],
    }



@router_v1.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task_endpoint(
    task_id: int,
    db: Session = Depends(get_db),
):
    delete_task(db, task_id)