@echo off
chcp 65001 > nul
setlocal enabledelayedexpansion

:: Set colors for better visibility
color 0A

:: Set title
title Shakespeare Database Access Fixer

:: Get the directory where the batch file is located
set "SCRIPT_DIR=%~dp0"
set "SCRIPT_DIR=%SCRIPT_DIR:~0,-1%"

:: Create necessary directories
if not exist "%SCRIPT_DIR%\logs" mkdir "%SCRIPT_DIR%\logs"
if not exist "%SCRIPT_DIR%\backup" mkdir "%SCRIPT_DIR%\backup"

echo ================================
echo Shakespeare Database Access Fixer
echo ================================
echo.

:: Check Python installation
echo Checking Python installation...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    color 0C
    echo [ERROR] Python is not installed or not in PATH
    echo Please install Python 3.x and try again
    pause
    exit /b 1
)

:: Set up platform-tools
set "PLATFORM_TOOLS=%SCRIPT_DIR%\platform-tools"
set "ADB=%PLATFORM_TOOLS%\adb.exe"

:: Verify platform-tools
if not exist "%PLATFORM_TOOLS%" (
    echo Installing Android Platform Tools...
    
    :: Create temp directory
    set "TEMP_DIR=%SCRIPT_DIR%\temp"
    mkdir "%TEMP_DIR%" 2>nul
    
    :: Download platform-tools
    powershell -Command "& {$ProgressPreference = 'SilentlyContinue'; Invoke-WebRequest -Uri 'https://dl.google.com/android/repository/platform-tools-latest-windows.zip' -OutFile '%TEMP_DIR%\platform-tools.zip'}"
    
    :: Extract platform-tools
    powershell -Command "& {Add-Type -AssemblyName System.IO.Compression.FileSystem; [System.IO.Compression.ZipFile]::ExtractToDirectory('%TEMP_DIR%\platform-tools.zip', '%SCRIPT_DIR%')}"
    
    :: Clean up
    rmdir /s /q "%TEMP_DIR%" 2>nul
)

:: Add platform-tools to PATH
set "PATH=%PLATFORM_TOOLS%;%PATH%"

:MENU
cls
echo ================================
echo Shakespeare Database Access Fixer
echo ================================
echo.
echo 1. Run Full Fix
echo 2. Check Device Connection
echo 3. Fix Permissions
echo 4. Verify Database Access
echo 5. Create Backup
echo 6. Exit
echo.
set /p choice="Enter your choice (1-6): "

if "%choice%"=="1" goto FULL_FIX
if "%choice%"=="2" goto CHECK_DEVICE
if "%choice%"=="3" goto FIX_PERMISSIONS
if "%choice%"=="4" goto VERIFY_DATABASE
if "%choice%"=="5" goto CREATE_BACKUP
if "%choice%"=="6" goto EOF

echo Invalid choice. Please try again.
timeout /t 2 >nul
goto MENU

:CHECK_DEVICE
echo.
echo Checking device connection...
echo.

:: Kill existing ADB server
"%ADB%" kill-server >nul 2>&1
timeout /t 2 >nul

:: Start ADB server
"%ADB%" start-server >nul 2>&1
timeout /t 2 >nul

:: Check for devices
"%ADB%" devices > "%TEMP%\adb_devices.txt"
type "%TEMP%\adb_devices.txt"
echo.

:: Check if device is connected
findstr "device" "%TEMP%\adb_devices.txt" >nul
if %errorlevel% equ 0 (
    echo Device found and connected successfully.
) else (
    echo No device found or not authorized.
    echo.
    echo Please ensure:
    echo 1. Your device is connected via USB
    echo 2. USB debugging is enabled
    echo 3. You have accepted the USB debugging prompt on your device
)

echo.
pause
goto MENU

:FULL_FIX
echo Running full fix...
python fix_database_access.py "%ADB%" --full-fix
pause
goto MENU

:FIX_PERMISSIONS
echo Fixing permissions...
python fix_database_access.py "%ADB%" --fix-permissions
pause
goto MENU

:VERIFY_DATABASE
echo Verifying database access...
python fix_database_access.py "%ADB%" --verify
pause
goto MENU

:CREATE_BACKUP
echo Creating backup...
python fix_database_access.py "%ADB%" --backup
pause
goto MENU

:EOF
echo.
echo Cleaning up...
"%ADB%" kill-server >nul 2>&1
echo Done.
echo.
pause
exit /b 0
