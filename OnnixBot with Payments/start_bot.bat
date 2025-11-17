@echo off
echo.
echo ========================================
echo  POCKET OPTION BOT - STARTUP SCRIPT
echo ========================================
echo.

REM Check if .env exists
if not exist ".env" (
    echo ERROR: .env file not found!
    echo Please copy .env.example to .env and configure it.
    echo.
    echo Steps:
    echo 1. copy .env.example .env
    echo 2. Edit .env with your bot token
    echo 3. Run this script again
    pause
    exit /b 1
)

echo Checking environment configuration...
echo.

REM Check for bot token
findstr /C:"TELEGRAM_BOT_TOKEN" .env >nul
if %errorlevel% neq 0 (
    echo ERROR: TELEGRAM_BOT_TOKEN not found in .env
    echo Please configure your bot token in the .env file.
    pause
    exit /b 1
)

echo ✅ Environment configured
echo.
echo Starting bot...
echo.
echo ========================================
echo  BOT IS RUNNING...
echo ========================================
echo.
echo Press Ctrl+C to stop the bot
echo.

REM Start the bot
python run_bot.py

if %errorlevel% neq 0 (
    echo.
    echo ERROR: Bot failed to start
    echo.
    echo Troubleshooting:
    echo 1. Check your .env file configuration
    echo 2. Ensure all packages are installed
    echo 3. Verify your bot token is correct
    echo.
    pause
)