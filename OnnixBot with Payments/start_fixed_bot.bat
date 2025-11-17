@echo off
echo.
echo ==============================================
echo  POCKET OPTION BOT - FIXED VERSION STARTER
echo ==============================================
echo.

REM Check if .env exists and has bot token
if not exist ".env" (
    echo ERROR: .env file not found!
    echo Please copy .env.example to .env and configure it.
    pause
    exit /b 1
)

echo Checking bot configuration...
echo.

REM Check for bot token
findstr /C:"TELEGRAM_BOT_TOKEN" .env >nul
if %errorlevel% neq 0 (
    echo ERROR: TELEGRAM_BOT_TOKEN not found in .env
    echo Please add your bot token from @BotFather to .env
    pause
    exit /b 1
)

REM Check if bot token is still placeholder
findstr /C:"your_telegram_bot_token_here" .env >nul
if %errorlevel% equ 0 (
    echo ERROR: Bot token is still the placeholder!
    echo Please replace 'your_telegram_bot_token_here' with your actual token.
    pause
    exit /b 1
)

echo Configuration looks good!
echo.
echo ==============================================
echo  CHOOSE TEST TYPE:
echo ==============================================
echo 1 - Simple Test Bot (recommended first)
echo 2 - Full Fixed Bot (with all features)
echo 3 - Run diagnostic tool
echo.
set /p choice="Enter your choice (1-3): "

if "%choice%"=="1" goto test_simple
if "%choice%"=="2" goto test_full
if "%choice%"=="3" goto diagnostic
echo Invalid choice
pause
exit /b 1

:test_simple
echo.
echo Starting simple test bot...
echo This will test basic Telegram connectivity.
echo Press Ctrl+C to stop.
echo.
python simple_test_bot.py
if %errorlevel% neq 0 (
    echo.
    echo ERROR: Simple bot failed to start
    echo Check your bot token and try again
    pause
)
exit /b 0

:test_full
echo.
echo Starting full fixed bot...
echo This includes all trading analysis features.
echo Press Ctrl+C to stop.
echo.
python main_fixed.py
if %errorlevel% neq 0 (
    echo.
    echo ERROR: Full bot failed to start
    echo Try the simple test first
    pause
)
exit /b 0

:diagnostic
echo.
echo Running diagnostic tool...
python bot_debug.py
if %errorlevel% neq 0 (
    echo.
    echo Diagnostic found issues - please fix them
    pause
)
exit /b 0