#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Task management script for Agent workflow.
Supports: add, start, reflect, done, list operations on tasks.json
"""

import json
import sys
import io
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Any

# Fix Windows console encoding
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

TASKS_FILE = Path(__file__).parent.parent / ".claude" / "tasks.json"
PROGRESS_FILE = Path(__file__).parent.parent / ".claude" / "PROGRESS.md"


def load_tasks() -> List[Dict[str, Any]]:
    """Load tasks from tasks.json"""
    if not TASKS_FILE.exists():
        return []
    with open(TASKS_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)


def save_tasks(tasks: List[Dict[str, Any]]) -> None:
    """Save tasks to tasks.json"""
    TASKS_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(TASKS_FILE, 'w', encoding='utf-8') as f:
        json.dump(tasks, f, indent=2, ensure_ascii=False)


def add_task(description: str) -> None:
    """Add a new task with status 'todo'"""
    tasks = load_tasks()
    task_id = max([t.get('id', 0) for t in tasks], default=0) + 1

    new_task = {
        "id": task_id,
        "description": description,
        "status": "todo",
        "created_at": datetime.now().isoformat(),
        "reflections": []
    }

    tasks.append(new_task)
    save_tasks(tasks)
    print(f"✓ Task {task_id} added: {description}")


def start_task(task_id: int) -> None:
    """Change task status to 'in_progress'"""
    tasks = load_tasks()
    task = next((t for t in tasks if t['id'] == task_id), None)

    if not task:
        print(f"✗ Task {task_id} not found")
        sys.exit(1)

    task['status'] = 'in_progress'
    task['started_at'] = datetime.now().isoformat()
    save_tasks(tasks)
    print(f"✓ Task {task_id} started: {task['description']}")


def reflect_task(task_id: int, note: str) -> None:
    """Add a reflection note to a task"""
    tasks = load_tasks()
    task = next((t for t in tasks if t['id'] == task_id), None)

    if not task:
        print(f"✗ Task {task_id} not found")
        sys.exit(1)

    reflection = {
        "timestamp": datetime.now().isoformat(),
        "note": note
    }

    task['reflections'].append(reflection)
    save_tasks(tasks)
    print(f"✓ Reflection added to task {task_id}")


def archive_task(task: Dict[str, Any]) -> None:
    """Archive completed task to PROGRESS.md"""
    # Prepare archive entry
    completed_date = task.get('completed_at', datetime.now().isoformat()).split('T')[0]
    task_id = task['id']
    description = task['description']
    reflections = task.get('reflections', [])

    # Build archive entry
    entry = f"\n## Task #{task_id}: {description}\n"
    entry += f"**Completed:** {completed_date}\n\n"

    if reflections:
        entry += "**Key Insights:**\n"
        for ref in reflections:
            note = ref['note']
            entry += f"- {note}\n"
    else:
        entry += "*No reflections recorded*\n"

    entry += "\n---\n"

    # Append to PROGRESS.md
    PROGRESS_FILE.parent.mkdir(parents=True, exist_ok=True)

    # Create file with header if it doesn't exist
    if not PROGRESS_FILE.exists():
        with open(PROGRESS_FILE, 'w', encoding='utf-8') as f:
            f.write("# Progress History\n\n")
            f.write("This file tracks completed tasks and their key insights.\n")
            f.write("Tasks are automatically archived here when marked as done.\n")
            f.write("\n---\n")

    # Append the task
    with open(PROGRESS_FILE, 'a', encoding='utf-8') as f:
        f.write(entry)


def done_task(task_id: int) -> None:
    """Mark task as completed (but keep in tasks.json until committed)"""
    tasks = load_tasks()
    task = next((t for t in tasks if t['id'] == task_id), None)

    if not task:
        print(f"✗ Task {task_id} not found")
        sys.exit(1)

    # Mark as completed
    task['status'] = 'completed'
    task['completed_at'] = datetime.now().isoformat()
    save_tasks(tasks)

    print(f"✓ Task {task_id} completed: {task['description']}")
    print(f"")
    print(f"Next steps:")
    print(f"  1. Commit your changes: git add . && git commit -m '...'")
    print(f"  2. Archive completed tasks: python scripts/plan.py archive")
    print(f"")
    print(f"Note: Completed tasks remain in tasks.json until archived.")


def list_tasks() -> None:
    """Display all tasks in table format"""
    tasks = load_tasks()

    if not tasks:
        print("No tasks found.")
        print("\nTip: Add a new task with 'python plan.py add <description>'")
        return

    # Print header
    print("\n" + "="*100)
    print(f"{'ID':<5} {'Status':<15} {'Description':<40} {'Reflections':<20}")
    print("="*100)

    # Print tasks
    for task in tasks:
        task_id = task['id']
        status = task['status']
        desc = task['description'][:37] + "..." if len(task['description']) > 40 else task['description']
        ref_count = len(task.get('reflections', []))

        print(f"{task_id:<5} {status:<15} {desc:<40} {ref_count} reflection(s)")

        # Print reflections if any
        for i, ref in enumerate(task.get('reflections', []), 1):
            timestamp = ref['timestamp'].split('T')[0]  # Just the date
            note = ref['note'][:60] + "..." if len(ref['note']) > 60 else ref['note']
            print(f"      └─ [{timestamp}] {note}")

    print("="*100 + "\n")


def archive_all_completed(force: bool = False) -> None:
    """Archive all completed tasks that have been committed"""
    tasks = load_tasks()
    completed_tasks = [t for t in tasks if t.get('status') == 'completed']

    if not completed_tasks:
        print("No completed tasks to archive.")
        return

    # Check if there are uncommitted changes
    import subprocess
    try:
        result = subprocess.run(
            ['git', 'status', '--porcelain'],
            capture_output=True,
            text=True,
            timeout=5
        )
        has_changes = bool(result.stdout.strip())
    except Exception:
        # If git check fails, warn but allow archiving
        print("⚠ Warning: Unable to check git status. Proceeding anyway...")
        has_changes = False

    if has_changes and not force:
        print("⚠ Warning: You have uncommitted changes.")
        print("It's recommended to commit your changes before archiving.")
        print("")
        try:
            response = input("Continue with archiving? (y/N): ")
            if response.lower() not in ['y', 'yes']:
                print("Archiving cancelled.")
                return
        except EOFError:
            print("\nArchiving cancelled (non-interactive mode).")
            print("Use 'python scripts/plan.py archive --force' to skip confirmation.")
            return

    print(f"Found {len(completed_tasks)} completed task(s) to archive...")

    for task in completed_tasks:
        archive_task(task)
        print(f"  ✓ Archived task #{task['id']}: {task['description']}")

    # Keep only non-completed tasks
    active_tasks = [t for t in tasks if t.get('status') != 'completed']
    save_tasks(active_tasks)

    print(f"\n✓ {len(completed_tasks)} task(s) archived to PROGRESS.md")
    print(f"✓ tasks.json now contains only {len(active_tasks)} active task(s)")


def main():
    if len(sys.argv) < 2:
        print("Usage: python plan.py <command> [args]")
        print("Commands:")
        print("  add <description>     - Add new task")
        print("  start <id>           - Start task")
        print("  reflect <id> <note>  - Add reflection")
        print("  done <id>            - Complete task (stays in tasks.json)")
        print("  list                 - Show all tasks")
        print("  archive              - Archive all completed tasks (after commit)")
        sys.exit(1)

    command = sys.argv[1]

    try:
        if command == "add":
            if len(sys.argv) < 3:
                print("✗ Usage: python plan.py add <description>")
                sys.exit(1)
            description = " ".join(sys.argv[2:])
            add_task(description)

        elif command == "start":
            if len(sys.argv) < 3:
                print("✗ Usage: python plan.py start <id>")
                sys.exit(1)
            task_id = int(sys.argv[2])
            start_task(task_id)

        elif command == "reflect":
            if len(sys.argv) < 4:
                print("✗ Usage: python plan.py reflect <id> <note>")
                sys.exit(1)
            task_id = int(sys.argv[2])
            note = " ".join(sys.argv[3:])
            reflect_task(task_id, note)

        elif command == "done":
            if len(sys.argv) < 3:
                print("✗ Usage: python plan.py done <id>")
                sys.exit(1)
            task_id = int(sys.argv[2])
            done_task(task_id)

        elif command == "list":
            list_tasks()

        elif command == "archive":
            force = '--force' in sys.argv or '-f' in sys.argv
            archive_all_completed(force)

        else:
            print(f"✗ Unknown command: {command}")
            sys.exit(1)

    except ValueError as e:
        print(f"✗ Error: Invalid task ID - must be a number")
        sys.exit(1)
    except Exception as e:
        print(f"✗ Error: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
