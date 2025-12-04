@echo off
chcp 65001 >nul
title KAIROS ngrok Tunnel
echo ========================================
echo KAIROS AI - ngrok Tunnel Starting...
echo ========================================
echo.

cd /d "%~dp0"

REM Set ngrok path
set NGROK_PATH=C:\dev\ngrok-v3-stable-windows-amd64\ngrok.exe

if exist "%NGROK_PATH%" (
    echo Using ngrok: %NGROK_PATH%
    echo.
    echo Exposing http://127.0.0.1:8000 to public internet...
    echo.
    %NGROK_PATH% http 8000
) else (
    echo [WARNING] ngrok not found at: %NGROK_PATH%
    echo Checking PATH...
    ngrok version >nul 2>&1
    if errorlevel 1 (
        echo [ERROR] ngrok not found in PATH either
        echo Please check the path in start_ngrok.bat
        echo Expected: %NGROK_PATH%
        pause
        exit /b 1
    ) else (
        echo Found ngrok in PATH
        echo.
        echo Exposing http://127.0.0.1:8000 to public internet...
        echo.
        ngrok http 8000
    )
)

pause

