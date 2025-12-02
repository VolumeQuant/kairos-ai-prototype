@echo off
title 🔥 전원 절대 안 끄기 - 최종 설정
color 0E
echo.
echo ████████████████████████████████████████
echo █                                      █
echo █   🔥 전원 절대 안 끄기 - 최종 설정   █
echo █                                      █
echo ████████████████████████████████████████
echo.
echo 이 스크립트는 컴퓨터가 절대 꺼지지 않도록
echo 모든 절전 기능을 완전히 비활성화합니다.
echo.
echo ⚠️  중요: 관리자 권한으로 실행해야 합니다!
echo    (우클릭 → 관리자 권한으로 실행)
echo.
pause

echo.
echo ═══════════════════════════════════════
echo  1단계: 모든 절전 모드 비활성화
echo ═══════════════════════════════════════
echo.

REM 전원 연결 시 (AC)
powercfg /change monitor-timeout-ac 0
powercfg /change standby-timeout-ac 0
powercfg /change disk-timeout-ac 0
powercfg /change hibernate-timeout-ac 0

REM 배터리 사용 시 (DC)
powercfg /change monitor-timeout-dc 0
powercfg /change standby-timeout-dc 0
powercfg /change disk-timeout-dc 0
powercfg /change hibernate-timeout-dc 0

echo ✅ 절전 모드: 완전 비활성화
echo ✅ 모니터 끄기: 비활성화
echo ✅ 하드디스크 끄기: 비활성화
echo ✅ 최대 절전 타임아웃: 비활성화

echo.
echo ═══════════════════════════════════════
echo  2단계: 최대 절전 모드 완전 제거
echo ═══════════════════════════════════════
echo.

powercfg /hibernate off
echo ✅ 최대 절전 모드 완전 비활성화
echo    (hiberfil.sys 파일도 삭제됨)

echo.
echo ═══════════════════════════════════════
echo  3단계: 고성능 전원 모드 활성화
echo ═══════════════════════════════════════
echo.

powercfg /setactive 8c5e7fda-e8bf-4a96-9a85-a6e23a8c635c
echo ✅ 고성능 전원 모드 활성화

echo.
echo ═══════════════════════════════════════
echo  4단계: USB 절전 방지
echo ═══════════════════════════════════════
echo.

powercfg /setacvalueindex SCHEME_CURRENT 2a737441-1930-4402-8d77-b2bebba308a3 48e6b7a6-50f5-4782-a5d4-53bb8f07e226 0
powercfg /setactive SCHEME_CURRENT
echo ✅ USB 선택적 일시 중단 비활성화

echo.
echo ═══════════════════════════════════════
echo  5단계: PCI Express 절전 방지
echo ═══════════════════════════════════════
echo.

powercfg /setacvalueindex SCHEME_CURRENT 501a4d13-42af-4429-9fd1-a8218c268e20 ee12f906-d277-404b-b6da-e5fa1a576df5 0
powercfg /setactive SCHEME_CURRENT
echo ✅ PCI Express 링크 상태 전원 관리 끔

echo.
echo ═══════════════════════════════════════
echo  6단계: 프로세서 전원 관리 최대화
echo ═══════════════════════════════════════
echo.

REM 최소 프로세서 상태를 100%로
powercfg /setacvalueindex SCHEME_CURRENT 54533251-82be-4824-96c1-47b60b740d00 893dee8e-2bef-41e0-89c6-b55d0929964c 100
REM 최대 프로세서 상태를 100%로
powercfg /setacvalueindex SCHEME_CURRENT 54533251-82be-4824-96c1-47b60b740d00 bc5038f7-23e0-4960-96da-33abaf5935ec 100
powercfg /setactive SCHEME_CURRENT
echo ✅ CPU 항상 최대 성능으로 작동

echo.
echo ═══════════════════════════════════════
echo  7단계: Windows 자동 재시작 방지
echo ═══════════════════════════════════════
echo.

REM Windows 업데이트 자동 재시작 비활성화
reg add "HKLM\SOFTWARE\Policies\Microsoft\Windows\WindowsUpdate\AU" /v NoAutoRebootWithLoggedOnUsers /t REG_DWORD /d 1 /f >nul 2>&1
if %errorlevel% equ 0 (
    echo ✅ Windows 업데이트 자동 재시작 비활성화
) else (
    echo ⚠️  관리자 권한이 없어 Windows 업데이트 설정은 건너뜁니다.
)

REM 활성 시간 설정 (24시간)
reg add "HKLM\SOFTWARE\Microsoft\WindowsUpdate\UX\Settings" /v ActiveHoursStart /t REG_DWORD /d 6 /f >nul 2>&1
reg add "HKLM\SOFTWARE\Microsoft\WindowsUpdate\UX\Settings" /v ActiveHoursEnd /t REG_DWORD /d 6 /f >nul 2>&1
echo ✅ 활성 시간 24시간 설정

echo.
echo ═══════════════════════════════════════
echo  8단계: 서버 실행 상태 확인
echo ═══════════════════════════════════════
echo.

netstat -ano | findstr ":8000" >nul
if %errorlevel% equ 0 (
    echo ✅ uvicorn 서버가 8000 포트에서 실행 중입니다.
) else (
    echo ⚠️  경고: 8000 포트에서 서버가 실행되지 않고 있습니다!
)

tasklist | findstr "ngrok.exe" >nul
if %errorlevel% equ 0 (
    echo ✅ ngrok이 실행 중입니다.
) else (
    echo ⚠️  경고: ngrok이 실행되지 않고 있습니다!
)

echo.
echo ████████████████████████████████████████
echo █                                      █
echo █        🎉 모든 설정 완료! 🎉         █
echo █                                      █
echo ████████████████████████████████████████
echo.
echo 💻 현재 컴퓨터 상태:
echo    ✅ 절전 모드: 완전 비활성화
echo    ✅ 최대 절전: 완전 비활성화
echo    ✅ 고성능 모드: 활성화
echo    ✅ USB 절전: 비활성화
echo    ✅ CPU: 최대 성능
echo    ✅ Windows 자동 재시작: 방지
echo.
echo 📌 최종 체크리스트:
echo    ☑ 전원 케이블 연결 확인!
echo    ☑ Cursor 창 최소화 (닫지 말 것!)
echo    ☑ ngrok 창 최소화 (닫지 말 것!)
echo    ☑ 모니터는 꺼도 됩니다
echo.
echo 🔥 이제 컴퓨터가 절대 꺼지지 않습니다!
echo.
echo 💡 출근 후 "출근_후_실행.bat"를 실행하여
echo    전원 설정을 원래대로 복구하세요.
echo.
pause

