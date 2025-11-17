"""
Technical Analysis Module for Pocket Option Trading Bot
Provides comprehensive technical analysis across multiple timeframes
"""

import pandas as pd
import numpy as np
import yfinance as yf
import ta
from typing import Dict, List, Tuple, Optional
import logging
from datetime import datetime, timedelta
import asyncio
import aiohttp
import warnings
warnings.filterwarnings('ignore')

class TechnicalAnalyzer:
    """Advanced technical analysis engine for trading signals"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        
    def get_historical_data(self, symbol: str, period: str = "1d", interval: str = "1m") -> pd.DataFrame:
        """Fetch historical price data using yfinance"""
        try:
            ticker = yf.Ticker(symbol)
            data = ticker.history(period=period, interval=interval)
            if data.empty:
                raise ValueError(f"No data found for {symbol}")
            return data
        except Exception as e:
            self.logger.error(f"Error fetching data for {symbol}: {e}")
            return pd.DataFrame()
    
    def calculate_indicators(self, data: pd.DataFrame) -> pd.DataFrame:
        """Calculate all technical indicators"""
        if data.empty:
            return data
            
        df = data.copy()
        
        # Moving Averages
        df['MA10'] = ta.trend.sma_indicator(df['Close'], window=10)
        df['MA20'] = ta.trend.sma_indicator(df['Close'], window=20)
        df['MA50'] = ta.trend.sma_indicator(df['Close'], window=50)
        df['MA200'] = ta.trend.sma_indicator(df['Close'], window=200)
        df['EMA12'] = ta.trend.ema_indicator(df['Close'], window=12)
        df['EMA26'] = ta.trend.ema_indicator(df['Close'], window=26)
        
        # RSI
        df['RSI'] = ta.momentum.RSIIndicator(df['Close'], window=14).rsi()
        
        # MACD
        macd = ta.trend.MACD(df['Close'])
        df['MACD'] = macd.macd()
        df['MACD_Signal'] = macd.macd_signal()
        df['MACD_Histogram'] = macd.macd_diff()
        
        # Bollinger Bands
        bb = ta.volatility.BollingerBands(df['Close'], window=20, window_dev=2)
        df['BB_Upper'] = bb.bollinger_hband()
        df['BB_Lower'] = bb.bollinger_lband()
        df['BB_Middle'] = bb.bollinger_mavg()
        df['BB_Width'] = bb.bollinger_wband()
        
        # Stochastic
        stoch = ta.momentum.StochasticOscillator(df['High'], df['Low'], df['Close'])
        df['Stoch_K'] = stoch.stoch()
        df['Stoch_D'] = stoch.stoch_signal()
        
        # ADX (Average Directional Index)
        df['ADX'] = ta.trend.ADXIndicator(df['High'], df['Low'], df['Close']).adx()
        
        # Williams %R
        df['Williams_R'] = ta.momentum.WilliamsRIndicator(df['High'], df['Low'], df['Close']).willr()
        
        # CCI (Commodity Channel Index)
        df['CCI'] = ta.trend.CCIIndicator(df['High'], df['Low'], df['Close']).cci()
        
        # ATR (Average True Range)
        df['ATR'] = ta.volatility.AverageTrueRange(df['High'], df['Low'], df['Close']).average_true_range()
        
        # Volume indicators
        df['Volume_SMA'] = ta.volume.volume_sma(df['Close'], df['Volume'])
        df['OBV'] = ta.volume.on_balance_volume(df['Close'], df['Volume'])
        
        # Support and Resistance
        df = self.calculate_support_resistance(df)
        
        return df
    
    def calculate_support_resistance(self, data: pd.DataFrame, window: int = 20) -> pd.DataFrame:
        """Calculate support and resistance levels"""
        df = data.copy()
        highs = df['High'].rolling(window=window, center=True).max()
        lows = df['Low'].rolling(window=window, center=True).min()
        
        df['Resistance'] = highs
        df['Support'] = lows
        
        return df
    
    def detect_candlestick_patterns(self, data: pd.DataFrame) -> Dict:
        """Detect candlestick patterns"""
        if len(data) < 2:
            return {}
            
        latest = data.iloc[-1]
        prev = data.iloc[-2]
        
        patterns = {}
        body = abs(latest['Close'] - latest['Open'])
        upper_shadow = latest['High'] - max(latest['Open'], latest['Close'])
        lower_shadow = min(latest['Open'], latest['Close']) - latest['Low']
        
        # Doji
        if body <= (latest['High'] - latest['Low']) * 0.1:
            patterns['doji'] = True
        
        # Hammer
        if (lower_shadow >= 2 * body) and (upper_shadow <= body):
            patterns['hammer'] = True
        
        # Shooting Star
        if (upper_shadow >= 2 * body) and (lower_shadow <= body):
            patterns['shooting_star'] = True
        
        # Engulfing patterns
        if latest['Close'] > latest['Open']:  # Bullish candle
            if prev['Close'] < prev['Open']:  # Previous was bearish
                if latest['Open'] < prev['Close'] and latest['Close'] > prev['Open']:
                    patterns['bullish_engulfing'] = True
        else:  # Bearish candle
            if prev['Close'] > prev['Open']:  # Previous was bullish
                if latest['Open'] > prev['Close'] and latest['Close'] < prev['Open']:
                    patterns['bearish_engulfing'] = True
        
        # Morning/Evening Star (simplified)
        if len(data) >= 3:
            first = data.iloc[-3]
            second = data.iloc[-2]
            
            # Morning Star
            if (first['Close'] < first['Open'] and  # First day bearish
                abs(second['Open'] - second['Close']) < body * 0.5 and  # Second day small
                latest['Close'] > latest['Open'] and  # Third day bullish
                latest['Close'] > (first['Open'] + first['Close']) / 2):
                patterns['morning_star'] = True
            
            # Evening Star
            if (first['Close'] > first['Open'] and  # First day bullish
                abs(second['Open'] - second['Close']) < body * 0.5 and  # Second day small
                latest['Close'] < latest['Open'] and  # Third day bearish
                latest['Close'] < (first['Open'] + first['Close']) / 2):
                patterns['evening_star'] = True
        
        return patterns
    
    def generate_trend_analysis(self, data: pd.DataFrame) -> Dict:
        """Generate trend analysis based on multiple timeframes"""
        if data.empty:
            return {}
        
        latest = data.iloc[-1]
        analysis = {
            'trend': 'SIDEWAYS',
            'strength': 'WEAK',
            'direction': 'NEUTRAL'
        }
        
        # Trend analysis using moving averages
        if latest['Close'] > latest['MA20'] > latest['MA50']:
            analysis['trend'] = 'BULLISH'
            analysis['direction'] = 'UP'
        elif latest['Close'] < latest['MA20'] < latest['MA50']:
            analysis['trend'] = 'BEARISH'
            analysis['direction'] = 'DOWN'
        
        # Trend strength using ADX
        if latest['ADX'] > 25:
            analysis['strength'] = 'STRONG'
        elif latest['ADX'] > 20:
            analysis['strength'] = 'MODERATE'
        
        return analysis
    
    def calculate_market_sentiment(self, data: pd.DataFrame) -> Dict:
        """Calculate market sentiment indicators"""
        if data.empty:
            return {}
        
        latest = data.iloc[-1]
        prev = data.iloc[-2] if len(data) > 1 else latest
        
        sentiment = {
            'overall': 'NEUTRAL',
            'momentum': 'NEUTRAL',
            'volatility': 'MODERATE'
        }
        
        # RSI sentiment
        rsi = latest['RSI']
        if rsi > 70:
            sentiment['momentum'] = 'OVERBOUGHT'
        elif rsi < 30:
            sentiment['momentum'] = 'OVERSOLD'
        
        # Volume analysis
        if latest['Volume'] > latest['Volume_SMA'] * 1.5:
            sentiment['volatility'] = 'HIGH'
        elif latest['Volume'] < latest['Volume_SMA'] * 0.5:
            sentiment['volatility'] = 'LOW'
        
        # Bollinger Bands position
        if latest['Close'] > latest['BB_Upper']:
            sentiment['overall'] = 'VERY_BULLISH'
        elif latest['Close'] < latest['BB_Lower']:
            sentiment['overall'] = 'VERY_BEARISH'
        elif latest['Close'] > latest['MA20']:
            sentiment['overall'] = 'BULLISH'
        elif latest['Close'] < latest['MA20']:
            sentiment['overall'] = 'BEARISH'
        
        return sentiment
    
    def generate_signal(self, symbol: str, timeframe: str = "1m") -> Dict:
        """Generate trading signal for a symbol"""
        try:
            # Get data
            data = self.get_historical_data(symbol, period="2d", interval=timeframe)
            if data.empty:
                return {'error': f'No data available for {symbol}'}
            
            # Calculate indicators
            df = self.calculate_indicators(data)
            latest = df.iloc[-1]
            
            # Get patterns and analysis
            patterns = self.detect_candlestick_patterns(df)
            trend = self.generate_trend_analysis(df)
            sentiment = self.calculate_market_sentiment(df)
            
            # Signal generation logic
            signal_score = 0
            signal_type = "HOLD"
            confidence = 0
            reasons = []
            
            # RSI analysis
            if latest['RSI'] < 30:
                signal_score += 1
                reasons.append("RSI Oversold")
                confidence += 10
            elif latest['RSI'] > 70:
                signal_score -= 1
                reasons.append("RSI Overbought")
                confidence += 10
            
            # MACD analysis
            if latest['MACD'] > latest['MACD_Signal']:
                signal_score += 1
                reasons.append("MACD Bullish Crossover")
                confidence += 15
            else:
                signal_score -= 1
                reasons.append("MACD Bearish")
                confidence += 15
            
            # Moving Average analysis
            if latest['Close'] > latest['MA20'] > latest['MA50']:
                signal_score += 2
                reasons.append("Price above MA20 > MA50")
                confidence += 20
            elif latest['Close'] < latest['MA20'] < latest['MA50']:
                signal_score -= 2
                reasons.append("Price below MA20 < MA50")
                confidence += 20
            
            # Bollinger Bands
            if latest['Close'] < latest['BB_Lower']:
                signal_score += 1
                reasons.append("Price below BB Lower")
                confidence += 15
            elif latest['Close'] > latest['BB_Upper']:
                signal_score -= 1
                reasons.append("Price above BB Upper")
                confidence += 15
            
            # Stochastic
            if latest['Stoch_K'] < 20 and latest['Stoch_D'] < 20:
                signal_score += 1
                reasons.append("Stochastic Oversold")
                confidence += 10
            elif latest['Stoch_K'] > 80 and latest['Stoch_D'] > 80:
                signal_score -= 1
                reasons.append("Stochastic Overbought")
                confidence += 10
            
            # Candlestick patterns
            if patterns.get('bullish_engulfing'):
                signal_score += 2
                reasons.append("Bullish Engulfing Pattern")
                confidence += 25
            if patterns.get('hammer'):
                signal_score += 1
                reasons.append("Hammer Pattern")
                confidence += 20
            
            # Determine final signal
            if signal_score >= 3:
                signal_type = "BUY"
            elif signal_score <= -3:
                signal_type = "SELL"
            
            # Normalize confidence
            confidence = min(confidence, 95)
            
            # Calculate entry, stop loss, and take profit
            current_price = latest['Close']
            atr = latest['ATR']
            
            if signal_type == "BUY":
                entry_price = current_price
                stop_loss = current_price - (atr * 1.5)
                take_profit = current_price + (atr * 2)
            else:
                entry_price = current_price
                stop_loss = current_price + (atr * 1.5)
                take_profit = current_price - (atr * 2)
            
            return {
                'symbol': symbol,
                'timeframe': timeframe,
                'signal': signal_type,
                'confidence': confidence,
                'current_price': current_price,
                'entry_price': entry_price,
                'stop_loss': stop_loss,
                'take_profit': take_profit,
                'reasons': reasons,
                'trend': trend,
                'sentiment': sentiment,
                'patterns': patterns,
                'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'technical_indicators': {
                    'RSI': latest['RSI'],
                    'MACD': latest['MACD'],
                    'MACD_Signal': latest['MACD_Signal'],
                    'ADX': latest['ADX'],
                    'Stoch_K': latest['Stoch_K'],
                    'Stoch_D': latest['Stoch_D'],
                    'BB_Position': (latest['Close'] - latest['BB_Lower']) / (latest['BB_Upper'] - latest['BB_Lower'])
                }
            }
            
        except Exception as e:
            self.logger.error(f"Error generating signal for {symbol}: {e}")
            return {'error': str(e)}