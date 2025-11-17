#!/bin/bash
# Server Setup Script for Telegram Bot
# Run this script on your VPS (Ubuntu/Debian)

echo "🤖 Setting up Telegram Bot server..."

# Update system
echo "📦 Updating system packages..."
sudo apt update && sudo apt upgrade -y

# Install Python and pip
echo "🐍 Installing Python and pip..."
sudo apt install python3 python3-pip python3-venv -y

# Create bot directory
echo "📁 Creating bot directory..."
mkdir -p ~/telegram_bot
cd ~/telegram_bot

# Create virtual environment
echo "🌐 Creating virtual environment..."
python3 -m venv bot_env
source bot_env/bin/activate

# Install dependencies
echo "📦 Installing bot dependencies..."
pip install -r requirements.txt

echo "✅ Server setup complete!"
echo ""
echo "📋 Next steps:"
echo "1. Upload your bot files (ENHANCED_POCKET_OPTION_BOT.py, .env, requirements.txt)"
echo "2. Run: source bot_env/bin/activate && python ENHANCED_POCKET_OPTION_BOT.py"
echo ""
echo "💡 To run bot in background:"
echo "   nohup python ENHANCED_POCKET_OPTION_BOT.py &"
echo ""
echo "🎯 Your bot will be accessible 24/7!"