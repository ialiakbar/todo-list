"""Scheduler for running periodic tasks."""

from __future__ import annotations

import time
import logging
from typing import Optional

import schedule

from ..db import get_session_ctx
from ..config.settings import settings
from .autoclose_overdue import autoclose_overdue_tasks

logger = logging.getLogger(__name__)


def run_autoclose_job() -> None:
    """Job function to run auto-close overdue tasks."""
    try:
        with get_session_ctx() as session:
            count = autoclose_overdue_tasks(session)
            if count > 0:
                logger.info(f"Auto-closed {count} overdue task(s)")
            else:
                logger.debug("No overdue tasks found")
    except Exception as e:
        logger.error(f"Error running auto-close job: {e}", exc_info=True)


def start_scheduler(interval_minutes: Optional[int] = None) -> None:
    """Start the scheduler to run auto-close overdue tasks periodically.

    Args:
        interval_minutes: Interval in minutes between runs (defaults to settings value)
    """
    interval = interval_minutes or settings.AUTOCLOSE_INTERVAL_MINUTES
    schedule.every(interval).minutes.do(run_autoclose_job)
    
    logger.info(f"Scheduler started: auto-close overdue tasks every {interval} minutes")
    
    try:
        while True:
            schedule.run_pending()
            time.sleep(60)  # Check every minute
    except KeyboardInterrupt:
        logger.info("Scheduler stopped by user")
        raise


def run_scheduler_once() -> None:
    """Run the auto-close job once and exit (useful for testing or manual runs)."""
    logger.info("Running auto-close overdue tasks job once")
    run_autoclose_job()

