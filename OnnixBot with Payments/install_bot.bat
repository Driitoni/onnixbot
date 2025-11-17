@echo off
echo.
echo ========================================
echo  POCKET OPTION BOT - AUTO INSTALLER
echo ========================================
echo.

REM Check if we're in the right directory
if not exist "main.py" (
    echo ERROR: main.py not found!
    echo Please run this script from your bot folder.
    pause
    exit /b 1
)

echo Installing dependencies...
echo.

REM Upgrade pip first
echo [1/3] Upgrading pip...
python -m pip install --upgrade pip
if %errorlevel% neq 0 (
    echo ERROR: Failed to upgrade pip
    pause
    exit /b 1
)

REM Install requirements
echo.
echo [2/3] Installing requirements...
python -m pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo ERROR: Failed to install requirements
    echo.
    echo Trying alternative method...
    pip install --user -r requirements.txt
    if %errorlevel% neq 0 (
        echo FAILED: Manual installation required
        echo.
        echo Try: pip install --user python-telegram-bot yfinance pandas numpy ta requests python-dotenv
        pause
        exit /b 1
    )
)

echo.
echo [3/3] Testing installation...
python -c "from technical_analysis import TechnicalAnalyzer; print('✅ Technical analysis OK')" 2>nul
if %errorlevel% neq 0 echo ⚠️  Technical analysis import failed

python -c "from telegram import Update; print('✅ Telegram bot OK')" 2>nul
if %errorlevel% neq 0 echo ⚠️  Telegram import failed

echo.
echo ========================================
echo  INSTALLATION COMPLETE!
echo ========================================
echo.
echo Next steps:
echo 1. Edit .env file with your bot token
echo 2. Run: python run_bot.py
echo 3. Message your bot on Telegram
echo.
echo Type 'python run_bot.py' to start the bot now!
echo.