@echo off
setlocal
set PYTHON=python

REM Check if Python 3.12.13 is installed
%PYTHON% --version | findstr "3.12.13" >nul
if errorlevel 1 (
    echo Python 3.12.13 not found. Please install it first.
    exit /b 1
)

set VENV_DIR=.venv

%PYTHON% -m venv %VENV_DIR%
call %VENV_DIR%\Scripts\activate.bat
pip install --upgrade pip
pip install -r requirements.txt

echo ✅ Environment setup complete. To activate: call %VENV_DIR%\Scripts\activate.bat
