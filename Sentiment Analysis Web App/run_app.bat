@echo off
echo Starting Sentiment Analysis Web Application...
echo.

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python from https://python.org
    pause
    exit /b 1
)

REM Check if virtual environment exists
if not exist "sentiment_env" (
    echo Creating virtual environment...
    python -m venv sentiment_env
    if %errorlevel% neq 0 (
        echo ERROR: Failed to create virtual environment
        pause
        exit /b 1
    )
)

REM Activate virtual environment
echo Activating virtual environment...
call sentiment_env\Scripts\activate.bat

REM Check if requirements are installed
python -c "import flask, textblob" >nul 2>&1
if %errorlevel% neq 0 (
    echo Installing requirements...
    pip install -r requirements.txt
    if %errorlevel% neq 0 (
        echo ERROR: Failed to install requirements
        pause
        exit /b 1
    )
    
    echo Downloading NLTK data...
    python -c "import nltk; nltk.download('punkt'); nltk.download('brown')"
)

REM Start the application
echo.
echo Starting Flask application...
echo Open your browser and go to: http://localhost:5000
echo Press Ctrl+C to stop the server
echo.
python app.py

pause
