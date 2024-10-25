@echo off
setlocal

REM Define the directory where the script is located
set "SCRIPT_DIR=%~dp0"

REM Specify the path to Python located in the same folder as the script
set "MAYA_PYTHON_PATH=%SCRIPT_DIR%mayapy.exe"

REM Check if Python exists
if not exist "%MAYA_PYTHON_PATH%" (
    echo Python not found in this folder. Please place this script next to the required mayapy.exe.
    pause
    exit /b 1
)

REM Install numpy
echo Installing numpy...
"%MAYA_PYTHON_PATH%" -m pip install numpy

echo Installation completed.
pause
