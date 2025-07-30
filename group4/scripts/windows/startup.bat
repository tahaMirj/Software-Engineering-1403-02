@echo off

REM Get the directory where this script is located
set "SCRIPT_DIR=%~dp0"
REM Go up three levels to get to project root directory (where manage.py is)
for %%i in ("%SCRIPT_DIR%..\..\..") do set "PROJECT_ROOT=%%~fi"

echo [92mMaking migrations for group4...[0m
cd /d "%PROJECT_ROOT%" && python manage.py makemigrations group4

echo.
echo [92mApplying migrations...[0m
cd /d "%PROJECT_ROOT%" && python manage.py migrate

echo.
echo [92mStarting development server...[0m
cd /d "%PROJECT_ROOT%" && python manage.py runserver
