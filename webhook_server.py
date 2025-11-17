#!/usr/bin/env python3
"""
Webhook server for CoinPayments payment confirmations
Handles payment webhooks and activates user subscriptions
"""

from flask import Flask, request, jsonify
import sqlite3
import hmac
import hashlib
import logging
import os
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# CoinPayments IPN Secret
COINPAYMENTS_IPN_SECRET = os.getenv('COINPAYMENTS_IPN_SECRET')

def verify_coinpayments_ipn(form_data, secret):
    """Verify CoinPayments IPN signature"""
    try:
        # Get the merchant's signature from form data
        merchant_signature = form_data.get('merchant')
        
        # Create the expected signature using HMAC-SHA512
        expected_signature = hmac.new(
            secret.encode('utf-8'),
            str(form_data).encode('utf-8'),
            hashlib.sha512
        ).hexdigest()
        
        return merchant_signature == expected_signature
        
    except Exception as e:
        logger.error(f"IPN verification error: {e}")
        return False

def update_payment_status(payment_id, user_id, status, amount_crypto, currency):
    """Update payment status and activate user"""
    try:
        conn = sqlite3.connect('crypto_bot.db')
        cursor = conn.cursor()
        
        # Update payment status
        cursor.execute('''
            UPDATE payments SET payment_status = ?, confirmed_at = ?
            WHERE transaction_id = ? AND telegram_id = ?
        ''', (status, datetime.now(), payment_id, user_id))
        
        if cursor.rowcount == 0:
            logger.warning(f"Payment not found: {payment_id}")
            return False
        
        # Get payment plan
        cursor.execute('''
            SELECT payment_plan FROM payments WHERE transaction_id = ?
        ''', (payment_id,))
        payment_plan = cursor.fetchone()
        
        if payment_plan:
            plan_id = payment_plan[0]
            
            # Set premium duration based on plan
            plan_durations = {
                '1month': 30,
                '3months': 90,
                '1year': 365
            }
            
            duration_days = plan_durations.get(plan_id, 30)
            expires_at = datetime.now().timestamp() + (duration_days * 24 * 60 * 60)
            
            # Activate premium access
            cursor.execute('''
                UPDATE users SET is_premium = 1, premium_expires = ?
                WHERE telegram_id = ?
            ''', (expires_at, user_id))
            
            logger.info(f"Activated premium for user {user_id} until {datetime.fromtimestamp(expires_at)}")
        
        conn.commit()
        conn.close()
        return True
        
    except Exception as e:
        logger.error(f"Database update error: {e}")
        return False

@app.route('/webhook/coinpayments', methods=['POST'])
def coinpayments_webhook():
    """Handle CoinPayments webhook for payment confirmations"""
    try:
        # Get form data from CoinPayments
        form_data = request.form.to_dict()
        
        logger.info(f"Received CoinPayments webhook: {form_data}")
        
        # Verify IPN signature
        if COINPAYMENTS_IPN_SECRET:
            if not verify_coinpayments_ipn(form_data, COINPAYMENTS_IPN_SECRET):
                logger.warning("Invalid IPN signature - rejecting webhook")
                return jsonify({"error": "Invalid signature"}), 400
        else:
            logger.warning("No IPN secret configured - webhook not verified")
        
        # Extract payment information
        payment_id = form_data.get('payment_id')
        user_id = int(form_data.get('ipn_data', 0))
        status = int(form_data.get('status', 0))
        amount_crypto = form_data.get('amount1', '0')
        currency = form_data.get('currency1', 'USD')
        
        if not payment_id or not user_id:
            logger.error("Missing payment_id or user_id in webhook")
            return jsonify({"error": "Missing required fields"}), 400
        
        # Check payment status
        if status == 100:  # Payment confirmed
            success = update_payment_status(
                payment_id=payment_id,
                user_id=user_id,
                status='confirmed',
                amount_crypto=amount_crypto,
                currency=currency
            )
            
            if success:
                logger.info(f"Payment confirmed for user {user_id}: {payment_id}")
                return jsonify({"status": "confirmed"}), 200
            else:
                logger.error(f"Failed to update payment for user {user_id}")
                return jsonify({"error": "Update failed"}), 500
        
        elif status == 0:  # Payment pending
            logger.info(f"Payment pending for user {user_id}: {payment_id}")
            return jsonify({"status": "pending"}), 200
        
        else:
            logger.info(f"Payment status {status} for user {user_id}: {payment_id}")
            return jsonify({"status": "unknown"}), 200
        
    except Exception as e:
        logger.error(f"Webhook processing error: {e}")
        return jsonify({"error": "Server error"}), 500

@app.route('/webhook/test', methods=['GET'])
def test_webhook():
    """Test webhook endpoint"""
    return jsonify({"status": "Webhook server is running", "timestamp": datetime.now().isoformat()})

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({"status": "healthy", "service": "crypto-payment-webhook"})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
