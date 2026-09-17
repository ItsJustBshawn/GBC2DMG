@echo off
setlocal
cd /d "%~dp0"
where py >nul 2>&1
if not errorlevel 1 (
    py -3 app.py %*
    if errorlevel 1 goto failed
    exit /b 0
)
where python >nul 2>&1
if not errorlevel 1 (
    python app.py %*
    if errorlevel 1 goto failed
    exit /b 0
)
echo GBC2DMG needs Python 3.11 or newer with Tk.
echo Install Python from https://www.python.org/downloads/ and try again.
pause
exit /b 1
:failed
echo.
echo GBC2DMG could not start. See the message above.
echo Check that Python 3.11 or newer and Tk are installed.
pause
exit /b 1
