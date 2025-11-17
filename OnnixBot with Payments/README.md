# Pocket Option Trading Analysis Bot for Telegram

A comprehensive Telegram bot for Pocket Option trading analysis with multi-timeframe technical analysis, risk management, portfolio tracking, and market news integration.

## Features

### 📊 Technical Analysis
- **Multi-timeframe Analysis**: 1m, 5m, 15m, 1h, 4h, 1d
- **50+ Technical Indicators**: RSI, MACD, Bollinger Bands, Stochastic, ADX, Williams %R, CCI, ATR
- **Pattern Recognition**: Candlestick patterns, chart patterns
- **Support/Resistance**: Dynamic level calculation
- **Market Sentiment**: Real-time sentiment analysis

### 🛡️ Risk Management
- Position sizing calculator
- Risk-reward ratio analysis
- Daily limits protection
- Portfolio heat monitoring
- Drawdown protection
- Comprehensive risk scoring

### 📈 Signal Generation
- BUY/SELL signals with confidence scores
- Entry, stop loss, and take profit levels
- Multiple confirmation factors
- False signal filtering
- Real-time signal alerts

### 💼 Portfolio Tracking
- Trade history logging
- Performance metrics
- Win rate tracking
- Profit/Loss calculations
- Symbol and timeframe performance analysis
- Risk metrics calculation

### 📰 Market News
- Real-time market news integration
- Economic calendar
- Breaking news alerts
- News sentiment analysis
- Asset-specific news impact assessment

## Installation

### Prerequisites
- Python 3.8 or higher
- Telegram account
- Internet connection for market data

### Step 1: Create Telegram Bot
1. Open Telegram and search for `@BotFather`
2. Start a chat and send `/newbot`
3. Follow the instructions to create your bot
4. Save the bot token provided

### Step 2: Setup Environment
1. Clone or download the bot files
2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install requirements:
   ```bash
   pip install -r requirements.txt
   ```

### Step 3: Configure Bot
1. Copy `.env.example` to `.env`
2. Edit `.env` file with your settings:
   ```env
   TELEGRAM_BOT_TOKEN=your_bot_token_here
   AUTHORIZED_USERS=your_telegram_user_id
   DEFAULT_ASSET=EURUSD
   RISK_LEVEL=MEDIUM
   MAX_DAILY_SIGNALS=50
   ACCOUNT_BALANCE=1000
   ```

### Step 4: Run the Bot
```bash
python main.py
```

## Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `TELEGRAM_BOT_TOKEN` | Your Telegram bot token (required) | - |
| `AUTHORIZED_USERS` | Comma-separated list of authorized user IDs | Empty (all users) |
| `DEFAULT_ASSET` | Default currency pair to analyze | EURUSD |
| `DEFAULT_TIMEFRAMES` | Timeframes to analyze | 1m,5m,15m,1h,4h,1d |
| `RISK_LEVEL` | Risk tolerance level | MEDIUM |
| `MAX_DAILY_SIGNALS` | Maximum signals per day | 50 |
| `ACCOUNT_BALANCE` | Trading account balance | 1000 |
| `ANALYSIS_INTERVAL` | Seconds between analysis | 300 |

### API Keys (Optional)
For enhanced features, you can add these API keys to your `.env`:
- `NEWS_API_KEY` - For real-time news
- `ALPHA_VANTAGE_API_KEY` - For enhanced market data
- `FINNHUB_API_KEY` - For additional financial data

## Usage

### Commands
- `/start` - Welcome message and quick actions
- `/help` - Detailed help and documentation
- `/analyze [symbol]` - Get comprehensive market analysis
- `/signal [symbol]` - Get specific trading signal
- `/timeframes` - View all supported timeframes
- `/portfolio` - Track trading portfolio
- `/news` - Get latest market news
- `/settings` - Configure bot preferences
- `/risk` - View risk analysis dashboard
- `/status` - Check bot status
- `/subscribe` - Subscribe to trading alerts
- `/unsubscribe` - Unsubscribe from alerts

### Supported Assets
**Forex Pairs:**
- Major: EURUSD, GBPUSD, USDJPY, AUDUSD, USDCAD, USDCHF
- Cross: EURJPY, GBPJPY, AUDJPY, NZDUSD

**Indices:**
- US30, SPX500, NASDAQ, GER40, UK100, JP225

**Commodities:**
- US OIL, UK OIL, XAUUSD (Gold), XAGUSD (Silver)

**Cryptocurrencies:**
- BTCUSD, ETHUSD, LTCUSD, ADAUSD, DOTUSD

### Quick Start
1. Start the bot: `/start`
2. Get analysis: `/analyze EURUSD`
3. Get signal: `/signal EURUSD`
4. Subscribe for alerts: `/subscribe`

## Bot Interface

### Inline Keyboards
The bot uses inline keyboards for quick actions:
- **Quick Analysis** - Instant market analysis
- **Signal Generation** - Get trading signals
- **Portfolio Management** - Track performance
- **News Updates** - Latest market news

