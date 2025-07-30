#!/usr/bin/env bash

set -e

# Get the directory where this script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# Go up two levels to get to group4/ directory
GROUP4_DIR="$(cd "$SCRIPT_DIR/../.." && pwd)"

GREEN='\033[0;32m'
NC='\033[0m' # No Color

echo -e "${GREEN}Executing ruff...${NC}"
ruff format "$GROUP4_DIR"

echo -e "\n${GREEN}Executing isort...${NC}"
isort "$GROUP4_DIR"
