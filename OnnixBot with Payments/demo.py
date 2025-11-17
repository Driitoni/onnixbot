#!/usr/bin/env python3
"""
Pocket Option Trading Bot - Demo Script
Demonstrates the bot's analysis capabilities without Telegram
"""

import os
import sys
import time
from datetime import datetime, timedelta
import pandas as pd
import numpy as np

# Add current directory to path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def print_header():
    """Print demo header"""
    print("=" * 60)
    print("🔥 POCKET OPTION TRADING BOT - DEMO")
    print("=" * 60)
    print("This demo shows the bot's analysis capabilities")
    print("without requiring a Telegram bot setup.")
    print("=" * 60)

def demo_technical_analysis():
    """Demonstrate technical analysis features"""
    print("\n📊 TECHNICAL ANALYSIS DEMO")
    print("-" * 40)
    
    try:
        from technical_analysis import TechnicalAnalyzer
        
        analyzer = TechnicalAnalyzer()
        symbol = "EURUSD"
        
        print(f"Analyzing {symbol} across multiple timeframes...")
        
        timeframes = ["1m", "5m", "15m", "1h"]
        results = []
        
        for tf in timeframes:
            print(f"  📈 {tf.upper()} timeframe...")
            try:
                signal = analyzer.generate_signal(symbol, tf)
                if 'error' not in signal:
                    results.append(signal)
                    print(f"    ✅ Signal: {signal.get('signal', 'N/A')}")
                    print(f"    🎯 Confidence: {signal.get('confidence', 0)}%")
                    print(f"    💰 Price: {signal.get('current_price', 0):.5f}")
                else:
                    print(f"    ❌ {signal['error']}")
            except Exception as e:
                print(f"    ❌ Error: {e}")
            time.sleep(1)  # Rate limiting
        
        if results:
            print(f"\n📋 SUMMARY for {symbol}:")
            buy_signals = sum(1 for s in results if s.get('signal') == 'BUY')
            sell_signals = sum(1 for s in results if s.get('signal') == 'SELL')
            
            overall = "BUY" if buy_signals > sell_signals else "SELL" if sell_signals > buy_signals else "HOLD"
            avg_confidence = sum(s.get('confidence', 0) for s in results) / len(results)
            
            print(f"  🎯 Overall Signal: {overall}")
            print(f"  📊 Average Confidence: {avg_confidence:.1f}%")
            print(f"  🟢 Buy Signals: {buy_signals}")
            print(f"  🔴 Sell Signals: {sell_signals}")
            
            # Show latest indicators
            if "1m" in [s.get('timeframe') for s in results]:
                latest = next(s for s in results if s.get('timeframe') == "1m")
                indicators = latest.get('technical_indicators', {})
                print(f"\n📈 KEY INDICATORS (1m):")
                print(f"  RSI: {indicators.get('RSI', 0):.1f}")
                print(f"  MACD: {indicators.get('MACD', 0):.4f}")
                print(f"  ADX: {indicators.get('ADX', 0):.1f}")
        
        return True
    except Exception as e:
        print(f"❌ Technical analysis demo failed: {e}")
        return False

def demo_risk_management():
    """Demonstrate risk management features"""
    print("\n🛡️ RISK MANAGEMENT DEMO")
    print("-" * 40)
    
    try:
        from risk_management import RiskManager
        from technical_analysis import TechnicalAnalyzer
        
        # Create risk manager
        config = {
            'RISK_PERCENTAGE': 2.0,
            'MAX_POSITION_SIZE': 100,
            'MAX_DAILY_SIGNALS': 50,
            'ACCOUNT_BALANCE': 1000
        }
        
        risk_manager = RiskManager(config)
        analyzer = TechnicalAnalyzer()
        
        # Generate a sample signal
        print("Generating sample trading signal...")
        signal = analyzer.generate_signal("EURUSD", "1m")
        
        if 'error' not in signal:
            print(f"  📊 Signal: {signal.get('signal')} for {signal.get('symbol')}")
            print(f"  💰 Price: {signal.get('current_price', 0):.5f}")
            print(f"  🎯 Confidence: {signal.get('confidence', 0)}%")
            
            # Perform risk assessment
            print("\nPerforming risk assessment...")
            risk_assessment = risk_manager.assess_trade_risk(signal, 1000)
            
            print(f"  🛡️ Risk Level: {risk_assessment.get('risk_level', 'Unknown')}")
            print(f"  ✅ Recommendation: {risk_assessment.get('recommendation', 'Unknown')}")
            print(f"  💵 Position Size: ${risk_assessment.get('position_size', 0):.2f}")
            print(f"  📊 Risk/Reward: {risk_assessment.get('risk_reward_ratio', 0):.2f}")
            
            if risk_assessment.get('warnings'):
                print(f"\n⚠️ Warnings:")
                for warning in risk_assessment['warnings']:
                    print(f"  • {warning}")
            
            # Show daily stats
            print(f"\n📅 Daily Summary:")
            daily = risk_manager.get_daily_summary()
            print(f"  Signals Sent: {daily['signals_sent']}")
            print(f"  Remaining: {daily['remaining_signals']}")
            print(f"  Max Reached: {daily['max_trades_reached']}")
        else:
            print(f"❌ Error generating signal: {signal['error']}")
        
        return True
    except Exception as e:
        print(f"❌ Risk management demo failed: {e}")
        return False

