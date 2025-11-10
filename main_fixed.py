"""
Fixed Pocket Option Trading Analysis Bot for Telegram
Main bot implementation with callback query fix
"""

import os
import logging
import asyncio
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import json
import pandas as pd
from dotenv import load_dotenv
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, ContextTypes, filters
from telegram.constants import ParseMode

# Import custom modules
from technical_analysis import TechnicalAnalyzer
from risk_management import RiskManager
from market_news import MarketNews
from portfolio_tracker import PortfolioTracker

# Load environment variables
load_dotenv()

# Configure logging with proper encoding
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO,
    handlers=[
        logging.FileHandler('bot.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class PocketOptionBot:
    """Fixed bot class for Pocket Option trading analysis"""
    
    def __init__(self):
        # Configuration - Allow all users by default
        self.config = {
            'TELEGRAM_BOT_TOKEN': os.getenv('TELEGRAM_BOT_TOKEN'),
            'AUTHORIZED_USERS': [],  # Empty = allow all users
            'DEFAULT_ASSET': os.getenv('DEFAULT_ASSET', 'EURUSD'),
            'DEFAULT_TIMEFRAMES': os.getenv('DEFAULT_TIMEFRAMES', '1m,5m,15m,1h,4h,1d').split(','),
            'ANALYSIS_INTERVAL': int(os.getenv('ANALYSIS_INTERVAL', 300)),
            'RISK_LEVEL': os.getenv('RISK_LEVEL', 'MEDIUM'),
            'MAX_DAILY_SIGNALS': int(os.getenv('MAX_DAILY_SIGNALS', 50)),
            'ACCOUNT_BALANCE': float(os.getenv('ACCOUNT_BALANCE', 1000))
        }
        
        # Initialize components
        self.technical_analyzer = TechnicalAnalyzer()
        self.risk_manager = RiskManager(self.config)
        self.market_news = MarketNews()
        self.portfolio_tracker = PortfolioTracker()
        
        # Bot state
        self.user_preferences = {}
        self.analysis_cache = {}
        self.last_analysis_time = {}
        
        # Create bot application
        self.application = Application.builder().token(self.config['TELEGRAM_BOT_TOKEN']).build()
        self.setup_handlers()
    
    def setup_handlers(self):
        """Setup bot command and message handlers"""
        # Command handlers
        self.application.add_handler(CommandHandler("start", self.start_command))
        self.application.add_handler(CommandHandler("help", self.help_command))
        self.application.add_handler(CommandHandler("analyze", self.analyze_command))
        self.application.add_handler(CommandHandler("signal", self.signal_command))
        self.application.add_handler(CommandHandler("timeframes", self.timeframes_command))
        self.application.add_handler(CommandHandler("portfolio", self.portfolio_command))
        self.application.add_handler(CommandHandler("news", self.news_command))
        self.application.add_handler(CommandHandler("settings", self.settings_command))
        self.application.add_handler(CommandHandler("risk", self.risk_command))
        self.application.add_handler(CommandHandler("status", self.status_command))
        self.application.add_handler(CommandHandler("subscribe", self.subscribe_command))
        self.application.add_handler(CommandHandler("unsubscribe", self.unsubscribe_command))
        
        # Callback query handlers - Fixed to handle callback queries properly
        self.application.add_handler(CallbackQueryHandler(self.fixed_button_callback))
        
        # Message handlers
        self.application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self.handle_text))
    
    async def start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /start command"""
        user_id = update.effective_user.id
        user_name = update.effective_user.first_name or "User"
        
        welcome_text = f"""
🤖 **Pocket Option Trading Bot**

Welcome, {user_name}! 📈

🔍 **Available Commands:**
/analyze - Get market analysis
/signal - Get trading signals  
/portfolio - View your portfolio
/news - Latest market news
/risk - Risk management tools
/settings - Configure your preferences
/help - Show detailed help

