#!/bin/bash
# Code verification script - Full validation pipeline
# Runs: lint -> type-check -> test
# Exits with non-zero status if any step fails

set -e  # Exit immediately if any command fails
set -o pipefail  # Catch failures in pipes

echo "=========================================="
echo "Starting Code Verification Pipeline"
echo "=========================================="
echo ""

# Color codes for better readability
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Track overall status
FAILED=0

# Step 1: ESLint
echo -e "${YELLOW}[1/3] Running ESLint...${NC}"
echo "Command: npm run lint"
echo ""

if npm run lint; then
    echo -e "${GREEN}✓ ESLint passed${NC}"
else
    echo -e "${RED}✗ ESLint failed${NC}"
    exit 1
fi
echo ""

# Step 2: TypeScript Type Check
echo -e "${YELLOW}[2/3] Running TypeScript type check...${NC}"
echo "Command: npx tsc --noEmit"
echo ""

if npx tsc --noEmit; then
    echo -e "${GREEN}✓ Type check passed${NC}"
else
    echo -e "${RED}✗ Type check failed${NC}"
    exit 1
fi
echo ""

# Step 3: Tests
echo -e "${YELLOW}[3/3] Running tests...${NC}"
echo "Command: npm test"
echo ""

if npm test; then
    echo -e "${GREEN}✓ Tests passed${NC}"
else
    echo -e "${RED}✗ Tests failed${NC}"
    exit 1
fi
echo ""

# Success
echo "=========================================="
echo -e "${GREEN}✓ All verification steps passed!${NC}"
echo "=========================================="
exit 0
