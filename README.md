# todo-cli

A simple command-line todo app in Python — built for hands-on practice.

## Usage

```bash
# Add a task
python todo.py add Buy groceries

# List all tasks
python todo.py list

# Mark task #1 as done
python todo.py done 1

# Delete task #2
python todo.py delete 2
```

## How it works

- Todos are stored locally in `todos.json`
- No external dependencies — pure Python stdlib

## Ideas to extend this project

- [ ] Add due dates
- [ ] Filter by status (pending / done)
- [ ] Add priority levels
- [ ] Colorize output with `colorama`
- [ ] Write unit tests with `pytest`
