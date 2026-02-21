# Task Management API - Assesssment

An efficient and scalable REST API designed with FastAPI, PostgreSQL, and SQLAlchemy to handle task management features like task creation, advanced searching, tagging, deadlines, and soft deletion.

---

## Quick Start

### Prerequisites
- Docker & Docker Compose
- Python

### Start the container

```bash
docker-compose up --build
```

## Monitoring and documentation APIs:
- **Swagger UI (docs)**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **Health check**: http://localhost:8000/health

---

## API Endpoints

A versioned URL API approach is taken for potential future enhancement.

| Method   | Path            | Description                              |
|----------|-----------------|------------------------------------------|
| `POST`   | `/api/v1/tasks`        | Create a new task                        |
| `GET`    | `/api/v1/tasks`        | Retrieve tasks with sorting, filtering & pagination   |
| `GET`    | `/api/v1/tasks/{id}`   | Get detailed information of a specific task                        |
| `PATCH`  | `/api/v1/tasks/{id}`   | Modify a task partially                  |
| `DELETE` | `/api/v1/tasks/{id}`   | Soft-delete a task                       |



## Design Choices

### Database: PostgreSQL

- PostgreSQL was selected as the database for its robustness and features:
- High performance for complex queries and large datasets
- ACID compliance and strong consistency guarantees
- Integration with asyncpg for asynchronous operations

### Soft Delete

Tasks are soft-deleted by setting the deleted flag to true. 

The default query behavior excludes tasks marked as deleted, but a background task or admin endpoint could be used to clean up old records.

### Indexing

The following indexes are applied for efficient filtering:

```sql
CREATE INDEX idx_tasks_priority  ON tasks (priority);
CREATE INDEX idx_tasks_completed ON tasks (completed);
CREATE INDEX idx_tasks_due_date ON tasks (due_date);
```

`priority`, `completed`, and `due_Date` are especially important for filtering tasks efficiently.

### Validation & Error Handling

All validation is handled through Pydantic models. Errors are consistently returned with clear descriptions.

```json
{
    "error": "Validation failed",
    "details": "Input should be less than or equal to 5"
}
```

This is enforced globally via a custom `RequestValidationError` and `HttpException` handler on the FastAPI app.

---

## Production Readiness Improvements

The following improvements would be made before deploying this to production:

### 1. Database Caching with Redis

To reduce the load on the database and improve performance for frequently accessed data (e.g., tasks with common filters), Redis can be used as a caching layer. Common queries, such as fetching tasks by priority or tags, can be cached in Redis to avoid repetitive database calls.

- Caching Strategy: Cache responses for common filters and purge cache on task updates or deletions.

- Tools: Use aioredis for asynchronous Redis interactions with FastAPI.

### 2. Connection Pooling & Load Balancing
For handling high traffic, connection pooling and load balancing can be set up:
- PostgreSQL Connection Pooling: Use asyncpg with pooling settings (pool_size, max_overflow, etc.) to manage connections efficiently.
- Load Balancing: Set up load balancing with tools like NGINX or HAProxy in front of the API instances to distribute traffic across multiple application servers.

### 3. Caching API Responses with FastAPI
Leverage FastAPI’s built-in support for caching headers to reduce the load on endpoints that return static or infrequently updated data (e.g., /tasks).
- Implementation: Use Cache-Control headers and integrate with a caching library like cachetools for in-memory caching.


### 4. Structured Logging and Error Reporting
Enable structured logging with proper log levels (INFO, DEBUG, ERROR) to facilitate monitoring and debugging:
