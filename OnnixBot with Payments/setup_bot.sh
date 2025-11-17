#!/bin/bash
# Quick Setup Script for Crypto Payment Bot
# This script helps you set up the project structure and files

echo "🚀 Crypto Payment Bot - Quick Setup"
echo "=================================="

# Create project directory
PROJECT_NAME="crypto-payment-bot"
mkdir -p $PROJECT_NAME
cd $PROJECT_NAME

echo "📁 Creating project directory: $PROJECT_NAME"

# Copy required files
echo "📋 Copying bot files..."
cp ../REAL_COINPAYMENTS_BOT.py .
cp ../webhook_server.py .
cp ../requirements.txt .
cp ../Procfile .

# Create .env file
echo "⚙️ Creating .env file..."
cat > .env << 'EOF'
# Telegram Bot Configuration
TELEGRAM_BOT_TOKEN=7369201109:AAFCU6umw6bA7RVd-2JbhDnxt5QeiEF7ueQ

# CoinPayments Configuration (UPDATE THESE WITH YOUR ACTUAL CREDENTIALS)
# Get these from https://www.coinpayments.net -> Account -> API Keys
COINPAYMENTS_API_KEY=cp_api_key_xxxxxxxxxxxx
COINPAYMENTS_IPN_SECRET=YourSecureIPNSecret2025!@#

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
echo "   ⚠️  Please update CoinPayments API credentials!"

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

# Create README
echo "📚 Creating README..."
cat > README.md << 'EOF'
# 🤖 Crypto Payment Bot

A Telegram bot for Pocket Option trading signals with integrated crypto payments via CoinPayments.

## Features

- 💰 Crypto payment integration (BTC, ETH, USDT, LTC, BCH)
- 📊 Real-time trading signals with technical analysis
- 🔐 Premium access control
- ⚡ Automatic payment verification
- 🌐 Railway deployment ready

## Quick Start

1. Get CoinPayments API credentials from https://www.coinpayments.net
2. Update `.env` file with your credentials
3. Deploy to Railway:
   - Connect GitHub repository
   - Set environment variables
   - Start processes

## Files

- `REAL_COINPAYMENTS_BOT.py` - Main Telegram bot
- `webhook_server.py` - Payment webhook handler
- `requirements.txt` - Python dependencies
- `Procfile` - Railway process configuration

## Deployment

See `RAILWAY_DEPLOYMENT_GUIDE.md` for detailed setup instructions.

## Demo Mode

The bot includes demo mode for testing without real payments. Enable by leaving CoinPayments credentials blank.

## Support

For issues and support, check the deployment guide.
EOF

echo ""
echo "✅ Setup Complete!"
echo "=================="
echo ""
echo "📁 Project created in: $PROJECT_NAME/"
echo "📋 Files created:"
echo "   - REAL_COINPAYMENTS_BOT.py"
echo "   - webhook_server.py"
echo "   - requirements.txt"
echo "   - Procfile"
echo "   - .env (with placeholder values)"
echo "   - .gitignore"
echo "   - README.md"
echo ""
echo "🔑 Next Steps:"
echo "1. Get CoinPayments API credentials from https://www.coinpayments.net"
echo "2. Update .env file with your actual API key and IPN secret"
echo "3. Create GitHub repository"
echo "4. Deploy to Railway (see RAILWAY_DEPLOYMENT_GUIDE.md)"
echo ""
echo "🚀 Ready to deploy!"
