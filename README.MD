# 🚀 Webhook to Adaptive Card for Webex Integration

This is a sample Python application that demonstrates how to receive a webhook and convert the data into an adaptive card that is posted into a Webex space by a Webex bot. The application showcases a rocket launch notification system with rich, interactive cards that provide detailed mission information.

## ✨ Features

- **🔗 Webhook Reception** - RESTful endpoint for receiving external webhook data
- **🎴 Adaptive Card Generation** - Dynamic creation of rich, interactive cards
- **🤖 Webex Bot Integration** - Automated posting to Webex spaces
- **🚀 Rocket Launch Theme** - Example implementation with space mission data
- **⚡ Flask Web Framework** - Lightweight, scalable web server
- **🔧 Environment Configuration** - Secure credential management
- **📊 Status Monitoring** - Health check endpoint for service monitoring

## 📋 Prerequisites

- Python 3.6+
- Flask
- Requests
- Adaptive Card JSON schema

## 🚀 Getting Started

### Installation & Setup

1. **Clone this repository:**
   ```bash
   git clone <repository-url>
   cd webhook-to-card
   ```

2. **Install the required packages:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure environment variables:**
   - Rename `.env.example` to `.env`
   - Replace the variables with your own values:
     - `WEBEX_ACCESS_TOKEN`: Your Webex bot access token
     - `WEBEX_ROOM_ID`: The ID of the Webex room where the adaptive card will be posted

4. **Start the application:**
   ```bash
   python app.py
   ```

5. **Test the webhook endpoint:**
   Send a POST request to the `/webhook` endpoint with a JSON payload that contains the data for the adaptive card.

   Example:
   ```bash
   curl -X POST -H "Content-Type: application/json" -d @webhook-payload.json http://localhost:5000/webhook
   ```

6. **Verify the result:**
   The application will parse the JSON payload, generate an adaptive card, and post it into the Webex room specified by `WEBEX_ROOM_ID`.

## 📖 Usage Guide

### Webhook Payload Structure

The application expects a specific JSON structure for rocket launch data:

```json
{
    "event": "rocket_launch",
    "data": {
        "rocket_name": "Falcon 9 Webex",
        "payload_type": "Satellite",
        "payload_description": "Communications satellite for commercial use",
        "launch_time": "2023-03-25T16:30:00Z",
        "launch_site": "Cape Canaveral, FL",
        "mission_patch": "https://example.com/mission_patch.png",
        "video_stream": "https://example.com/live_stream.mp4"
    }
}
```

### Environment Configuration

Create a `.env` file with the following variables:

```bash
# Webex Bot Token (from developer.webex.com)
WEBEX_BOT_TOKEN=your_bot_access_token_here

# Target Webex Room ID
WEBEX_ROOM_ID=your_room_id_here
```

### Testing the Integration

1. **Check Service Status:**
   ```bash
   curl http://localhost:5000/status
   ```

2. **Send Test Webhook:**
   ```bash
   curl -X POST \
     -H "Content-Type: application/json" \
     -d @webhook-payload.json \
     http://localhost:5000/webhook
   ```

3. **Verify in Webex:**
   - Check your configured Webex space
   - Look for the adaptive card with rocket launch details
   - Interact with the "Watch the Launch" button

## 🏗️ Project Structure

```
webhook-to-card/
├── app.py                     # Main Flask application
├── requirements.txt           # Python dependencies
├── .env.example              # Environment variables template
├── webhook-payload.json      # Sample webhook data
├── adaptive_card.json        # Example adaptive card structure
├── templates/
│   └── status.html           # Status page template
├── .gitignore                # Git ignore patterns
├── LICENSE                   # Cisco Sample Code License
└── README.MD                 # This documentation
```

### Core Components

| Component | Description | File Location |
|-----------|-------------|---------------|
| **Flask App** | Main web server and routing | [`app.py`](app.py) |
| **Webhook Handler** | Processes incoming webhook data | [`app.py`](app.py) lines 20-131 |
| **Card Generator** | Creates adaptive card from data | [`app.py`](app.py) lines 36-111 |
| **Webex Integration** | Posts cards to Webex spaces | [`app.py`](app.py) lines 114-131 |
| **Status Monitor** | Health check endpoint | [`app.py`](app.py) lines 134-136 |

## 🔧 Code Implementation

### Flask Application Setup

```python
from flask import Flask, request, jsonify, render_template
from dotenv import load_dotenv
import os, json, requests

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Webex API configuration
api_url = "https://webexapis.com/v1/messages"
headers = {
    "Content-Type": "application/json",
    "Authorization": "Bearer " + os.getenv("WEBEX_BOT_TOKEN")
}
```

### Webhook Processing

