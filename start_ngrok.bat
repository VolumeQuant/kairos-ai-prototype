@echo off
title KAIROS ngrok Tunnel
echo ========================================
echo KAIROS AI - ngrok Tunnel Starting...
echo ========================================
echo.
echo Exposing http://127.0.0.1:8000 to public internet...
echo.
ngrok http 8000

pause

