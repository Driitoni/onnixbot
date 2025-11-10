# 📦 INSTALL REAL-TIME DATA LIBRARIES

## 🔧 If you need to install yfinance for real market data:

```bash
pip install yfinance>=0.2.40
```

## 🏃‍♂️ OR install all requirements at once:

```bash
pip install -r requirements.txt
```

## ✅ Verify installation:
```python
import yfinance as yf
print("yfinance version:", yf.__version__)
```

## 🌐 What yfinance gives us:
- **Real stock prices** - Live market data
- **Historical data** - For technical analysis
- **Real-time quotes** - Current market prices
- **Currency pairs** - Live forex data
- **Volatility data** - Real market measurements

## 📊 Currency pairs available:
- EUR/USD (EURUSD=X)
- GBP/USD (GBPUSD=X) 
- USD/JPY (USDJPY=X)
- AUD/USD (AUDUSD=X)
- USD/CAD (USDCAD=X)
- EUR/GBP (EURGBP=X)

After installing yfinance, run:
```bash
python REALTIME_TRADING_BOT.py
```