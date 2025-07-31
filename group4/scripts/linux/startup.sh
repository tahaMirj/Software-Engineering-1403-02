#!/usr/bin/env bash

# Get the directory where this script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# Go up three levels to get to project root directory (where manage.py is)
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../../.." && pwd)"

GREEN='\033[0;32m'
NC='\033[0m' # No Color

echo -e "${GREEN}Making migrations for group4...${NC}"
cd "$PROJECT_ROOT" && python manage.py makemigrations group4

echo -e "\n${GREEN}Applying migrations...${NC}"
cd "$PROJECT_ROOT" && python manage.py migrate

echo -e "\n${GREEN}Starting development server...${NC}"
cd "$PROJECT_ROOT" && python manage.py runserver

