"""Command to auto-close overdue tasks."""

from __future__ import annotations

from sqlalchemy.orm import Session

from ..factory import create_task_repository
from ..models.task_orm import TaskStatus


def autoclose_overdue_tasks(session: Session) -> int:
    """Auto-close overdue tasks that are not done.

    Finds all tasks where:
    - deadline < now
    - status != DONE

    Marks them as DONE and sets closed_at timestamp.

    Args:
        session: Database session

    Returns:
        Number of tasks that were closed
    """
    task_repo = create_task_repository(session)
    overdue_tasks = task_repo.get_overdue_tasks()

    closed_count = 0
    for task in overdue_tasks:
        if task.status != TaskStatus.DONE:
            task.update_status(TaskStatus.DONE)
            task_repo.update(task)
            closed_count += 1

    if closed_count > 0:
        session.commit()
    else:
        session.rollback()

    return closed_count

