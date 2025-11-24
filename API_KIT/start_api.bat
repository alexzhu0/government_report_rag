@echo off
chcp 65001 >nul
echo Starting Government Report RAG API Server...
echo.

echo Activating virtual environment .venv...
cd /d "%~dp0\.."
call .venv\Scripts\activate.bat
if errorlevel 1 (
    echo Failed to activate virtual environment
    pause
    exit /b 1
)

echo.
echo Starting API server on port 8000...
uvicorn API_KIT.api_server:app --host 0.0.0.0 --port 8000 --reload

pause