from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.responses import JSONResponse
from sqlalchemy import select, func, or_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

# from app.configs.database import get_db
# from app.models.task import Task, Tag, task_tags
# from app.schemas.task import TaskCreate, TaskOut, TaskUpdate, PaginatedTasks

router = APIRouter()