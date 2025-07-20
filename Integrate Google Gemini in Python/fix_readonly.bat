@echo off
REM Fix read-only file issues in VS Code
echo Fixing file permissions...

REM Remove read-only attribute from all Python files
attrib -r "*.py"

REM Grant full permissions to current user
icacls "*.py" /grant "%USERNAME%:F" /T

REM Reset VS Code workspace cache (optional)
if exist ".vscode" (
    echo Clearing VS Code cache...
    rmdir /s /q ".vscode\.cache" 2>nul
)

echo File permissions fixed!
echo You can now edit your Python files normally.
pause
