@echo off
chcp 65001 >nul
echo ========================================
echo KAIROS AI - System Diagnosis
echo ========================================
echo.

cd /d "%~dp0"

REM Set Python path from miniconda environment
set PYTHON_PATH=C:\Users\user\miniconda3\envs\volumequant\python.exe

REM Set ngrok path
set NGROK_PATH=C:\dev\ngrok-v3-stable-windows-amd64\ngrok.exe

echo [1/5] Checking Python...
if exist "%PYTHON_PATH%" (
    "%PYTHON_PATH%" --version
    echo [OK] Python is installed at: %PYTHON_PATH%
) else (
    echo [X] Python NOT FOUND at: %PYTHON_PATH%
    echo     Checking system Python...
    python --version >nul 2>&1
    if errorlevel 1 (
        echo [X] System Python also NOT FOUND
        echo     Please check the path in 진단.bat
    ) else (
        python --version
        echo [OK] System Python found (but using miniconda path)
    )
)
echo.

echo [2/5] Checking pip...
if exist "%PYTHON_PATH%" (
    "%PYTHON_PATH%" -m pip --version
    echo [OK] pip is installed
) else (
    pip --version >nul 2>&1
    if errorlevel 1 (
        echo [X] pip NOT FOUND
    ) else (
        pip --version
        echo [OK] pip is installed
    )
)
echo.

echo [3/5] Checking uvicorn...
if exist "%PYTHON_PATH%" (
    "%PYTHON_PATH%" -m uvicorn --version >nul 2>&1
    if errorlevel 1 (
        echo [X] uvicorn NOT FOUND
        echo     Run: "%PYTHON_PATH%" -m pip install -r requirements.txt
    ) else (
        "%PYTHON_PATH%" -m uvicorn --version
        echo [OK] uvicorn is installed
    )
) else (
    python -m uvicorn --version >nul 2>&1
    if errorlevel 1 (
        echo [X] uvicorn NOT FOUND
        echo     Run: pip install -r requirements.txt
    ) else (
        python -m uvicorn --version
        echo [OK] uvicorn is installed
    )
)
echo.

echo [4/5] Checking FastAPI...
if exist "%PYTHON_PATH%" (
    "%PYTHON_PATH%" -c "import fastapi; print('FastAPI version:', fastapi.__version__)" >nul 2>&1
    if errorlevel 1 (
        echo [X] FastAPI NOT FOUND
        echo     Run: "%PYTHON_PATH%" -m pip install -r requirements.txt
    ) else (
        "%PYTHON_PATH%" -c "import fastapi; print('FastAPI version:', fastapi.__version__)"
        echo [OK] FastAPI is installed
    )
) else (
    python -c "import fastapi; print(fastapi.__version__)" >nul 2>&1
    if errorlevel 1 (
        echo [X] FastAPI NOT FOUND
        echo     Run: pip install -r requirements.txt
    ) else (
        python -c "import fastapi; print('FastAPI version:', fastapi.__version__)"
        echo [OK] FastAPI is installed
    )
)
echo.

echo [5/5] Checking ngrok...
if exist "%NGROK_PATH%" (
    "%NGROK_PATH%" version
    echo [OK] ngrok is installed at: %NGROK_PATH%
) else (
    echo [X] ngrok NOT FOUND at: %NGROK_PATH%
    echo     Checking PATH...
    ngrok version >nul 2>&1
    if errorlevel 1 (
        echo [X] ngrok also NOT FOUND in PATH
        echo     Please check the path in 진단.bat
        echo     Expected: %NGROK_PATH%
        echo     Download from: https://ngrok.com/download
    ) else (
        ngrok version
        echo [OK] ngrok found in PATH (but expected at: %NGROK_PATH%)
    )
)
echo.

echo ========================================
echo Diagnosis Complete
echo ========================================
echo.
echo If you see [X] errors above, please fix them first.
echo.
pause

