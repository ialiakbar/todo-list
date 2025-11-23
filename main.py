#!/usr/bin/env python3

"""CLI entry point for ToDoList application.

DEPRECATED: The CLI interface is deprecated. Please use the Web API instead.
Run the API server with: poetry run python api_main.py
Then access the API at http://localhost:8000/docs
"""

import warnings

from src.todo.cli import ToDoCLI
from src.todo.db import get_session


def main():
    """Main CLI entry point (deprecated)."""
    warnings.warn(
        "CLI interface is deprecated. Please use the Web API instead. "
        "Run 'poetry run python api_main.py' to start the API server, "
        "then access http://localhost:8000/docs for API documentation.",
        DeprecationWarning,
        stacklevel=2,
    )
    print("\n⚠️  WARNING: CLI is deprecated. Please use the Web API instead.")
    print("   Start the API server: poetry run python api_main.py")
    print("   API documentation: http://localhost:8000/docs\n")
    
    with get_session() as db_session:
        cli = ToDoCLI(db_session)
        cli.run()


if __name__ == "__main__":
    main()
