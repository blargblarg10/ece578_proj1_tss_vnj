@echo off

:: Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Python is not installed. Please install Python first.
    exit /b 1
)

:: Get the directory of the current script
set "SCRIPT_DIR=%~dp0"

:: Set the directory for the virtual environment
set "VENV_DIR=%SCRIPT_DIR%.env"

:: Check if the .env directory already exists
if not exist "%VENV_DIR%" (
    :: If not, create the virtual environment
    echo Creating a virtual environment at "%VENV_DIR%". This may take a few moments.
    python -m venv "%VENV_DIR%"
    echo Virtual environment created at "%VENV_DIR%".
) else (
    echo .env directory already exists. Skipping virtual environment creation.
)

:: Activate the virtual environment
call "%VENV_DIR%\Scripts\activate.bat"

:: Set the GIT_PROJ_DIR environment variable
set "GIT_PROJ_DIR=%SCRIPT_DIR%"
echo GIT_PROJ_DIR is set to "%GIT_PROJ_DIR%"

:: Install the current area as an editable package
pip install -e .
echo Completed.
