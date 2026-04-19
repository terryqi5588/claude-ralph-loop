# Agent Behavior Protocol

This document defines the highest-level rules for how the Agent (Claude) operates in this repository.

## Workflow: Ralph Loop

The Agent must follow the **Ralph Loop** methodology for all development tasks:

**Plan → Act → Observe → Reflect → Complete**

---

## 1. Plan Phase

**REQUIRED ACTIONS:**

1. **Check current tasks:**
   ```bash
   python3 scripts/plan.py list
   ```

2. **If no active tasks exist:**
   ```bash
   python3 scripts/plan.py add "<task description>"
   ```

3. **Before starting work:**
   ```bash
   python3 scripts/plan.py start <task_id>
   ```

**Rules:**
- NEVER start coding without an active task
- Each task must have a clear, specific description
- Only work on ONE task at a time (status: `in_progress`)

---

## 2. Act Phase

**Modify code following these principles:**

### React/TypeScript Best Practices:
- Use functional components with hooks
- Implement proper TypeScript types (no `any`)
- Follow React conventions for state management
- Use semantic HTML and proper accessibility attributes
- Keep components small and focused
- Extract reusable logic into custom hooks

### Code Quality:
- Write clean, readable code
- Follow existing project patterns
- No console.logs in production code
- Handle errors appropriately
- Write meaningful variable and function names

---

## 3. Observe Phase

**MANDATORY: Execute BOTH verification steps**

### Step 1: Logic Verification
```bash
bash scripts/verify.sh
```

This runs:
- ESLint (code quality)
- TypeScript type checking
- Unit tests

### Step 2: Visual Verification
```bash
npx ts-node scripts/capture_ui.ts
```

This generates:
- `logs/screenshot.png` - Visual snapshot of the UI
- `logs/ui_structure.txt` - Accessibility tree (text representation of DOM)

**Rules:**
- BOTH steps must be executed after every code change
- Do NOT skip verification steps
- Do NOT proceed to Reflect if verification fails to run

---

## 4. Reflect Phase

**Read and analyze verification outputs:**

1. **Read verification results:**
   - Check console output from `verify.sh`
   - Read `logs/ui_structure.txt` to understand UI layout
   - Review screenshot if needed

2. **If issues are found:**
   ```bash
   python3 scripts/plan.py reflect <task_id> "<description of what went wrong and why>"
   ```

3. **Return to Act Phase** and fix the issues

**Rules:**
- ALWAYS record reflections when issues are found
- Be specific about what went wrong
- Reflections help track the development journey
- If verification passes, proceed to Complete phase

---

## 5. Complete Phase

**ONLY proceed when:**
- ✅ `bash scripts/verify.sh` passes (all green)
- ✅ `npx ts-node scripts/capture_ui.ts` succeeds
- ✅ UI structure in `logs/ui_structure.txt` looks correct
- ✅ No errors or warnings in verification output

**Required actions:**

1. **Mark task as done:**
   ```bash
   python3 scripts/plan.py done <task_id>
   ```

2. **Commit changes (if appropriate):**
   ```bash
   git add .
   git commit -m "feat: <descriptive commit message>"
   ```

**Rules:**
- NEVER commit failing code
- NEVER mark a task as done if verification fails
- Commit messages should be clear and descriptive
- Use conventional commit format (feat:, fix:, refactor:, etc.)

---

## Key Principles

### 1. **Discipline**
Follow the loop strictly. No shortcuts.

### 2. **Visibility**
Every action is tracked through `plan.py` for transparency.

### 3. **Quality**
Code must pass ALL verification before completion.

### 4. **Learning**
Reflections document what was learned and why changes were made.

### 5. **Honesty**
If something fails, record it. Don't hide problems.

---

## Command Reference

```bash
# Task Management
python3 scripts/plan.py list                          # Show all tasks
python3 scripts/plan.py add "<description>"          # Create new task
python3 scripts/plan.py start <id>                   # Start a task
python3 scripts/plan.py reflect <id> "<note>"        # Add reflection
python3 scripts/plan.py done <id>                    # Complete task

# Verification
bash scripts/verify.sh                               # Run logic verification
npx ts-node scripts/capture_ui.ts                   # Capture UI state

# Development
npm run dev                                          # Start dev server
npm run build                                        # Build for production
```

---

## Example Workflow

```bash
# 1. PLAN
python3 scripts/plan.py add "Implement login form"
python3 scripts/plan.py start 5

# 2. ACT
# ... modify code ...

# 3. OBSERVE
bash scripts/verify.sh
npx ts-node scripts/capture_ui.ts

# 4. REFLECT (if issues found)
python3 scripts/plan.py reflect 5 "Form validation failed - missing email regex check"
# ... go back to ACT and fix ...

# 5. COMPLETE (when all green)
python3 scripts/plan.py done 5
git add .
git commit -m "feat: implement login form with validation"
```

---

**This protocol is NON-NEGOTIABLE. Follow it for every task, every time.**
