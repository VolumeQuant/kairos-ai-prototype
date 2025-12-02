@echo off
title 🌅 출근 후 설정 - KAIROS AI
color 0B
echo ========================================
echo     🌅 출근 후 설정 - KAIROS AI
echo ========================================
echo.
echo 전원 설정을 원래대로 복구합니다.
echo (배터리 절약을 위해 정상 모드로 변경)
echo.
pause

echo.
echo [1/4] 절전 모드 복구 중...
echo.

REM 모니터 끄기: 15분 후
powercfg /change monitor-timeout-ac 15
powercfg /change monitor-timeout-dc 5
echo ✅ 모니터 끄기: 15분 후

REM 절전 모드: 30분 후 (배터리는 10분)
powercfg /change standby-timeout-ac 30
powercfg /change standby-timeout-dc 10
echo ✅ 절전 모드: 30분 후

REM 하드디스크: 20분 후
powercfg /change disk-timeout-ac 20
powercfg /change disk-timeout-dc 10
echo ✅ 하드디스크: 20분 후

echo.
echo [2/4] 최대 절전 모드 재활성화...
echo.

powercfg /hibernate on
echo ✅ 최대 절전 모드 재활성화

echo.
echo [3/4] 균형 잡힌 전원 모드로 전환...
echo.

REM 균형 잡힌 전원 모드로 변경
powercfg /setactive 381b4222-f694-41f0-9685-ff5bb260df2e
echo ✅ 균형 잡힌 전원 모드 활성화

echo.
echo [4/4] USB 절전 재활성화...
echo.

powercfg /setacvalueindex SCHEME_CURRENT 2a737441-1930-4402-8d77-b2bebba308a3 48e6b7a6-50f5-4782-a5d4-53bb8f07e226 1
powercfg /setactive SCHEME_CURRENT
echo ✅ USB 절전 재활성화

echo.
echo ========================================
echo 🎉 전원 설정이 복구되었습니다!
echo ========================================
echo.
echo 💻 복구된 설정:
echo    ✅ 모니터 끄기: 15분 후
echo    ✅ 절전 모드: 30분 후
echo    ✅ 최대 절전: 활성화
echo    ✅ 전원 모드: 균형 잡힌 모드
echo.
echo 💡 서버 상태:
echo    - 서버는 계속 실행 중입니다
echo    - 종료하려면 Cursor 터미널에서 Ctrl+C
echo.
pause

