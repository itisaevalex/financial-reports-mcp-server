@echo off
echo Installing Financial Reports MCP Server in Claude Desktop...
echo.

:: Check if Python is available
where python >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo Error: Python is not found in your PATH.
    echo Please install Python and try again.
    pause
    exit /b 1
)

:: Run the installation script
python install.py

:: Check if the installation was successful
if %ERRORLEVEL% NEQ 0 (
    echo.
    echo There was an error during installation.
    echo Please check the messages above for more information.
) else (
    echo.
    echo Installation completed!
)

pause
