# Claude Ralph Loop

An intelligent task management and code verification system powered by the **Ralph Loop** methodology for AI Agent workflows.

[![CI](https://github.com/terryqi5588/claude-ralph-loop/workflows/Verify%20Code%20Quality/badge.svg)](https://github.com/terryqi5588/claude-ralph-loop/actions)

## 🎯 What is Ralph Loop?

Ralph Loop is a disciplined, iterative workflow designed for AI agents (like Claude) to build high-quality software systematically:

```
┌─────────────────────────────────────────────────────────────────────┐
│                         Ralph Loop Workflow                         │
└─────────────────────────────────────────────────────────────────────┘

    ┌──────────────┐
    │   1. PLAN    │◄─────────────────┐  Decompose
    │              │  • Check: python plan.py list         │  Strategy
    │              │  • Add task if needed                 │  Switch
    │              │  • Start: python plan.py start <id>   │
    └──────┬───────┘  • Track: attempts counter (max 3)   │
           │                                               │
           ↓                                               │
    ┌──────────────┐                                      │
    │   2. ACT     │◄─────────────┐  Minor fixes         │
    │              │  • Write/modify code         │       │
    │              │  • Follow best practices     │       │
    │              │  • Keep changes focused      │       │
    └──────┬───────┘                              │       │
           │                                      │       │
           ↓                                      │       │
    ┌──────────────┐                             │       │
    │  3. OBSERVE  │  • Run: bash scripts/verify.sh       │
    │              │    - ESLint (exit code 1)            │
    │              │    - TypeScript (exit code 2)        │
    │              │    - Tests (exit code 3)             │
    │              │  • Run: npm run capture-ui           │
    └──────┬───────┘  • Get detailed error feedback      │
           │                                              │
           ↓                                              │
        ┌──────┐                                         │
        │ Pass?│────── YES ────┐                         │
        └──┬───┘               │                         │
           │                   ↓                         │
          NO            ┌──────────────┐                 │
           │            │ 5. COMPLETE  │  • Mark: python plan.py done <id>
           ↓            │              │  • Commit: git commit -m "..."
    ┌──────────────┐    │              │  • Archive: python plan.py archive
    │  4. REFLECT  │    └──────────────┘
    │              │  • Record: python plan.py reflect <id> "<note>"
    │              │  • Analyze: What went wrong?
    │              │  • Check: attempts count
    └──────┬───────┘  • If attempts >= 2: MUST switch strategy
           │
           │
    ┌──────▼──────────────────┐
    │   Attempts Check        │
    │                         │
    │  ┌─── < 3 attempts? ───┐│
    │  │                      ││
    │  │  YES          NO     ││
    │  ↓               ↓      ││
    │ Simple       Strategy   ││
    │  Fix?        Switch     ││
    │  │             │        ││
    │  YES           NO       ││
    │  │             │        ││
    └──┼─────────────┼────────┘│
       │             │         │
       │             ↓         │ (3 attempts reached)
       │      ┌──────────────┐ │
       │      │ Choose One:  │ │     ┌─────────────┐
       │      │              │ │     │  🔴 BLOCK   │
       │      │ 1. Decompose ├─┼─────│             │
       │      │    → PLAN    │ │     │ Task blocked│
       │      │              │ │     │ Manual fix  │
       │      │ 2. Ask Help  │ │     │  required   │
       │      │    [BLOCKER] │ │     └─────────────┘
       │      │              │ │
       │      │ 3. Reset     │ │
       │      │    Context   │ │
       │      └──────────────┘ │
       │                        │
       └────────────────────────┘

Key Safeguards:
━━━━━━━━━━━━━━
⚠️  Attempts counter: Every 'start' increments (visible in 'list')
⚠️  2-failure rule: After 2 failures, MUST change strategy
⚠️  3-attempt limit: Task auto-blocked, requires manual intervention
⚠️  Closed loop: Failed tasks cycle back to ACT or PLAN
⚠️  High-signal feedback: Detailed errors prevent blind retries
```

### The Five Phases:

1. **Plan** - Define clear tasks with `plan.py`
2. **Act** - Write code following best practices
3. **Observe** - Run automated verification (lint, type-check, tests, UI capture)
4. **Reflect** - Analyze results, document learnings, iterate if needed
5. **Complete** - Commit only when all verifications pass

## ✨ Features

### 📋 Task Management (`scripts/plan.py`)
- Add, start, reflect, and complete tasks
- **Circuit breaker**: Automatic retry limit (max 3 attempts)
- **Infinite loop prevention**: Tasks blocked after 3 failed attempts
- Automatic archiving to `PROGRESS.md` after git commit
- Clean, signal-focused `tasks.json` (only active tasks)
- Rich reflection system for capturing insights

### ✅ Code Verification (`scripts/verify.sh`)
- **Enhanced error reporting** with detailed diagnostics
- **Stage-specific feedback**: Clear identification of which step failed
- **Auto-display key errors**: First 10 lines of critical issues
- **Contextual help**: Fix suggestions for each failure type
- **Smart exit codes**: Different codes for ESLint (1), TypeCheck (2), Tests (3)
- Runs: ESLint → TypeScript → Tests in sequence
- High-signal feedback reduces invalid retry attempts

### 👁️ Visual Feedback (`scripts/capture_ui.ts`)
- Screenshot capture of running UI
- **Accessibility tree extraction** - text-based UI representation
- Enables AI to "see" and verify UI structure without visual processing

### 🤖 Agent Protocol ([`.claude/CLAUDE.md`](.claude/CLAUDE.md))
- Defines strict behavior rules for AI agents
- Enforces quality gates before commits
- Documents the complete workflow

### 🔄 CI/CD ([`.github/workflows/verify.yml`](.github/workflows/verify.yml))
- Automated verification on push/PR
- Blocks commits with incomplete tasks
- Ensures code quality across the team

## 🚀 Quick Start

### Prerequisites

```bash
# Node.js 20+ and Python 3
node --version  # v20.x.x
python --version  # 3.x.x
```

### Installation

```bash
# Clone the repository
git clone https://github.com/terryqi5588/claude-ralph-loop.git
cd claude-ralph-loop

# Install dependencies
npm install

# Install Playwright browsers
npx playwright install chromium
```

### Basic Usage

#### Task Management

```bash
# List all tasks
python scripts/plan.py list

# Add a new task
python scripts/plan.py add "Implement user authentication"

# Start working on a task
python scripts/plan.py start 1

# Add reflections as you work
python scripts/plan.py reflect 1 "Discovered edge case with OAuth flow"

# Complete the task (marks as done, stays in tasks.json)
python scripts/plan.py done 1

# After git commit, archive completed tasks
python scripts/plan.py archive
```

#### Code Verification

```bash
# Run full verification pipeline
bash scripts/verify.sh

# Or via npm
npm run verify
```

#### UI Capture

```bash
# Start dev server
npm run dev

# In another terminal, capture UI
npm run capture-ui

# View results
cat logs/ui_structure.txt  # Text-based UI structure
# logs/screenshot.png       # Visual screenshot
```

## 📁 Project Structure

```
.
├── .claude/
│   ├── CLAUDE.md         # Agent behavior protocol
│   ├── PROGRESS.md       # Archived task history
│   └── tasks.json        # Active tasks only
├── .github/
│   └── workflows/
│       └── verify.yml    # CI/CD pipeline
├── scripts/
│   ├── plan.py          # Task manager
│   ├── verify.sh        # Verification pipeline
│   ├── capture_ui.ts    # UI capture tool
│   └── check_tasks.sh   # Task status checker
├── logs/
│   ├── screenshot.png   # UI screenshot
│   └── ui_structure.txt # Accessibility tree
└── src/                 # React application
```

## 🔧 Command Reference

### Task Management

| Command | Description |
|---------|-------------|
| `python scripts/plan.py list` | Show all active tasks |
| `python scripts/plan.py add "<desc>"` | Create a new task |
| `python scripts/plan.py start <id>` | Start working on a task |
| `python scripts/plan.py reflect <id> "<note>"` | Add reflection/insight |
| `python scripts/plan.py done <id>` | Mark task as completed |
| `python scripts/plan.py archive` | Archive completed tasks (after commit) |

### Development

| Command | Description |
|---------|-------------|
| `npm run dev` | Start development server |
| `npm run build` | Build for production |
| `npm run verify` | Run verification pipeline |
| `npm run capture-ui` | Capture UI state |

### Verification Steps (in `verify.sh`)

1. **ESLint** - Code quality and style
2. **TypeScript** - Type safety (`tsc --noEmit`)
3. **Tests** - Unit/integration tests

**Enhanced Error Reporting:**

When verification fails, you get clear, actionable feedback:

```bash
==========================================
VERIFICATION FAILED: TypeScript Type Check
==========================================

Failed at: TypeScript Type Check
Command: npx tsc --noEmit

What this means:
  • TypeScript found type errors in your code
  • These must be fixed before proceeding

Key Errors (first 10 lines):
----------------------------------------
src/App.tsx(5,7): error TS2322: Type 'string' is not assignable to type 'number'
src/utils/helper.ts(12,15): error TS2345: Argument of type 'undefined'...
----------------------------------------

Common fixes:
  • Add missing type annotations
  • Fix type mismatches
  • Import missing types
  • Check for 'any' types that should be specific
```

Each failure stage provides:
- 🎯 **Clear identification** of which step failed
- 📋 **Key errors** extracted (first 10 lines for quick diagnosis)
- 💡 **Context and suggestions** for common fixes
- 🔢 **Unique exit codes** (1=ESLint, 2=TypeCheck, 3=Tests)

## 🎓 Ralph Loop in Practice

### Example Workflow

```bash
# 1. PLAN - Start with a clear task
python scripts/plan.py add "Add dark mode toggle"
python scripts/plan.py start 5

# 2. ACT - Write the code
# ... implement dark mode ...

# 3. OBSERVE - Run verification
bash scripts/verify.sh          # Check code quality
npm run capture-ui              # Capture UI

# 4. REFLECT - If issues found
python scripts/plan.py reflect 5 "Toggle state not persisting - need localStorage"
# ... fix issues, return to ACT ...

# 5. COMPLETE - When all green
python scripts/plan.py done 5
git add .
git commit -m "feat: add dark mode toggle"
python scripts/plan.py archive  # Archive to PROGRESS.md
```

### Key Principles

- ✅ **Discipline**: Follow the loop strictly, no shortcuts
- ✅ **Visibility**: Every action tracked through `plan.py`
- ✅ **Quality**: Code must pass all verification before completion
- ✅ **Learning**: Reflections document insights and decisions
- ✅ **Honesty**: Record failures, don't hide problems
- 🔴 **Circuit Breaker**: Automatic retry limits prevent infinite loops

### 🛡️ Infinite Loop Prevention

Ralph Loop includes built-in safeguards to prevent wasted attempts:

**Automatic Retry Tracking:**
- Each task tracks `attempts` (visible in `plan.py list`)
- Counter increments on every `start`
- **Hard limit: 3 attempts maximum**
- Task automatically blocked on 4th attempt

**Mandatory Strategy Switch:**

After 2 failed attempts, the agent MUST:

1. **Decompose** - Break complex task into 2-3 atomic sub-tasks
2. **Seek Help** - Create `[BLOCKER]` report with error details
3. **Reset Context** - Suggest `/clear` and restart from `PROGRESS.md`

**Prohibited Actions:**
- ❌ Repeating the same approach 3+ times
- ❌ Minor tweaks hoping for different results
- ❌ Ignoring the attempts counter

This ensures high-quality iterations and prevents the frustration of repeated failures.

## 🤝 Contributing

This project follows the Ralph Loop methodology. To contribute:

1. Fork the repository
2. Create a task: `python scripts/plan.py add "Your contribution"`
3. Follow the Ralph Loop workflow
4. Ensure all verification passes: `bash scripts/verify.sh`
5. Archive completed tasks before submitting PR
6. Submit PR with clear description

## 📝 CI Checks

Pull requests must pass:
- ✅ No incomplete tasks (`in_progress` status blocks CI)
- ✅ ESLint (no errors)
- ✅ TypeScript type check (no errors)
- ✅ All tests passing

## 📖 Learn More

- [Agent Protocol (CLAUDE.md)](.claude/CLAUDE.md) - Complete workflow rules
- [Progress History (PROGRESS.md)](.claude/PROGRESS.md) - Archived task insights

## 📄 License

MIT License - See [LICENSE](LICENSE) for details

## 🙏 Acknowledgments

Built with:
- [React](https://react.dev/) + [TypeScript](https://www.typescriptlang.org/)
- [Vite](https://vitejs.dev/) - Lightning-fast build tool
- [Playwright](https://playwright.dev/) - UI capture and testing
- [ESLint](https://eslint.org/) - Code quality

---

**🤖 Powered by the Ralph Loop methodology - Disciplined, transparent, and quality-driven development.**
