@echo off
title Jasper AI — Live Voice Copilot
cd /d "%~dp0"
echo ===================================================
echo   JASPER AI - LIVE VOICE COPILOT (JARVIS 2.0)
echo   Muallif: Javohirbek Asqarov (Jasper)
echo ===================================================
echo [1/2] Server ishga tushirilmoqda...
start "Jasper Copilot Server" /min python -m uvicorn server.main:app --port 8000 --host 127.0.0.1
timeout /t 2 /nobreak >nul
echo [2/2] Interfeys http://127.0.0.1:8000 manzilida ochilmoqda...
start "" "http://127.0.0.1:8000"
echo Bajarildi! Ovozli yordamchi ishga tushdi.
