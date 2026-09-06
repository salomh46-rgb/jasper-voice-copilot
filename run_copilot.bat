@echo off
title Jasper AI Live Voice Copilot Launcher
echo ========================================================
echo     JASPER AI LIVE VOICE COPILOT (JARVIS ASSISTANT)
echo ========================================================
echo.
echo [1/2] Launching Backend Voice Action Server on Port 8000...
start cmd /k "python -m uvicorn server.main:app --host 127.0.0.1 --port 8000 --reload"
timeout /t 2 >nul
echo.
echo [2/2] Opening Futuristic Voice Control Panel in Browser...
start "" "client\index.html"
echo.
echo Ready! Speak your commands to your computer.
