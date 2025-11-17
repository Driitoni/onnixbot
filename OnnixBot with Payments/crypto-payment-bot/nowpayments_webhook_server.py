#!/usr/bin/env python3
"""
Webhook server for NOWPayments payment confirmations
Handles payment webhooks and activates user subscriptions
"""

from flask import Flask, request, jsonify
import sqlite3
import hashlib
import hmac
import logging
import os
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# NOWPayments IPN Secret
NOWPAYMENTS_IPN_SECRET = os.getenv('NOWPAYMENTS_IPN_SECRET')

def verify_nowpayments_ipn(data, secret):
    """Verify NOWPayments IPN signature"""
    try:
        # NOWPayments sends data as form-encoded, convert to dict
        if hasattr(data, 'to_dict'):
            form_data = data.to_dict()
        else:
            form_data = data
        
        # Get signature from headers
        signature = request.headers.get('NOWPAYMENTS-IPN-SIGNATURE', '')
        
        # Create expected signature using HMAC-SHA512
        message = json.dumps(form_data, separators=(',', ':'))
        expected_signature = hmac.new(
            secret.encode('utf-8'),
            message.encode('utf-8'),
            hashlib.sha512
        ).hexdigest()
        
        logger.info(f"Received signature: {signature}")
        logger.info(f"Expected signature: {expected_signature}")
        
        return signature == expected_signature
        
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
        
        # Get payment plan from database
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

@app.route('/webhook/nowpayments', methods=['POST'])
def nowpayments_webhook():
    """Handle NOWPayments webhook for payment confirmations"""
    try:
        # Get form data from NOWPayments
        form_data = request.form.to_dict()
        
        logger.info(f"Received NOWPayments webhook: {form_data}")
        
        # Verify IPN signature
        if NOWPAYMENTS_IPN_SECRET:
            if not verify_nowpayments_ipn(form_data, NOWPAYMENTS_IPN_SECRET):
                logger.warning("Invalid IPN signature - rejecting webhook")
                return jsonify({"error": "Invalid signature"}), 400
        else:
            logger.warning("No IPN secret configured - webhook not verified")
        
        # Extract payment information
        payment_id = form_data.get('payment_id')
        user_id = int(form_data.get('ipn_data', 0))
        order_status = form_data.get('order_status', '')
        pay_amount = form_data.get('pay_amount', '0')
        pay_currency = form_data.get('pay_currency', 'USD')
        
        if not payment_id or not user_id:
            logger.error("Missing payment_id or user_id in webhook")
            return jsonify({"error": "Missing required fields"}), 400
        
        # Check payment status (NOWPayments order statuses)
        if order_status == 'finished':  # Payment completed
            success = update_payment_status(
                payment_id=payment_id,
                user_id=user_id,
                status='confirmed',
                amount_crypto=pay_amount,
                currency=pay_currency
            )
            
            if success:
                logger.info(f"Payment confirmed for user {user_id}: {payment_id}")
                return jsonify({"status": "confirmed"}), 200
            else:
                logger.error(f"Failed to update payment for user {user_id}")
                return jsonify({"error": "Update failed"}), 500
        
        elif order_status == 'waiting':  # Payment pending
            logger.info(f"Payment pending for user {user_id}: {payment_id}")
            return jsonify({"status": "pending"}), 200
        
        elif order_status == 'partially_paid':  # Partial payment
            logger.info(f"Payment partially paid for user {user_id}: {payment_id}")
            return jsonify({"status": "partially_paid"}), 200
        
        elif order_status == 'expired':  # Payment expired
            logger.info(f"Payment expired for user {user_id}: {payment_id}")
            return jsonify({"status": "expired"}), 200
        
        else:
            logger.info(f"Unknown payment status {order_status} for user {user_id}: {payment_id}")
            return jsonify({"status": "unknown"}), 200
        
    except Exception as e:
        logger.error(f"Webhook processing error: {e}")
        return jsonify({"error": "Server error"}), 500

@app.route('/webhook/test', methods=['GET'])
def test_webhook():
    """Test webhook endpoint"""
    return jsonify({
        "status": "NOWPayments webhook server is running",
        "service": "crypto-payment-webhook",
        "timestamp": datetime.now().isoformat()
    })

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy", 
        "service": "crypto-payment-webhook",
        "provider": "NOWPayments"
    })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
