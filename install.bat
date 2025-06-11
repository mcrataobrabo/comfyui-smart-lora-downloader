@echo off
echo Installing LoRA Auto Downloader dependencies...

cd /d "%~dp0"

:: Check if pip is available
python -m pip --version >nul 2>&1
if errorlevel 1 (
    echo Error: pip not found. Please ensure Python and pip are installed.
    pause
    exit /b 1
)

:: Install requirements
echo Installing requests library...
python -m pip install requests

if errorlevel 1 (
    echo Error: Failed to install dependencies.
    pause
    exit /b 1
)

echo.
echo LoRA Auto Downloader dependencies installed successfully!
echo Please restart ComfyUI to load the custom nodes.
echo.
pause
