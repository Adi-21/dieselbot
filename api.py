from flask import Flask, request, jsonify
from flask_cors import CORS
import logging
import os

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@app.route('/echo', methods=['POST'])
def echo():
    try:
        # Get the request data
        data = request.get_json(force=True)
        
        # Log the received data
        logger.info(f"Received data: {data}")
        
        # Return the same data with 200 status code
        return jsonify({
            "status": "success",
            "message": "Data echoed successfully",
            "data": data
        }), 200
        
    except Exception as e:
        # Log the error
        logger.error(f"Error processing request: {str(e)}")
        
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

if __name__ == '__main__':
    # Get port from environment variable or default to 10000
    port = int(os.getenv('PORT', 10000))
    app.run(host='0.0.0.0', port=port)