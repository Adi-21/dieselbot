from flask import Flask, request, jsonify
from flask_cors import CORS
import logging
import requests

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Telegram Bot Configuration
BOT_TOKEN = "7499451487:AAEl5raH45sIeEwCTra_gxZ8-UmhsYiq41o"
CHAT_ID = -1002279477839  # Group chat ID extracted from getUpdates response

# Second Telegram Bot Configuration
BOT2_TOKEN = "7950948075:AAHN3BDcVLhZSLbkM8zu2T4XOXyXFJI99Zc"
BOT2_CHAT_ID = -1002321536247

def send_telegram_notification(data):
    """Send a beautifully formatted message to the Telegram bot."""
    try:
        asset = data["data"]["asset_bought"]
        asset_name = asset["name"]
        asset_symbol = asset["symbol"]
        asset_icon = asset["icon"]
        trx_hash = data["data"]["trx_hash"]
        eth_in = data["data"]["eth_in"]
        asset_out = data["data"]["asset_out"]

        # Beautifully format the message with emojis
        message = (
            f"🎉 *New Transaction Notification* 🎉\n\n"
            f"💎 *Asset Bought*: [{asset_name}]({asset_icon})\n"
            f"🔤 *Symbol*: `{asset_symbol}`\n"
            f"📈 *Asset Out*: `{asset_out}`\n"
            f"💰 *ETH In*: `{eth_in}`\n"
            f"🔗 *Transaction Hash*: [View on Fuel Explorer](https://app.fuel.network/tx/{trx_hash})"
        )

        # Telegram API details
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
        payload = {
            "chat_id": CHAT_ID,
            "text": message,
            "parse_mode": "Markdown"  # Enables bold, italic, links, etc.
        }

        # Make the POST request
        response = requests.post(url, json=payload)
        response.raise_for_status()  # Raise exception for HTTP errors
        logger.info("Notification sent successfully")

    except KeyError as e:
        logger.error(f"Missing key in data: {e}")
    except requests.exceptions.RequestException as e:
        logger.error(f"Failed to send Telegram notification: {e}")

def send_telegram_notification_bot2(data):
    """Send a beautifully formatted message to the second Telegram bot."""
    try:
        asset = data["data"]["asset_bought"]
        asset_name = asset["name"]
        asset_symbol = asset["symbol"]
        asset_icon = asset["icon"]
        trx_hash = data["data"]["trx_hash"]
        eth_in = data["data"]["eth_in"]
        asset_out = data["data"]["asset_out"]

        # Beautifully format the message with emojis
        message = (
            f"🎉 *New Transaction Notification* 🎉\n\n"
            f"💎 *Asset Bought*: [{asset_name}]({asset_icon})\n"
            f"🔤 *Symbol*: `{asset_symbol}`\n"
            f"📈 *Asset Out*: `{asset_out}`\n"
            f"💰 *ETH In*: `{eth_in}`\n"
            f"🔗 *Transaction Hash*: [View on Fuel Explorer](https://app.fuel.network/tx/{trx_hash})"
        )

        # Telegram API details
        url = f"https://api.telegram.org/bot{BOT2_TOKEN}/sendMessage"
        payload = {
            "chat_id": BOT2_CHAT_ID,
            "text": message,
            "parse_mode": "Markdown"  # Enables bold, italic, links, etc.
        }

        # Make the POST request
        response = requests.post(url, json=payload)
        response.raise_for_status()  # Raise exception for HTTP errors
        logger.info("Notification sent successfully to bot2")

    except KeyError as e:
        logger.error(f"Missing key in data for bot2: {e}")
    except requests.exceptions.RequestException as e:
        logger.error(f"Failed to send Telegram notification to bot2: {e}")

@app.route('/echo', methods=['POST'])
def echo():
    try:
        # Get the request data
        data = request.get_json(force=True)
        
        # Log the received data
        logger.info(f"Received data: {data}")
        
        # Notify Telegram bot with beautiful format
        send_telegram_notification(data)
        
        # Return the same data with 200 status code
        return jsonify({
            "status": "success",
            "message": "Data echoed successfully",
            "data": data
        }), 200
        
    except Exception as e:
        # Log the error
        logger.error(f"Error processing request: {str(e)}")
        
        # Notify Telegram bot about the error
        send_telegram_notification({
            "data": {
                "asset_bought": {"name": "Error", "symbol": "N/A", "icon": ""},
                "trx_hash": "",
                "eth_in": "N/A",
                "asset_out": "N/A"
            }
        })
        
        # Return error response
        return jsonify({
            "status": "error",
            "message": f"Error processing request: {str(e)}",
            "data": None
        }), 400

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        "status": "success",
        "message": "Service is healthy"
    }), 200

@app.route('/', methods=['GET'])
def home():
    """Root endpoint"""
    return jsonify({
        "status": "success",
        "message": "Welcome to Echo API",
        "endpoints": {
            "echo": "/echo (POST)",
            "health": "/health (GET)"
        }
    }), 200



@app.route('/echo-bot2', methods=['POST'])
def echo_bot2():
    try:
        # Get the request data
        data = request.get_json(force=True)
        
        # Log the received data
        logger.info(f"Received data for bot2: {data}")
        
        # Notify Telegram bot2 with beautiful format
        send_telegram_notification_bot2(data)
        
        # Return the same data with 200 status code
        return jsonify({
            "status": "success",
            "message": "Data echoed successfully to bot2",
            "data": data
        }), 200
        
    except Exception as e:
        # Log the error
        logger.error(f"Error processing request for bot2: {str(e)}")
        
        # Notify Telegram bot2 about the error
        send_telegram_notification_bot2({
            "data": {
                "asset_bought": {"name": "Error", "symbol": "N/A", "icon": ""},
                "trx_hash": "",
                "eth_in": "N/A",
                "asset_out": "N/A"
            }
        })
        
        # Return error response
        return jsonify({
            "status": "error",
            "message": f"Error processing request for bot2: {str(e)}",
            "data": None
        }), 400

if __name__ == '__main__':
    # Run the Flask app
    app.run(host='0.0.0.0', port=10000)
