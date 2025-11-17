@echo off
echo.
echo =============================================
echo  POCKET OPTION BOT - PYTHON 3.13 INSTALLER
echo =============================================
echo.

REM Check if we're in the right directory
if not exist "main.py" (
    echo ERROR: main.py not found!
    echo Please run this script from your bot folder.
    pause
    exit /b 1
)

echo Installing Python 3.13 compatible dependencies...
echo.

REM Upgrade pip first
echo [1/4] Upgrading pip...
python -m pip install --upgrade pip setuptools wheel
if %errorlevel% neq 0 (
    echo WARNING: Failed to upgrade pip, continuing...
)

REM Install core dependencies
echo.
echo [2/4] Installing core dependencies...
pip install python-telegram-bot
if %errorlevel% neq 0 (
    echo ERROR: Failed to install python-telegram-bot
    pause
    exit /b 1
)

pip install yfinance pandas numpy
if %errorlevel% neq 0 (
    echo ERROR: Failed to install pandas/numpy
    pause
    exit /b 1
)

REM Install additional dependencies
echo.
echo [3/4] Installing additional dependencies...
pip install ta requests python-dotenv aiohttp
pip install matplotlib seaborn schedule apscheduler

REM Test installation
echo.
echo [4/4] Testing installation...
python -c "import pandas; print('✅ Pandas OK:', pandas.__version__)" 2>nul
if %errorlevel% neq 0 echo ❌ Pandas failed

python -c "import telegram; print('✅ Telegram OK')" 2>nul
if %errorlevel% neq 0 echo ❌ Telegram failed

python -c "import yfinance; print('✅ YFinance OK')" 2>nul
if %errorlevel% neq 0 echo ❌ YFinance failed

python -c "import ta; print('✅ Technical Analysis OK')" 2>nul
if %errorlevel% neq 0 echo ❌ Technical Analysis failed

echo.
echo =============================================
echo  INSTALLATION COMPLETE!
echo =============================================
echo.
echo Your bot is ready to run with:
echo   python run_bot.py
echo.
echo Next steps:
echo 1. Edit .env with your bot token
echo 2. Test with: python demo.py
echo 3. Start bot: python run_bot.py
echo.
pause