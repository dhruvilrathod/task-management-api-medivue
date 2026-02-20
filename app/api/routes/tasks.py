from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.responses import JSONResponse
from sqlalchemy import select, func, or_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload



router_v1 = APIRouter(prefix="/tasks")

@router_v1.get("/")
def get_tasks():
    return JSONResponse(content={"message": "This is the GET /tasks endpoint for API v1"})