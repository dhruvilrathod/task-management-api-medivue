from fastapi import FastAPI
from fastapi.concurrency import asynccontextmanager
from fastapi.responses import RedirectResponse

from app.configs.database import Base, engine
from app.api.routes.tasks import router_v1 as tasks_api_router_v1


# Initialize the FastAPI application
def init_app() -> FastAPI:

    # life cycle management for startup and shutdown events
    @asynccontextmanager
    async def lifespan(app: FastAPI):

        # Startup event: create tables in the database
        Base.metadata.create_all(bind=engine)
        yield  
        

    app = FastAPI(
        title="Task Management API",
        description="A robust task management API built with FastAPI and PostgreSQL for advanced filtering, tagging and deadlines.",
        version="1.0.0",
        lifespan=lifespan
        )

    # Include documentation routers
    @app.get("/", include_in_schema=False)
    async def root():
        return RedirectResponse(url="/docs")

    # API health check endpoint
    @app.get("/api_status")
    def api_status():
        return {"status": "ok"}

    # api endpoints for version 1 of the task management API
    app.include_router(tasks_api_router_v1, prefix="/api/v1")

    return app


app = init_app()