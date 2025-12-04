@echo off
chcp 65001 >nul
echo ========================================
echo KAIROS AI - Starting All Services (Simple)
echo ========================================
echo.

cd /d "%~dp0"

REM Set Python path from miniconda environment
set PYTHON_PATH=C:\Users\user\miniconda3\envs\volumequant\python.exe
set CONDA_ENV=C:\Users\user\miniconda3\envs\volumequant

REM Set ngrok path
set NGROK_PATH=C:\dev\ngrok-v3-stable-windows-amd64\ngrok.exe

echo Checking Python installation...
if not exist "%PYTHON_PATH%" (
    echo.
    echo [ERROR] Python not found at: %PYTHON_PATH%
    echo Please check the path and update start_all_simple.bat
    echo.
    pause
    exit /b 1
)

"%PYTHON_PATH%" --version
if errorlevel 1 (
    echo.
    echo [ERROR] Python is not working!
    echo.
    pause
    exit /b 1
)

echo Checking uvicorn...
"%PYTHON_PATH%" -m uvicorn --version >nul 2>&1
if errorlevel 1 (
    echo.
    echo [WARNING] uvicorn is not installed!
    echo Installing dependencies...
    "%PYTHON_PATH%" -m pip install -r requirements.txt
    if errorlevel 1 (
        echo.
        echo [ERROR] Failed to install dependencies!
        echo Please run manually: "%PYTHON_PATH%" -m pip install -r requirements.txt
        echo.
        pause
        exit /b 1
    )
)

echo.
echo [1/2] Starting Backend Server...
echo (Using miniconda Python: %PYTHON_PATH%)
start "KAIROS Backend" cmd /k "chcp 65001 >nul && cd /d %~dp0 && echo Starting server... && %PYTHON_PATH% -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000 && pause"

timeout /t 5 /nobreak >nul

echo [2/2] Starting ngrok Tunnel...
if not exist "%NGROK_PATH%" (
    echo [WARNING] ngrok not found at: %NGROK_PATH%
    echo Checking PATH...
    ngrok version >nul 2>&1
    if errorlevel 1 (
        echo [ERROR] ngrok not found in PATH either
        echo Please check the path in start_all_simple.bat
        echo Expected: %NGROK_PATH%
    ) else (
        echo [OK] Found ngrok in PATH
        start "KAIROS ngrok" cmd /k "chcp 65001 >nul && cd /d %~dp0 && echo Starting ngrok... && ngrok http 8000 && pause"
    )
) else (
    echo [OK] Found ngrok at: %NGROK_PATH%
    start "KAIROS ngrok" cmd /k "chcp 65001 >nul && cd /d %~dp0 && echo Starting ngrok... && %NGROK_PATH% http 8000 && pause"
)

echo.
echo ========================================
echo All services started!
echo ========================================
echo.
echo - Backend Server: http://127.0.0.1:8000
echo - ngrok tunnel: Check the ngrok window for public URL
echo.
echo IMPORTANT: 
echo 1. Check the "KAIROS Backend" window for server status
echo 2. If you see errors, run "진단.bat" to check your setup
echo 3. Do not close the windows, minimize them instead!
echo.
pause