def demo_portfolio_tracking():
    """Demonstrate portfolio tracking features"""
    print("\n💼 PORTFOLIO TRACKING DEMO")
    print("-" * 40)
    
    try:
        from portfolio_tracker import PortfolioTracker, Trade, TradeType, TradeStatus
        import uuid
        
        # Create portfolio tracker
        portfolio = PortfolioTracker("demo_portfolio.json")
        
        # Add sample trades
        print("Adding sample trades to portfolio...")
        
        # Trade 1: Winner
        trade1 = Trade(
            id=str(uuid.uuid4())[:8],
            symbol="EURUSD",
            trade_type=TradeType.BUY,
            entry_price=1.0850,
            exit_price=1.0870,
            quantity=1000,
            entry_time=datetime.now() - timedelta(hours=2),
            exit_time=datetime.now() - timedelta(hours=1),
            status=TradeStatus.CLOSED_WIN,
            stop_loss=1.0830,
            take_profit=1.0890,
            profit_loss=20.0,
            confidence=75,
            signal_reasons=["RSI oversold", "Bullish engulfing"],
            timeframe="5m"
        )
        
        # Trade 2: Loser
        trade2 = Trade(
            id=str(uuid.uuid4())[:8],
            symbol="GBPUSD",
            trade_type=TradeType.SELL,
            entry_price=1.2650,
            exit_price=1.2680,
            quantity=1000,
            entry_time=datetime.now() - timedelta(hours=3),
            exit_time=datetime.now() - timedelta(hours=2),
            status=TradeStatus.CLOSED_LOSS,
            stop_loss=1.2670,
            take_profit=1.2620,
            profit_loss=-30.0,
            confidence=60,
            signal_reasons=["MACD bearish", "Resistance rejection"],
            timeframe="15m"
        )
        
        portfolio.add_trade(trade1)
        portfolio.add_trade(trade2)
        
        # Show portfolio summary
        print("\n📊 Portfolio Summary:")
        summary = portfolio.get_summary()
        print(f"  Total Trades: {summary['total_trades']}")
        print(f"  Win Rate: {summary['win_rate']}%")
        print(f"  Total P&L: ${summary['total_profit_loss']}")
        print(f"  Consecutive Wins: {summary['consecutive_wins']}")
        print(f"  Consecutive Losses: {summary['consecutive_losses']}")
        
        # Show detailed stats
        stats = portfolio.get_trade_statistics()
        print(f"\n📈 Detailed Statistics:")
        print(f"  Winning Trades: {stats['winning_trades']}")
        print(f"  Losing Trades: {stats['losing_trades']}")
        print(f"  Average Win: ${stats['avg_win']}")
        print(f"  Average Loss: ${stats['avg_loss']}")
        print(f"  Largest Win: ${stats['largest_win']}")
        print(f"  Largest Loss: ${stats['largest_loss']}")
        print(f"  Profit Factor: {stats['profit_factor']}")
        
        # Symbol performance
        print(f"\n🎯 Symbol Performance:")
        symbol_perf = portfolio.get_symbol_performance("EURUSD")
        print(f"  EURUSD: {symbol_perf['total_trades']} trades, {symbol_perf['win_rate']}% win rate, ${symbol_perf['profit_loss']} P&L")
        
        symbol_perf = portfolio.get_symbol_performance("GBPUSD")
        print(f"  GBPUSD: {symbol_perf['total_trades']} trades, {symbol_perf['win_rate']}% win rate, ${symbol_perf['profit_loss']} P&L")
        
        return True
    except Exception as e:
        print(f"❌ Portfolio tracking demo failed: {e}")
        return False