```python
@app.route("/webhook", methods=["POST"])
def handle_webhook():
    # Extract webhook data
    webhook = request.get_json()
    data = webhook["data"]
    
    # Parse rocket launch details
    rocket_name = data["rocket_name"]
    payload_type = data["payload_type"]
    payload_description = data["payload_description"]
    launch_time = data["launch_time"]
    launch_site = data["launch_site"]
    mission_patch = data["mission_patch"]
    video_stream = data["video_stream"]
```

### Adaptive Card Generation

```python
# Dynamic card payload creation
card_payload = {
    "$schema": "http://adaptivecards.io/schemas/adaptive-card.json",
    "type": "AdaptiveCard",
    "version": "1.3",
    "body": [
        {
            "type": "TextBlock",
            "text": "Rocket Launch Successful!",
            "weight": "Bolder",
            "size": "Large",
            "color": "Accent",
            "wrap": True
        },
        {
            "type": "ColumnSet",
            "columns": [
                {
                    "type": "Column",
                    "width": "auto",
                    "items": [
                        {
                            "type": "Image",
                            "url": mission_patch,
                            "size": "Small",
                            "style": "Person"
                        }
                    ]
                },
                {
                    "type": "Column",
                    "width": "stretch",
                    "items": [
                        {
                            "type": "TextBlock",
                            "text": "Rocket Launch Details",
                            "weight": "Bolder",
                            "wrap": True
                        },
                        {
                            "type": "FactSet",
                            "facts": [
                                {
                                    "title": "Rocket Name",
                                    "value": rocket_name
                                },
                                {
                                    "title": "Payload Type",
                                    "value": payload_type
                                },
                                {
                                    "title": "Launch Time",
                                    "value": launch_time
                                },
                                {
                                    "title": "Launch Site",
                                    "value": launch_site
                                }
                            ]
                        }
                    ]
                }
            ]
        }
    ],
    "actions": [
        {
            "type": "Action.OpenUrl",
            "title": "Watch the Launch",
            "url": video_stream
        }
    ]
}
```

### Webex API Integration

```python
# Message payload for Webex
message_payload = {
    "roomId": os.getenv("WEBEX_ROOM_ID"),
    "attachments": [
        {
            "contentType": "application/vnd.microsoft.card.adaptive",
            "content": card_payload
        }
    ],
    "text": "New Rocket Launch Detected"
}

# Send to Webex API
response = requests.post(api_url, headers=headers, json=message_payload)
```

## 🎴 Adaptive Card Features

### Card Structure

The generated adaptive card includes:

1. **Header Section:**
   - Bold title: "Rocket Launch Successful!"
   - Accent color for visual emphasis
   - Large size for prominence

2. **Content Layout:**
   - Two-column design with mission patch and details
   - Mission patch image (left column)
   - Fact set with structured data (right column)

3. **Interactive Elements:**
   - "Watch the Launch" action button
   - Opens video stream in new window/tab

### Fact Set Data

| Field | Description | Source |
|-------|-------------|--------|
| **Rocket Name** | Launch vehicle identifier | `data.rocket_name` |
| **Payload Type** | Cargo classification | `data.payload_type` |
| **Payload Description** | Mission details | `data.payload_description` |
| **Launch Time** | ISO 8601 timestamp | `data.launch_time` |
| **Launch Site** | Geographic location | `data.launch_site` |

### Visual Elements

```json
{
  "type": "Image",
  "url": "mission_patch_url",
  "size": "Small",
  "style": "Person"
}
```

## 🔐 Security Considerations

### Environment Variables

- Store sensitive tokens in `.env` file
- Never commit `.env` to version control
- Use environment-specific configurations

### Bot Token Management

```python
# Secure token loading
headers = {
    "Authorization": "Bearer " + os.getenv("WEBEX_BOT_TOKEN")
}
```

### Input Validation

```python
# Validate webhook structure
webhook = request.get_json()
if "data" not in webhook:
    return jsonify({"error": "Invalid payload"}), 400
```

## 🧪 Testing

### Local Development

1. **Start the Flask server:**
   ```bash
   python app.py
   ```

2. **Test status endpoint:**
   ```bash
   curl http://localhost:5000/status
   # Expected: "Webhook Server Listening"
   ```

3. **Send test webhook:**
   ```bash
   curl -X POST \
     -H "Content-Type: application/json" \
     -d @webhook-payload.json \
     http://localhost:5000/webhook
   ```

### Production Deployment

```python
# For production, configure proper WSGI server
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=False)
```

### Error Handling

```python
# Response validation
if response.ok:
    return jsonify({"success": True}), 200
else:
    return jsonify({
        "success": False, 
        "message": response.text
    }), response.status_code
```

## 🔧 Customization

