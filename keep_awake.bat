@echo off
title 컴퓨터 절전 모드 방지
echo ========================================
echo 컴퓨터 절전 모드 방지 설정 중...
echo ========================================
echo.

REM 화면 끄기 방지 (전원 연결 시)
powercfg /change monitor-timeout-ac 0
echo ✅ 화면 끄기 방지: 완료

REM 절전 모드 방지 (전원 연결 시)
powercfg /change standby-timeout-ac 0
echo ✅ 절전 모드 방지: 완료

REM 최대 절전 모드 방지 (전원 연결 시)
powercfg /change hibernate-timeout-ac 0
echo ✅ 최대 절전 모드 방지: 완료

REM 디스크 끄기 방지 (전원 연결 시)
powercfg /change disk-timeout-ac 0
echo ✅ 디스크 끄기 방지: 완료

echo.
echo ========================================
echo 🎉 설정 완료!
echo ========================================
echo.
echo 이제 컴퓨터가 자동으로 꺼지지 않습니다.
echo 전원 케이블이 연결되어 있는지 확인하세요!
echo.
pause