### Analysis Display
- Overall market sentiment
- Multi-timeframe breakdown
- Technical indicators
- Entry/exit levels
- Risk assessment

### Risk Warnings
The bot includes comprehensive risk management:
- Position size recommendations
- Risk-reward ratios
- Daily limits
- Drawdown protection
- Market volatility alerts

## Risk Management Features

### Position Sizing
- Automatic position size calculation based on risk percentage
- Account balance consideration
- Stop loss distance analysis

### Risk Scoring
- Multi-factor risk assessment
- Technical indicator alignment
- Market condition analysis
- Confidence-based filtering

### Daily Limits
- Maximum signals per day
- Cooldown periods between signals
- Automatic trading suspension when limits reached

## Portfolio Tracking

### Trade Management
- Add/edit/delete trades
- Track open and closed positions
- Calculate real-time P&L
- Performance metrics

### Analytics
- Win rate analysis
- Profit factor calculation
- Symbol performance comparison
- Timeframe analysis
- Risk metrics

### Reports
- Daily performance summary
- Weekly/monthly reports
- Export to CSV
- Detailed trade history

## News Integration

### News Sources
- Multiple news API integration
- Real-time market updates
- Economic calendar events
- Breaking news alerts

### Sentiment Analysis
- News sentiment scoring
- Asset-specific impact assessment
- Market sentiment indicators
- Risk event monitoring

## Advanced Features

### Multi-Timeframe Analysis
- Automatic timeframe analysis
- Trend direction confirmation
- Entry timing optimization
- Market structure analysis

### Pattern Recognition
- Candlestick pattern detection
- Chart pattern recognition
- Signal confirmation
- False signal filtering

### Risk Monitoring
- Real-time risk assessment
- Portfolio heat monitoring
- Drawdown tracking
- Emergency stop mechanisms

## API Integration

### Market Data
- Yahoo Finance (yfinance)
- Alpha Vantage (optional)
- Finnhub (optional)
- Real-time price feeds

### News APIs
- NewsAPI.org
- Finnhub News
- Custom news feeds
- Economic calendar APIs

## Customization

### Adding New Assets
1. Add symbol to `SUPPORTED_ASSETS` in `.env`
2. Update symbol mappings in the bot code
3. Test with analysis commands

### Custom Indicators
1. Modify `technical_analysis.py`
2. Add new indicators to the calculation function
3. Update signal generation logic

### Risk Parameters
1. Adjust risk settings in `.env`
2. Modify position sizing logic
3. Update risk scoring algorithm

## Troubleshooting

### Common Issues

**Bot not responding:**
- Check bot token in `.env` file
- Verify internet connection
- Check Python version (3.8+)

**No market data:**
- Verify internet connection
- Check if symbol is supported
- Try different timeframe

**Authorization errors:**
- Add your user ID to `AUTHORIZED_USERS`
- Restart the bot after changes

**High CPU usage:**
- Reduce `ANALYSIS_INTERVAL`
- Limit number of assets
- Check for infinite loops in code

### Debug Mode
Enable debug logging by modifying the logging level:
```python
logging.basicConfig(level=logging.DEBUG)
```

### Log Files
Check `bot.log` for detailed error information and debugging.

## Performance Optimization

### Resource Usage
- Minimize API calls with caching
- Use efficient data structures
- Implement rate limiting
- Monitor memory usage

### Speed Optimization
- Async operations for API calls
- Data preprocessing
- Caching results
- Parallel processing

## Security Considerations

### API Keys
- Never share API keys
- Use environment variables
- Rotate keys regularly
- Monitor usage

### User Data
- Protect user privacy
- Secure data storage
- Regular backups
- Access controls

## Legal Disclaimer

⚠️ **IMPORTANT DISCLAIMER**

This bot is for **educational and informational purposes only**. 

- **Not Financial Advice**: The analysis and signals provided are for educational purposes only and should not be considered as financial advice.
- **Risk Warning**: Trading involves significant risk. You can lose all of your invested capital.
- **No Guarantees**: Past performance does not guarantee future results.
- **Independent Research**: Always conduct your own research and analysis before making any trading decisions.
- **Professional Advice**: Consider consulting with a qualified financial advisor.
- **Demo Trading**: Practice with demo accounts before risking real money.

**Use at your own risk. The authors and developers are not responsible for any trading losses.**

## Support

### Getting Help
1. Check the documentation above
2. Review the log files
3. Test with different symbols
4. Verify configuration settings

### Contributing
To contribute to the project:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is open source. Please review the license terms before use.

## Version History

### v1.0.0
- Initial release
- Basic technical analysis
- Telegram bot integration
- Risk management system
- Portfolio tracking
- Market news integration

### Future Updates
- Machine learning signals
- Advanced chart generation
- Mobile app support
- Web dashboard
- Multi-language support

---

**Happy Trading! 📈**