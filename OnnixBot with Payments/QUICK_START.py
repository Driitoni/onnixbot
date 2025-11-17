#!/usr/bin/env python3
"""
Quick Start Guide for Pocket Option Trading Bot
"""

def print_quick_start():
    """Print quick start guide"""
    print("=" * 80)
    print("🚀 POCKET OPTION TRADING BOT - QUICK START GUIDE")
    print("=" * 80)
    
    print("""
📋 SETUP INSTRUCTIONS:

1️⃣ CREATE TELEGRAM BOT
   • Open Telegram and search for @BotFather
   • Send /newbot command
   • Follow instructions to create your bot
   • Save the bot token

2️⃣ INSTALL REQUIREMENTS
   • Make sure you have Python 3.8+
   • Run: pip install -r requirements.txt

3️⃣ CONFIGURE ENVIRONMENT
   • Copy .env.example to .env
   • Add your bot token to .env file
   • Optionally add API keys for enhanced features

4️⃣ RUN THE BOT
   • Run: python run_bot.py
   • Or use setup script: python setup.py

🎯 QUICK COMMANDS:
   /start - Get started
   /analyze EURUSD - Analyze market
   /signal EURUSD - Get trading signal
   /help - Full documentation

📊 FEATURES INCLUDED:
   ✅ Multi-timeframe analysis (1m, 5m, 15m, 1h, 4h, 1d)
   ✅ 50+ Technical indicators
   ✅ Risk management system
   ✅ Portfolio tracking
   ✅ Market news integration
   ✅ Signal generation
   ✅ Pattern recognition
   ✅ Support/resistance levels

⚠️  IMPORTANT REMINDERS:
   • This is for EDUCATIONAL purposes only
   • NOT financial advice
   • Trading involves significant risk
   • Never risk more than you can afford to lose
   • Always do your own research

🔧 DEMO MODE:
   • Run: python demo.py
   • See bot features without Telegram setup

📖 DOCUMENTATION:
   • README.md - Complete guide
   • Setup.py - Automated setup
   • run_bot.py - Quick start script
   • demo.py - Feature demonstration

💡 NEXT STEPS:
   1. Test the demo: python demo.py
   2. Set up Telegram bot and token
   3. Configure your .env file
   4. Start the bot: python run_bot.py
   5. Start chatting with your bot!

Happy Trading! 📈
""")
    
    print("=" * 80)

if __name__ == "__main__":
    print_quick_start()