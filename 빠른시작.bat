@echo off
chcp 65001 >nul
echo ========================================
echo 🌐 KAIROS AI 공개 URL 설정
echo ========================================
echo.

cd /d "%~dp0"

REM Set Python path from miniconda environment
set PYTHON_PATH=C:\Users\user\miniconda3\envs\volumequant\python.exe

echo 1단계: 서버 실행 중...
echo.

if not exist "%PYTHON_PATH%" (
    echo [ERROR] Python not found at: %PYTHON_PATH%
    echo Please check the path in 빠른시작.bat
    pause
    exit /b 1
)

start "KAIROS 서버" cmd /k "chcp 65001 >nul && cd /d %~dp0 && %PYTHON_PATH% -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000"

timeout /t 3 /nobreak >nul

echo.
echo ✅ 서버가 실행되었습니다!
echo.
echo 2단계: ngrok을 실행하세요
echo.
echo 다음 명령을 새 터미널에서 실행하세요:
echo    ngrok http 8000
echo.
echo 또는 ngrok.exe가 있는 폴더에서:
echo    .\ngrok.exe http 8000
echo.
echo ========================================
echo 📌 ngrok이 제공하는 URL을 복사하세요
echo 📌 그 URL을 https://bit.ly 에서 단축하세요
echo ========================================
echo.
pause

