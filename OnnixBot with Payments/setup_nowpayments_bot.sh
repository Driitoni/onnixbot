#!/bin/bash
# Quick Setup Script for NOWPayments Crypto Payment Bot
# This script helps you set up the project structure and files

echo "🪙 NOWPayments Crypto Payment Bot - Quick Setup"
echo "==============================================="

# Create project directory
PROJECT_NAME="nowpayments-crypto-bot"
mkdir -p $PROJECT_NAME
cd $PROJECT_NAME

echo "📁 Creating project directory: $PROJECT_NAME"

# Copy required files
echo "📋 Copying NOWPayments bot files..."
cp ../REAL_NOWPAYMENTS_BOT.py .
cp ../nowpayments_webhook_server.py .
cp ../requirements.txt .
cp ../Procfile .

# Create .env file
echo "⚙️ Creating .env file..."
cat > .env << 'EOF'
# Telegram Bot Configuration
TELEGRAM_BOT_TOKEN=7369201109:AAFCU6umw6bA7RVd-2JbhDnxt5QeiEF7ueQ

# NOWPayments Configuration (UPDATE THESE WITH YOUR ACTUAL CREDENTIALS)
# Sign up at https://account.nowpayments.io/create-account
# Get API key from Dashboard -> Add new key
# Get IPN secret from Store Settings -> IPN Secret
NOWPAYMENTS_API_KEY=your_nowpayments_api_key
NOWPAYMENTS_IPN_SECRET=YourSecureIPNSecret2025!@#

# Webhook URL (Railway will set this automatically)
# WEBHOOK_BASE_URL=https://your-railway-app.railway.app

# Payment Plan Prices (USD)
PAYMENT_PLAN_1MONTH_PRICE=29.99
PAYMENT_PLAN_3MONTH_PRICE=79.99
PAYMENT_PLAN_1YEAR_PRICE=299.99

# Server Configuration
PORT=5000
FLASK_ENV=production
EOF

echo "📝 Created .env file with placeholder values"
echo "   ⚠️  Please update NOWPayments API credentials!"

# Create .gitignore
echo "🔒 Creating .gitignore..."
cat > .gitignore << 'EOF'
# Environment variables
.env

# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# Database
*.db
*.sqlite

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db
EOF

# Create updated README
echo "📚 Creating README..."
cat > README.md << 'EOF'
# 🪙 NOWPayments Crypto Payment Bot

A Telegram bot for Pocket Option trading signals with integrated crypto payments via NOWPayments.

## Features

- 💰 Crypto payment integration (300+ cryptocurrencies)
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

- `REAL_NOWPAYMENTS_BOT.py` - Main Telegram bot
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
EOF

echo ""
echo "✅ Setup Complete!"
echo "=================="
echo ""
echo "📁 Project created in: $PROJECT_NAME/"
echo "📋 Files created:"
echo "   - REAL_NOWPAYMENTS_BOT.py"
echo "   - nowpayments_webhook_server.py"
echo "   - requirements.txt"
echo "   - Procfile"
echo "   - .env (with placeholder values)"
echo "   - .gitignore"
echo "   - README.md"
echo ""
echo "🔑 Next Steps:"
echo "1. Get NOWPayments API credentials from https://account.nowpayments.io"
echo "2. Update .env file with your actual API key and IPN secret"
echo "3. Create GitHub repository"
echo "4. Deploy to Railway (see NOWPAYMENTS_INTEGRATION_GUIDE.md)"
echo ""
echo "🚀 Ready to deploy with NOWPayments!"
