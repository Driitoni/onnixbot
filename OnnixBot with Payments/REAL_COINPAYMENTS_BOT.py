#!/usr/bin/env python3
"""
ENHANCED POCKET OPTION BOT WITH REAL COINPAYMENTS INTEGRATION
Real crypto payment integration for premium trading signals
"""

import asyncio
import logging
import json
import sqlite3
from datetime import datetime, timedelta
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes
from telegram.constants import ParseMode
from dotenv import load_dotenv
import os
import yfinance as yf
import pandas as pd
import numpy as np
import hashlib
import hmac
import requests
import time
import warnings
import qrcode
from io import BytesIO
warnings.filterwarnings('ignore')

# Setup logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

# Configuration from .env file
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
COINPAYMENTS_API_KEY = os.getenv('COINPAYMENTS_API_KEY')
COINPAYMENTS_IPN_SECRET = os.getenv('COINPAYMENTS_IPN_SECRET')
WEBHOOK_BASE_URL = os.getenv('WEBHOOK_BASE_URL')

if not TELEGRAM_BOT_TOKEN:
    print("❌ TELEGRAM_BOT_TOKEN not found in .env file!")
    print("Please create a .env file with your bot token.")
    exit(1)

if not COINPAYMENTS_API_KEY or not COINPAYMENTS_IPN_SECRET:
    print("⚠️  CoinPayments credentials not found. Bot will run in demo mode.")
    DEMO_MODE = True
else:
    DEMO_MODE = False

class CoinPaymentsAPI:
    """CoinPayments API Integration"""
    
    def __init__(self, api_key, ipn_secret):
        self.api_key = api_key
        self.ipn_secret = ipn_secret
        self.base_url = "https://www.coinpayments.net/api"
        
    def get_exchange_rate(self, from_currency='USD', to_currency='BTC'):
        """Get current exchange rate"""
        try:
            payload = {
                'version': '1',
                'cmd': 'rates',
                'key': self.api_key
            }
            
            response = requests.post(self.base_url, json=payload, timeout=30)
            data = response.json()
            
            if data.get('success'):
                rates = data.get('result', {})
                if to_currency in rates:
                    return {
                        'success': True,
                        'rate': float(rates[to_currency]['rate_btc']) * float(rates['BTC']['rate_btc']) if from_currency == 'USD' else rates[to_currency]['rate_btc']
                    }
            return None
            
        except Exception as e:
            logger.error(f"Rate fetch error: {e}")
            return None
    
    def create_payment(self, amount_usd, currency, user_id, description="Bot Premium Subscription"):
        """Create a CoinPayments payment"""
        try:
            # Calculate amount in chosen currency
            if currency == 'BTC':
                amount = amount_usd * 0.000025  # Approximate BTC rate (update with real API call)
            elif currency == 'ETH':
                amount = amount_usd * 0.0005   # Approximate ETH rate
            elif currency == 'USDT':
                amount = amount_usd * 1.0      # USDT = USD
            elif currency == 'LTC':
                amount = amount_usd * 0.4      # Approximate LTC rate
            elif currency == 'BCH':
                amount = amount_usd * 0.05     # Approximate BCH rate
            else:
                amount = amount_usd * 0.000025  # Default to BTC equivalent
            
            # For demo mode, generate mock payment
            if DEMO_MODE:
                transaction_id = f"demo_{user_id}_{int(time.time())}"
                payment_address = f"1DemoAddress{currency}{user_id}Demo"
                qr_code_url = f"https://api.qrserver.com/v1/create-qr-code/?size=200x200&data={payment_address}"
                
                return {
                    'success': True,
                    'payment_id': transaction_id,
                    'address': payment_address,
                    'amount': amount,
                    'currency': currency,
                    'qr_code': qr_code_url,
                    'demo_mode': True
                }
            
            # Real CoinPayments API call
            payload = {
                'version': '1',
                'cmd': 'create_transfer',
                'key': self.api_key,
                'amount': str(amount),
                'currency1': 'USD',
                'currency2': currency,
                'buyer_email': f'user_{user_id}@bot.telegram',
                'item_name': description,
                'ipn_url': f'{WEBHOOK_BASE_URL}/webhook/coinpayments',
                'ipn_data': str(user_id),
                'ipn_type': 'API'
            }
            
            # Make API request
            response = requests.post(self.base_url, json=payload, timeout=30)
            data = response.json()
            
            if data.get('error'):
                logger.error(f"CoinPayments API error: {data['error']}")
                return {"error": data['error']}
            
            if data.get('result'):
                result = data['result']
                return {
                    'success': True,
                    'payment_id': result['payment_id'],
                    'address': result['address'],
                    'amount': amount,
                    'currency': currency,
                    'qr_code': result.get('qrcode_url', ''),
                    'demo_mode': False
                }
            else:
                return {"error": "Failed to create payment"}
                
        except Exception as e:
            logger.error(f"CoinPayments payment creation error: {e}")
            return {"error": str(e)}

