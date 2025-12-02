@echo off
title Windows 업데이트 자동 재시작 방지
color 0C
echo ========================================
echo   Windows 업데이트 자동 재시작 방지
echo ========================================
echo.
echo ⚠️  주의: 이 작업은 관리자 권한이 필요합니다!
echo.
echo 이 스크립트는 다음을 수행합니다:
echo 1. Windows 업데이트 자동 재시작 비활성화
echo 2. 활성 시간 설정 (24시간 보호)
echo.
pause

echo.
echo [1/2] Windows 업데이트 자동 재시작 비활성화...
echo.

REM 자동 재시작 비활성화 (레지스트리)
reg add "HKLM\SOFTWARE\Policies\Microsoft\Windows\WindowsUpdate\AU" /v NoAutoRebootWithLoggedOnUsers /t REG_DWORD /d 1 /f >nul 2>&1
if %errorlevel% equ 0 (
    echo ✅ 자동 재시작 비활성화 완료
) else (
    echo ❌ 관리자 권한으로 실행해야 합니다!
    echo    파일을 우클릭 → "관리자 권한으로 실행"
    echo.
    pause
    exit /b 1
)

REM 자동 업데이트 다운로드만 (자동 설치 안 함)
reg add "HKLM\SOFTWARE\Policies\Microsoft\Windows\WindowsUpdate\AU" /v AUOptions /t REG_DWORD /d 3 /f >nul

echo.
echo [2/2] 활성 시간 설정 (오후 6시 ~ 오전 10시)...
echo.

REM 활성 시간 설정 (18:00 ~ 10:00 = 16시간)
reg add "HKLM\SOFTWARE\Microsoft\WindowsUpdate\UX\Settings" /v ActiveHoursStart /t REG_DWORD /d 18 /f >nul
reg add "HKLM\SOFTWARE\Microsoft\WindowsUpdate\UX\Settings" /v ActiveHoursEnd /t REG_DWORD /d 10 /f >nul
echo ✅ 활성 시간 설정 완료 (18:00 ~ 다음날 10:00)

echo.
echo ========================================
echo 🎉 설정 완료!
echo ========================================
echo.
echo 이제 Windows가 자동으로 재시작하지 않습니다.
echo.
echo 💡 참고:
echo    - 보안을 위해 주기적으로 수동 업데이트를 권장합니다
echo    - 설정 → Windows Update에서 수동 업데이트 가능
echo.
pause

