from flask import Flask, request, jsonify
import json
import hashlib
import hmac
import sqlite3
from datetime import datetime
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Database setup
def init_db():
    conn = sqlite3.connect('bot_database.db')
    cursor = conn.cursor()
    
    # Users table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY,
            telegram_id INTEGER UNIQUE,
            username TEXT,
            first_name TEXT,
            last_access TIMESTAMP,
            access_level TEXT DEFAULT 'free',
            subscription_start TIMESTAMP,
            subscription_end TIMESTAMP,
            payment_verified BOOLEAN DEFAULT FALSE
        )
    ''')
    
    # Payments table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS payments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            telegram_id INTEGER,
            payment_plan TEXT,
            amount_crypto REAL,
            crypto_currency TEXT,
            transaction_id TEXT,
            payment_status TEXT DEFAULT 'pending',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            confirmed_at TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (user_id)
        )
    ''')
    
    conn.commit()
    conn.close()

@app.route('/webhook/coinpayments', methods=['POST'])
def coinpayments_webhook():
    """Handle CoinPayments webhook"""
    try:
        # Get webhook data
        data = request.get_json()
        
        # Verify webhook (CoinPayments specific)
        ipn_secret = os.getenv('PAYMENT_IPN_SECRET')
        expected_hmac = hmac.new(
            ipn_secret.encode('utf-8'),
            request.get_data(),
            hashlib.sha512
        ).hexdigest()
        
        if 'hmac' not in data or data['hmac'] != expected_hmac:
            return jsonify({"error": "Invalid HMAC"}), 401
        
        # Extract payment information
        transaction_id = data.get('txn_id')
        status = data.get('status')  # 0 = pending, 1 = complete, -1 = cancelled
        amount1 = float(data.get('amount1', 0))  # Original amount
        amount2 = float(data.get('amount2', 0))  # Received amount
        currency1 = data.get('currency1')  # Original currency
        currency2 = data.get('currency2')  # Received currency
        order_id = data.get('order_id')
        
        # Update payment in database
        if update_payment_status(transaction_id, status, amount2, currency2):
            return jsonify({"status": "success"})
        else:
            return jsonify({"status": "error"}), 400
            
    except Exception as e:
        print(f"CoinPayments webhook error: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/webhook/nowpayments', methods=['POST'])
def nowpayments_webhook():
    """Handle NOWPayments webhook"""
    try:
        data = request.get_json()
        
        # Verify webhook signature
        ipn_secret = os.getenv('NOWPAYMENTS_IPN_SECRET')
        signature = request.headers.get('x-nowpayments-sig')
        
        if not verify_nowpayments_signature(data, signature, ipn_secret):
            return jsonify({"error": "Invalid signature"}), 401
        
        # Extract payment information
        payment_id = data.get('payment_id')
        order_id = data.get('order_id')
        payment_status = data.get('payment_status')  # finished, waiting, confirming
        actual_amount = float(data.get('actual_amount', 0))
        actual_currency = data.get('actual_currency')
        
        # Update payment status
        if update_payment_status(payment_id, payment_status, actual_amount, actual_currency):
            return jsonify({"status": "success"})
        else:
            return jsonify({"status": "error"}), 400
            
    except Exception as e:
        print(f"NOWPayments webhook error: {e}")
        return jsonify({"error": str(e)}), 500

def verify_nowpayments_signature(data, signature, secret):
    """Verify NOWPayments webhook signature"""
    try:
        payload = json.dumps(data)
        expected_signature = hmac.new(
            secret.encode('utf-8'),
            payload.encode('utf-8'),
            hashlib.sha512
        ).hexdigest()
        return hmac.compare_digest(signature, expected_signature)
    except:
        return False

def update_payment_status(transaction_id, status, amount, currency):
    """Update payment status in database"""
    try:
        conn = sqlite3.connect('bot_database.db')
        cursor = conn.cursor()
        
        # Determine if payment is successful
        if status in [1, 'finished', 'confirmed']:  # Completed
            payment_status = 'confirmed'
            
            # Get payment details
            cursor.execute('''
                SELECT telegram_id, payment_plan FROM payments 
                WHERE transaction_id = ?
            ''', (transaction_id,))
            payment_info = cursor.fetchone()
            
            if payment_info:
                telegram_id, plan_id = payment_info
                
                # Activate user access
                plan_durations = {
                    '1_month': 30,
                    '3_months': 90,
                    '1_year': 365
                }
                
                duration = plan_durations.get(plan_id, 30)
                subscription_end = datetime.now().timestamp() + (duration * 24 * 60 * 60)
                
                # Create or update user
                cursor.execute('''
                    INSERT OR REPLACE INTO users (telegram_id, access_level, subscription_start, subscription_end, payment_verified)
                    VALUES (?, 'premium', ?, ?, ?)
                ''', (telegram_id, datetime.now().isoformat(), datetime.fromtimestamp(subscription_end).isoformat(), True))
        
        # Update payment record
        cursor.execute('''
            UPDATE payments 
            SET payment_status = ?, confirmed_at = ?
            WHERE transaction_id = ?
        ''', (payment_status if payment_status else 'pending', datetime.now().isoformat(), transaction_id))
        
        conn.commit()
        conn.close()
        return True
        
    except Exception as e:
        print(f"Database update error: {e}")
        return False

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({"status": "healthy", "timestamp": datetime.now().isoformat()})

@app.route('/payments/status/<transaction_id>', methods=['GET'])
def get_payment_status(transaction_id):
    """Get payment status by transaction ID"""
    try:
        conn = sqlite3.connect('bot_database.db')
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT payment_status, amount_crypto, crypto_currency, created_at 
            FROM payments WHERE transaction_id = ?
        ''', (transaction_id,))
        
        result = cursor.fetchone()
        conn.close()
        
        if result:
            return jsonify({
                "transaction_id": transaction_id,
                "status": result[0],
                "amount": result[1],
                "currency": result[2],
                "created_at": result[3]
            })
        else:
            return jsonify({"error": "Transaction not found"}), 404
            
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    init_db()
    print("🚀 Payment webhook server starting...")
    print("📡 Webhook endpoints ready:")
    print("   - POST /webhook/coinpayments")
    print("   - POST /webhook/nowpayments") 
    print("   - GET /health")
    print("   - GET /payments/status/{transaction_id}")
    app.run(host='0.0.0.0', port=5000, debug=False)