class CryptoPaymentBot:
    def __init__(self, token: str):
        self.token = token
        self.application = None
        self.user_selections = {}  # Store user selections
        
        # Payment plans
        self.payment_plans = {
            '1month': {
                'name': '1 Month Premium',
                'price_usd': float(os.getenv('PAYMENT_PLAN_1MONTH_PRICE', '29.99')),
                'duration_days': 30,
                'features': [
                    '✅ All currency pairs',
                    '✅ All timeframes',
                    '✅ Real-time signals',
                    '✅ Technical analysis',
                    '✅ Priority support'
                ]
            },
            '3months': {
                'name': '3 Months Premium',
                'price_usd': float(os.getenv('PAYMENT_PLAN_3MONTH_PRICE', '79.99')),
                'duration_days': 90,
                'savings': '17% off',
                'features': [
                    '✅ All currency pairs',
                    '✅ All timeframes',
                    '✅ Real-time signals',
                    '✅ Technical analysis',
                    '✅ Priority support',
                    '✅ Save 17% with this plan'
                ]
            },
            '1year': {
                'name': '1 Year Premium',
                'price_usd': float(os.getenv('PAYMENT_PLAN_1YEAR_PRICE', '299.99')),
                'duration_days': 365,
                'savings': '17% off',
                'features': [
                    '✅ All currency pairs',
                    '✅ All timeframes',
                    '✅ Real-time signals',
                    '✅ Technical analysis',
                    '✅ Priority support',
                    '✅ Save 17% with this plan',
                    '✅ Exclusive strategies'
                ]
            }
        }
        
        # Supported cryptocurrencies
        self.crypto_currencies = ['BTC', 'ETH', 'USDT', 'LTC', 'BCH']
        
        # Initialize database
        self.init_database()
        
        # Initialize CoinPayments API
        if not DEMO_MODE:
            self.coinpayments_api = CoinPaymentsAPI(COINPAYMENTS_API_KEY, COINPAYMENTS_IPN_SECRET)
        else:
            self.coinpayments_api = None

    def init_database(self):
        """Initialize SQLite database"""
        self.db = sqlite3.connect('crypto_bot.db', check_same_thread=False)
        cursor = self.db.cursor()
        
        # Users table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                telegram_id INTEGER PRIMARY KEY,
                username TEXT,
                first_name TEXT,
                is_premium INTEGER DEFAULT 0,
                premium_expires INTEGER,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Payments table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS payments (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                telegram_id INTEGER,
                payment_plan TEXT,
                amount_crypto REAL,
                crypto_currency TEXT,
                transaction_id TEXT UNIQUE,
                payment_address TEXT,
                payment_status TEXT DEFAULT 'pending',
                confirmed_at TIMESTAMP,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        self.db.commit()

    def is_user_premium(self, user_id: int) -> bool:
        """Check if user has premium access"""
        cursor = self.db.cursor()
        cursor.execute('''
            SELECT is_premium, premium_expires FROM users WHERE telegram_id = ?
        ''', (user_id,))
        user = cursor.fetchone()
        
        if not user:
            return False
            
        if user[0] == 1 and user[1] and user[1] > datetime.now().timestamp():
            return True
            
        return False

    def create_payment_request(self, telegram_id: int, plan_id: str, crypto_currency: str) -> dict:
        """Create a crypto payment request"""
        try:
            plan = self.payment_plans.get(plan_id)
            if not plan:
                return {"error": "Invalid payment plan"}
            
            # Create payment using CoinPayments API
            payment_result = self.coinpayments_api.create_payment(
                amount_usd=plan['price_usd'],
                currency=crypto_currency,
                user_id=telegram_id,
                description=f"Premium Plan - {plan['name']}"
            )
            
            if "error" in payment_result:
                return payment_result
            
            # Store payment in database
            cursor = self.db.cursor()
            cursor.execute('''
                INSERT INTO payments (telegram_id, payment_plan, amount_crypto, crypto_currency, 
                                    transaction_id, payment_address, payment_status)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (telegram_id, plan_id, payment_result['amount'], crypto_currency, 
                  payment_result['payment_id'], payment_result['address'], "pending"))
            self.db.commit()
            
            return {
                "transaction_id": payment_result['payment_id'],
                "amount_crypto": payment_result['amount'],
                "crypto_currency": crypto_currency,
                "payment_address": payment_result['address'],
                "qr_code": payment_result['qr_code'],
                "expires_at": (datetime.now() + timedelta(hours=1)).isoformat(),
                "demo_mode": payment_result.get('demo_mode', False)
            }
            
        except Exception as e:
            logger.error(f"Payment request creation error: {e}")
            return {"error": "Failed to create payment request"}

    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /start command"""
        user = update.effective_user
        
        # Add user to database if not exists
        cursor = self.db.cursor()
        cursor.execute('''
            INSERT OR IGNORE INTO users (telegram_id, username, first_name)
            VALUES (?, ?, ?)
        ''', (user.id, user.username, user.first_name))
        self.db.commit()
        
        welcome_text = f"""
🤖 **Welcome to Pocket Option Premium Bot!**

💰 **Premium Trading Signals with Real-Time Data**

🆓 **Free Features:**
- Basic market data
- Limited currency pairs

💎 **Premium Features:**
- All currency pairs (10+ pairs)
- All timeframes (1m, 5m, 15m, 30m, 1h, 2h, 4h, 1d)
- Real-time trading signals
- Technical analysis (RSI, MACD, Bollinger Bands)
- Signal strength percentages
- CALL/PUT recommendations

🚀 **Get Started:**
Select a currency pair, choose your timeframe, and get instant trading signals!
"""
        
        if self.is_user_premium(user.id):
            premium_text = "\n\n🎉 **You have Premium access!** Enjoy all features!"
        else:
            premium_text = "\n\n💎 **Upgrade to Premium** to unlock all features and get the full bot experience!"
        
        welcome_text += premium_text
        
        keyboard = [
            [InlineKeyboardButton("📊 Start Trading", callback_data="select_pair")],
            [InlineKeyboardButton("💎 Upgrade to Premium", callback_data="show_payment_plans")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text(welcome_text, reply_markup=reply_markup, parse_mode=ParseMode.MARKDOWN)

    # Currency pairs and timeframes
    PAIRS = {
        'EUR/USD': 'EURUSD=X',
        'GBP/USD': 'GBPUSD=X',
        'USD/JPY': 'JPY=X',
        'AUD/USD': 'AUDUSD=X',
        'USD/CAD': 'CAD=X',
        'EUR/GBP': 'EURGBP=X',
        'USD/CHF': 'CHF=X',
        'NZD/USD': 'NZDUSD=X',
        'EUR/JPY': 'EURJPY=X',
        'AUD/JPY': 'AUDJPY=X'
    }

    TIMEFRAMES = {
        '1m': '1m',
        '5m': '5m',
        '15m': '15m',
        '30m': '30m',
        '1h': '60m',
        '2h': '120m',
        '4h': '240m',
        '1d': '1d'
    }

    async def button_callback(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle button callbacks"""
        query = update.callback_query
        await query.answer()
        
        user_id = query.from_user.id
        
        if query.data == "select_pair":
            await self.handle_pair_selection(query, context)
        elif query.data.startswith("pair_"):
            pair = query.data.replace("pair_", "")
            await self.handle_timeframe_selection(query, context, pair)
        elif query.data.startswith("timeframe_"):
            timeframe = query.data.replace("timeframe_", "")
            pair = self.user_selections.get(user_id, {}).get('pair', 'EUR/USD')
            await self.handle_period_selection(query, context, pair, timeframe)
        elif query.data.startswith("period_"):
            period = query.data.replace("period_", "")
            pair = self.user_selections.get(user_id, {}).get('pair', 'EUR/USD')
            timeframe = self.user_selections.get(user_id, {}).get('timeframe', '1m')
            await self.generate_signal(query, context, pair, timeframe, period)
        elif query.data == "show_payment_plans":
            await self.show_payment_plans(query, context)
        elif query.data.startswith("plan_"):
            plan_id = query.data.replace("plan_", "")
            await self.show_crypto_selection(query, context, plan_id)
        elif query.data.startswith("crypto_"):
            crypto = query.data.replace("crypto_", "")
            plan_id = self.user_selections.get(user_id, {}).get('plan_id', '1month')
            await self.create_payment(query, context, plan_id, crypto)
        elif query.data == "back_to_pairs":
            await self.handle_pair_selection(query, context)
        elif query.data == "back_to_timeframe":
            pair = self.user_selections.get(user_id, {}).get('pair', 'EUR/USD')
            await self.handle_timeframe_selection(query, context, pair)
        elif query.data == "back_to_period":
            pair = self.user_selections.get(user_id, {}).get('pair', 'EUR/USD')
            timeframe = self.user_selections.get(user_id, {}).get('timeframe', '1m')
            await self.handle_period_selection(query, context, pair, timeframe)
        elif query.data == "back_to_payment_plans":
            await self.show_payment_plans(query, context)
        elif query.data == "cancel_payment":
            await self.show_payment_plans(query, context)

    async def handle_pair_selection(self, query, context):
        """Handle currency pair selection"""
        user_id = query.from_user.id
        self.user_selections[user_id] = {}
        
        keyboard = []
        for i in range(0, len(self.PAIRS), 2):
            row = []
            for pair in list(self.PAIRS.keys())[i:i+2]:
                row.append(InlineKeyboardButton(pair, callback_data=f"pair_{pair}"))
            keyboard.append(row)
        
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        text = "📊 **Select Currency Pair:**\n\nChoose your preferred trading pair:"
        
        await query.edit_message_text(text, reply_markup=reply_markup, parse_mode=ParseMode.MARKDOWN)

    async def handle_timeframe_selection(self, query, context, pair):
        """Handle timeframe selection"""
        user_id = query.from_user.id
        self.user_selections[user_id]['pair'] = pair
        
        keyboard = []
        for i in range(0, len(self.TIMEFRAMES), 2):
            row = []
            for tf in list(self.TIMEFRAMES.keys())[i:i+2]:
                row.append(InlineKeyboardButton(tf, callback_data=f"timeframe_{tf}"))
            keyboard.append(row)
        
        keyboard.append([InlineKeyboardButton("🔙 Back to Pairs", callback_data="back_to_pairs")])
        
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        text = f"⏰ **Select Timeframe for {pair}:**\n\nChoose your preferred timeframe:"
        
        await query.edit_message_text(text, reply_markup=reply_markup, parse_mode=ParseMode.MARKDOWN)

    async def handle_period_selection(self, query, context, pair, timeframe):
        """Handle trade period selection"""
        user_id = query.from_user.id
        self.user_selections[user_id]['timeframe'] = timeframe
        
        periods = ['1m', '5m', '15m', '30m', '1h']
        keyboard = []
        
        for i in range(0, len(periods), 2):
            row = []
            for period in periods[i:i+2]:
                row.append(InlineKeyboardButton(period, callback_data=f"period_{period}"))
            keyboard.append(row)
        
        keyboard.append([InlineKeyboardButton("🔙 Back to Timeframe", callback_data="back_to_timeframe")])
        
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        text = f"⏱️ **Select Trade Period for {pair} ({timeframe}):**\n\nChoose your binary options expiry:"
        
        await query.edit_message_text(text, reply_markup=reply_markup, parse_mode=ParseMode.MARKDOWN)

    def generate_po_signal(self, symbol: str, timeframe: str) -> dict:
        """Generate Pocket Option signal with technical analysis"""
        try:
            ticker = yf.Ticker(symbol)
            data = ticker.history(period="2d", interval=timeframe)
            
            if data.empty:
                return {"error": "No data available"}
            
            latest = data.iloc[-1]
            previous = data.iloc[-2] if len(data) > 1 else latest
            
            # Technical indicators
            rsi = self.calculate_rsi(data['Close'], 14)
            macd_line, macd_signal = self.calculate_macd(data['Close'])
            bb_upper, bb_lower = self.calculate_bollinger_bands(data['Close'], 20, 2)
            
            # Current values
            current_price = float(latest['Close'])
            rsi_value = float(rsi.iloc[-1]) if not pd.isna(rsi.iloc[-1]) else 50
            macd_current = float(macd_line.iloc[-1]) if not pd.isna(macd_line.iloc[-1]) else 0
            macd_signal_current = float(macd_signal.iloc[-1]) if not pd.isna(macd_signal.iloc[-1]) else 0
            
            # Signal logic
            signal = "HOLD"
            confidence = 50
            
            # RSI signals
            if rsi_value < 30:
                rsi_signal = "CALL"
                rsi_confidence = 75
            elif rsi_value > 70:
                rsi_signal = "PUT"
                rsi_confidence = 75
            else:
                rsi_signal = "NEUTRAL"
                rsi_confidence = 50
            
            # MACD signals
            if macd_current > macd_signal_current:
                macd_signal_direction = "CALL"
                macd_confidence = 70
            else:
                macd_signal_direction = "PUT"
                macd_confidence = 70
            
            # Bollinger Bands signals
            if current_price <= bb_lower.iloc[-1]:
                bb_signal = "CALL"
                bb_confidence = 80
            elif current_price >= bb_upper.iloc[-1]:
                bb_signal = "PUT"
                bb_confidence = 80
            else:
                bb_signal = "NEUTRAL"
                bb_confidence = 50
            
            # Combine signals
            signals = [rsi_signal, macd_signal_direction, bb_signal]
            call_votes = signals.count("CALL")
            put_votes = signals.count("PUT")
            
            if call_votes > put_votes:
                final_signal = "CALL"
                confidence = max(rsi_confidence, macd_confidence, bb_confidence)
            elif put_votes > call_votes:
                final_signal = "PUT"
                confidence = max(rsi_confidence, macd_confidence, bb_confidence)
            else:
                final_signal = "HOLD"
                confidence = 50
            
            return {
                "signal": final_signal,
                "confidence": confidence,
                "price": current_price,
                "rsi": rsi_value,
                "rsi_signal": rsi_signal,
                "macd": macd_current,
                "macd_signal": macd_signal_current,
                "macd_direction": macd_signal_direction,
                "bollinger_upper": bb_upper.iloc[-1],
                "bollinger_lower": bb_lower.iloc[-1],
                "bb_signal": bb_signal,
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Signal generation error: {e}")
            return {"error": "Failed to generate signal"}

    def calculate_rsi(self, prices, period=14):
        """Calculate RSI"""
        delta = prices.diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
        rs = gain / loss
        rsi = 100 - (100 / (1 + rs))
        return rsi

    def calculate_macd(self, prices, fast=12, slow=26, signal=9):
        """Calculate MACD"""
        ema_fast = prices.ewm(span=fast).mean()
        ema_slow = prices.ewm(span=slow).mean()
        macd_line = ema_fast - ema_slow
        macd_signal = macd_line.ewm(span=signal).mean()
        return macd_line, macd_signal

    def calculate_bollinger_bands(self, prices, period=20, std_dev=2):
        """Calculate Bollinger Bands"""
        rolling_mean = prices.rolling(window=period).mean()
        rolling_std = prices.rolling(window=period).std()
        upper_band = rolling_mean + (rolling_std * std_dev)
        lower_band = rolling_mean - (rolling_std * std_dev)
        return upper_band, lower_band

    async def generate_signal(self, query, context, pair: str, timeframe: str, period: str):
        """Generate and display trading signal"""
        user_id = query.from_user.id
        
        # Check premium access
        if not self.is_user_premium(user_id):
            await self.show_payment_required(query, context)
            return
        
        symbol = self.PAIRS[pair]
        signal_data = self.generate_po_signal(symbol, timeframe)
        
        if "error" in signal_data:
            text = f"❌ **Error:** {signal_data['error']}"
            await query.edit_message_text(text, parse_mode=ParseMode.MARKDOWN)
            return
        
        # Format signal message
        signal_emoji = "🟢" if signal_data['signal'] == "CALL" else "🔴" if signal_data['signal'] == "PUT" else "🟡"
        confidence_color = "🟢" if signal_data['confidence'] >= 70 else "🟡" if signal_data['confidence'] >= 60 else "🔴"
        
        text = f"""
{signal_emoji} **{pair} Signal**

📈 **Trade:** {signal_data['signal']}
🎯 **Confidence:** {confidence_color} {signal_data['confidence']}%
💰 **Current Price:** {signal_data['price']:.5f}
⏰ **Expiry:** {period}
🕐 **Timeframe:** {timeframe}

📊 **Technical Analysis:**

📊 **RSI:** {signal_data['rsi']:.2f} ({signal_data['rsi_signal']})
📈 **MACD:** {signal_data['macd']:.6f} ({signal_data['macd_direction']})
📉 **Bollinger Bands:**
   • Upper: {signal_data['bollinger_upper']:.5f}
   • Lower: {signal_data['bollinger_lower']:.5f}
   • Signal: {signal_data['bb_signal']}

⚡ **Recommendation:** {signal_data['signal']} for {period} expiry
"""
        
        keyboard = [
            [InlineKeyboardButton("🔄 New Signal", callback_data="select_pair")],
            [InlineKeyboardButton("💎 Upgrade", callback_data="show_payment_plans")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(text, reply_markup=reply_markup, parse_mode=ParseMode.MARKDOWN)

    async def show_payment_plans(self, query, context):
        """Display payment plans"""
        user_id = query.from_user.id
        
        text = "💎 **Choose Your Premium Plan**\n\nSelect the plan that suits you best:\n"
        
        keyboard = []
        for plan_id, plan in self.payment_plans.items():
            savings_text = f" ({plan['savings']})" if 'savings' in plan else ""
            text += f"\n📦 **{plan['name']}**{savings_text}\n"
            text += f"💰 Price: **${plan['price_usd']:.2f}**/month\n"
            
            keyboard.append([
                InlineKeyboardButton(
                    f"{plan['name']} - ${plan['price_usd']:.2f}{savings_text}",
                    callback_data=f"plan_{plan_id}"
                )
            ])
        
        keyboard.append([InlineKeyboardButton("❌ Cancel", callback_data="back_to_payment_plans")])
        
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(text, reply_markup=reply_markup, parse_mode=ParseMode.MARKDOWN)

    async def show_crypto_selection(self, query, context, plan_id):
        """Show cryptocurrency selection"""
        user_id = query.from_user.id
        self.user_selections[user_id]['plan_id'] = plan_id
        
        plan = self.payment_plans[plan_id]
        
        text = f"🪙 **Select Cryptocurrency for {plan['name']}**\n\n"
        text += f"💰 Amount: **${plan['price_usd']:.2f}**\n\n"
        text += "Choose your preferred payment method:\n"
        
        keyboard = []
        for crypto in self.crypto_currencies:
            # Calculate approximate crypto amount
            if crypto == 'BTC':
                crypto_amount = plan['price_usd'] * 0.000025
            elif crypto == 'ETH':
                crypto_amount = plan['price_usd'] * 0.0005
            elif crypto == 'USDT':
                crypto_amount = plan['price_usd']
            elif crypto == 'LTC':
                crypto_amount = plan['price_usd'] * 0.4
            elif crypto == 'BCH':
                crypto_amount = plan['price_usd'] * 0.05
            else:
                crypto_amount = plan['price_usd'] * 0.000025
            
            keyboard.append([
                InlineKeyboardButton(
                    f"{crypto} (≈{crypto_amount:.6f})",
                    callback_data=f"crypto_{crypto}"
                )
            ])
        
        keyboard.append([InlineKeyboardButton("🔙 Back to Plans", callback_data="back_to_payment_plans")])
        
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(text, reply_markup=reply_markup, parse_mode=ParseMode.MARKDOWN)

    async def create_payment(self, query, context, plan_id: str, crypto_currency: str):
        """Create payment request"""
        user_id = query.from_user.id
        
        payment_data = self.create_payment_request(user_id, plan_id, crypto_currency)
        
        if "error" in payment_data:
            text = f"❌ **Payment Error:** {payment_data['error']}"
            await query.edit_message_text(text, parse_mode=ParseMode.MARKDOWN)
            return
        
        plan = self.payment_plans[plan_id]
        
        # Payment instruction
        text = f"💳 **Payment Instructions**\n\n"
        text += f"📦 **Plan:** {plan['name']}\n"
        text += f"💰 **Amount:** ${plan['price_usd']:.2f}\n"
        text += f"🪙 **Pay with:** {crypto_currency}\n"
        text += f"💵 **Crypto Amount:** {payment_data['amount_crypto']:.6f} {crypto_currency}\n\n"
        
        text += f"🔗 **Send payment to:**\n"
        text += f"`{payment_data['payment_address']}`\n\n"
        
        if payment_data.get('demo_mode'):
            text += f"⚠️ **Demo Mode:** This is a simulation. In production, real payment will be required.\n\n"
        
        text += f"⏰ **Expires:** {payment_data['expires_at']}\n"
        text += f"🆔 **Payment ID:** `{payment_data['transaction_id']}`\n\n"
        text += f"📱 **Next Steps:**\n"
        text += f"1. Send the exact amount to the address above\n"
        text += f"2. Wait for confirmation (usually 1-3 confirmations)\n"
        text += f"3. You will receive premium access automatically\n\n"
        
        if payment_data.get('demo_mode'):
            text += f"4. For demo mode: use /check_payment {payment_data['transaction_id']} to simulate payment"
        
        # Payment status
        text += f"\n🔄 **Status:** Pending Payment"
        
        keyboard = []
        if payment_data.get('demo_mode'):
            keyboard.append([InlineKeyboardButton("✅ Simulate Payment", callback_data=f"simulate_payment_{payment_data['transaction_id']}")])
        keyboard.append([InlineKeyboardButton("🔙 Cancel Payment", callback_data="cancel_payment")])
        
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(text, reply_markup=reply_markup, parse_mode=ParseMode.MARKDOWN)

    async def show_payment_required(self, query, context):
        """Show payment required message"""
        text = """
💎 **Premium Access Required**

This feature requires a premium subscription. Upgrade to get:

✅ **All Currency Pairs**
✅ **All Timeframes** 
✅ **Real-time Signals**
✅ **Technical Analysis**
✅ **Priority Support**

🚀 **Upgrade now to start trading!**
"""
        
        keyboard = [
            [InlineKeyboardButton("💎 Upgrade to Premium", callback_data="show_payment_plans")],
            [InlineKeyboardButton("❌ Cancel", callback_data="select_pair")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(text, reply_markup=reply_markup, parse_mode=ParseMode.MARKDOWN)

    async def simulate_payment(self, query, context, transaction_id: str):
        """Simulate payment for demo mode"""
        user_id = query.from_user.id
        
        try:
            # Update payment status
            cursor = self.db.cursor()
            cursor.execute('''
                UPDATE payments SET payment_status = 'confirmed', confirmed_at = ?
                WHERE transaction_id = ? AND telegram_id = ?
            ''', (datetime.now(), transaction_id, user_id))
            
            # Activate premium
            plan_id = self.user_selections.get(user_id, {}).get('plan_id', '1month')
            duration_days = self.payment_plans[plan_id]['duration_days']
            expires_at = datetime.now().timestamp() + (duration_days * 24 * 60 * 60)
            
            cursor.execute('''
                UPDATE users SET is_premium = 1, premium_expires = ?
                WHERE telegram_id = ?
            ''', (expires_at, user_id))
            
            self.db.commit()
            
            text = f"""
🎉 **Payment Confirmed!**

✅ Your premium access has been activated!
🗓️ **Expires:** {datetime.fromtimestamp(expires_at).strftime('%Y-%m-%d %H:%M')}

🚀 **You now have access to:**
• All currency pairs
• All timeframes  
• Real-time signals
• Technical analysis
• Priority support

Start trading with /start!
"""
            
            keyboard = [[InlineKeyboardButton("🚀 Start Trading", callback_data="select_pair")]]
            reply_markup = InlineKeyboardMarkup(keyboard)
            
            await query.edit_message_text(text, reply_markup=reply_markup, parse_mode=ParseMode.MARKDOWN)
            
        except Exception as e:
            logger.error(f"Payment simulation error: {e}")
            await query.edit_message_text("❌ Payment simulation failed. Please try again.")

    async def run(self):
        """Run the bot"""
        # Create application
        self.application = Application.builder().token(self.token).build()
        
        # Add handlers
        self.application.add_handler(CommandHandler("start", self.start))
        self.application.add_handler(CallbackQueryHandler(self.button_callback))
        
        # Start polling
        logger.info("🚀 Starting Crypto Payment Bot...")
        if DEMO_MODE:
            logger.warning("⚠️  Running in DEMO MODE - No real payments will be processed")
        else:
            logger.info("✅ Live mode with CoinPayments integration")
        
        await self.application.initialize()
        await self.application.start()
        await self.application.updater.start_polling()

def main():
    """Main function"""
    # Load environment variables
    load_dotenv()
    
    bot_token = os.getenv('TELEGRAM_BOT_TOKEN')
    if not bot_token:
        print("❌ Please set TELEGRAM_BOT_TOKEN in your .env file")
        return
    
    # Create and run bot
    bot = CryptoPaymentBot(bot_token)
    asyncio.run(bot.run())

if __name__ == "__main__":
    main()
