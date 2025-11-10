#!/usr/bin/env python3
"""
Pocket Option Trading Bot - Setup Script
This script helps you set up the trading bot quickly
"""

import os
import sys
import subprocess
import json
from pathlib import Path

def print_header():
    """Print setup header"""
    print("=" * 60)
    print("🔥 POCKET OPTION TRADING BOT SETUP")
    print("=" * 60)
    print()

def check_python_version():
    """Check if Python version is compatible"""
    print("🐍 Checking Python version...")
    if sys.version_info < (3, 8):
        print("❌ Error: Python 3.8 or higher is required")
        print(f"   Current version: {sys.version}")
        return False
    
    print(f"✅ Python {sys.version_info.major}.{sys.version_info.minor} is compatible")
    return True

def install_requirements():
    """Install required packages"""
    print("\n📦 Installing requirements...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Requirements installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error installing requirements: {e}")
        return False

def create_env_file():
    """Create .env file if it doesn't exist"""
    print("\n⚙️  Setting up environment...")
    
    if os.path.exists('.env'):
        print("✅ .env file already exists")
        return True
    
    try:
        # Copy example file
        if os.path.exists('.env.example'):
            with open('.env.example', 'r') as src:
                with open('.env', 'w') as dst:
                    dst.write(src.read())
            print("✅ Created .env file from example")
        else:
            # Create basic .env file
            env_content = """# Telegram Bot Configuration
TELEGRAM_BOT_TOKEN=your_telegram_bot_token_here
TELEGRAM_CHAT_ID=your_chat_id_here

# Bot Settings
ANALYSIS_INTERVAL=300
DEFAULT_TIMEFRAMES=1m,5m,15m,1h,4h,1d
RISK_LEVEL=MEDIUM
MAX_DAILY_SIGNALS=50
ACCOUNT_BALANCE=1000
DEFAULT_ASSET=EURUSD

# Risk Management
RISK_PERCENTAGE=2.0
MAX_POSITION_SIZE=100
MAX_DRAWDOWN_PERCENTAGE=10

# User Settings (comma-separated user IDs for authorization)
AUTHORIZED_USERS=

# API Keys (optional - leave empty if not available)
NEWS_API_KEY=
ALPHA_VANTAGE_API_KEY=
FINNHUB_API_KEY=
"""
            with open('.env', 'w') as f:
                f.write(env_content)
            print("✅ Created basic .env file")
        
        return True
    except Exception as e:
        print(f"❌ Error creating .env file: {e}")
        return False

def get_telegram_user_id():
    """Help user get their Telegram user ID"""
    print("\n👤 Getting your Telegram User ID...")
    print("To find your user ID:")
    print("1. Start a chat with @userinfobot on Telegram")
    print("2. The bot will return your user ID")
    print("3. Copy that number and paste it here when prompted")
    
    user_id = input("\nEnter your Telegram User ID (or press Enter to skip): ").strip()
    return user_id

def update_env_file(user_id=None, bot_token=None):
    """Update .env file with user inputs"""
    if not os.path.exists('.env'):
        return False
    
    try:
        # Read current .env
        with open('.env', 'r') as f:
            content = f.read()
        
        # Update user ID if provided
        if user_id:
            content = content.replace('TELEGRAM_CHAT_ID=your_chat_id_here', f'TELEGRAM_CHAT_ID={user_id}')
            print("✅ Updated Telegram Chat ID in .env")
        
        # Update bot token if provided
        if bot_token:
            content = content.replace('TELEGRAM_BOT_TOKEN=your_telegram_bot_token_here', f'TELEGRAM_BOT_TOKEN={bot_token}')
            print("✅ Updated Telegram Bot Token in .env")
        
        # Write updated content
        with open('.env', 'w') as f:
            f.write(content)
        
        return True
    except Exception as e:
        print(f"❌ Error updating .env file: {e}")
        return False

def show_telegram_setup_instructions():
    """Show instructions for setting up Telegram bot"""
    print("\n📱 TELEGRAM BOT SETUP")
    print("=" * 40)
    print("1. Open Telegram and search for @BotFather")
    print("2. Start a chat and send: /newbot")
    print("3. Follow the instructions to create your bot")
    print("4. Save the bot token provided")
    print("5. Start your bot by sending /start to it")
    print("6. Add your bot token to the .env file")
    print()

def test_setup():
    """Test if the setup is working"""
    print("\n🧪 Testing setup...")
    try:
        # Test imports
        from technical_analysis import TechnicalAnalyzer
        from risk_management import RiskManager
        from market_news import MarketNews
        from portfolio_tracker import PortfolioTracker
        print("✅ All modules imported successfully")
        
        # Test basic functionality
        analyzer = TechnicalAnalyzer()
        risk_manager = RiskManager({'RISK_PERCENTAGE': 2.0})
        news = MarketNews()
        portfolio = PortfolioTracker()
        print("✅ All components initialized successfully")
        
        return True
    except Exception as e:
        print(f"❌ Setup test failed: {e}")
        return False

def show_next_steps():
    """Show next steps for the user"""
    print("\n🚀 SETUP COMPLETE!")
    print("=" * 40)
    print("Next steps:")
    print("1. Edit the .env file with your configuration")
    print("2. Make sure your Telegram bot token is set")
    print("3. Run the bot: python main.py")
    print("4. Start chatting with your bot on Telegram")
    print()
    print("Quick start commands:")
    print("• /start - Welcome message")
    print("• /analyze EURUSD - Get market analysis")
    print("• /signal EURUSD - Get trading signal")
    print("• /help - Full documentation")
    print()
    print("📖 Check README.md for detailed instructions")
    print("⚠️  Remember: This is for educational purposes only!")
    print()

def main():
    """Main setup function"""
    print_header()
    
    # Check Python version
    if not check_python_version():
        return
    
    # Install requirements
    if not install_requirements():
        print("\n❌ Setup failed during requirements installation")
        return
    
    # Create .env file
    if not create_env_file():
        print("\n❌ Setup failed during environment setup")
        return
    
    # Show Telegram setup instructions
    show_telegram_setup_instructions()
    
    # Ask for user inputs
    bot_token = input("Enter your Telegram bot token (or press Enter to skip): ").strip()
    user_id = get_telegram_user_id()
    
    # Update .env file
    update_env_file(user_id, bot_token)
    
    # Test setup
    if test_setup():
        show_next_steps()
    else:
        print("\n❌ Setup test failed. Please check the error messages above.")
    
    print("\n✨ Setup script completed!")

if __name__ == "__main__":
    main()