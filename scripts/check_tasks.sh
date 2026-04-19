#!/bin/bash
# Task Status Checker for CI
# Checks if there are any incomplete tasks in tasks.json

TASKS_FILE=".claude/tasks.json"

if [ ! -f "$TASKS_FILE" ]; then
  echo "✓ No tasks.json found - skipping task check"
  exit 0
fi

# Count tasks by status
IN_PROGRESS=$(grep -c '"status": "in_progress"' "$TASKS_FILE" 2>/dev/null || echo "0")
TODO=$(grep -c '"status": "todo"' "$TASKS_FILE" 2>/dev/null || echo "0")

echo "Task Status Check:"
echo "  In Progress: $IN_PROGRESS"
echo "  Todo: $TODO"
echo ""

# Fail if there are in_progress tasks
if [ "$IN_PROGRESS" -gt 0 ]; then
  echo "✗ Found $IN_PROGRESS task(s) still in progress"
  echo "All tasks must be completed before pushing to main/master"
  echo ""
  python scripts/plan.py list 2>/dev/null || echo "Unable to display task list"
  exit 1
fi

# Warn if there are todo tasks (but don't fail)
if [ "$TODO" -gt 0 ]; then
  echo "⚠ Warning: Found $TODO todo task(s)"
  echo "Consider completing or removing todo tasks before merging"
  echo ""
fi

echo "✓ No incomplete tasks found"
exit 0
