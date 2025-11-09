from __future__ import annotations

import datetime
from typing import Optional

from ..db import SessionLocal
from ..models.task import TaskStatus
from ..repositories import TaskRepository, ProjectRepository
from ..services import ToDoListManager


class ToDoCLI:
    def __init__(self, db_session: SessionLocal):
        project_repository = ProjectRepository(db_session)
        task_repository = TaskRepository(db_session)
        self.manager = ToDoListManager(
            task_repository=task_repository,
            project_repository=project_repository
        )
        self.running = True

    def run(self) -> None:
        print("Welcome to My Awesome ToDo List Application!")
        print("=" * 40)

        while self.running:
            self._display_menu()
            choice = input("\nEnter your choice (1-9): ").strip()
            self._handle_choice(choice)

    def _display_menu(self) -> None:
        print("\n" + "=" * 40)
        print("ToDo List Menu")
        print("=" * 40)
        print("1. Create Project")
        print("2. Edit Project")
        print("3. Delete Project")
        print("4. Add Task to Project")
        print("5. Change Task Status")
        print("6. Edit Task")
        print("7. Delete Task")
        print("8. List All Projects")
        print("9. List Tasks in Project")
        print("0. Exit")
    
    def _handle_choice(self, choice: str) -> None:
        try:
            if choice == "1":
                self._create_project()
            elif choice == "2":
                self._edit_project()
            elif choice == "3":
                self._delete_project()
            elif choice == "4":
                self._add_task()
            elif choice == "5":
                self._change_task_status()
            elif choice == "6":
                self._edit_task()
            elif choice == "7":
                self._delete_task()
            elif choice == "8":
                self._list_projects()
            elif choice == "9":
                self._list_project_tasks()
            elif choice == "0":
                self._exit()
            else:
                print("Invalid choice. Please try again.")
        except ValueError as e:
            print(f"Error: {e}")
        except KeyboardInterrupt:
            print("\n\nExiting...")
            self.running = False
    
    def _create_project(self) -> None:
        print("\n--- Create Project ---")
        name = input("Enter project name: ").strip()
        description = input("Enter project description: ").strip()

        if not name:
            print("Error: Name is required.")
            return

        project = self.manager.create_project(name, description)
        print(f"Success: Project '{project.name}' created with ID: {project.id}")
    
    def _edit_project(self) -> None:
        print("\n--- Edit Project ---")
        project_id = input("Enter project ID: ").strip()

        if not project_id:
            print("Error: Project ID is required.")
            return
        
        project = self.manager.get_project(project_id)
        if project is None:
            print("Error: Project not found.")
            return
        
        print(f"Current project: {project.name} - {project.description}")
        new_name = input("Enter new name (or press Enter to keep current): ").strip()
        new_description = input("Enter new description (or press Enter to keep current): ").strip()

        if not new_name:
            new_name = project.name
        if not new_description:
            new_description = project.description

        self.manager.edit_project(project_id, new_name, new_description)
        print(f"Success: Project updated to '{new_name}'")

    def _delete_project(self) -> None:
        print("\n--- Delete Project ---")
        project_id = input("Enter project ID: ").strip()

        if not project_id:
            print("Error: Project ID is required.")
            return

        project = self.manager.get_project(project_id)
        if project is None:
            print("Error: Project not found.")
            return

        confirm = input(f"Are you sure you want to delete project '{project.name}' and all its tasks? (y/N): ").strip().lower()
        if confirm == 'y':
            if self.manager.delete_project(project_id):
                print(f"Success: Project '{project.name}' and all its tasks deleted.")
            else:
                print("Error: Failed to delete project.")
        else:
            print("Project deletion cancelled.")

    def _add_task(self) -> None:
        print("\n--- Add Task to Project ---")
        project_id = input("Enter project ID: ").strip()

        if not project_id:
            print("Error: Project ID is required.")
            return

        project = self.manager.get_project(project_id)
        if project is None:
            print("Error: Project not found.")
            return

        title = input("Enter task title: ").strip()
        description = input("Enter task description: ").strip()
        deadline_str = input("Enter deadline (YYYY-MM-DD) or press Enter to skip: ").strip()

        if not title:
            print("Error: Title is required.")
            return

        deadline = None
        if deadline_str:
            try:
                deadline = datetime.datetime.strptime(deadline_str, "%Y-%m-%d")
            except ValueError:
                print("Error: Invalid date format. Use YYYY-MM-DD")
                return
        
        task = self.manager.add_task_to_project(project_id, title, description, deadline)
        print(f"Success: Task '{task.title}' added to project '{project.name}' with ID: {task.id}")

    def _change_task_status(self) -> None:
        print("\n--- Change Task Status ---")
        task_id = input("Enter task ID: ").strip()

        if not task_id:
            print("Error: Task ID is required.")
            return

        status_map: dict[str, TaskStatus] = {str(i): status for i, status in enumerate(TaskStatus)}  # NOQA
        print("Available statuses:")
        for i, status in status_map.items():
            print(f"{i}. {status.value}")

        status_choice = input("Enter status choice (1-3): ").strip()

        if status_choice not in status_map:
            print("Error: Invalid status choice.")
            return
        
        task = self.manager.change_task_status(task_id, status_map[status_choice])
        print(f"Success: Task '{task.title}' status changed to {task.status}")
    
    def _edit_task(self) -> None:
        print("\n--- Edit Task ---")
        task_id = input("Enter task ID: ").strip()

        if not task_id:
            print("Error: Task ID is required.")
            return

        task = self.manager.tasks.get(task_id)
        if task is None:
            print("Error: Task not found.")
            return

        print(f"Current task: {task.title} - {task.description} (Status: {task.status})")

        new_title = input("Enter new title (or press Enter to keep current): ").strip()
        new_description = input("Enter new description (or press Enter to keep current): ").strip()
        new_deadline_str = input("Enter new deadline (YYYY-MM-DD) or press Enter to keep current: ").strip()

        new_deadline = None
        if new_deadline_str:
            try:
                new_deadline = datetime.datetime.strptime(new_deadline_str, "%Y-%m-%d")
            except ValueError:
                print("Error: Invalid date format. Use YYYY-MM-DD")
                return

        status_map: dict[str, TaskStatus] = {str(i): status for i, status in enumerate(TaskStatus)}  # NOQA
        print("Available statuses:")
        for i, status in status_map.items():
            print(f"{i}. {status.value}")
        print(f"{len(status_map)}. Keep current status")

        status_choice = input(f"Enter status choice (0-{len(status_map)}): ").strip()
        new_status = None
        if status_choice in list(status_map.keys()):
            new_status = status_map[status_choice]

        self.manager.edit_task(
            task_id,
            new_title if new_title else None,
            new_description if new_description else None,
            new_deadline,
            new_status
        )
        print(f"Success: Task updated")

    def _delete_task(self) -> None:
        print("\n--- Delete Task ---")
        task_id = input("Enter task ID: ").strip()

        if not task_id:
            print("Error: Task ID is required.")
            return

        task = self.manager.tasks.get(task_id)
        if task is None:
            print("Error: Task not found.")
            return

        confirm = input(f"Are you sure you want to delete task '{task.title}'? (y/N): ").strip().lower()
        if confirm == 'y':
            if self.manager.delete_task(task_id):
                print(f"Success: Task '{task.title}' deleted.")
            else:
                print("Error: Failed to delete task.")
        else:
            print("Task deletion cancelled.")

    def _list_projects(self) -> None:
        print("\n--- All Projects ---")
        projects = self.manager.list_all_projects()

        if not projects:
            print("No projects found.")
            return

        for project in projects:
            print(f"ID: {project.id}")
            print(f"Name: {project.name}")
            print(f"Description: {project.description}")
            print(f"Created: {project.created_at.strftime('%Y-%m-%d %H:%M:%S')}")
            print(f"Tasks: {len(project.tasks)}")
            print("-" * 30)

    def _list_project_tasks(self) -> None:
        print("\n--- Project Tasks ---")
        project_id = input("Enter project ID: ").strip()

        if not project_id:
            print("Error: Project ID is required.")
            return

        try:
            tasks = self.manager.list_project_tasks(project_id)

            if not tasks:
                print("No tasks found in this project.")
                return

            project = self.manager.get_project(project_id)
            print(f"Tasks in project '{project.name}':")
            print("-" * 50)

            for task in tasks:
                deadline_str = task.deadline.strftime('%Y-%m-%d') if task.deadline else "No deadline"
                print(f"ID: {task.id}")
                print(f"Title: {task.title}")
                print(f"Description: {task.description}")
                print(f"Status: {task.status}")
                print(f"Deadline: {deadline_str}")
                print(f"Created: {task.created_at.strftime('%Y-%m-%d %H:%M:%S')}")
                print("-" * 30)

        except ValueError as e:
            print(f"Error: {e}")

    def _exit(self) -> None:
        print("Thank you for using My ToDo List Application!")
        self.running = False
