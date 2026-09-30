import pytest

from todo_cli.cli import main


@pytest.fixture
def data_file(tmp_path):
    return tmp_path / "todos.json"


def run(args, data_file, capsys):
    main(["--file", str(data_file), *args])
    return capsys.readouterr()


def test_add_and_list(data_file, capsys):
    run(["add", "buy", "milk"], data_file, capsys)
    out = run(["list"], data_file, capsys).out
    assert "buy milk" in out
    assert "[ ] 1." in out
    assert "1 pending, 0 done." in out


def test_done_marks_x(data_file, capsys):
    run(["add", "buy milk"], data_file, capsys)
    run(["done", "1"], data_file, capsys)
    out = run(["list"], data_file, capsys).out
    assert "[x] 1. buy milk" in out
    assert "0 pending, 1 done." in out


def test_remove(data_file, capsys):
    run(["add", "buy milk"], data_file, capsys)
    run(["remove", "1"], data_file, capsys)
    out = run(["list"], data_file, capsys).out
    assert "No todos yet" in out


def test_clear(data_file, capsys):
    run(["add", "a"], data_file, capsys)
    run(["add", "b"], data_file, capsys)
    run(["clear"], data_file, capsys)
    out = run(["list"], data_file, capsys).out
    assert "No todos yet" in out


def test_done_missing_exits(data_file, capsys):
    with pytest.raises(SystemExit):
        run(["done", "99"], data_file, capsys)


def test_remove_missing_exits(data_file, capsys):
    with pytest.raises(SystemExit):
        run(["remove", "99"], data_file, capsys)
