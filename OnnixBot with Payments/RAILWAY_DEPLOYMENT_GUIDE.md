# 🚀 Railway Deployment Guide - Complete Setup

## 📋 **Step 1: CoinPayments Account Setup**

### **1.1 Sign Up for CoinPayments**
1. Go to https://www.coinpayments.net
2. Click "Sign Up" (top right)
3. Complete registration with email verification
4. Log into your dashboard

### **1.2 Get Your API Credentials**
1. In CoinPayments dashboard, go to **"Account"** → **"API Keys"**
2. Click **"Create New API Key"**
3. Enable these permissions:
   - ✅ **Get Rates** - To get crypto prices
   - ✅ **Create Payment** - To generate payment addresses
   - ✅ **Get Transfer Info** - To check payment status
   - ✅ **IPN/Webhook** - For automatic notifications

4. **Save these credentials:**
   - **API Key**: `cp_api_key_xxxxxxxxxxxx` (starts with cp_api_key_)
   - **IPN Secret**: Create a strong random string like `MyBotSecret2025!@#`

---

## 📁 **Step 2: Prepare Your Files**

### **2.1 Required Files for Railway**
Create a folder with these files:
```
crypto-payment-bot/
├── REAL_COINPAYMENTS_BOT.py    # Main bot with CoinPayments integration
├── webhook_server.py           # Webhook server for payment confirmations
├── requirements.txt            # Python dependencies
├── Procfile                    # Railway process configuration
├── .env                        # Environment variables (you'll create this)
└── README.md                   # Optional documentation
```

### **2.2 Create .env File**
Create a `.env` file with your actual credentials:

```bash
# Telegram Bot Token (your existing bot)
TELEGRAM_BOT_TOKEN=7369201109:AAFCU6umw6bA7RVd-2JbhDnxt5QeiEF7ueQ

# CoinPayments API Credentials (GET FROM CoinPayments.net)
COINPAYMENTS_API_KEY=cp_api_key_xxxxxxxxxxxx
COINPAYMENTS_IPN_SECRET=YourSecureIPNSecret2025!@#

# Webhook URL (will be your Railway app URL)
# This will be set automatically by Railway, but you can use a placeholder:
WEBHOOK_BASE_URL=https://your-app.railway.app

# Payment Plan Prices (USD)
PAYMENT_PLAN_1MONTH_PRICE=29.99
PAYMENT_PLAN_3MONTH_PRICE=79.99
PAYMENT_PLAN_1YEAR_PRICE=299.99

# Server Configuration
PORT=5000
FLASK_ENV=production
```

---

## 🔧 **Step 3: GitHub Repository Setup**

### **3.1 Create GitHub Repository**
1. Go to https://github.com and create a new repository
2. Name it: `crypto-payment-bot`
3. Make it **Public** (Railway free tier works with public repos)
4. Don't initialize with README (we already have files)

### **3.2 Upload Your Files**
Open terminal in your project folder and run:

```bash
# Initialize git repository
git init

# Add all files
git add .

# Make first commit
git commit -m "Initial crypto payment bot with CoinPayments"

# Set main branch
git branch -M main

# Add GitHub repository (replace with your actual repository URL)
git remote add origin https://github.com/yourusername/crypto-payment-bot.git

# Push to GitHub
git push -u origin main
```

---

## 🌐 **Step 4: Railway Deployment**

### **4.1 Sign Up for Railway**
1. Go to https://railway.app
2. Click **"Start a New Project"**
3. Choose **"Deploy from GitHub repo"**
4. Sign in with your GitHub account
5. **Authorize Railway** to access your repositories

### **4.2 Deploy Your Bot**
1. Click **"New Project"**
2. Select **"Deploy from GitHub repo"**
3. Choose your `crypto-payment-bot` repository
4. Railway will automatically detect it's a Python app

### **4.3 Configure Environment Variables**
In Railway dashboard:
1. Click on your project
2. Go to **"Variables"** tab
3. Add these environment variables:

```bash
# Bot Configuration
TELEGRAM_BOT_TOKEN=7369201109:AAFCU6umw6bA7RVd-2JbhDnxt5QeiEF7ueQ
COINPAYMENTS_API_KEY=cp_api_key_xxxxxxxxxxxx
COINPAYMENTS_IPN_SECRET=YourSecureIPNSecret2025!@#

# Payment Plans
PAYMENT_PLAN_1MONTH_PRICE=29.99
PAYMENT_PLAN_3MONTH_PRICE=79.99
PAYMENT_PLAN_1YEAR_PRICE=299.99

# Server Configuration
PORT=5000
FLASK_ENV=production
```

