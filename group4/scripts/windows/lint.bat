@echo off

REM Get the directory where this script is located
set "SCRIPT_DIR=%~dp0"
REM Go up two levels to get to group4/ directory
for %%i in ("%SCRIPT_DIR%..\..") do set "GROUP4_DIR=%%~fi"

echo [92mExecuting ruff on %GROUP4_DIR%...[0m
ruff check "%GROUP4_DIR%" --fix

echo.
echo [92mExecuting mypy on %GROUP4_DIR%...[0m
mypy "%GROUP4_DIR%"
