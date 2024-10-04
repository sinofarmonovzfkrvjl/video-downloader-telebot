# setup_webhook.py

import requests
from flask import Flask, request
from main import process_update, API_TOKEN, types  # Import the function to process updates

WEBHOOK_URL = "https://video-downloader-telebot.onrender.com/webhook"  # Replace with your ngrok URL

# Set up Flask app
app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def webhook():  
    json_str = request.get_data(as_text=True)
    update = types.Update.de_json(json_str)
    process_update(update)  # Call the imported function to process the update
    return 'OK', 200

# Set the webhook
def set_webhook():
    url = f"https://api.telegram.org/bot{API_TOKEN}/setWebhook"
    payload = {"url": WEBHOOK_URL}
    response = requests.post(url, json=payload)
    print(response.json())  # Print the response for debugging

if __name__ == '__main__':
    set_webhook()  # Set the webhook when the script runs
    app.run(host='0.0.0.0', port=8080)  # Change the port if needed
