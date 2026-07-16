@echo off
setlocal EnableExtensions EnableDelayedExpansion
cd /d "%~dp0"
chcp 65001 >nul
set PYTHONUTF8=1
set PYTHONIOENCODING=utf-8

fltmc >nul 2>&1
if errorlevel 1 (
    echo Administrator permission is required for the system-wide scan.
    echo Windows will ask for confirmation through UAC.
    powershell -NoProfile -ExecutionPolicy Bypass -Command "$p=Start-Process -FilePath '%ComSpec%' -ArgumentList @('/d','/c',([char]34 + '%~f0' + [char]34)) -Verb RunAs -Wait -PassThru; exit $p.ExitCode"
    exit /b !ERRORLEVEL!
)

where python >nul 2>nul
if errorlevel 1 (
    echo Python 3.14 or a compatible Python installation was not found.
    pause
    exit /b 1
)

if not exist ".venv\Scripts\python.exe" (
    echo Creating virtual environment...
    python -m venv .venv
    if errorlevel 1 (
        echo Failed to create the virtual environment.
        pause
        exit /b 1
    )
)

call ".venv\Scripts\activate.bat"
if errorlevel 1 (
    echo Failed to activate the virtual environment.
    pause
    exit /b 1
)

python -m pip install --upgrade pip
if errorlevel 1 (
    echo Failed to update pip.
    pause
    exit /b 1
)

python -m pip install -r requirements.txt
if errorlevel 1 (
    echo Failed to install dependencies.
    pause
    exit /b 1
)

python -m app
set "APP_EXIT_CODE=%ERRORLEVEL%"
if not "%APP_EXIT_CODE%"=="0" (
    echo.
    echo The application exited with code %APP_EXIT_CODE%.
    pause
)
exit /b %APP_EXIT_CODE%
