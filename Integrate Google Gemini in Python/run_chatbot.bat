@echo off
title AI Assistant - Enhanced GUI
cd /d "%~dp0"

echo ====================================
echo 🤖 AI Assistant - Enhanced GUI
echo ====================================
echo 🎨 Modern Dark Theme Interface
echo ✨ Enhanced User Experience
echo 🤖 Powered by Google Gemini AI
echo ====================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python is not installed or not in PATH
    echo Please install Python from https://python.org
    pause
    exit /b 1
)

echo 🔍 Checking dependencies...
python -c "import tkinter; import google.generativeai; import requests; import dotenv" >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Missing required packages. Installing...
    pip install google-generativeai requests python-dotenv
    echo.
)

echo 🚀 Starting AI Assistant...
echo 💡 Ready to help with your questions!
echo.

REM Run the chatbot
python chatbot.py

echo.
echo 👋 Thank you for using AI Assistant!
pause
