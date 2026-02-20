from fastapi import FastAPI
from fastapi.concurrency import asynccontextmanager
from fastapi.responses import RedirectResponse

from app.configs.database import Base, engine
from app.api.routes.tasks import router as tasks_router



def init_app() -> FastAPI:

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


    @app.get("/", include_in_schema=False)
    async def root():
        return RedirectResponse(url="/docs")

    @app.get("/api_status")
    def api_status():
        return {"status": "ok"}

    return app


app = init_app()