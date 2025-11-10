#!/usr/bin/env python3
"""
Pocket Option Trading Bot - Quick Start Script
Run this script to start the trading bot
"""

import os
import sys
import subprocess
import logging
from pathlib import Path

def check_dependencies():
    """Check if all required files exist"""
    required_files = [
        'main.py',
        'technical_analysis.py',
        'risk_management.py',
        'market_news.py',
        'portfolio_tracker.py',
        'requirements.txt',
        '.env'
    ]
    
    missing_files = []
    for file in required_files:
        if not os.path.exists(file):
            missing_files.append(file)
    
    if missing_files:
        print(f"❌ Missing required files: {', '.join(missing_files)}")
        print("Please run 'python setup.py' first to set up the bot.")
        return False
    
    return True

def check_env_config():
    """Check if .env is properly configured"""
    if not os.path.exists('.env'):
        print("❌ .env file not found. Please run 'python setup.py' first.")
        return False
    
    # Read .env file and check for bot token
    try:
        with open('.env', 'r') as f:
            content = f.read()
        
        if 'TELEGRAM_BOT_TOKEN=your_telegram_bot_token_here' in content or not content.strip():
            print("⚠️  WARNING: Bot token not configured in .env file")
            print("   The bot will not work without a valid bot token.")
            print("   Please edit the .env file and add your Telegram bot token.")
            return False
        
        return True
    except Exception as e:
        print(f"❌ Error reading .env file: {e}")
        return False

def install_missing_packages():
    """Install any missing packages"""
    try:
        print("📦 Checking and installing packages...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        return True
    except subprocess.CalledProcessError:
        print("❌ Failed to install packages. Please run: pip install -r requirements.txt")
        return False

def setup_logging():
    """Setup logging configuration"""
    logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=logging.INFO,
        handlers=[
            logging.FileHandler('bot.log'),
            logging.StreamHandler()
        ]
    )

def show_startup_info():
    """Show information about the bot startup"""
    print("=" * 60)
    print("🔥 POCKET OPTION TRADING BOT")
    print("=" * 60)
    print("📊 Features:")
    print("  • Multi-timeframe technical analysis")
    print("  • Trading signal generation")
    print("  • Risk management system")
    print("  • Portfolio tracking")
    print("  • Market news integration")
    print()
    print("🤖 Starting bot...")
    print("📋 Check 'bot.log' for detailed logs")
    print("⚠️  Remember: This is for educational purposes only!")
    print("=" * 60)

def handle_keyboard_interrupt():
    """Handle keyboard interrupt gracefully"""
    print("\n\n🛑 Bot stopped by user")
    print("Thanks for using the Pocket Option Trading Bot!")

def main():
    """Main function to start the bot"""
    try:
        # Check dependencies
        if not check_dependencies():
            sys.exit(1)
        
        # Check environment configuration
        if not check_env_config():
            print("\nTo fix this:")
            print("1. Get a bot token from @BotFather on Telegram")
            print("2. Edit the .env file and replace 'your_telegram_bot_token_here' with your token")
            print("3. Run this script again")
            sys.exit(1)
        
        # Install missing packages
        if not install_missing_packages():
            sys.exit(1)
        
        # Setup logging
        setup_logging()
        
        # Show startup information
        show_startup_info()
        
        # Import and run the bot
        from main import main as bot_main
        
        try:
            bot_main()
        except KeyboardInterrupt:
            handle_keyboard_interrupt()
        except Exception as e:
            print(f"❌ Error running bot: {e}")
            print("Check 'bot.log' for detailed error information")
            sys.exit(1)
    
    except KeyboardInterrupt:
        print("\n\n🛑 Setup interrupted by user")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()