#!/usr/bin/env python3
"""
Test script to verify bot installation for Python 3.13
"""

def test_imports():
    """Test if all required packages can be imported"""
    print("🧪 Testing Package Imports...")
    print("-" * 40)
    
    # Test core packages
    try:
        import pandas as pd
        print(f"✅ pandas {pd.__version__}")
    except ImportError as e:
        print(f"❌ pandas: {e}")
        return False
    
    try:
        import telegram
        print(f"✅ python-telegram-bot")
    except ImportError as e:
        print(f"❌ python-telegram-bot: {e}")
        return False
    
    try:
        import yfinance
        print(f"✅ yfinance")
    except ImportError as e:
        print(f"❌ yfinance: {e}")
        return False
    
    try:
        import numpy as np
        print(f"✅ numpy {np.__version__}")
    except ImportError as e:
        print(f"❌ numpy: {e}")
        return False
    
    try:
        import ta
        print(f"✅ ta (technical analysis)")
    except ImportError as e:
        print(f"❌ ta: {e}")
        return False
    
    try:
        import requests
        print(f"✅ requests")
    except ImportError as e:
        print(f"❌ requests: {e}")
        return False
    
    try:
        from dotenv import load_dotenv
        print(f"✅ python-dotenv")
    except ImportError as e:
        print(f"❌ python-dotenv: {e}")
        return False
    
    try:
        import aiohttp
        print(f"✅ aiohttp")
    except ImportError as e:
        print(f"⚠️  aiohttp: {e}")
        # aiohttp is not critical
    
    # Test bot modules
    try:
        from technical_analysis import TechnicalAnalyzer
        print(f"✅ technical_analysis module")
    except ImportError as e:
        print(f"❌ technical_analysis: {e}")
        return False
    
    try:
        from risk_management import RiskManager
        print(f"✅ risk_management module")
    except ImportError as e:
        print(f"❌ risk_management: {e}")
        return False
    
    return True

def test_bot_initialization():
    """Test if bot components can be initialized"""
    print("\n🤖 Testing Bot Initialization...")
    print("-" * 40)
    
    try:
        from technical_analysis import TechnicalAnalyzer
        analyzer = TechnicalAnalyzer()
        print("✅ TechnicalAnalyzer initialized")
    except Exception as e:
        print(f"❌ TechnicalAnalyzer: {e}")
        return False
    
    try:
        from risk_management import RiskManager
        risk_manager = RiskManager({'RISK_PERCENTAGE': 2.0})
        print("✅ RiskManager initialized")
    except Exception as e:
        print(f"❌ RiskManager: {e}")
        return False
    
    try:
        from market_news import MarketNews
        news = MarketNews()
        print("✅ MarketNews initialized")
    except Exception as e:
        print(f"⚠️  MarketNews: {e}")
        # Market news is not critical
    
    try:
        from portfolio_tracker import PortfolioTracker
        portfolio = PortfolioTracker()
        print("✅ PortfolioTracker initialized")
    except Exception as e:
        print(f"❌ PortfolioTracker: {e}")
        return False
    
    return True

def test_basic_functionality():
    """Test basic functionality without API calls"""
    print("\n⚙️  Testing Basic Functionality...")
    print("-" * 40)
    
    try:
        from technical_analysis import TechnicalAnalyzer
        analyzer = TechnicalAnalyzer()
        
        # Test with dummy data
        import pandas as pd
        import numpy as np
        
        # Create dummy data
        dates = pd.date_range('2023-01-01', periods=50, freq='H')
        prices = 100 + np.cumsum(np.random.randn(50) * 0.1)
        dummy_data = pd.DataFrame({'Close': prices}, index=dates)
        
        # Test analysis
        result = analyzer.analyze_timeframe('AAPL', dummy_data, '1h')
        print("✅ Technical analysis with dummy data")
        
    except Exception as e:
        print(f"❌ Basic functionality: {e}")
        return False
    
    return True

def main():
    """Run all tests"""
    print("=" * 50)
    print("🔍 POCKET OPTION BOT - INSTALLATION TEST")
    print("=" * 50)
    
    # Test Python version
    import sys
    print(f"Python version: {sys.version}")
    print()
    
    # Run tests
    if not test_imports():
        print("\n❌ IMPORT TESTS FAILED")
        print("Please install missing packages with: pip install -r requirements.txt")
        return False
    
    if not test_bot_initialization():
        print("\n❌ INITIALIZATION TESTS FAILED")
        return False
    
    if not test_basic_functionality():
        print("\n❌ FUNCTIONALITY TESTS FAILED")
        return False
    
    print("\n" + "=" * 50)
    print("🎉 ALL TESTS PASSED!")
    print("=" * 50)
    print("\nYour bot is ready to run!")
    print("Next steps:")
    print("1. Configure your .env file")
    print("2. Run: python run_bot.py")
    print("3. Test with your Telegram bot")
    
    return True

if __name__ == "__main__":
    success = main()
    if not success:
        exit(1)