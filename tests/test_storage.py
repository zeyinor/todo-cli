import pytest

from todo_cli.storage import Storage


@pytest.fixture
def storage(tmp_path):
    return Storage(tmp_path / "todos.json")


def test_add_and_list(storage):
    storage.add("buy milk")
    storage.add("write report")
    todos = storage.list()
    assert len(todos) == 2
    assert todos[0].text == "buy milk"
    assert todos[0].id == 1
    assert todos[1].id == 2
    assert todos[0].done is False


def test_done(storage):
    todo = storage.add("buy milk")
    result = storage.done(todo.id)
    assert result is not None
    assert storage.get(todo.id).done is True


def test_done_missing_returns_none(storage):
    assert storage.done(99) is None


def test_remove(storage):
    todo = storage.add("buy milk")
    removed = storage.remove(todo.id)
    assert removed is not None
    assert storage.get(todo.id) is None
    assert storage.list() == []


def test_remove_missing_returns_none(storage):
    assert storage.remove(99) is None


def test_clear(storage):
    storage.add("a")
    storage.add("b")
    storage.clear()
    assert storage.list() == []


def test_persistence(tmp_path):
    path = tmp_path / "todos.json"
    s1 = Storage(path)
    s1.add("buy milk")
    s2 = Storage(path)
    assert len(s2.list()) == 1
    assert s2.list()[0].text == "buy milk"


def test_id_not_reused_after_remove(storage):
    a = storage.add("a")
    storage.add("b")
    storage.remove(a.id)
    c = storage.add("c")
    assert c.id == 3


def test_corrupted_file_recovers(tmp_path):
    path = tmp_path / "todos.json"
    path.write_text("not valid json", encoding="utf-8")
    storage = Storage(path)
    assert storage.list() == []
