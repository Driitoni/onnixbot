# 🪙 NOWPayments Integration Guide
## Complete Setup for Crypto Payment Bot

### 🎯 **Why NOWPayments?**
- **300+ cryptocurrencies** supported (BTC, ETH, USDT, LTC, BCH, SOL, ADA, MATIC, SHIB, and more)
- **Simple API** with excellent documentation
- **Low fees**: 0.5% per payment
- **No KYC required** for receiving payments
- **Fast setup** with instant approval
- **Great Webhook system** for payment notifications
- **99.99% uptime** with 350ms response time

---

## 📋 **Step 1: NOWPayments Account Setup**

### **1.1 Create Account**
1. Go to https://account.nowpayments.io/create-account
2. Complete registration with email verification
3. Sign in to your dashboard

### **1.2 Get API Credentials**
1. In NOWPayments dashboard, go to **"Dashboard"**
2. Click **"Add new key"** to create API key
3. Save the API key (starts with `np_`)
4. Go to **"Store Settings"** → **"IPN Secret"**
5. Generate IPN secret key
6. Save both credentials:
   - **API Key**: `np_api_key_xxxxxxxxxxxx`
   - **IPN Secret**: Generate a strong random string

---

## 💻 **Step 2: Bot Code Integration**

### **2.1 Install Required Packages**
```bash
pip install python-telegram-bot==22.5 yfinance==0.2.66 pandas>=2.2.0 numpy>=1.24.0 python-dotenv>=1.2.0 requests>=2.31.0 cryptography>=41.0.0 qrcode>=7.4.0 flask>=2.3.0
```

### **2.2 Environment Configuration (.env)**
```bash
# Telegram Bot
TELEGRAM_BOT_TOKEN=7369201109:AAFCU6umw6bA7RVd-2JbhDnxt5QeiEF7ueQ

# NOWPayments Configuration
NOWPAYMENTS_API_KEY=np_api_key_xxxxxxxxxxxx
NOWPAYMENTS_IPN_SECRET=YourSecureIPNSecret2025!@#

# Webhook URL (will be your Railway app URL)
WEBHOOK_BASE_URL=https://your-railway-app.railway.app

# Payment Plans (USD prices)
PAYMENT_PLAN_1MONTH_PRICE=29.99
PAYMENT_PLAN_3MONTH_PRICE=79.99
PAYMENT_PLAN_1YEAR_PRICE=299.99
```

---

## 🔌 **Step 3: NOWPayments API Integration**

### **3.1 Supported Cryptocurrencies**
NOWPayments supports 300+ cryptocurrencies including:
- **Major Coins**: BTC, ETH, LTC, BCH, XRP, DOT, ADA, SOL
- **Stablecoins**: USDT, USDC, BUSD, DAI, TUSD
- **DeFi Tokens**: MATIC, UNI, AAVE, COMP, SNX
- **Meme Coins**: DOGE, SHIB, PEPE, BONK
- **And many more!**

### **3.2 Payment Creation Process**
```python
# Create payment with NOWPayments API
payload = {
    'price_amount': 29.99,           # USD amount
    'price_currency': 'usd',         # Base currency
    'pay_currency': 'btc',           # Payment currency
    'pay_amount': 0.000025,          # Crypto amount
    'order_id': f"premium_{user_id}", # Unique order ID
    'order_description': "Premium Plan",
    'ipn_callback_url': f"{webhook_url}/webhook/nowpayments",
    'ipn_data': str(user_id)         # Pass user ID for tracking
}

# API call to NOWPayments
response = requests.post(
    'https://api.nowpayments.io/v1/payment',
    headers={'x-api-key': api_key},
    json=payload
)
```

### **3.3 Payment Status Handling**
NOWPayments sends webhooks with these statuses:
- `waiting` - Payment pending
- `partially_paid` - Partial payment received
- `finished` - Payment completed successfully
- `expired` - Payment expired

---

## 🌐 **Step 4: Webhook Server for Payment Confirmations**

### **4.1 Webhook Endpoint**
Your webhook URL: `https://your-railway-app.railway.app/webhook/nowpayments`

### **4.2 Set Webhook in NOWPayments**
1. Go to NOWPayments → Store Settings → IPN (webhook) URLs
2. Add your webhook URL: `https://your-railway-app.railway.app/webhook/nowpayments`
3. Enable signature verification with your IPN secret

