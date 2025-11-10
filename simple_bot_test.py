#!/usr/bin/env python3
"""
Simple test bot to verify Telegram functionality
"""

import os
import logging
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /start command"""
    await update.message.reply_text(
        "🤖 Bot is working!\n"
        "This is a simple test to verify your Telegram bot is configured correctly.\n\n"
        "If you see this, the bot is running properly!"
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /help command"""
    await update.message.reply_text(
        "📚 Help commands:\n"
        "/start - Test bot connection\n"
        "/help - Show this help\n"
        "/ping - Test bot response\n\n"
        "Your bot is working correctly! 🎉"
    )

async def ping_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /ping command"""
    await update.message.reply_text("🏓 Pong! Bot is responding perfectly!")

def main():
    """Run the simple test bot"""
    # Get bot token
    bot_token = os.getenv('TELEGRAM_BOT_TOKEN')
    
    if not bot_token:
        print("❌ Error: TELEGRAM_BOT_TOKEN not found in .env file")
        return
    
    if bot_token == 'your_telegram_bot_token_here':
        print("❌ Error: Please configure your bot token in .env file")
        return
    
    print("🤖 Starting simple test bot...")
    print("This bot will respond to: /start, /help, /ping")
    print("Press Ctrl+C to stop")
    
    # Create application
    application = Application.builder().token(bot_token).build()
    
    # Add handlers
    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("ping", ping_command))
    
    # Start polling
    application.run_polling()

if __name__ == "__main__":
    main()