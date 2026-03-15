"""Unit tests for todo.py — each function is tested in isolation.

File I/O is redirected to a temporary path via monkeypatch so tests
never touch the real todos.json.
"""
import json
import pytest
import todo


@pytest.fixture(autouse=True)
def isolated_data_file(tmp_path, monkeypatch):
    """Redirect DATA_FILE to a temp path for every test."""
    monkeypatch.setattr(todo, "DATA_FILE", str(tmp_path / "todos.json"))


# ---------------------------------------------------------------------------
# load_todos
# ---------------------------------------------------------------------------

class TestLoadTodos:
    def test_returns_empty_list_when_file_missing(self):
        """No file on disk → empty list, no error."""
        assert todo.load_todos() == []

    def test_returns_todos_from_file(self, tmp_path, monkeypatch):
        """Existing JSON file is parsed and returned."""
        data = [{"task": "Buy milk", "done": False}]
        data_file = tmp_path / "todos.json"
        data_file.write_text(json.dumps(data))
        monkeypatch.setattr(todo, "DATA_FILE", str(data_file))

        assert todo.load_todos() == data


# ---------------------------------------------------------------------------
# save_todos
# ---------------------------------------------------------------------------

class TestSaveTodos:
    def test_writes_json_to_disk(self, tmp_path, monkeypatch):
        """Saved data can be read back as valid JSON."""
        data_file = tmp_path / "todos.json"
        monkeypatch.setattr(todo, "DATA_FILE", str(data_file))
        todos = [{"task": "Walk dog", "done": True}]

        todo.save_todos(todos)

        assert json.loads(data_file.read_text()) == todos

    def test_overwrites_existing_file(self, tmp_path, monkeypatch):
        """Calling save_todos twice keeps only the latest data."""
        data_file = tmp_path / "todos.json"
        monkeypatch.setattr(todo, "DATA_FILE", str(data_file))

        todo.save_todos([{"task": "Old task", "done": False}])
        todo.save_todos([{"task": "New task", "done": True}])

        result = json.loads(data_file.read_text())
        assert len(result) == 1
        assert result[0]["task"] == "New task"


# ---------------------------------------------------------------------------
# add
# ---------------------------------------------------------------------------

class TestAdd:
    def test_adds_task_with_done_false(self, capsys):
        """New task is appended with done=False."""
        todo.add("Write tests")

        todos = todo.load_todos()
        assert len(todos) == 1
        assert todos[0] == {"task": "Write tests", "done": False}

    def test_prints_confirmation(self, capsys):
        """A confirmation message is printed after adding."""
        todo.add("Read a book")
        assert "Added: Read a book" in capsys.readouterr().out

    def test_adds_multiple_tasks(self):
        """Multiple add calls accumulate tasks."""
        todo.add("Task A")
        todo.add("Task B")

        todos = todo.load_todos()
        assert len(todos) == 2
        assert todos[1]["task"] == "Task B"


# ---------------------------------------------------------------------------
# list_todos
# ---------------------------------------------------------------------------

class TestListTodos:
    def test_prints_empty_message_when_no_todos(self, capsys):
        """Empty list produces a helpful prompt."""
        todo.list_todos()
        assert "No todos yet" in capsys.readouterr().out

    def test_prints_pending_task(self, capsys):
        """A pending task is shown with [ ] marker."""
        todo.add("Clean house")
        todo.list_todos()
        out = capsys.readouterr().out
        assert "[ ]" in out
        assert "Clean house" in out

    def test_prints_completed_task(self, capsys):
        """A completed task is shown with [x] marker."""
        todo.add("Exercise")
        todo.complete(1)
        todo.list_todos()
        out = capsys.readouterr().out
        assert "[x]" in out
        assert "Exercise" in out

    def test_shows_1_based_index(self, capsys):
        """Index in output starts at 1."""
        todo.add("First task")
        todo.list_todos()
        assert "1." in capsys.readouterr().out


# ---------------------------------------------------------------------------
# complete
# ---------------------------------------------------------------------------

class TestComplete:
    def test_marks_task_done(self):
        """Task at given index has done set to True after complete()."""
        todo.add("Study Python")
        todo.complete(1)
        assert todo.load_todos()[0]["done"] is True

    def test_prints_confirmation(self, capsys):
        """Completion confirmation message includes the task name."""
        todo.add("Meditate")
        todo.complete(1)
        assert "Completed: Meditate" in capsys.readouterr().out

    def test_index_zero_is_invalid(self, capsys):
        """Index 0 is out of range."""
        todo.add("Some task")
        todo.complete(0)
        assert "Invalid index" in capsys.readouterr().out

    def test_index_exceeding_length_is_invalid(self, capsys):
        """Index greater than list length is rejected."""
        todo.add("Only task")
        todo.complete(99)
        assert "Invalid index" in capsys.readouterr().out

    def test_does_not_alter_other_tasks(self):
        """Completing one task leaves others unchanged."""
        todo.add("Task 1")
        todo.add("Task 2")
        todo.complete(1)
        todos = todo.load_todos()
        assert todos[1]["done"] is False


# ---------------------------------------------------------------------------
# delete
# ---------------------------------------------------------------------------

class TestDelete:
    def test_removes_task_from_list(self):
        """Deleted task is no longer present."""
        todo.add("Buy coffee")
        todo.delete(1)
        assert todo.load_todos() == []

    def test_prints_confirmation(self, capsys):
        """Deletion confirmation message includes the task name."""
        todo.add("Go for a run")
        todo.delete(1)
        assert "Deleted: Go for a run" in capsys.readouterr().out

    def test_index_zero_is_invalid(self, capsys):
        """Index 0 is out of range."""
        todo.add("Some task")
        todo.delete(0)
        assert "Invalid index" in capsys.readouterr().out

    def test_index_exceeding_length_is_invalid(self, capsys):
        """Index greater than list length is rejected."""
        todo.add("Only task")
        todo.delete(99)
        assert "Invalid index" in capsys.readouterr().out

    def test_remaining_tasks_are_preserved(self):
        """Other tasks remain intact after a deletion."""
        todo.add("Keep me")
        todo.add("Delete me")
        todo.delete(2)
        todos = todo.load_todos()
        assert len(todos) == 1
        assert todos[0]["task"] == "Keep me"


# ---------------------------------------------------------------------------
# usage
# ---------------------------------------------------------------------------

class TestUsage:
    def test_prints_all_commands(self, capsys):
        """usage() output mentions all four CLI commands."""
        todo.usage()
        out = capsys.readouterr().out
        assert "add" in out
        assert "list" in out
        assert "done" in out
        assert "delete" in out
