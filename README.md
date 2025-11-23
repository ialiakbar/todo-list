# ToDo List Application

A RESTful Web API for ToDo List management built with Python, FastAPI, and PostgreSQL. Features project and task management with automatic validation, business rules, and database persistence.

> **Note**: The CLI interface is **deprecated**. Please use the Web API instead. The CLI may be removed in a future version.

## Features

- **Project Management**: Create, edit, and delete projects
- **Task Management**: Add, edit, delete, and change status of tasks within projects
- **Status Tracking**: Tasks can have three statuses: TODO, DOING, DONE
- **Deadline Support**: Optional deadline setting for tasks
- **Validation**: Input validation with configurable limits
- **Cascade Delete**: Deleting a project removes all associated tasks

## Installation

### Prerequisites
- Python 3.12+
- Poetry (for dependency management)
- Docker and Docker Compose (for PostgreSQL database)

### Setup

1. **Clone the repository**:
   ```bash
   git clone https://github.com/ialiakbar/todo-list
   cd todo-list
   ```

2. **Start PostgreSQL database**:
   ```bash
   docker-compose -f infra/docker-compose.yml up -d
   ```
   This will start a PostgreSQL container on port 5431.

3. **Run database migrations**:
   ```bash
   poetry run alembic upgrade head
   ```

4. **Install dependencies**:
   ```bash
   poetry install
   ```

5. **Configure environment**:
   ```bash
   cp .env.example .env
   ```
   
   Edit `.env` file to customize limits and database connection:
   ```
   MAX_NUMBER_OF_PROJECTS=5
   MAX_NUMBER_OF_TASKS=50
   DATABASE_URL=postgresql://todo-user:todo-pass@localhost:5431/todo-db
   DATABASE_ECHO=false
   ```

6. **Run the Web API server**:
   ```bash
   poetry run python api_main.py
   ```
   
   The API will be available at:
   - API Base: http://localhost:8000/api/v1
   - Interactive API Docs (Swagger): http://localhost:8000/docs
   - Alternative API Docs (ReDoc): http://localhost:8000/redoc

   **Note**: The CLI interface (`poetry run python main.py` or `poetry run todo`) is deprecated and will show a deprecation warning.

## Usage

### Web API (Primary Interface)

The application provides a RESTful Web API with the following endpoints:

#### Projects

- `GET /api/v1/projects` - List all projects
- `POST /api/v1/projects` - Create a new project
- `GET /api/v1/projects/{project_id}` - Get a project by ID
- `PUT /api/v1/projects/{project_id}` - Update a project
- `DELETE /api/v1/projects/{project_id}` - Delete a project

#### Tasks

- `GET /api/v1/projects/{project_id}/tasks` - List all tasks in a project
- `POST /api/v1/projects/{project_id}/tasks` - Create a new task in a project
- `GET /api/v1/tasks/{task_id}` - Get a task by ID
- `PUT /api/v1/tasks/{task_id}` - Update a task (partial update supported)
- `PATCH /api/v1/tasks/{task_id}/status` - Change task status
- `DELETE /api/v1/tasks/{task_id}` - Delete a task

#### Health Check

- `GET /api/v1/health` - Check API health status

### API Examples

#### Create a Project

```bash
curl -X POST "http://localhost:8000/api/v1/projects" \
  -H "Content-Type: application/json" \
  -d '{"name": "My Project", "description": "Project description"}'
```

#### Create a Task

```bash
curl -X POST "http://localhost:8000/api/v1/projects/{project_id}/tasks" \
  -H "Content-Type: application/json" \
  -d '{"title": "My Task", "description": "Task description", "deadline": "2025-12-31T23:59:59Z"}'
```

#### List All Projects

```bash
curl "http://localhost:8000/api/v1/projects"
```

### Interactive API Documentation

Once the API server is running, visit:
- **Swagger UI**: http://localhost:8000/docs - Interactive API documentation with "Try it out" functionality
- **ReDoc**: http://localhost:8000/redoc - Alternative API documentation interface

### CLI Interface (Deprecated)

> ⚠️ **The CLI interface is deprecated**. Please use the Web API instead.

The CLI provides a menu-driven interface with the following options:

1. **Create Project** - Create a new project with name and description
2. **Edit Project** - Modify an existing project's details
3. **Delete Project** - Remove a project and all its tasks (cascade delete)
4. **Add Task to Project** - Create a new task within a project
5. **Change Task Status** - Update a task's status (TODO/DOING/DONE)
6. **Edit Task** - Modify task details including title, description, deadline, and status
7. **Delete Task** - Remove a specific task
8. **List All Projects** - Display all projects with their details
9. **List Tasks in Project** - Show all tasks within a specific project
10. **Auto-close Overdue Tasks** - Automatically mark overdue tasks as done (handled by scheduler)
0. **Exit** - Quit the application

To run the CLI (deprecated):
```bash
poetry run python main.py
# or
poetry run todo
```

## Configuration

The application uses environment variables for configuration:

- `MAX_NUMBER_OF_PROJECTS`: Maximum number of projects allowed (default: 5)
- `MAX_NUMBER_OF_TASKS`: Maximum number of tasks per project (default: 50)
- `MAX_PROJECT_NAME_LENGTH`: Maximum length for project name.
- `MAX_PROJECT_DESCRIPTION_LENGTH`: Maximum length for project description.
- `MAX_TASK_TITLE_LENGTH`: Maximum length for task title.
- `MAX_TASK_DESCRIPTION_LENGTH`: Maximum length for task description.
- `DATABASE_URL`: PostgreSQL connection string (required).
- `DATABASE_ECHO`: Enable SQL query logging (default: false).

## Architecture

The application follows a layered architecture with separation of concerns:

- **API Layer** (`src/todo/api/`): FastAPI controllers, Pydantic schemas, and routers
- **Models** (`src/todo/models/`): SQLAlchemy ORM models for Task and Project entities
- **Repositories** (`src/todo/repositories/`): Data access layer with repository pattern
- **Services** (`src/todo/services/`): Business logic layer (ToDoListManager)
- **CLI** (`src/todo/cli/`): Command-line interface (deprecated)
- **Commands** (`src/todo/commands/`): Standalone commands (e.g., auto-close overdue tasks)
- **Config** (`src/todo/config/`): Environment configuration management
- **Database** (`src/todo/db/`): Database session and connection management

## Development

### Project Structure
```
todo/
├── src/todo/
│   ├── api/             # FastAPI Web API layer
│   │   ├── controllers/ # Route handlers
│   │   ├── controller_schemas/ # Pydantic models
│   │   ├── app.py       # FastAPI application
│   │   └── routers.py   # API router configuration
│   ├── models/          # ORM models (ProjectORM, TaskORM)
│   ├── repositories/    # Data access layer
│   ├── services/        # Business logic
│   ├── cli/             # Command-line interface (deprecated)
│   ├── commands/        # Standalone commands
│   ├── db/              # Database configuration
│   ├── exceptions/      # Exception hierarchy
│   ├── config/          # Configuration management
│   └── factory.py       # Dependency injection factory
├── alembic/             # Database migrations
├── api_main.py          # API server entry point
├── main.py              # CLI entry point (deprecated)
├── infra/               # Infrastructure (Docker Compose)
├── pyproject.toml       # Poetry configuration
├── .env.example         # Environment variables template
└── README.md            # This file
```

### Database Migrations

To create a new migration:
```bash
poetry run alembic revision --autogenerate -m "description"
```

To apply migrations:
```bash
poetry run alembic upgrade head
```

To rollback a migration:
```bash
poetry run alembic downgrade -1
```

