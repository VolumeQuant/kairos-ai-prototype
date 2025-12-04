@echo off
chcp 65001 >nul
title KAIROS Backend Server
echo ========================================
echo KAIROS AI - Backend Server Starting...
echo ========================================
echo.

cd /d "%~dp0"

REM Set Python path from miniconda environment
set PYTHON_PATH=C:\Users\user\miniconda3\envs\volumequant\python.exe

if not exist "%PYTHON_PATH%" (
    echo [ERROR] Python not found at: %PYTHON_PATH%
    echo Please check the path in start_uvicorn.bat
    pause
    exit /b 1
)

echo Using Python: %PYTHON_PATH%
echo.
echo Starting uvicorn server on http://127.0.0.1:8000
echo.
%PYTHON_PATH% -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000

pause