### Extending the Card Schema

```python
# Add new fields to webhook payload
def extract_additional_data(data):
    return {
        "mission_status": data.get("mission_status", "Unknown"),
        "weather_conditions": data.get("weather", "Clear"),
        "crew_count": data.get("crew_count", 0)
    }
```

### Multiple Card Templates

```python
# Template selection based on event type
def get_card_template(event_type):
    templates = {
        "rocket_launch": create_launch_card,
        "mission_update": create_update_card,
        "abort_sequence": create_abort_card
    }
    return templates.get(event_type, create_default_card)
```

### Custom Webhook Sources

```python
# Support multiple webhook formats
@app.route("/webhook/<source>", methods=["POST"])
def handle_webhook_by_source(source):
    parsers = {
        "spacex": parse_spacex_webhook,
        "nasa": parse_nasa_webhook,
        "generic": parse_generic_webhook
    }
    
    parser = parsers.get(source, parse_generic_webhook)
    return parser(request.get_json())
```

## 📚 Dependencies

### Core Requirements

```txt
Flask==2.2.3              # Web framework
requests==2.28.2          # HTTP library
python-dotenv==1.0.0      # Environment variable management
Jinja2==3.1.2             # Template engine
Werkzeug==2.2.3           # WSGI utilities
```

### Development Tools

```txt
certifi==2022.12.7        # SSL certificate bundle
charset-normalizer==3.0.1 # Character encoding
click==8.1.3              # Command line interface
idna==3.4                 # Internationalized domain names
itsdangerous==2.1.2       # Cryptographic signing
MarkupSafe==2.1.2         # String handling
urllib3==1.26.14          # HTTP client
```

## 🚨 Troubleshooting

### Common Issues

| Issue | Solution |
|-------|----------|
| **401 Unauthorized** | Check WEBEX_BOT_TOKEN validity |
| **404 Room Not Found** | Verify WEBEX_ROOM_ID exists and bot has access |
| **Invalid JSON** | Validate webhook payload structure |
| **Module Not Found** | Run `pip install -r requirements.txt` |

### Debug Mode

```python
# Enable Flask debug mode
if __name__ == "__main__":
    app.run(debug=True)
```

### Logging

```python
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Add to webhook handler
logger.info(f"Received webhook: {webhook}")
logger.info(f"Generated card: {card_payload}")
```

## 🔄 Webhook Integration Examples

### GitHub Actions

```yaml
# .github/workflows/notify-webex.yml
name: Notify Webex on Launch
on:
  push:
    tags: ['v*']
jobs:
  notify:
    runs-on: ubuntu-latest
    steps:
      - name: Send Launch Notification
        run: |
          curl -X POST \
            -H "Content-Type: application/json" \
            -d '{"event":"rocket_launch","data":{"rocket_name":"${{ github.ref_name }}"}}' \
            ${{ secrets.WEBHOOK_URL }}/webhook
```

### External Monitoring

```bash
# Cron job for regular status checks
*/5 * * * * curl -f http://your-domain.com/status || echo "Webhook service down"
```

## 🤝 Contributing

We truly appreciate your contribution to the Webex Samples!

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/card-enhancement`
3. Commit changes: `git commit -am 'Add card feature'`
4. Push to branch: `git push origin feature/card-enhancement`
5. Submit a Pull Request

### Development Guidelines

- Follow PEP 8 Python style guidelines
- Add error handling for new webhook sources
- Test adaptive cards in Webex client
- Update documentation for new features
- Validate JSON schemas for new card types

## 📚 Acknowledgements

This sample application was created using the following resources:

- [Webex API Documentation](https://developer.webex.com/docs/api/getting-started)
- [Adaptive Cards Documentation](https://adaptivecards.io/)
- [ChatGPT](https://chat.openai.com)

### Additional Resources

- [Adaptive Cards Designer](https://adaptivecards.io/designer/)
- [Webex Bot Creation Guide](https://developer.webex.com/docs/bots)
- [Flask Documentation](https://flask.palletsprojects.com/)
- [Python Webhooks Guide](https://webhooks.fyi/)

## 📄 License

This project is licensed under the Cisco Sample Code License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

For technical support and questions:

- **Issues**: Submit via GitHub Issues
- **Adaptive Cards**: [Microsoft Adaptive Cards Documentation](https://docs.microsoft.com/en-us/adaptive-cards/)
- **Webex API**: [Webex Developer Portal](https://developer.webex.com)
- **Community**: [Webex Developer Community](https://developer.webex.com/community)

## Thanks!

Made with ❤️ by the Webex Developer Relations Team at Cisco

---

**Note**: This sample demonstrates webhook-to-card conversion for educational purposes. For production use, implement proper error handling, input validation, and security measures.