**Note:** Railway will automatically set `WEBHOOK_BASE_URL` to your app URL.

### **4.4 Deploy the Application**
1. Railway will start building automatically
2. Go to **"Deploy"** tab to monitor progress
3. Wait for "Build Completed Successfully"
4. Your app will be available at: `https://your-app-name.railway.app`

---

## 🔗 **Step 5: Configure CoinPayments Webhook**

### **5.1 Set Webhook URL**
1. Go back to CoinPayments.net dashboard
2. Go to **"Account"** → **"API Keys"**
3. Find your API key and click **"Edit"**
4. Set **IPN URL** to: `https://your-railway-app.railway.app/webhook/coinpayments`
5. Click **"Save"**

### **5.2 Verify Webhook**
Test your webhook URL:
- Go to: `https://your-railway-app.railway.app/webhook/test`
- You should see: `{"status": "Webhook server is running", "timestamp": "..."}`

---

## 🤖 **Step 6: Start Your Bot Processes**

### **6.1 Start the Webhook Server**
In Railway dashboard:
1. Go to **"Deploy"** tab
2. Railway will automatically start the `web` process (webhook server)
3. Check logs to ensure it's running without errors

### **6.2 Start the Bot Process**
1. In **"Deploy"** tab, click **"Start New Process"**
2. Select **"worker"** process type
3. Set command: `python REAL_COINPAYMENTS_BOT.py`
4. Click **"Start"**

### **6.3 Monitor Both Processes**
- **Web Server**: Handle payment webhooks
- **Worker**: Run the Telegram bot
- Both should show "Running" status with green indicators

---

## ✅ **Step 7: Test Your Integration**

### **7.1 Test Bot Response**
1. Open Telegram and find your bot: `@YourBotName`
2. Send `/start`
3. You should see the welcome message with premium upgrade options

### **7.2 Test Payment Flow**
1. Click **"💎 Upgrade to Premium"**
2. Select a payment plan
3. Choose a cryptocurrency
4. You should see a payment address and amount

### **7.3 Test Webhook**
1. Try the test endpoint: `https://your-app.railway.app/health`
2. Should return: `{"status": "healthy", "service": "crypto-payment-webhook"}`

---

## 🚨 **Step 8: Troubleshooting**

### **Bot Not Starting**
- Check Railway logs for Python errors
- Ensure all environment variables are set
- Verify `requirements.txt` has all dependencies

### **Webhook Not Working**
- Verify CoinPayments IPN URL is correct
- Check Railway webhook server is running
- Look for errors in Railway logs

### **Payment Not Processing**
- Test with a small amount first
- Check CoinPayments dashboard for payment status
- Verify webhook is receiving notifications

### **Database Errors**
- Check if `crypto_bot.db` is being created
- Verify file permissions in Railway
- Look for SQLite errors in logs

---

## 📊 **Step 9: Monitoring & Maintenance**

### **9.1 Check Bot Status**
- Monitor Railway dashboard regularly
- Set up notifications for process failures
- Check bot response time and availability

### **9.2 Monitor Payments**
- Check CoinPayments dashboard for payments
- Monitor your database for user activations
- Set up alerts for payment failures

### **9.3 Update Bot**
- Keep dependencies updated
- Monitor for Telegram Bot API changes
- Update technical analysis indicators as needed

---

## 🎯 **Summary**

After completing these steps, you'll have:
- ✅ **Live crypto payment bot** running 24/7 on Railway
- ✅ **CoinPayments integration** with 1300+ cryptocurrencies
- ✅ **Automatic webhook handling** for payment confirmations
- ✅ **Database tracking** of users and payments
- ✅ **Premium access control** based on payments
- ✅ **Real-time trading signals** with technical analysis

**Your bot will be ready to accept real crypto payments and automatically upgrade users to premium! 🚀**

---

## 🆘 **Need Help?**

If you encounter issues:
1. Check Railway logs for detailed error messages
2. Verify all environment variables are set correctly
3. Test individual components (bot, webhook) separately
4. Ensure CoinPayments API credentials are valid
5. Check that webhook URL is accessible from CoinPayments

The bot includes demo mode for testing if CoinPayments credentials aren't configured yet!