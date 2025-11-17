# 🔧 Bot Commands Not Working - Complete Fix

## 🚨 Most Common Issues:

### 1. **Bot Token Not Configured** (Most Common)
**Problem:** `TELEGRAM_BOT_TOKEN` is empty or invalid
**Solution:** 
- Check your `.env` file
- Make sure you copied your bot token from @BotFather
- Bot token should look like: `1234567890:ABCdefGHIjklMNOpqrsTUVwxyz`

### 2. **Import Errors**
**Problem:** Required modules missing
**Solution:** 
```bash
pip install python-telegram-bot yfinance pandas numpy ta requests python-dotenv
```

### 3. **Bot Not Connected to Telegram**
**Problem:** Application failed to initialize
**Solution:** Run diagnostic tool

### 4. **Wrong Directory**
**Problem:** Running bot from wrong folder
**Solution:** Make sure all files (main.py, technical_analysis.py, etc.) are in the same directory

## 🩺 **DIAGNOSTIC COMMANDS:**

### Run the diagnostic tool:
```bash
python bot_debug.py
```

### Run simple test bot:
```bash
python simple_bot_test.py
```

### Test basic imports:
```bash
python -c "import telegram; print('✅ Telegram OK')"
python -c "from main import PocketOptionBot; print('✅ Bot OK')"
```

## 🛠️ **FIXING STEPS:**

### Step 1: Check .env File
```bash
# Make sure your .env contains:
TELEGRAM_BOT_TOKEN=1234567890:your_actual_bot_token_here
```

### Step 2: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 3: Test Simple Bot First
```bash
# Test with simple bot first:
python simple_bot_test.py
```

### Step 4: Test Full Bot
```bash
# If simple bot works, test full bot:
python run_bot.py
```

## 🎯 **Expected Behavior:**

**✅ Working Bot:**
- Terminal shows: "Starting bot..." and "INFO: Application started"
- Commands like `/start` work in Telegram
- Bot responds immediately

**❌ Broken Bot:**
- Terminal shows errors
- Commands don't respond
- Bot appears "stuck" or "offline"

## 📱 **What Should Happen:**

1. **Start bot** → Terminal shows: `Starting bot...`
2. **Message bot** → Send `/start` in Telegram
3. **Get response** → Bot replies with welcome message
4. **All commands work** → `/help`, `/ping`, etc.

## 🚀 **Quick Fix Commands:**
```bash
# If you have issues, run these in order:
1. python bot_debug.py           # Diagnose issues
2. python simple_bot_test.py     # Test basic functionality
3. python run_bot.py            # Start full bot
```

## 💡 **Pro Tips:**
- **Check terminal output** for error messages
- **Make sure bot token is correct** from @BotFather
- **Try simple bot first** to isolate issues
- **Keep terminal open** while testing
- **Restart bot** if you make changes to .env

## 🔄 **If Still Not Working:**

1. **Delete and recreate bot** with @BotFather
2. **Use new bot token** in .env
3. **Test with simple bot** again
4. **Check firewall/antivirus** not blocking connection

---
**The diagnostic tool will tell you exactly what's wrong!** 🕵️‍♂️