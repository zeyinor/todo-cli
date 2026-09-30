"""JSON-backed storage for todo items."""

import json
from pathlib import Path
from typing import List, Optional

from .models import Todo

DEFAULT_PATH = Path.home() / ".todo.json"


class Storage:
    """Loads todos from a JSON file and persists changes back to it."""

    def __init__(self, path: Path = DEFAULT_PATH):
        self.path = Path(path)
        self.todos: List[Todo] = []
        self._load()

    # ---------- internal ----------

    def _load(self) -> None:
        if not self.path.exists():
            self.todos = []
            return
        try:
            with self.path.open("r", encoding="utf-8") as f:
                data = json.load(f)
            if not isinstance(data, list):
                raise ValueError("root must be a list")
            self.todos = [Todo.from_dict(item) for item in data]
        except (json.JSONDecodeError, ValueError, KeyError, TypeError):
            # Corrupted file: start clean rather than crashing.
            self.todos = []

    def _save(self) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with self.path.open("w", encoding="utf-8") as f:
            json.dump(
                [t.to_dict() for t in self.todos],
                f,
                ensure_ascii=False,
                indent=2,
            )

    def _next_id(self) -> int:
        if not self.todos:
            return 1
        return max(t.id for t in self.todos) + 1

    # ---------- public API ----------

    def add(self, text: str) -> Todo:
        todo = Todo(id=self._next_id(), text=text, done=False)
        self.todos.append(todo)
        self._save()
        return todo

    def list(self) -> List[Todo]:
        return list(self.todos)

    def get(self, todo_id: int) -> Optional[Todo]:
        for todo in self.todos:
            if todo.id == todo_id:
                return todo
        return None

    def done(self, todo_id: int) -> Optional[Todo]:
        todo = self.get(todo_id)
        if todo is None:
            return None
        todo.done = True
        self._save()
        return todo

    def remove(self, todo_id: int) -> Optional[Todo]:
        todo = self.get(todo_id)
        if todo is None:
            return None
        self.todos.remove(todo)
        self._save()
        return todo

    def clear(self) -> None:
        self.todos = []
        self._save()

    def pending_count(self) -> int:
        return sum(1 for t in self.todos if not t.done)
