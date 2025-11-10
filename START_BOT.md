# Bot Configuration Checklist

## ✅ Step-by-Step Configuration

### 1. Create Telegram Bot
- [ ] Open Telegram, search for @BotFather
- [ ] Send `/newbot` and follow instructions
- [ ] Save your bot token

### 2. Get Your Chat ID
**Option A: Use @userinfobot**
- [ ] Search for @userinfobot on Telegram
- [ ] Send any message
- [ ] Copy your User ID number

**Option B: Use find_chat_id.py script**
- [ ] Run: `python find_chat_id.py`
- [ ] Enter your bot token
- [ ] Send /start to your bot first
- [ ] Copy the Chat ID from output

### 3. Configure .env File
- [ ] Copy `.env.example` to `.env`
- [ ] Add your `TELEGRAM_BOT_TOKEN`
- [ ] Add your `TELEGRAM_CHAT_ID`
- [ ] Save the file

### 4. Install and Run
- [ ] Install dependencies: `pip install -r requirements.txt`
- [ ] Run bot: `python run_bot.py`
- [ ] Start chatting with your bot!

## 🔧 Configuration Details

**Bot Token Format:** `1234567890:ABCdefGHIjklMNOpqrsTUVwxyz`
**Chat ID Format:** `123456789` (just numbers)

**Your .env file should look like:**
```env
TELEGRAM_BOT_TOKEN=1234567890:ABCdefGHIjklMNOpqrsTUVwxyz
TELEGRAM_CHAT_ID=123456789
```

## 🚀 Testing Your Setup

1. **Start the bot** with `python run_bot.py`
2. **Open Telegram** and find your bot
3. **Send `/start`** - you should get a welcome message
4. **Try commands:**
   - `/help` - See all available commands
   - `/analyze EURUSD` - Get market analysis
   - `/signal BTCUSD` - Get trading signals

## ⚙️ Optional Enhancements

You can enhance your bot by adding these optional API keys to your .env file:
- `NEWS_API_KEY` - For market news
- `ALPHA_VANTAGE_API_KEY` - For premium market data
- `FINNHUB_API_KEY` - For enhanced technical analysis

## 🆘 Troubleshooting

**Bot not responding?**
- Check your bot token is correct
- Ensure the bot is started (check terminal for errors)
- Verify your chat ID is correct

**Getting "Unauthorized" messages?**
- Double-check your chat ID in .env
- Make sure you sent /start to your bot

**Data not updating?**
- Check your internet connection
- Market data may have delays
- Some forex pairs may not be available via yfinance

---

**Ready to start trading analysis? Your bot is configured and ready to go! 🎯**