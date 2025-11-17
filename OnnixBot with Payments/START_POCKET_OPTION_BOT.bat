@echo off
echo ===============================================
echo  🤖 POCKET OPTION REAL DATA BOT
echo  🎯 PO COMPATIBLE - CALL/PUT SIGNALS
echo ===============================================
echo.

echo ⚠️  STOPPING ANY RUNNING BOTS...
taskkill /f /im python.exe >nul 2>&1
timeout /t 2 >nul

echo 🚀 STARTING POCKET OPTION BOT...
echo.
echo 📋 PO-Specific Features:
echo    ✅ CALL/PUT signals (not BUY/SELL)
echo    ✅ PO compatible expiry times (1m-1h)
echo    ✅ Real forex market data
echo    ✅ PO platform instructions
echo    ✅ Binary options analysis
echo    ✅ Step-by-step usage guide
echo.
echo 💰 Available PO Pairs:
echo    • EUR/USD, GBP/USD, USD/JPY
echo    • AUD/USD, USD/CAD, USD/CHF
echo    • NZD/USD, EUR/GBP, EUR/JPY, GBP/JPY
echo.
echo 🤖 Run this command in your terminal/VS Code:
echo    python POCKET_OPTION_REAL_DATA_BOT.py
echo.
echo ⏰ Perfect for Pocket Option trading!
echo 🎯 Real data + PO format = Win!
echo.
pause