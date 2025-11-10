#!/usr/bin/env python3
"""
Bot diagnostic script to troubleshoot why commands don't work
"""

import os
import sys
import logging
from dotenv import load_dotenv

def check_env_file():
    """Check if .env file is properly configured"""
    print("🔍 Checking environment configuration...")
    print("-" * 40)
    
    if not os.path.exists('.env'):
        print("❌ .env file not found!")
        print("   Please copy .env.example to .env")
        return False
    
    # Load environment variables
    load_dotenv()
    
    bot_token = os.getenv('TELEGRAM_BOT_TOKEN')
    if not bot_token:
        print("❌ TELEGRAM_BOT_TOKEN not found in .env")
        print("   Please add your bot token from @BotFather")
        return False
    
    if bot_token == 'your_telegram_bot_token_here':
        print("❌ TELEGRAM_BOT_TOKEN is still the default placeholder")
        print("   Please replace with your actual bot token")
        return False
    
    print(f"✅ Bot token configured: {bot_token[:20]}...")
    
    chat_id = os.getenv('TELEGRAM_CHAT_ID')
    if chat_id and chat_id != 'your_chat_id_here':
        print(f"✅ Chat ID configured: {chat_id}")
    else:
        print("⚠️  Chat ID not configured (optional)")
    
    return True

def check_imports():
    """Check if all required modules can be imported"""
    print("\n📦 Checking module imports...")
    print("-" * 40)
    
    # Test standard imports
    try:
        import telegram
        print("✅ python-telegram-bot imported")
    except ImportError as e:
        print(f"❌ python-telegram-bot: {e}")
        return False
    
    try:
        import pandas as pd
        print(f"✅ pandas {pd.__version__}")
    except ImportError as e:
        print(f"❌ pandas: {e}")
        return False
    
    try:
        import yfinance
        print("✅ yfinance imported")
    except ImportError as e:
        print(f"❌ yfinance: {e}")
        return False
    
    # Test bot modules
    try:
        from technical_analysis import TechnicalAnalyzer
        print("✅ technical_analysis module")
    except ImportError as e:
        print(f"❌ technical_analysis: {e}")
        return False
    
    try:
        from risk_management import RiskManager
        print("✅ risk_management module")
    except ImportError as e:
        print(f"❌ risk_management: {e}")
        return False
    
    try:
        from market_news import MarketNews
        print("✅ market_news module")
    except ImportError as e:
        print("⚠️  market_news: (non-critical)")
    
    try:
        from portfolio_tracker import PortfolioTracker
        print("✅ portfolio_tracker module")
    except ImportError as e:
        print("⚠️  portfolio_tracker: (non-critical)")
    
    return True

def check_bot_initialization():
    """Check if bot can be initialized"""
    print("\n🤖 Checking bot initialization...")
    print("-" * 40)
    
    try:
        from main import PocketOptionBot
        print("✅ PocketOptionBot class imported")
    except ImportError as e:
        print(f"❌ PocketOptionBot: {e}")
        return False
    
    try:
        # Try to create bot instance
        bot = PocketOptionBot()
        print("✅ Bot instance created")
        
        # Check if application is set up
        if bot.application:
            print("✅ Bot application initialized")
        else:
            print("❌ Bot application not initialized")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ Bot initialization failed: {e}")
        return False

def test_telegram_connection():
    """Test connection to Telegram"""
    print("\n🌐 Testing Telegram connection...")
    print("-" * 40)
    
    load_dotenv()
    bot_token = os.getenv('TELEGRAM_BOT_TOKEN')
    
    if not bot_token:
        print("❌ No bot token to test")
        return False
    
    try:
        from telegram import Bot
        bot = Bot(token=bot_token)
        
        # Try to get bot info
        bot_info = bot.get_me()
        print(f"✅ Connected to Telegram")
        print(f"   Bot name: {bot_info.first_name}")
        print(f"   Username: @{bot_info.username}")
        print(f"   Bot ID: {bot_info.id}")
        
        return True
        
    except Exception as e:
        print(f"❌ Telegram connection failed: {e}")
        print("   This usually means:")
        print("   • Invalid bot token")
        print("   • Bot doesn't exist")
        print("   • Network connection issues")
        return False

def main():
    """Run all diagnostic tests"""
    print("=" * 60)
    print("🔍 POCKET OPTION BOT - DIAGNOSTIC TOOL")
    print("=" * 60)
    
    # Test environment
    if not check_env_file():
        print("\n❌ ENVIRONMENT CHECK FAILED")
        print("Fix .env configuration and run again")
        return False
    
    # Test imports
    if not check_imports():
        print("\n❌ IMPORT CHECK FAILED")
        print("Install missing packages: pip install -r requirements.txt")
        return False
    
    # Test bot initialization
    if not check_bot_initialization():
        print("\n❌ BOT INITIALIZATION FAILED")
        print("Check for import errors and try again")
        return False
    
    # Test Telegram connection
    if not test_telegram_connection():
        print("\n❌ TELEGRAM CONNECTION FAILED")
        print("Check your bot token and try again")
        return False
    
    print("\n" + "=" * 60)
    print("🎉 ALL DIAGNOSTIC TESTS PASSED!")
    print("=" * 60)
    print("\nYour bot should be working correctly.")
    print("If commands still don't work:")
    print("• Make sure you sent /start to your bot in Telegram")
    print("• Check the bot's terminal/console for any error messages")
    print("• Verify your bot is running (console should show 'polling' messages)")
    
    return True

if __name__ == "__main__":
    success = main()
    if not success:
        print("\n🚨 Please fix the issues above before running your bot.")
        print("Then try: python run_bot.py")
        sys.exit(1)
    else:
        print("\n🚀 Ready to start your bot!")
        print("Run: python run_bot.py")