@echo off
title Texas Hold'em AI Battle Simulator
color 0A

echo.
echo ========================================
echo   TEXAS HOLD'EM AI BATTLE SIMULATOR
echo ========================================
echo.
echo   Starting your poker game...
echo.
echo   This will:
echo   1. Start the backend server
echo   2. Start the frontend UI
echo   3. Open your browser
echo.
echo ========================================
echo.

timeout /t 2 /nobreak >nul

echo [*] Starting Backend Server...
start "Backend Server" cmd /k "cd /d "%~dp0" && START_BACKEND.bat"

echo [*] Waiting for backend to initialize...
timeout /t 5 /nobreak >nul

echo [*] Starting Frontend...
start "Frontend UI" cmd /k "cd /d "%~dp0" && START_FRONTEND.bat"

echo.
echo ========================================
echo   POKER GAME IS STARTING!
echo ========================================
echo.
echo   Backend: http://localhost:8000
echo   Frontend: http://localhost:3000
echo.
echo   Two windows will open:
echo   - Backend Server (keep it running)
echo   - Frontend UI (keep it running)
echo.
echo   Your browser will open automatically!
echo ========================================
echo.
echo Press any key to close this window...
echo (Don't close the Backend and Frontend windows!)
pause >nul

