"""Step definitions for todo.feature.

Each step maps a plain-English Gherkin line to Python that drives
the todo module directly (no subprocess needed).
"""
import io
import sys
from behave import given, when, then
import todo


def _run(fn, *args):
    """Run a todo function, capture printed output, and store it on context."""
    buf = io.StringIO()
    old_stdout = sys.stdout
    sys.stdout = buf
    try:
        fn(*args)
    finally:
        sys.stdout = old_stdout
    return buf.getvalue()


# ---------------------------------------------------------------------------
# Given steps
# ---------------------------------------------------------------------------

@given("I have an empty todo list")
def step_empty_list(context):
    """Ensure no tasks exist (environment.py already handles this)."""
    assert todo.load_todos() == []


@given('I have a task "{task}"')
def step_given_task(context, task):
    """Pre-populate the list with a task."""
    todo.add(task)


# ---------------------------------------------------------------------------
# When steps
# ---------------------------------------------------------------------------

@when('I add a task "{task}"')
def step_add_task(context, task):
    context.output.append(_run(todo.add, task))


@when("I list my todos")
def step_list_todos(context):
    context.output.append(_run(todo.list_todos))


@when("I complete task number {index:d}")
def step_complete_task(context, index):
    context.output.append(_run(todo.complete, index))


@when("I delete task number {index:d}")
def step_delete_task(context, index):
    context.output.append(_run(todo.delete, index))


# ---------------------------------------------------------------------------
# Then steps
# ---------------------------------------------------------------------------

@then('the task "{task}" should be in my list')
def step_task_in_list(context, task):
    tasks = [t["task"] for t in todo.load_todos()]
    assert task in tasks, f"'{task}' not found in {tasks}"


@then('the task "{task}" should be pending')
def step_task_pending(context, task):
    match = next(t for t in todo.load_todos() if t["task"] == task)
    assert match["done"] is False, f"Expected '{task}' to be pending"


@then('the task "{task}" should be done')
def step_task_done(context, task):
    match = next(t for t in todo.load_todos() if t["task"] == task)
    assert match["done"] is True, f"Expected '{task}' to be done"


@then("my todo list should have {count:d} tasks")
def step_list_count(context, count):
    actual = len(todo.load_todos())
    assert actual == count, f"Expected {count} tasks, got {actual}"


@then('the output should contain "{text}"')
def step_output_contains(context, text):
    combined = "".join(context.output)
    assert text in combined, f"Expected '{text}' in output:\n{combined}"