### **4.3 Webhook Handler Code**
```python
@app.route('/webhook/nowpayments', methods=['POST'])
def nowpayments_webhook():
    # Verify signature for security
    signature = request.headers.get('NOWPAYMENTS-IPN-SIGNATURE')
    if not verify_signature(data, ipn_secret, signature):
        return jsonify({"error": "Invalid signature"}), 400
    
    # Process payment
    payment_id = data['payment_id']
    user_id = int(data['ipn_data'])
    status = data['order_status']
    
    if status == 'finished':
        # Activate premium access for user
        activate_premium(user_id, payment_id)
        
    return jsonify({"status": "processed"})
```

---

## 🚀 **Step 5: Railway Deployment**

### **5.1 Prepare Files for Railway**

**Files in your project:**
- `REAL_NOWPAYMENTS_BOT.py` - Main bot with NOWPayments integration
- `nowpayments_webhook_server.py` - Webhook server
- `requirements.txt` - Python dependencies
- `Procfile` - Railway process configuration
- `.env` - Environment variables

### **5.2 Deploy to Railway**
1. Create GitHub repository: `crypto-payment-bot`
2. Go to https://railway.app
3. Sign up with GitHub
4. Click "New Project" → "Deploy from GitHub repo"
5. Select your repository

### **5.3 Configure Environment Variables in Railway**
```
TELEGRAM_BOT_TOKEN=7369201109:AAFCU6umw6bA7RVd-2JbhDnxt5QeiEF7ueQ
NOWPAYMENTS_API_KEY=np_api_key_xxxxxxxxxxxx
NOWPAYMENTS_IPN_SECRET=YourSecureIPNSecret2025!@#
PAYMENT_PLAN_1MONTH_PRICE=29.99
PAYMENT_PLAN_3MONTH_PRICE=79.99
PAYMENT_PLAN_1YEAR_PRICE=299.99
PORT=5000
FLASK_ENV=production
```

### **5.4 Start Processes in Railway**
1. **Webhook server** starts automatically (web process)
2. **Bot process**: worker → `python REAL_NOWPAYMENTS_BOT.py`

---

## ✅ **Step 6: Testing Your Integration**

### **6.1 Test API Connection**
```python
# Test NOWPayments API connection
nowpayments = NOWPaymentsAPI(api_key, ipn_secret)
currencies = nowpayments.get_supported_currencies()
print(f"Supported currencies: {len(currencies)}")
```

### **6.2 Test Bot Response**
1. Start bot in Railway
2. Send `/start` to your Telegram bot
3. Try upgrading to premium
4. Should see payment options with real crypto amounts

### **6.3 Test Webhook**
- Visit: `https://your-app.railway.app/webhook/test`
- Should return: `"NOWPayments webhook server is running"`

### **6.4 Test Payment Flow**
1. Select payment plan
2. Choose cryptocurrency
3. Get payment address and amount
4. Send small test payment
5. Check webhook logs in Railway

---

## 🔒 **Step 7: Security Best Practices**

### **7.1 API Security**
- Keep API keys in environment variables
- Never commit credentials to GitHub
- Use HTTPS for webhook URLs
- Verify webhook signatures

### **7.2 Payment Security**
- Minimum payment verification
- Double-check amounts before activation
- Monitor for suspicious activity
- Implement rate limiting

### **7.3 Data Security**
- Encrypt sensitive data
- Regular database backups
- Monitor for unauthorized access
- Update dependencies regularly

---

## 📊 **Step 8: Monitoring & Analytics**

### **8.1 Track Payments**
- Monitor NOWPayments dashboard
- Check Railway logs for webhook activity
- Track user activations in database
- Monitor failed payments

### **8.2 Performance Metrics**
- Bot response time
- Payment success rate
- User conversion rate
- Revenue tracking

---

## 🎯 **Summary**

With NOWPayments integration, you'll have:
- ✅ **300+ cryptocurrencies** supported
- ✅ **Simple API** with clear documentation
- ✅ **0.5% fees** (very competitive)
- ✅ **Fast setup** with instant approval
- ✅ **Automatic webhook verification**
- ✅ **Real-time payment tracking**
- ✅ **Database integration** for user management

**Next Steps:**
1. Get NOWPayments API credentials (5 minutes)
2. Update your bot files with NOWPayments integration
3. Deploy to Railway
4. Configure webhook URL
5. Test with small payment

**Total setup time: ~15 minutes** ⏱️

Your bot will be ready to accept real crypto payments and automatically upgrade users to premium! 🚀

---

## 🆘 **Support & Resources**

- **NOWPayments Documentation**: https://documenter.getpostman.com/view/7907941/2s93JusNJt
- **API Status**: https://status.nowpayments.io
- **Support**: https://nowpayments.io/help
- **Developer Docs**: https://nowpayments.io/help/api
