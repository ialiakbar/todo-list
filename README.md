# ToDo List Application

A command-line ToDo List application built with Python, featuring project and task management with PostgreSQL database persistence.

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

6. **Run the application**:
   ```bash
   poetry run python main.py
   ```
   
   Or using the entry point:
   ```bash
   poetry run todo
   ```

## Usage

The application provides a menu-driven interface with the following options:

1. **Create Project** - Create a new project with name and description
2. **Edit Project** - Modify an existing project's details
3. **Delete Project** - Remove a project and all its tasks (cascade delete)
4. **Add Task to Project** - Create a new task within a project
5. **Change Task Status** - Update a task's status (TODO/DOING/DONE)
6. **Edit Task** - Modify task details including title, description, deadline, and status
7. **Delete Task** - Remove a specific task
8. **List All Projects** - Display all projects with their details
9. **List Tasks in Project** - Show all tasks within a specific project
10. **Auto-close Overdue Tasks** - Automatically mark overdue tasks as done
0. **Exit** - Quit the application

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

- **Models** (`src/todo/models/`): SQLAlchemy ORM models for Task and Project entities
- **Repositories** (`src/todo/repositories/`): Data access layer with repository pattern
- **Services** (`src/todo/services/`): Business logic layer (ToDoListManager)
- **CLI** (`src/todo/cli/`): User interface layer
- **Commands** (`src/todo/commands/`): Standalone commands (e.g., auto-close overdue tasks)
- **Config** (`src/todo/config/`): Environment configuration management
- **Database** (`src/todo/db/`): Database session and connection management

## Development

### Project Structure
```
todo/
├── src/todo/
│   ├── models/          # ORM models (ProjectORM, TaskORM)
│   ├── repositories/    # Data access layer
│   ├── services/        # Business logic
│   ├── cli/             # Command-line interface
│   ├── commands/        # Standalone commands
│   ├── db/              # Database configuration
│   ├── exceptions/      # Exception hierarchy
│   ├── config/          # Configuration management
│   └── factory.py       # Dependency injection factory
├── alembic/             # Database migrations
├── main.py              # Application entry point
├── docker-compose.yml   # PostgreSQL Docker setup
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

