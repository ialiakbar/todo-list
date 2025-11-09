#!/usr/bin/env python3
"""Scheduler entry point for running periodic tasks."""

import logging
import sys

from src.todo.commands import start_scheduler
from src.todo.config.settings import settings

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

logger = logging.getLogger(__name__)


def main():
    """Run the scheduler."""
    try:
        logger.info("Starting ToDo List scheduler...")
        logger.info(f"Auto-close interval: {settings.AUTOCLOSE_INTERVAL_MINUTES} minutes")
        start_scheduler()
    except KeyboardInterrupt:
        logger.info("Scheduler stopped")
        sys.exit(0)
    except Exception as e:
        logger.error(f"Fatal error in scheduler: {e}", exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    main()

