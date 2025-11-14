@echo off
echo ========================================
echo  Texas Hold'em AI Battle Simulator
echo  Starting Backend Server...
echo ========================================
echo.

cd backend

echo [1/4] Checking Python installation...
python --version
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.11+ from python.org
    pause
    exit /b 1
)
echo.

echo [2/4] Testing imports...
python test_imports.py
if errorlevel 1 (
    echo ERROR: Import test failed
    echo Installing dependencies...
    pip install fastapi uvicorn pydantic pydantic-settings
    python test_imports.py
    if errorlevel 1 (
        echo ERROR: Still failing after install
        pause
        exit /b 1
    )
)
echo.

echo [3/4] Installing dependencies...
pip install -r requirements.txt
if errorlevel 1 (
    echo WARNING: Some packages may have failed to install
    echo Trying minimal installation...
    pip install fastapi uvicorn pydantic pydantic-settings
)
echo.

echo [4/4] Starting FastAPI server...
echo.
echo ========================================
echo  Backend is starting!
echo  API will be available at:
echo  http://localhost:8000
echo  API Docs: http://localhost:8000/docs
echo ========================================
echo.

python -m app.main

