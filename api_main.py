#!/usr/bin/env python3

"""FastAPI Web API entry point."""

import uvicorn

from src.todo.api.app import app


def main():
    """Run the FastAPI application server."""
    uvicorn.run(
        "src.todo.api.app:app",
        host="0.0.0.0",
        port=8000,
        reload=True,  # Enable auto-reload in development
    )


if __name__ == "__main__":
    main()

