@echo off

REM Get the directory where this script is located
set "SCRIPT_DIR=%~dp0"
REM Go up two levels to get to group4/ directory
for %%i in ("%SCRIPT_DIR%..\..") do set "GROUP4_DIR=%%~fi"

echo [92mExecuting ruff format on %GROUP4_DIR%...[0m
ruff format "%GROUP4_DIR%"

echo.
echo [92mExecuting isort on %GROUP4_DIR%...[0m
isort "%GROUP4_DIR%"
