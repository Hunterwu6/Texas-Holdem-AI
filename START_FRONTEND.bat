@echo off
echo ========================================
echo  Texas Hold'em AI Battle Simulator
echo  Starting Frontend...
echo ========================================
echo.

cd frontend

echo [1/3] Checking Node.js installation...
node --version
if errorlevel 1 (
    echo ERROR: Node.js is not installed or not in PATH
    echo Please install Node.js 18+ from nodejs.org
    pause
    exit /b 1
)
echo.

echo [2/3] Installing dependencies...
echo This may take a few minutes on first run...
call npm install
if errorlevel 1 (
    echo ERROR: Failed to install dependencies
    pause
    exit /b 1
)
echo.

echo [3/3] Starting development server...
echo.
echo ========================================
echo  Frontend is starting!
echo  Opening browser automatically...
echo  URL: http://localhost:3000
echo ========================================
echo.

start http://localhost:3000
call npm run dev

pause

