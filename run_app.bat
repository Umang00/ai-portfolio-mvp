@echo off
echo 🚀 Starting AI Portfolio Assistant...
echo.

REM Kill any existing Python processes
taskkill /f /im python.exe >nul 2>&1

REM Wait a moment for ports to be released
timeout /t 2 /nobreak >nul

REM Activate virtual environment and run app
call .venv\Scripts\activate.bat
python app.py

pause
