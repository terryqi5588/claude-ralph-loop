#!/bin/bash
# Code verification script - Full validation pipeline
# Runs: lint -> type-check -> test
# Provides detailed error feedback for debugging

set -o pipefail  # Catch failures in pipes

echo "=========================================="
echo "Starting Code Verification Pipeline"
echo "=========================================="
echo ""

# Color codes for better readability
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
BOLD='\033[1m'
NC='\033[0m' # No Color

# Temp file for capturing output
TEMP_OUTPUT=$(mktemp)
trap "rm -f $TEMP_OUTPUT" EXIT

# Helper function to print error summary
print_error_summary() {
    local step=$1
    local command=$2
    echo ""
    echo -e "${RED}${BOLD}=========================================="
    echo -e "VERIFICATION FAILED: $step"
    echo -e "==========================================${NC}"
    echo ""
    echo -e "${YELLOW}Failed at:${NC} $step"
    echo -e "${YELLOW}Command:${NC} $command"
    echo ""
}

# Helper function to extract and display key errors
show_key_errors() {
    local output_file=$1
    local max_lines=${2:-10}

    echo -e "${BLUE}Key Errors (first $max_lines lines):${NC}"
    echo "----------------------------------------"
    head -n "$max_lines" "$output_file"

    # Count total errors
    local total_lines=$(wc -l < "$output_file")
    if [ "$total_lines" -gt "$max_lines" ]; then
        echo "..."
        echo -e "${YELLOW}(+$(($total_lines - $max_lines)) more lines, see full output above)${NC}"
    fi
    echo "----------------------------------------"
}

# Step 1: ESLint
echo -e "${YELLOW}[1/3] Running ESLint...${NC}"
echo "Command: npm run lint"
echo ""

if npm run lint 2>&1 | tee "$TEMP_OUTPUT"; then
    echo -e "${GREEN}✓ ESLint passed${NC}"
else
    print_error_summary "ESLint" "npm run lint"
    echo -e "${BLUE}What this means:${NC}"
    echo "  • Code style or quality issues detected"
    echo "  • Check the errors above for specific line numbers"
    echo "  • Fix the issues and run verify.sh again"
    echo ""
    exit 1
fi
echo ""

# Step 2: TypeScript Type Check
echo -e "${YELLOW}[2/3] Running TypeScript type check...${NC}"
echo "Command: npx tsc --noEmit"
echo ""

if npx tsc --noEmit 2>&1 | tee "$TEMP_OUTPUT"; then
    echo -e "${GREEN}✓ Type check passed${NC}"
else
    print_error_summary "TypeScript Type Check" "npx tsc --noEmit"

    # Extract and show key type errors
    echo -e "${BLUE}What this means:${NC}"
    echo "  • TypeScript found type errors in your code"
    echo "  • These must be fixed before proceeding"
    echo ""

    # Show first 10 lines of errors
    show_key_errors "$TEMP_OUTPUT" 10

    echo ""
    echo -e "${BLUE}Common fixes:${NC}"
    echo "  • Add missing type annotations"
    echo "  • Fix type mismatches"
    echo "  • Import missing types"
    echo "  • Check for 'any' types that should be specific"
    echo ""
    exit 2
fi
echo ""

# Step 3: Tests
echo -e "${YELLOW}[3/3] Running tests...${NC}"
echo "Command: npm test"
echo ""

if npm test 2>&1 | tee "$TEMP_OUTPUT"; then
    echo -e "${GREEN}✓ Tests passed${NC}"
else
    print_error_summary "Tests" "npm test"

    echo -e "${BLUE}What this means:${NC}"
    echo "  • One or more tests failed"
    echo "  • Check test output for specific failures"
    echo ""

    # Show key test errors
    show_key_errors "$TEMP_OUTPUT" 15

    echo ""
    echo -e "${BLUE}Next steps:${NC}"
    echo "  • Review failing test output"
    echo "  • Fix the code or update tests"
    echo "  • Run 'npm test' to verify fixes"
    echo ""
    exit 3
fi
echo ""

# Success
echo "=========================================="
echo -e "${GREEN}${BOLD}✓ All verification steps passed!${NC}"
echo "=========================================="
echo ""
echo "Summary:"
echo "  ✓ ESLint - Code quality"
echo "  ✓ TypeScript - Type safety"
echo "  ✓ Tests - Functional correctness"
echo ""
exit 0
