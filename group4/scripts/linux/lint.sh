#!/usr/bin/env bash

# Get the directory where this script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# Go up two levels to get to group4/ directory
GROUP4_DIR="$(cd "$SCRIPT_DIR/../.." && pwd)"

GREEN='\033[0;32m'
NC='\033[0m' # No Color

echo -e "${GREEN}Executing ruff...${NC}"
ruff check "$GROUP4_DIR" --fix

echo -e "\n${GREEN}Executing mypy...${NC}"
mypy "$GROUP4_DIR"