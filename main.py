#!/usr/bin/env python3

from src.todo.cli import ToDoCLI
from src.todo.db import get_session


def main():
    with get_session() as db_session:
        cli = ToDoCLI(db_session)
        cli.run()


if __name__ == "__main__":
    main()
