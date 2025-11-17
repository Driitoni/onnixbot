@echo off
echo ===============================================
echo  🤖 POCKET OPTION TRADING BOT
echo  📈 IMPROVED VERSION - TIMEFRAME SELECTION
echo ===============================================
echo.

echo ⚠️  STOPPING ANY RUNNING BOTS...
taskkill /f /im python.exe >nul 2>&1
timeout /t 2 >nul

echo 🚀 STARTING TIMEFRAME-ENABLED BOT...
echo.
echo 📋 New Features:
echo    ✅ Timeframe selection after clicking Get Signal
echo    ✅ Different signals for each timeframe (1m to 1d)
echo    ✅ Tailored technical analysis per timeframe
echo    ✅ Smart navigation between features
echo.
echo 🤖 Now run this command in your terminal/VS Code:
echo    python BOT_WITH_TIMEFRAME.py
echo.
echo ⏰ Workflow:
echo    1. Send /start in Telegram
echo    2. Click "Get Signal" 
echo    3. Choose timeframe (1m, 5m, 15m, 1h, 4h, 1d)
echo    4. Get your customized trading signal!
echo.
pause