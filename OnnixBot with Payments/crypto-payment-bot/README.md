# 🤖 Crypto Payment Bot

A Telegram bot for Pocket Option trading signals with integrated crypto payments via NOWPayments.

## Features

- 💰 Crypto payment integration (300+ cryptocurrencies: BTC, ETH, USDT, LTC, BCH, SOL, ADA, MATIC, SHIB)
- 📊 Real-time trading signals with technical analysis
- 🔐 Premium access control
- ⚡ Automatic payment verification via webhooks
- 🌐 Railway deployment ready
- 🪙 NOWPayments integration (0.5% fees, 99.99% uptime)

## Quick Start

1. Get NOWPayments API credentials from https://account.nowpayments.io
2. Update `.env` file with your credentials
3. Deploy to Railway:
   - Connect GitHub repository
   - Set environment variables
   - Start processes

## Files

- `REAL_NOWPAYMENTS_BOT.py` - Main Telegram bot with NOWPayments integration
- `nowpayments_webhook_server.py` - Payment webhook handler
- `NOWPAYMENTS_INTEGRATION_GUIDE.md` - Complete setup guide
- `requirements.txt` - Python dependencies
- `Procfile` - Railway process configuration

## Supported Cryptocurrencies

BTC, ETH, USDT, LTC, BCH, SOL, ADA, MATIC, SHIB, XRP, DOT, DOGE, USDC, BUSD, DAI, UNI, AAVE, and 300+ more!

## Deployment

See `NOWPAYMENTS_INTEGRATION_GUIDE.md` for detailed setup instructions.

## Demo Mode

The bot includes demo mode for testing without real payments. Enable by leaving NOWPayments credentials blank.

## Support

For issues and support, check the NOWPayments integration guide.
