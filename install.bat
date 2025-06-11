@echo off
echo Installing LoRA Auto Downloader dependencies...

cd /d "%~dp0"

:: Try to find ComfyUI's embedded Python first
set "COMFY_PYTHON="
if exist "..\..\python_embeded\python.exe" (
    set "COMFY_PYTHON=..\..\python_embeded\python.exe"
    echo Found ComfyUI embedded Python: %COMFY_PYTHON%
) else (
    echo ComfyUI embedded Python not found, trying system Python...
    python -m pip --version >nul 2>&1
    if errorlevel 1 (
        echo Error: No Python found. Please ensure ComfyUI or Python is properly installed.
        echo.
        echo For portable ComfyUI, this script should be in:
        echo ComfyUI/custom_nodes/lora_auto_downloader_package/
        pause
        exit /b 1
    )
    set "COMFY_PYTHON=python"
)

:: Install requirements
echo Installing requests library with: %COMFY_PYTHON%
%COMFY_PYTHON% -m pip install requests

if errorlevel 1 (
    echo Error: Failed to install dependencies.
    echo.
    echo Try manually running:
    echo %COMFY_PYTHON% -m pip install requests
    pause
    exit /b 1
)

echo.
echo LoRA Auto Downloader dependencies installed successfully!
echo Please restart ComfyUI to load the custom nodes.
echo.
pause
