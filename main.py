from flask import Flask, request, jsonify
import requests
import os
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)

app = Flask(__name__)

@app.route('/')
def health_check():
    """Health check endpoint required by Railway"""
    return "Spiritual Guidance Bridge is running! Send POST requests to /bridge"

@app.route('/bridge', methods=['POST'])
def bridge():
    try:
        data = request.get_json()
        message = data.get('message', '')
        
        # Parse spiritual guidance message
        if 'Watch' in message and 'youtu' in message:
            parts = message.split(' - ')
            video_info = parts[0].replace('🎥 ', '').replace('Watch ', '')
            reason = parts[1] if len(parts) > 1 else 'Spiritual guidance'
            youtube_url = parts[-1] if 'youtu' in parts[-1] else 'https://youtube.com'
            
            if '(' in video_info and ')' in video_info:
                title = video_info.split('(')[0].strip()
                duration = video_info.split('(')[1].split(')')[0]
            else:
                title = video_info
                duration = 'N/A'
            
            webhook_data = {
                "title": "Spiritual Guidance",
                "video_title": title,
                "duration": duration,
                "reason": reason,
                "youtube_url": youtube_url,
                "priority": 0
            }
        else:
            webhook_data = {
                "title": "Spiritual Message",
                "video_title": "Daily Guidance",
                "duration": "reminder",
                "reason": message,
                "youtube_url": "https://youtube.com",
                "priority": 0
            }
        
        # Send to Make.com webhook - REPLACE WITH YOUR ACTUAL WEBHOOK URL
        make_webhook_url = "YOUR_MAKE_WEBHOOK_URL"
        
        response = requests.post(make_webhook_url, json=webhook_data, timeout=10)
        
        if response.status_code == 200:
            logging.info("Notification sent successfully")
            return jsonify({
                "success": True,
                "message": "✅ Notification sent to phone successfully!"
            })
        else:
            raise Exception(f"Webhook failed with status {response.status_code}")
            
    except Exception as e:
        logging.error(f"Bridge error: {str(e)}")
        return jsonify({
            "success": False,
            "error": f"❌ Failed to send notification: {str(e)}"
        }), 500

if __name__ == '__main__':
    logging.info("Starting Spiritual Guidance Bridge Service...")
    # Railway assigns PORT environment variable automatically (usually 8080)
    port = int(os.environ.get('PORT', 8080))  # Changed default to 8080
    app.run(host='0.0.0.0', port=port, debug=False)