**Quick Actions:**
"""
        
        keyboard = [
            [InlineKeyboardButton("📊 Analyze Market", callback_data="quick_analyze")],
            [InlineKeyboardButton("🎯 Get Signal", callback_data="quick_signal")],
            [InlineKeyboardButton("📈 Portfolio", callback_data="quick_portfolio")],
            [InlineKeyboardButton("📰 Market News", callback_data="quick_news")],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text(welcome_text, parse_mode=ParseMode.MARKDOWN, reply_markup=reply_markup)
    
    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /help command"""
        help_text = """
📚 **Bot Commands & Features**

**Core Analysis:**
• /analyze [SYMBOL] - Technical analysis
• /signal [SYMBOL] - Trading signals
• /timeframes - List available timeframes

**Portfolio & Risk:**
• /portfolio - View trade statistics
• /risk - Risk management tools
• /settings - Configure preferences

**Information:**
• /news - Latest market news
• /status - Bot status
• /subscribe - Get daily summaries

**Supported Symbols:** EURUSD, GBPUSD, USDJPY, BTCUSD, ETHUSD, etc.

⚠️ **Disclaimer:** This bot is for educational purposes only. Always do your own research before trading.
        """
        
        keyboard = [
            [InlineKeyboardButton("🔄 Refresh", callback_data="refresh_help")],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text(help_text, parse_mode=ParseMode.MARKDOWN, reply_markup=reply_markup)
    
    async def analyze_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /analyze command"""
        # For callback queries, we need to get user and send message differently
        if hasattr(update, 'callback_query') and update.callback_query:
            query = update.callback_query
            await query.answer()
            user_id = query.from_user.id
            symbol = context.args[0] if context.args else self.config['DEFAULT_ASSET']
            
            try:
                analysis_text = await self.generate_analysis_text(user_id, symbol)
                await query.edit_message_text(analysis_text, parse_mode=ParseMode.MARKDOWN)
            except Exception as e:
                await query.edit_message_text(f"❌ Error analyzing {symbol}: {str(e)}")
        else:
            # Regular command
            user_id = update.effective_user.id
            symbol = context.args[0] if context.args else self.config['DEFAULT_ASSET']
            
            try:
                analysis_text = await self.generate_analysis_text(user_id, symbol)
                keyboard = [
                    [InlineKeyboardButton("🔄 Analyze Again", callback_data=f"analyze_{symbol}")],
                    [InlineKeyboardButton("🎯 Get Signal", callback_data=f"signal_{symbol}")],
                ]
                reply_markup = InlineKeyboardMarkup(keyboard)
                
                await update.message.reply_text(analysis_text, parse_mode=ParseMode.MARKDOWN, reply_markup=reply_markup)
            except Exception as e:
                await update.message.reply_text(f"❌ Error analyzing {symbol}: {str(e)}")
    
    async def signal_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /signal command"""
        if hasattr(update, 'callback_query') and update.callback_query:
            query = update.callback_query
            await query.answer()
            user_id = query.from_user.id
            symbol = context.args[0] if context.args else self.config['DEFAULT_ASSET']
            
            try:
                signal_text = await self.generate_signal_text(user_id, symbol)
                await query.edit_message_text(signal_text, parse_mode=ParseMode.MARKDOWN)
            except Exception as e:
                await query.edit_message_text(f"❌ Error generating signal for {symbol}: {str(e)}")
        else:
            user_id = update.effective_user.id
            symbol = context.args[0] if context.args else self.config['DEFAULT_ASSET']
            
            try:
                signal_text = await self.generate_signal_text(user_id, symbol)
                keyboard = [
                    [InlineKeyboardButton("📊 Full Analysis", callback_data=f"analyze_{symbol}")],
                    [InlineKeyboardButton("🔄 New Signal", callback_data=f"signal_{symbol}")],
                ]
                reply_markup = InlineKeyboardMarkup(keyboard)
                
                await update.message.reply_text(signal_text, parse_mode=ParseMode.MARKDOWN, reply_markup=reply_markup)
            except Exception as e:
                await update.message.reply_text(f"❌ Error generating signal for {symbol}: {str(e)}")
    
    async def portfolio_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /portfolio command"""
        if hasattr(update, 'callback_query') and update.callback_query:
            query = update.callback_query
            await query.answer()
            user_id = query.from_user.id
            
            try:
                portfolio_text = await self.generate_portfolio_text(user_id)
                await query.edit_message_text(portfolio_text, parse_mode=ParseMode.MARKDOWN)
            except Exception as e:
                await query.edit_message_text(f"❌ Error accessing portfolio: {str(e)}")
        else:
            user_id = update.effective_user.id
            
            try:
                portfolio_text = await self.generate_portfolio_text(user_id)
                await update.message.reply_text(portfolio_text, parse_mode=ParseMode.MARKDOWN)
            except Exception as e:
                await update.message.reply_text(f"❌ Error accessing portfolio: {str(e)}")
    
    async def news_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /news command"""
        if hasattr(update, 'callback_query') and update.callback_query:
            query = update.callback_query
            await query.answer()
            user_id = query.from_user.id
            
            try:
                news_text = await self.generate_news_text(user_id)
                await query.edit_message_text(news_text, parse_mode=ParseMode.MARKDOWN)
            except Exception as e:
                await query.edit_message_text(f"❌ Error fetching news: {str(e)}")
        else:
            user_id = update.effective_user.id
            
            try:
                news_text = await self.generate_news_text(user_id)
                await update.message.reply_text(news_text, parse_mode=ParseMode.MARKDOWN)
            except Exception as e:
                await update.message.reply_text(f"❌ Error fetching news: {str(e)}")
    
    async def fixed_button_callback(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Fixed callback handler that properly handles callback queries"""
        query = update.callback_query
        await query.answer()
        
        data = query.data
        
        if data == "quick_analyze":
            context.args = []
            await self.analyze_command(update, context)
        elif data == "quick_signal":
            context.args = []
            await self.signal_command(update, context)
        elif data == "quick_portfolio":
            await self.portfolio_command(update, context)
        elif data == "quick_news":
            await self.news_command(update, context)
        elif data.startswith("analyze_"):
            symbol = data.replace("analyze_", "")
            context.args = [symbol]
            await self.analyze_command(update, context)
        elif data.startswith("signal_"):
            symbol = data.replace("signal_", "")
            context.args = [symbol]
            await self.signal_command(update, context)
        elif data == "refresh_help":
            await self.help_command(update, context)
        else:
            await query.edit_message_text("🔄 Feature coming soon!")
    
    async def generate_analysis_text(self, user_id: int, symbol: str) -> str:
        """Generate analysis text"""
        try:
            # Get analysis from technical analyzer
            analysis = self.technical_analyzer.get_quick_analysis(symbol)
            
            if analysis:
                text = f"""
📊 **Technical Analysis: {symbol}**

**Price:** {analysis.get('price', 'N/A')}
**Trend:** {analysis.get('trend', 'N/A')}
**RSI:** {analysis.get('rsi', 'N/A')}
**MACD:** {analysis.get('macd', 'N/A')}
**Recommendation:** {analysis.get('recommendation', 'N/A')}

*Analysis based on multiple timeframes*
                """
                return text
            else:
                return f"❌ No data available for {symbol}"
        except Exception as e:
            return f"❌ Error analyzing {symbol}: {str(e)}"
    
    async def generate_signal_text(self, user_id: int, symbol: str) -> str:
        """Generate signal text"""
        try:
            # Get signal from technical analyzer
            signal = self.technical_analyzer.get_quick_signal(symbol)
            
            if signal:
                text = f"""
🎯 **Trading Signal: {symbol}**

**Direction:** {signal.get('direction', 'N/A')}
**Confidence:** {signal.get('confidence', 'N/A')}
**Entry:** {signal.get('entry', 'N/A')}
**Stop Loss:** {signal.get('stop_loss', 'N/A')}
**Take Profit:** {signal.get('take_profit', 'N/A')}

⚠️ *For educational purposes only*
                """
                return text
            else:
                return f"❌ No signal available for {symbol}"
        except Exception as e:
            return f"❌ Error generating signal for {symbol}: {str(e)}"
    
    async def generate_portfolio_text(self, user_id: int) -> str:
        """Generate portfolio text"""
        try:
            summary = self.portfolio_tracker.get_summary()
            text = f"""
📈 **Portfolio Summary**

**Total Trades:** {summary.get('total_trades', 0)}
**Win Rate:** {summary.get('win_rate', 0):.1f}%
**Total P&L:** ${summary.get('total_pnl', 0):.2f}
**Active Trades:** {summary.get('active_trades', 0)}

*Start tracking your trades with /add_trade*
            """
            return text
        except Exception as e:
            return f"❌ Error accessing portfolio: {str(e)}"
    
    async def generate_news_text(self, user_id: int) -> str:
        """Generate news text"""
        try:
            news_items = self.market_news.get_market_sentiment()
            if news_items:
                text = "📰 **Market News**\\n\\n"
                for item in news_items[:3]:  # Show first 3 items
                    text += f"• {item}\\n"
                text += "\\n*News sentiment analysis*"
                return text
            else:
                return "📰 No recent news available"
        except Exception as e:
            return f"❌ Error fetching news: {str(e)}"
    
    # Simplified versions of other commands
    async def timeframes_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text("⏰ Available timeframes: 1m, 5m, 15m, 1h, 4h, 1d")
    
    async def settings_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text("⚙️ Settings feature coming soon!")
    
    async def risk_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text("🛡️ Risk management tools coming soon!")
    
    async def status_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text("🟢 Bot is online and running!")
    
    async def subscribe_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text("🔔 Subscription feature coming soon!")
    
    async def unsubscribe_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text("🔕 Unsubscription feature coming soon!")
    
    async def handle_text(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle text messages"""
        text = update.message.text.lower()
        if 'analyze' in text or 'analysis' in text:
            await self.analyze_command(update, context)
        elif 'signal' in text:
            await self.signal_command(update, context)
        elif 'portfolio' in text:
            await self.portfolio_command(update, context)
        elif 'news' in text:
            await self.news_command(update, context)
        else:
            await update.message.reply_text("I can help with market analysis! Try /help for commands.")
    
    def run(self):
        """Start the bot"""
        logger.info("Starting Pocket Option Trading Bot...")
        self.application.run_polling(allowed_updates=Update.ALL_TYPES)

# Main function
def main():
    """Main function to run the bot"""
    # Check if bot token is configured
    if not os.getenv('TELEGRAM_BOT_TOKEN'):
        print("❌ Error: TELEGRAM_BOT_TOKEN not found in .env file")
        print("Please create a bot using @BotFather and add the token to your .env file")
        return
    
    if os.getenv('TELEGRAM_BOT_TOKEN') == 'your_telegram_bot_token_here':
        print("❌ Error: Please configure your bot token in .env file")
        print("Replace 'your_telegram_bot_token_here' with your actual token from @BotFather")
        return
    
    # Create and run bot
    bot = PocketOptionBot()
    bot.run()

if __name__ == "__main__":
    main()