def demo_market_news():
    """Demonstrate market news features"""
    print("\n📰 MARKET NEWS DEMO")
    print("-" * 40)
    
    try:
        from market_news import MarketNews, NewsSentimentAnalyzer
        
        news = MarketNews()
        sentiment_analyzer = NewsSentimentAnalyzer()
        
        print("Fetching latest market news...")
        news_data = news.get_latest_news()
        
        if news_data and 'articles' in news_data:
            print(f"Found {len(news_data['articles'])} news articles:")
            
            for i, article in enumerate(news_data['articles'][:3], 1):
                print(f"\n{i}. {article.get('title', 'No title')}")
                if article.get('description'):
                    print(f"   {article['description'][:100]}...")
                print(f"   Source: {article.get('source', 'Unknown')}")
            
            # Analyze sentiment
            print(f"\n📊 Sentiment Analysis:")
            sentiment = sentiment_analyzer.analyze_news_sentiment(news_data['articles'])
            print(f"  Overall Sentiment: {sentiment['sentiment']}")
            print(f"  Sentiment Score: {sentiment['score']}")
            print(f"  Confidence: {sentiment['confidence']}%")
            print(f"  Articles Analyzed: {sentiment['articles_analyzed']}")
        else:
            print("No news articles found")
        
        # Show market sentiment
        print(f"\n🌍 Market Sentiment Indicators:")
        market_sentiment = news.get_market_sentiment()
        for key, value in market_sentiment.items():
            print(f"  {key.replace('_', ' ').title()}: {value}")
        
        return True
    except Exception as e:
        print(f"❌ Market news demo failed: {e}")
        return False

def demo_supported_assets():
    """Show supported assets and their analysis"""
    print("\n💱 SUPPORTED ASSETS")
    print("-" * 40)
    
    assets = {
        "Forex": ["EURUSD", "GBPUSD", "USDJPY", "AUDUSD", "USDCAD", "USDCHF"],
        "Indices": ["US30", "SPX500", "NASDAQ", "GER40", "UK100", "JP225"],
        "Commodities": ["USOIL", "UKOIL", "XAUUSD", "XAGUSD"],
        "Crypto": ["BTCUSD", "ETHUSD", "LTCUSD", "ADAUSD", "DOTUSD"]
    }
    
    for category, symbols in assets.items():
        print(f"\n{category}:")
        for symbol in symbols:
            print(f"  • {symbol}")
    
    print(f"\n📋 Demo covers: {list(assets['Forex'][:3])}")
    print("The full bot supports all symbols above!")

def show_bot_commands():
    """Show available bot commands"""
    print("\n🤖 TELEGRAM BOT COMMANDS")
    print("-" * 40)
    
    commands = {
        "Basic": ["/start", "/help", "/status"],
        "Analysis": ["/analyze [symbol]", "/signal [symbol]", "/timeframes"],
        "Portfolio": ["/portfolio", "/risk"],
        "Settings": ["/settings", "/subscribe", "/unsubscribe"],
        "News": ["/news"]
    }
    
    for category, cmds in commands.items():
        print(f"\n{category}:")
        for cmd in cmds:
            print(f"  {cmd}")
    
    print(f"\n💡 Quick Start:")
    print(f"  1. /start - Get welcome message")
    print(f"  2. /analyze EURUSD - Get market analysis")
    print(f"  3. /signal EURUSD - Get trading signal")
    print(f"  4. /subscribe - Get trading alerts")

def show_risk_disclaimer():
    """Show important risk disclaimer"""
    print("\n" + "=" * 60)
    print("⚠️  IMPORTANT RISK DISCLAIMER")
    print("=" * 60)
    print("This bot is for EDUCATIONAL PURPOSES ONLY.")
    print()
    print("• NOT financial advice")
    print("• Trading involves significant risk")
    print("• You can lose all invested capital")
    print("• Past performance ≠ future results")
    print("• Always do your own research")
    print("• Consider demo trading first")
    print("• Never risk more than you can afford to lose")
    print()
    print("The authors are not responsible for any trading losses.")
    print("=" * 60)

def main():
    """Main demo function"""
    print_header()
    
    demos = [
        ("Supported Assets", demo_supported_assets),
        ("Technical Analysis", demo_technical_analysis),
        ("Risk Management", demo_risk_management),
        ("Portfolio Tracking", demo_portfolio_tracking),
        ("Market News", demo_market_news),
        ("Bot Commands", show_bot_commands)
    ]
    
    for demo_name, demo_func in demos:
        print(f"\n{'='*20} {demo_name} {'='*20}")
        try:
            demo_func()
            time.sleep(2)  # Pause between demos
        except Exception as e:
            print(f"❌ {demo_name} demo failed: {e}")
    
    show_risk_disclaimer()
    
    print("\n🎉 DEMO COMPLETE!")
    print("=" * 60)
    print("To use the full Telegram bot:")
    print("1. Run: python setup.py")
    print("2. Configure your .env file")
    print("3. Run: python run_bot.py")
    print("4. Start chatting with your bot on Telegram!")
    print("=" * 60)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n🛑 Demo interrupted by user")
    except Exception as e:
        print(f"\n❌ Demo failed with error: {e}")