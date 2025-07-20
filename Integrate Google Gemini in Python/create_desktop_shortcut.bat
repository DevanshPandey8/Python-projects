@echo off
REM Create Desktop Shortcut for AI Assistant GUI
REM This script creates a desktop shortcut for easy access

echo Creating desktop shortcut for AI Assistant GUI...

REM Get current directory
set "CURRENT_DIR=%~dp0"
set "SHORTCUT_PATH=%USERPROFILE%\Desktop\AI Assistant GUI.lnk"

REM Create VBScript to make shortcut
echo Set oWS = WScript.CreateObject("WScript.Shell") > "%TEMP%\CreateShortcut.vbs"
echo sLinkFile = "%SHORTCUT_PATH%" >> "%TEMP%\CreateShortcut.vbs"
echo Set oLink = oWS.CreateShortcut(sLinkFile) >> "%TEMP%\CreateShortcut.vbs"
echo oLink.TargetPath = "%CURRENT_DIR%run_chatbot.bat" >> "%TEMP%\CreateShortcut.vbs"
echo oLink.WorkingDirectory = "%CURRENT_DIR%" >> "%TEMP%\CreateShortcut.vbs"
echo oLink.Description = "AI Assistant GUI - Gemini Chatbot" >> "%TEMP%\CreateShortcut.vbs"
echo oLink.IconLocation = "%CURRENT_DIR%run_chatbot.bat,0" >> "%TEMP%\CreateShortcut.vbs"
echo oLink.Save >> "%TEMP%\CreateShortcut.vbs"

REM Execute VBScript
cscript /nologo "%TEMP%\CreateShortcut.vbs"

REM Clean up
del "%TEMP%\CreateShortcut.vbs"

echo ✅ Desktop shortcut created successfully!
echo You can now access AI Assistant GUI from your desktop.
echo.
pause
