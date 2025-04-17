@echo off
chcp 65001 >nul
setlocal

echo =============================================
echo  Financial Reports MCP - Modern Installer
echo =============================================
echo.
echo Choose installation method:
echo   1. Docker (recommended, easiest)
echo   2. Python Virtual Environment (venv)
echo.
set /p install_choice="Enter 1 or 2 and press Enter: "

if "%install_choice%"=="1" goto docker_install
if "%install_choice%"=="2" goto venv_install

echo Invalid choice. Exiting.
goto end

docker_install:
where docker >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo Error: Docker is not found in your PATH.
    echo Please install Docker or choose Python venv.
    goto end
)
where docker-compose >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo Error: docker-compose is not found in your PATH.
    echo Please install docker-compose or choose Python venv.
    goto end
)
echo Building Docker image...
docker-compose build
if %ERRORLEVEL% NEQ 0 (
    echo Docker build failed.
    goto end
)
echo To run the server: docker-compose up
goto end

venv_install:
where python >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo Error: Python is not found in your PATH.
    echo Please install Python and try again.
    goto end
)
python install.py
if %ERRORLEVEL% NEQ 0 (
    echo There was an error during Python venv installation.
    goto end
)
echo Installation completed!
goto end

:end
pause
