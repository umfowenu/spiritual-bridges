from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import requests
import os

class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        try:
            # Get request body
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data.decode('utf-8'))
            
            # Extract message
            message = data.get('message', '')
            
            # Parse spiritual guidance message
            if 'Watch' in message and 'youtu' in message:
                # Extract video info from formatted message
                parts = message.split(' - ')
                video_info = parts[0].replace('🎥 ', '').replace('Watch ', '')
                reason = parts[1] if len(parts) > 1 else 'Spiritual guidance'
                youtube_url = parts[-1] if 'youtu' in parts[-1] else 'https://youtube.com'
                
                # Extract title and duration
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
                # Simple message format
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
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(json.dumps({
                    "success": True,
                    "message": "✅ Notification sent to phone successfully!"
                }).encode())
            else:
                raise Exception(f"Webhook failed with status {response.status_code}")
                
        except Exception as e:
            self.send_response(500)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps({
                "success": False,
                "error": f"❌ Failed to send notification: {str(e)}"
            }).encode())
    
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
    
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(b"Spiritual Guidance Bridge is running! Send POST requests here.")

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    server = HTTPServer(('0.0.0.0', port), handler)
    print(f"Server running on port {port}")
    server.serve_forever()
