#!/usr/bin/env python3
"""
Script to help find your Telegram Chat ID
"""
import requests
import os
import json

def get_updates(bot_token):
    """Get updates from Telegram bot to find chat ID"""
    url = f"https://api.telegram.org/bot{bot_token}/getUpdates"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Error: {response.status_code}")
            return None
    except Exception as e:
        print(f"Error fetching updates: {e}")
        return None

def main():
    bot_token = input("Enter your bot token: ").strip()
    
    if not bot_token:
        print("Bot token is required!")
        return
    
    print("Fetching updates...")
    updates = get_updates(bot_token)
    
    if updates and updates.get('ok'):
        updates_list = updates.get('result', [])
        if updates_list:
            print("\nFound chat information:")
            for update in updates_list[-5:]:  # Show last 5 updates
                if 'message' in update:
                    msg = update['message']
                    chat = msg.get('chat', {})
                    chat_id = chat.get('id')
                    first_name = chat.get('first_name', 'Unknown')
                    username = chat.get('username', 'No username')
                    
                    print(f"Chat ID: {chat_id}")
                    print(f"Name: {first_name}")
                    print(f"Username: {username}")
                    print("-" * 30)
        else:
            print("No messages found. Make sure you've sent /start to your bot!")
            print("Instructions:")
            print("1. Open Telegram and start a chat with your bot")
            print("2. Send /start command")
            print("3. Run this script again")
    else:
        print("Failed to get updates. Check your bot token.")

if __name__ == "__main__":
    main()