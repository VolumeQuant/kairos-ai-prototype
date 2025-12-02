@echo off
title 🏢 퇴근 전 설정 - KAIROS AI
color 0A
echo ========================================
echo     🏢 퇴근 전 설정 - KAIROS AI
echo ========================================
echo.
echo 이 스크립트는 다음을 수행합니다:
echo.
echo 1. 컴퓨터 절전 모드 완전 비활성화
echo 2. 최대 절전 모드 비활성화
echo 3. 빠른 시작 비활성화
echo 4. USB 절전 비활성화
echo 5. 서버 실행 상태 확인
echo.
echo ========================================
echo.
pause

echo [1/5] 모든 절전 기능 비활성화 중...
echo.

REM 모니터 끄기 방지
powercfg /change monitor-timeout-ac 0
powercfg /change monitor-timeout-dc 0
echo ✅ 모니터 끄기 방지

REM 절전 모드 방지
powercfg /change standby-timeout-ac 0
powercfg /change standby-timeout-dc 0
echo ✅ 절전 모드 방지

REM 하드디스크 끄기 방지
powercfg /change disk-timeout-ac 0
powercfg /change disk-timeout-dc 0
echo ✅ 하드디스크 끄기 방지

echo.
echo [2/5] 최대 절전 모드 완전 비활성화...
echo.

REM 최대 절전 모드 타임아웃 방지
powercfg /change hibernate-timeout-ac 0
powercfg /change hibernate-timeout-dc 0
echo ✅ 최대 절전 타임아웃 방지

REM 최대 절전 모드 자체를 비활성화
powercfg /hibernate off
echo ✅ 최대 절전 모드 완전 비활성화

echo.
echo [3/5] 고성능 전원 모드로 전환...
echo.

REM 고성능 전원 모드로 변경
powercfg /setactive 8c5e7fda-e8bf-4a96-9a85-a6e23a8c635c
echo ✅ 고성능 모드 활성화

echo.
echo [4/5] USB 절전 방지...
echo.

REM USB 선택적 일시 중단 비활성화
powercfg /setacvalueindex SCHEME_CURRENT 2a737441-1930-4402-8d77-b2bebba308a3 48e6b7a6-50f5-4782-a5d4-53bb8f07e226 0
powercfg /setactive SCHEME_CURRENT
echo ✅ USB 절전 방지

echo ✅ 모든 절전 기능 비활성화 완료!
echo.

echo [5/5] 서버 실행 상태 확인...
echo.

netstat -ano | findstr ":8000" >nul
if %errorlevel% equ 0 (
    echo ✅ uvicorn 서버가 8000 포트에서 실행 중입니다.
) else (
    echo ⚠️  경고: 8000 포트에서 서버가 실행되지 않고 있습니다!
    echo     Cursor 터미널에서 서버를 실행했는지 확인하세요.
)
echo.

tasklist | findstr "ngrok.exe" >nul
if %errorlevel% equ 0 (
    echo ✅ ngrok이 실행 중입니다.
) else (
    echo ⚠️  경고: ngrok이 실행되지 않고 있습니다!
    echo     ngrok을 실행했는지 확인하세요.
)

echo.
echo ========================================
echo 🎉 퇴근 준비 완료!
echo ========================================
echo.
echo 📌 체크리스트:
echo    ☐ 전원 케이블 연결 확인
echo    ☐ Cursor 창 최소화 (닫지 마세요!)
echo    ☐ ngrok 창 최소화 (닫지 마세요!)
echo    ☐ 모니터 전원은 꺼도 됩니다
echo.
echo 💡 출근 후 restore_power_settings.bat 실행하여
echo    전원 설정을 원래대로 복구하세요!
echo.
pause

