"""Behave environment hooks.

Before each scenario, redirect todo.DATA_FILE to a fresh temp file so
scenarios are fully isolated from each other and from the real todos.json.
"""
import os
import tempfile
import todo


def before_scenario(context, scenario):
    """Set up a temporary data file and a capture buffer for each scenario."""
    context._tmp = tempfile.NamedTemporaryFile(suffix=".json", delete=False)
    context._tmp.close()
    os.unlink(context._tmp.name)   # remove so load_todos() starts empty
    todo.DATA_FILE = context._tmp.name
    context.output = []


def after_scenario(context, scenario):
    """Clean up the temporary data file."""
    if os.path.exists(context._tmp.name):
        os.unlink(context._tmp.name)
