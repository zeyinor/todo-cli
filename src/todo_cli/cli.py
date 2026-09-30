"""Command-line interface for todo-cli."""

import argparse
import sys
from pathlib import Path
from typing import List, Optional

from .storage import DEFAULT_PATH, Storage


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="todo",
        description="A minimal command-line todo manager.",
    )
    parser.add_argument(
        "--file",
        type=Path,
        default=DEFAULT_PATH,
        help=f"Path to the todo data file (default: {DEFAULT_PATH})",
    )

    sub = parser.add_subparsers(dest="command", required=True)

    p_add = sub.add_parser("add", help="Add a new todo")
    p_add.add_argument("text", nargs="+", help="Todo text")

    sub.add_parser("list", help="List all todos")

    p_done = sub.add_parser("done", help="Mark a todo as done")
    p_done.add_argument("id", type=int, help="Todo id")

    p_remove = sub.add_parser("remove", help="Remove a todo")
    p_remove.add_argument("id", type=int, help="Todo id")

    sub.add_parser("clear", help="Remove all todos")

    return parser


# ---------- command handlers ----------

def cmd_add(args, storage: Storage) -> None:
    text = " ".join(args.text).strip()
    if not text:
        print("Todo text cannot be empty.", file=sys.stderr)
        sys.exit(1)
    todo = storage.add(text)
    print(f"Added #{todo.id}: {todo.text}")


def cmd_list(args, storage: Storage) -> None:
    todos = storage.list()
    if not todos:
        print('No todos yet. Add one with: todo add "buy milk"')
        return
    for todo in todos:
        mark = "x" if todo.done else " "
        print(f"[{mark}] {todo.id}. {todo.text}")
    done_count = len(todos) - storage.pending_count()
    print(f"\n{storage.pending_count()} pending, {done_count} done.")


def cmd_done(args, storage: Storage) -> None:
    todo = storage.done(args.id)
    if todo is None:
        print(f"Todo #{args.id} not found.", file=sys.stderr)
        sys.exit(1)
    print(f"Done #{todo.id}: {todo.text}")


def cmd_remove(args, storage: Storage) -> None:
    todo = storage.remove(args.id)
    if todo is None:
        print(f"Todo #{args.id} not found.", file=sys.stderr)
        sys.exit(1)
    print(f"Removed #{todo.id}: {todo.text}")


def cmd_clear(args, storage: Storage) -> None:
    storage.clear()
    print("All todos cleared.")


HANDLERS = {
    "add": cmd_add,
    "list": cmd_list,
    "done": cmd_done,
    "remove": cmd_remove,
    "clear": cmd_clear,
}


def main(argv: Optional[List[str]] = None) -> None:
    parser = build_parser()
    args = parser.parse_args(argv)
    storage = Storage(args.file)
    HANDLERS[args.command](args, storage)


if __name__ == "__main__":
    main()
