@echo off
title 전원 설정 원래대로 복구
echo ========================================
echo 전원 설정을 기본값으로 복구 중...
echo ========================================
echo.

REM 화면 끄기: 15분 후
powercfg /change monitor-timeout-ac 15
echo ✅ 화면 끄기: 15분 후

REM 절전 모드: 30분 후
powercfg /change standby-timeout-ac 30
echo ✅ 절전 모드: 30분 후

REM 최대 절전 모드: 사용 안 함
powercfg /change hibernate-timeout-ac 0
echo ✅ 최대 절전 모드: 사용 안 함

REM 디스크 끄기: 사용 안 함
powercfg /change disk-timeout-ac 0
echo ✅ 디스크 끄기: 사용 안 함

echo.
echo ========================================
echo 🎉 전원 설정이 복구되었습니다!
echo ========================================
echo.
pause

