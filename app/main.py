from fastapi import FastAPI, Request
from fastapi.concurrency import asynccontextmanager
from fastapi.exceptions import RequestValidationError, HTTPException
from fastapi.responses import JSONResponse, RedirectResponse

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

    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(request: Request, exc: RequestValidationError):
        errors = []
        print(exc)
        for err in exc.errors():
            errors.append(err["msg"])
        
        return JSONResponse(
            status_code=400,
            content={
                "error": "Validation failed",
                "details": ", ".join(errors)
            }
        )


    @app.exception_handler(HTTPException)
    async def http_exception_handler(request: Request, exc: HTTPException):
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "error": exc.detail,
                "details": exc.detail
            }
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