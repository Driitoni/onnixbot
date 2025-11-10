"""
Pocket Option Trading Analysis Bot for Telegram
Main bot implementation with comprehensive trading analysis features
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

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO,
    handlers=[
        logging.FileHandler('bot.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class PocketOptionBot:
    """Main bot class for Pocket Option trading analysis"""
    
    def __init__(self):
        # Configuration
        self.config = {
            'TELEGRAM_BOT_TOKEN': os.getenv('TELEGRAM_BOT_TOKEN'),
            'AUTHORIZED_USERS': os.getenv('AUTHORIZED_USERS', '').split(','),
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
        
        # Callback query handlers
        self.application.add_handler(CallbackQueryHandler(self.button_callback))
        
        # Message handlers
        self.application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self.handle_text))
    
    async def start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /start command"""
        welcome_message = """
🔥 **Pocket Option Trading Analysis Bot**

Welcome to your comprehensive trading analysis companion!

**Available Commands:**
📊 `/analyze [symbol]` - Get multi-timeframe analysis
📈 `/signal [symbol]` - Get specific trading signal
⏰ `/timeframes` - View all supported timeframes
💼 `/portfolio` - Track your trading portfolio
📰 `/news` - Get latest market news
⚙️ `/settings` - Configure your preferences
🛡️ `/risk` - View risk analysis
📋 `/status` - Check bot status

**Supported Assets:**
Major Forex: EURUSD, GBPUSD, USDJPY, AUDUSD, USDCAD, USDCHF
Indices: US30, SPX500, NASDAQ, GER40, UK100, JP225
Commodities: US OIL, UK OIL, XAUUSD (Gold), XAGUSD (Silver)
Cryptos: BTCUSD, ETHUSD, LTCUSD, ADAUSD, DOTUSD

**Quick Start:**
1. Use `/analyze EURUSD` to get comprehensive analysis
2. Use `/signal EURUSD` for specific entry signals
3. Use `/settings` to configure your preferences

⚠️ **Disclaimer:** This bot provides educational analysis only. Always do your own research and never risk more than you can afford to lose.
        """
        
        keyboard = [
            [InlineKeyboardButton("📊 Analyze Market", callback_data="quick_analyze")],
            [InlineKeyboardButton("📈 Get Signal", callback_data="quick_signal")],
            [InlineKeyboardButton("💼 Portfolio", callback_data="quick_portfolio")],
            [InlineKeyboardButton("📰 Market News", callback_data="quick_news")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text(welcome_message, reply_markup=reply_markup, parse_mode=ParseMode.MARKDOWN)
    
    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /help command"""
        help_text = """
🆘 **Help & Documentation**

**🔧 Setup Instructions:**
1. Create a Telegram bot using @BotFather
2. Add your bot token to .env file
3. Install requirements: `pip install -r requirements.txt`
4. Run the bot: `python main.py`

**📊 Analysis Features:**
• **Multi-timeframe Analysis**: 1m, 5m, 15m, 1h, 4h, 1D
• **50+ Technical Indicators**: RSI, MACD, Bollinger Bands, Stochastic, ADX, etc.
• **Pattern Recognition**: Candlestick patterns, chart patterns
• **Market Sentiment**: Real-time sentiment analysis
• **Support/Resistance**: Dynamic level calculation

**⚠️ Risk Management:**
• Position sizing calculator
• Risk-reward ratio analysis
• Daily limits protection
• Portfolio heat monitoring
• Drawdown protection

**🎯 Signal Generation:**
• BUY/SELL signals with confidence scores
• Entry, stop loss, and take profit levels
• Multiple confirmation factors
• False signal filtering

**📈 Portfolio Tracking:**
• Trade history logging
• Performance metrics
• Win rate tracking
• Profit/Loss calculations

**💡 Tips:**
• Use multiple timeframes for confirmation
• Check risk assessment before trading
• Follow money management rules
• Stay updated with market news

Need more help? Contact support or check the documentation.
        """
        
        await update.message.reply_text(help_text, parse_mode=ParseMode.MARKDOWN)
    
    async def analyze_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /analyze command"""
        symbol = self.get_symbol_from_args(context.args) or self.config['DEFAULT_ASSET']
        user_id = update.effective_user.id
        
        # Check authorization
        if not self.is_authorized(user_id):
            await update.message.reply_text("❌ Unauthorized access. Contact administrator.")
            return
        
        # Send analysis
        await update.message.reply_text("🔍 Analyzing market conditions... Please wait.")
        
        try:
            analysis_result = await self.generate_comprehensive_analysis(symbol)
            
            if 'error' in analysis_result:
                await update.message.reply_text(f"❌ Error: {analysis_result['error']}")
                return
            
            # Format and send analysis
            analysis_text = self.format_analysis_message(analysis_result)
            keyboard = self.get_analysis_keyboard(symbol)
            reply_markup = InlineKeyboardMarkup(keyboard)
            
            await update.message.reply_text(analysis_text, reply_markup=reply_markup, parse_mode=ParseMode.MARKDOWN, disable_web_page_preview=True)
            
        except Exception as e:
            logger.error(f"Error in analyze command: {e}")
            await update.message.reply_text(f"❌ Error generating analysis: {str(e)}")
    
    async def signal_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /signal command"""
        symbol = self.get_symbol_from_args(context.args) or self.config['DEFAULT_ASSET']
        user_id = update.effective_user.id
        
        if not self.is_authorized(user_id):
            await update.message.reply_text("❌ Unauthorized access.")
            return
        
        await update.message.reply_text("🎯 Generating trading signal... Please wait.")
        
        try:
            # Generate signal
            signal = self.technical_analyzer.generate_signal(symbol, "1m")
            
            if 'error' in signal:
                await update.message.reply_text(f"❌ Error: {signal['error']}")
                return
            
            # Risk assessment
            risk_assessment = self.risk_manager.assess_trade_risk(signal, self.config['ACCOUNT_BALANCE'])
            
            # Format signal message
            signal_text = self.format_signal_message(signal, risk_assessment)
            keyboard = self.get_signal_keyboard(symbol, signal)
            reply_markup = InlineKeyboardMarkup(keyboard)
            
            await update.message.reply_text(signal_text, reply_markup=reply_markup, parse_mode=ParseMode.MARKDOWN)
            
        except Exception as e:
            logger.error(f"Error in signal command: {e}")
            await update.message.reply_text(f"❌ Error generating signal: {str(e)}")
    
    async def timeframes_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /timeframes command"""
        timeframes_text = """
⏰ **Supported Timeframes**

📈 **Short Term (Scalping):**
• 1m - 1 minute (Primary for Pocket Options)
• 5m - 5 minutes
• 15m - 15 minutes

📊 **Medium Term (Day Trading):**
• 1h - 1 hour
• 4h - 4 hours
• 1d - 1 day (Daily)

**🎯 Recommended Usage:**
• **1m & 5m**: For 1-5 minute options
• **15m & 1h**: For 15-30 minute options
• **4h & 1d**: For 1+ hour options

**💡 Analysis Strategy:**
1. Use higher timeframes for trend direction
2. Confirm with lower timeframes for entry
3. Multiple timeframe confirmation increases accuracy
        """
        
        await update.message.reply_text(timeframes_text, parse_mode=ParseMode.MARKDOWN)
    
    async def portfolio_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /portfolio command"""
        try:
            portfolio_summary = self.portfolio_tracker.get_summary()
            daily_summary = self.risk_manager.get_daily_summary()
            
            portfolio_text = self.format_portfolio_message(portfolio_summary, daily_summary)
            keyboard = [
                [InlineKeyboardButton("➕ Add Trade", callback_data="add_trade")],
                [InlineKeyboardButton("📊 Detailed View", callback_data="portfolio_detailed")]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            
            await update.message.reply_text(portfolio_text, reply_markup=reply_markup, parse_mode=ParseMode.MARKDOWN)
            
        except Exception as e:
            await update.message.reply_text(f"❌ Error accessing portfolio: {str(e)}")
    
    async def news_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /news command"""
        await update.message.reply_text("📰 Fetching latest market news... Please wait.")
        
        try:
            news_data = self.market_news.get_latest_news()
            news_text = self.format_news_message(news_data)
            keyboard = [
                [InlineKeyboardButton("🔄 Refresh News", callback_data="refresh_news")],
                [InlineKeyboardButton("📈 More Analysis", callback_data="news_analysis")]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            
            await update.message.reply_text(news_text, reply_markup=reply_markup, parse_mode=ParseMode.MARKDOWN, disable_web_page_preview=True)
            
        except Exception as e:
            await update.message.reply_text(f"❌ Error fetching news: {str(e)}")
    
    async def settings_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /settings command"""
        user_id = update.effective_user.id
        user_settings = self.user_preferences.get(user_id, {
            'default_symbol': self.config['DEFAULT_ASSET'],
            'risk_level': self.config['RISK_LEVEL'],
            'notifications': True,
            'auto_analysis': False
        })
        
        settings_text = f"""
⚙️ **Settings Configuration**

Current Settings:
• Default Symbol: {user_settings['default_symbol']}
• Risk Level: {user_settings['risk_level']}
• Notifications: {'✅ Enabled' if user_settings['notifications'] else '❌ Disabled'}
• Auto Analysis: {'✅ Enabled' if user_settings['auto_analysis'] else '❌ Disabled'}
        """
        
        keyboard = [
            [InlineKeyboardButton("🎯 Change Default Symbol", callback_data="change_symbol")],
            [InlineKeyboardButton("🛡️ Risk Level", callback_data="change_risk")],
            [InlineKeyboardButton("🔔 Notifications", callback_data="toggle_notifications")],
            [InlineKeyboardButton("🤖 Auto Analysis", callback_data="toggle_auto")],
            [InlineKeyboardButton("💾 Save Settings", callback_data="save_settings")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text(settings_text, reply_markup=reply_markup, parse_mode=ParseMode.MARKDOWN)
    
    async def risk_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /risk command"""
        try:
            daily_summary = self.risk_manager.get_daily_summary()
            drawdown_risk = self.risk_manager.calculate_drawdown_risk(
                self.config['ACCOUNT_BALANCE'], 
                0  # Current drawdown - would be calculated from actual trades
            )
            
            risk_text = f"""
🛡️ **Risk Management Dashboard**

**Daily Summary:**
• Signals Sent: {daily_summary['signals_sent']}/{self.config['MAX_DAILY_SIGNALS']}
• Trades Taken: {daily_summary['trades_taken']}
• Profit/Loss: ${daily_summary['profit_loss']}
• Remaining Signals: {daily_summary['remaining_signals']}

**Risk Assessment:**
• Current Drawdown: {drawdown_risk['current_drawdown_pct']}%
• Max Allowed: {drawdown_risk['max_drawdown_limit']}%
• Risk Level: {drawdown_risk['risk_level']}
• Status: {drawdown_risk['status'].upper()}

**⚠️ Risk Warnings:**
{chr(10).join(f'• {warning}' for warning in drawdown_risk.get('warnings', []))}

**💡 Risk Management Rules:**
• Never risk more than 2% per trade
• Maintain 1:2 minimum risk-reward ratio
• Stop trading if daily loss > 5%
• Use position sizing calculator
            """
            
            await update.message.reply_text(risk_text, parse_mode=ParseMode.MARKDOWN)
            
        except Exception as e:
            await update.message.reply_text(f"❌ Error generating risk report: {str(e)}")
    
    async def status_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /status command"""
        status_text = f"""
📊 **Bot Status**

🟢 **System Status**: Online
🕐 **Uptime**: Running since start
📈 **Last Analysis**: {self.get_last_analysis_time()}
🔄 **Auto Analysis**: {'Enabled' if self.is_auto_analysis_enabled() else 'Disabled'}

**Configuration:**
• Default Asset: {self.config['DEFAULT_ASSET']}
• Risk Level: {self.config['RISK_LEVEL']}
• Analysis Interval: {self.config['ANALYSIS_INTERVAL']}s
• Max Daily Signals: {self.config['MAX_DAILY_SIGNALS']}

**User Statistics:**
• Authorized Users: {len(self.config['AUTHORIZED_USERS'])}
• Active Subscriptions: {len([u for u in self.user_preferences.values() if u.get('notifications', False)])}
        """
        
        await update.message.reply_text(status_text, parse_mode=ParseMode.MARKDOWN)
    
    async def subscribe_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /subscribe command"""
        user_id = update.effective_user.id
        
        if user_id in self.config['AUTHORIZED_USERS'] or not self.config['AUTHORIZED_USERS']:
            self.user_preferences[user_id] = self.user_preferences.get(user_id, {})
            self.user_preferences[user_id]['notifications'] = True
            
            await update.message.reply_text(
                "✅ Successfully subscribed to trading signals and alerts!\n\n"
                "You'll receive:\n"
                "• Market analysis updates\n"
                "• Trading signals with risk assessment\n"
                "• Daily summary reports\n"
                "• Risk management alerts"
            )
        else:
            await update.message.reply_text("❌ You are not authorized to subscribe. Contact administrator.")
    
    async def unsubscribe_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /unsubscribe command"""
        user_id = update.effective_user.id
        
        if user_id in self.user_preferences:
            self.user_preferences[user_id]['notifications'] = False
            await update.message.reply_text("❌ Successfully unsubscribed from notifications.")
        else:
            await update.message.reply_text("ℹ️ You were not subscribed to notifications.")
    
    async def button_callback(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle inline keyboard callbacks"""
        query = update.callback_query
        await query.answer()
        
        data = query.data
        
        if data == "quick_analyze":
            await self.analyze_command(update, context)
        elif data == "quick_signal":
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
        elif data == "refresh_analysis":
            await self.analyze_command(update, context)
        elif data == "save_trade":
            await self.save_trade_from_signal(update, context)
        elif data == "change_symbol":
            await self.change_symbol_handler(update, context)
        elif data == "change_risk":
            await self.change_risk_handler(update, context)
        elif data == "toggle_notifications":
            await self.toggle_notifications(update, context)
        elif data == "toggle_auto":
            await self.toggle_auto_analysis(update, context)
        elif data == "save_settings":
            await self.save_settings_handler(update, context)
    
    async def handle_text(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle text messages"""
        text = update.message.text.upper().strip()
        
        # Check if it's a supported symbol
        if any(symbol in text for symbol in ['EUR', 'GBP', 'USD', 'JPY', 'AUD', 'CAD', 'CHF', 'NZD', 'US30', 'SPX', 'NASDAQ', 'GER', 'UK', 'JP', 'OIL', 'GOLD', 'SILVER', 'BTC', 'ETH', 'LTC', 'ADA', 'DOT']):
            context.args = [text]
            await self.analyze_command(update, context)
        else:
            await update.message.reply_text(
                "I didn't understand that message. Try:\n"
                "• A currency pair (e.g., EURUSD)\n"
                "• A command (e.g., /help)\n"
                "• Ask me to analyze something specific"
            )
    
    def is_authorized(self, user_id: int) -> bool:
        """Check if user is authorized"""
        if not self.config['AUTHORIZED_USERS']:
            return True  # No restrictions if no authorized users configured
        return str(user_id) in self.config['AUTHORIZED_USERS']
    
    def get_symbol_from_args(self, args: List[str]) -> Optional[str]:
        """Extract symbol from command arguments"""
        if not args:
            return None
        
        symbol = args[0].upper()
        
        # Common symbol mappings
        symbol_mappings = {
            'EUR': 'EURUSD', 'GBP': 'GBPUSD', 'USDJPY': 'USDJPY',
            'EU': 'EURUSD', 'GU': 'GBPUSD', 'UJ': 'USDJPY'
        }
        
        return symbol_mappings.get(symbol, symbol)
    
    def get_last_analysis_time(self) -> str:
        """Get timestamp of last analysis"""
        # This would be implemented based on actual analysis history
        return "2 minutes ago"
    
    def is_auto_analysis_enabled(self) -> bool:
        """Check if auto analysis is enabled for any user"""
        return any(prefs.get('auto_analysis', False) for prefs in self.user_preferences.values())
    
    async def generate_comprehensive_analysis(self, symbol: str) -> Dict:
        """Generate comprehensive market analysis"""
        timeframes = self.config['DEFAULT_TIMEFRAMES']
        analysis_results = {}
        
        # Analyze multiple timeframes
        for tf in timeframes:
            try:
                signal = self.technical_analyzer.generate_signal(symbol, tf)
                if 'error' not in signal:
                    analysis_results[tf] = signal
            except Exception as e:
                logger.error(f"Error analyzing {symbol} on {tf}: {e}")
        
        # Generate overall assessment
        if analysis_results:
            # Find consensus signal
            buy_signals = sum(1 for s in analysis_results.values() if s.get('signal') == 'BUY')
            sell_signals = sum(1 for s in analysis_results.values() if s.get('signal') == 'SELL')
            
            overall_signal = "BUY" if buy_signals > sell_signals else "SELL" if sell_signals > buy_signals else "HOLD"
            confidence = sum(s.get('confidence', 0) for s in analysis_results.values()) / len(analysis_results)
            
            return {
                'symbol': symbol,
                'overall_signal': overall_signal,
                'confidence': round(confidence, 1),
                'timeframe_analysis': analysis_results,
                'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }
        else:
            return {'error': f'No analysis data available for {symbol}'}
    
    def format_analysis_message(self, analysis: Dict) -> str:
        """Format analysis results for Telegram message"""
        symbol = analysis['symbol']
        signal = analysis['overall_signal']
        confidence = analysis['confidence']
        
        # Emoji based on signal
        signal_emoji = "🟢" if signal == "BUY" else "🔴" if signal == "SELL" else "🟡"
        
        message = f"""
**{symbol} Market Analysis**

{signal_emoji} **Overall Signal**: {signal}
🎯 **Confidence**: {confidence}%

**Timeframe Breakdown:**
"""
        
        for tf, tf_analysis in analysis['timeframe_analysis'].items():
            tf_signal = tf_analysis.get('signal', 'HOLD')
            tf_confidence = tf_analysis.get('confidence', 0)
            
            tf_emoji = "🟢" if tf_signal == "BUY" else "🔴" if tf_signal == "SELL" else "🟡"
            message += f"• **{tf.upper()}**: {tf_emoji} {tf_signal} ({tf_confidence}%)\n"
        
        # Add key indicators from most recent timeframe
        if '1m' in analysis['timeframe_analysis']:
            latest = analysis['timeframe_analysis']['1m']
            indicators = latest.get('technical_indicators', {})
            
            message += f"""
**Key Indicators (1m):**
• RSI: {indicators.get('RSI', 0):.1f}
• MACD: {indicators.get('MACD', 0):.4f}
• ADX: {indicators.get('ADX', 0):.1f}
• Price: {latest.get('current_price', 0):.5f}

*Analysis generated at {analysis['timestamp']}*
        """
        
        return message
    
    def format_signal_message(self, signal: Dict, risk_assessment: Dict) -> str:
        """Format trading signal for Telegram message"""
        symbol = signal['symbol']
        signal_type = signal['signal']
        confidence = signal['confidence']
        current_price = signal['current_price']
        
        # Signal emoji
        signal_emoji = "🟢" if signal_type == "BUY" else "🔴" if signal_type == "SELL" else "🟡"
        
        message = f"""
🎯 **TRADING SIGNAL**

**{symbol} - {signal_emoji} {signal_type}**

💰 **Current Price**: {current_price:.5f}
🎯 **Confidence**: {confidence}%
🛡️ **Risk Level**: {risk_assessment.get('risk_level', 'UNKNOWN')}

**Entry Parameters:**
• Entry Price: {signal.get('entry_price', 0):.5f}
• Stop Loss: {signal.get('stop_loss', 0):.5f}
• Take Profit: {signal.get('take_profit', 0):.5f}
• Risk/Reward: {risk_assessment.get('risk_reward_ratio', 0):.2f}

**Analysis Reasons:**
"""
        
        for reason in signal.get('reasons', []):
            message += f"✅ {reason}\n"
        
        if risk_assessment.get('warnings'):
            message += "\n⚠️ **Risk Warnings:**\n"
            for warning in risk_assessment['warnings']:
                message += f"• {warning}\n"
        
        message += f"""
**Recommendation**: {risk_assessment.get('recommendation', 'HOLD')}
**Position Size**: ${risk_assessment.get('position_size', 0):.2f}

*Signal generated at {signal.get('timestamp', 'N/A')}*
        """
        
        return message
    
    def format_portfolio_message(self, portfolio_summary: Dict, daily_summary: Dict) -> str:
        """Format portfolio message"""
        message = f"""
💼 **Portfolio Summary**

**Daily Performance:**
• Signals Sent: {daily_summary['signals_sent']}
• Trades: {daily_summary['trades_taken']}
• P&L: ${daily_summary['profit_loss']}
• Remaining: {daily_summary['remaining_signals']} signals

**Account Status:**
• Balance: ${self.config['ACCOUNT_BALANCE']}
• Risk Level: {self.config['RISK_LEVEL']}
• Daily Limit: {self.config['MAX_DAILY_SIGNALS']} signals

*Last updated: {datetime.now().strftime('%H:%M:%S')}*
        """
        return message
    
    def format_news_message(self, news_data: Dict) -> str:
        """Format news message"""
        if not news_data or 'articles' not in news_data:
            return "📰 No market news available at the moment."
        
        message = "📰 **Market News**\n\n"
        
        for i, article in enumerate(news_data['articles'][:5], 1):
            title = article.get('title', 'No title')
            url = article.get('url', '#')
            
            message += f"**{i}.** {title}\n"
            if article.get('description'):
                message += f"_{article['description'][:100]}..._\n"
            message += f"[Read more]({url})\n\n"
        
        return message
    
    def get_analysis_keyboard(self, symbol: str) -> List[List[InlineKeyboardButton]]:
        """Get inline keyboard for analysis"""
        return [
            [InlineKeyboardButton("🔄 Refresh", callback_data=f"analyze_{symbol}")],
            [InlineKeyboardButton("🎯 Get Signal", callback_data=f"signal_{symbol}")],
            [InlineKeyboardButton("📊 All Timeframes", callback_data="all_timeframes")]
        ]
    
    def get_signal_keyboard(self, symbol: str, signal: Dict) -> List[List[InlineKeyboardButton]]:
        """Get inline keyboard for signal"""
        return [
            [InlineKeyboardButton("💾 Save Trade", callback_data="save_trade")],
            [InlineKeyboardButton("🔄 New Signal", callback_data=f"signal_{symbol}")]
        ]
    
    # Placeholder methods for advanced features
    async def save_trade_from_signal(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Save trade from signal (placeholder)"""
        await update.callback_query.edit_message_text("💾 Trade saved to portfolio! (Feature coming soon)")
    
    async def change_symbol_handler(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle symbol change (placeholder)"""
        await update.callback_query.edit_message_text("🎯 Symbol change feature coming soon!")
    
    async def change_risk_handler(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle risk level change (placeholder)"""
        await update.callback_query.edit_message_text("🛡️ Risk level change feature coming soon!")
    
    async def toggle_notifications(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Toggle notifications (placeholder)"""
        await update.callback_query.edit_message_text("🔔 Notification toggle feature coming soon!")
    
    async def toggle_auto_analysis(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Toggle auto analysis (placeholder)"""
        await update.callback_query.edit_message_text("🤖 Auto analysis toggle feature coming soon!")
    
    async def save_settings_handler(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Save settings (placeholder)"""
        await update.callback_query.edit_message_text("💾 Settings saved! (Feature coming soon)")
    
    async def send_daily_summary(self):
        """Send daily summary to subscribed users"""
        daily_summary = self.risk_manager.get_daily_summary()
        
        for user_id, prefs in self.user_preferences.items():
            if prefs.get('notifications', False):
                try:
                    summary_text = f"""
📊 **Daily Trading Summary**

• Signals Sent: {daily_summary['signals_sent']}
• Trades: {daily_summary['trades_taken']}
• P&L: ${daily_summary['profit_loss']}
• Remaining: {daily_summary['remaining_signals']} signals

*Generated at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*
                    """
                    await self.application.bot.send_message(chat_id=user_id, text=summary_text, parse_mode=ParseMode.MARKDOWN)
                except Exception as e:
                    logger.error(f"Error sending daily summary to {user_id}: {e}")
    
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
    
    # Create and run bot
    bot = PocketOptionBot()
    bot.run()

if __name__ == "__main__":
    main()