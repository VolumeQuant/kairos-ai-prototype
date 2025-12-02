@echo off
title KAIROS Backend Server
echo ========================================
echo KAIROS AI - Backend Server Starting...
echo ========================================
echo.

cd /d "%~dp0"
call conda activate volumequant
echo Conda environment activated: volumequant
echo.
echo Starting uvicorn server on http://127.0.0.1:8000
echo.
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000

pause

