@echo off
echo ========================================
echo KAIROS AI - Starting All Services
echo ========================================
echo.

cd /d "%~dp0"

echo [1/2] Starting Backend Server...
start "KAIROS Backend" cmd /k "conda activate volumequant && uvicorn app.main:app --reload --host 127.0.0.1 --port 8000"

timeout /t 3 /nobreak >nul

echo [2/2] Starting ngrok Tunnel...
start "KAIROS ngrok" cmd /k "ngrok http 8000"

echo.
echo ========================================
echo ✅ All services started!
echo ========================================
echo.
echo - Backend Server: http://127.0.0.1:8000
echo - ngrok tunnel: Check the ngrok window for public URL
echo.
echo 💡 두 창을 닫지 말고 최소화하세요!
echo.
pause

