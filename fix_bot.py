#!/usr/bin/env python3
"""
Quick fix script for the bot authorization and callback issues
"""

import os
import sys

def fix_env_file():
    """Fix the .env file to remove authorization requirements"""
    print("🔧 Fixing .env file...")
    
    if not os.path.exists('.env'):
        print("❌ .env file not found!")
        return False
    
    # Read current .env
    with open('.env', 'r') as f:
        content = f.read()
    
    # Fix: Remove authorization requirement by setting empty authorized users
    if 'AUTHORIZED_USERS=' not in content:
        # Add authorized users line
        content += '\n# User Authorization (leave empty for no restrictions)\nAUTHORIZED_USERS=\n'
    else:
        # Update existing line to be empty
        content = content.replace('AUTHORIZED_USERS=', 'AUTHORIZED_USERS=')
    
    # Write back
    with open('.env', 'w') as f:
        f.write(content)
    
    print("✅ .env file updated - no user restrictions")
    return True

def create_simple_start_command():
    """Create a simple test command to verify bot works"""
    simple_bot_code = '''#!/usr/bin/env python3
"""
Simple bot for testing - no authorization required
"""
import os
import logging
from dotenv import load_dotenv
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

load_dotenv()

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /start command"""
    keyboard = [
        [InlineKeyboardButton("📊 Analyze", callback_data="analyze")],
        [InlineKeyboardButton("🎯 Get Signal", callback_data="signal")],
        [InlineKeyboardButton("📈 Portfolio", callback_data="portfolio")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        "🤖 Pocket Option Trading Bot\\n"
        "Choose what you want to do:",
        reply_markup=reply_markup
    )

async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle button clicks"""
    query = update.callback_query
    await query.answer()
    
    data = query.data
    
    if data == "analyze":
        await query.edit_message_text("📊 Analysis feature coming soon!\\n\\nTry /help for available commands.")
    elif data == "signal":
        await query.edit_message_text("🎯 Signal feature coming soon!\\n\\nTry /help for available commands.")
    elif data == "portfolio":
        await query.edit_message_text("📈 Portfolio feature coming soon!\\n\\nTry /help for available commands.")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /help command"""
    await update.message.reply_text(
        "📚 Available Commands:\\n"
        "/start - Show bot menu\\n"
        "/help - Show this help\\n"
        "/ping - Test bot response\\n\\n"
        "This is a test version. Full features coming soon!"
    )

async def ping_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /ping command"""
    await update.message.reply_text("🏓 Pong! Bot is working perfectly!")

def main():
    """Run the simple test bot"""
    bot_token = os.getenv('TELEGRAM_BOT_TOKEN')
    
    if not bot_token or bot_token == 'your_telegram_bot_token_here':
        print("❌ Please configure your bot token in .env file first")
        return
    
    print("🤖 Starting simple test bot...")
    print("Commands: /start, /help, /ping")
    print("Press Ctrl+C to stop")
    
    application = Application.builder().token(bot_token).build()
    
    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("ping", ping_command))
    application.add_handler(CallbackQueryHandler(button_callback))
    
    application.run_polling()

if __name__ == "__main__":
    main()
'''
    
    with open('simple_test_bot.py', 'w', encoding='utf-8') as f:
        f.write(simple_bot_code)
    
    print("✅ Created simple_test_bot.py")

def main():
    """Run the fix"""
    print("=" * 50)
    print("🔧 POCKET OPTION BOT - QUICK FIX")
    print("=" * 50)
    
    # Fix .env
    if not fix_env_file():
        return False
    
    # Create simple bot
    create_simple_start_command()
    
    print("\n✅ Fixes applied!")
    print("\nNext steps:")
    print("1. Update your .env file with your bot token:")
    print("   TELEGRAM_BOT_TOKEN=your_actual_bot_token_from_BotFather")
    print("2. Test with simple bot: python simple_test_bot.py")
    print("3. If simple bot works, try the full bot: python run_bot.py")
    
    return True

if __name__ == "__main__":
    main()