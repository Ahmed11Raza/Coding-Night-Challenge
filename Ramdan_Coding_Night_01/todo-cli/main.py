import click
import json
import uuid
from datetime import datetime
from pathlib import Path

# Configuration
DATA_DIR = Path.home() / ".todo_cli"
DATA_DIR.mkdir(exist_ok=True)
TODO_FILE = DATA_DIR / "tasks.json"

def load_tasks():
    """Load tasks from JSON file"""
    try:
        if TODO_FILE.exists():
            with open(TODO_FILE, "r") as f:
                return json.load(f)
        return []
    except json.JSONDecodeError:
        click.echo("Error loading tasks file!")
        return []

def save_tasks(tasks):
    """Save tasks to JSON file"""
    with open(TODO_FILE, "w") as f:
        json.dump(tasks, f, indent=2)

@click.group()
def cli():
    """Simple Todo List Manager"""
    pass

@cli.command()
@click.option("--title", prompt=True, help="Task title")
@click.option("--description", prompt=True, help="Task description")
@click.option("--due-date", prompt=True, help="Due date (YYYY-MM-DD)")
def add(title, description, due_date):
    """Add a new task"""
    tasks = load_tasks()
    task_id = str(uuid.uuid4())
    new_task = {
        "id": task_id,
        "title": title,
        "description": description,
        "due_date": due_date,
        "completed": False,
        "created_at": datetime.now().isoformat()
    }
    tasks.append(new_task)
    save_tasks(tasks)
    click.echo(f"Task added! ID: {task_id}")

@cli.command()
def list():
    """List all tasks"""
    tasks = load_tasks()
    if not tasks:
        click.echo("No tasks found!")
        return
    for task in tasks:
        status = "✓" if task["completed"] else "✗"
        click.echo(f""" 
ID: {task['id']}
Title: {task['title']}
Description: {task['description']}
Due: {task['due_date']}
Status: {status}
{"-"*40}""")

@cli.command()
@click.argument("task_id")
def complete(task_id):
    """Mark a task as complete"""
    tasks = load_tasks()
    found = False
    for task in tasks:
        if task["id"] == task_id:
            task["completed"] = True
            found = True
            break
    
    if found:
        save_tasks(tasks)
        click.echo(f"Task {task_id} marked complete!")
    else:
        click.echo(f"Task {task_id} not found!")

@cli.command()
@click.argument("task_id")
def delete(task_id):
    """Delete a task"""
    tasks = load_tasks()
    original_count = len(tasks)
    tasks = [t for t in tasks if t["id"] != task_id]
    if len(tasks) < original_count:
        save_tasks(tasks)
        click.echo(f"Task {task_id} deleted!")
    else:
        click.echo(f"Task {task_id} not found!")

if __name__ == "__main__":
    cli()