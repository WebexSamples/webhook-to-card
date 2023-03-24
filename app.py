import os
import json
import requests
from flask import Flask, request, jsonify, render_template
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

# Define the Webex API endpoint and headers
api_url = "https://webexapis.com/v1/messages"
headers = {
    "Content-Type": "application/json",
    "Authorization": "Bearer " + os.getenv("WEBEX_BOT_TOKEN")
}

# Define the webhook route
@app.route("/webhook", methods=["POST"])
def handle_webhook():
    # Extract the webhook data from the request
    webhook = request.get_json()
    data = webhook["data"]

    # Extract the launch details from the webhook data
    rocket_name = data["rocket_name"]
    payload_type = data["payload_type"]
    payload_description = data["payload_description"]
    launch_time = data["launch_time"]
    launch_site = data["launch_site"]
    mission_patch = data["mission_patch"]
    video_stream = data["video_stream"]
    
    # Replace the placeholders in the adaptive card payload with the actual launch details
    card_payload = {
        "$schema": "http://adaptivecards.io/schemas/adaptive-card.json",
        "type": "AdaptiveCard",
        "version": "1.3",
        "body": 
        [{
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
                        "title": "Payload Description",
                        "value": payload_description
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
    
    # Create the message payload to send to the Webex API
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

    # Send the message payload to the Webex API
    response = requests.post(api_url, headers=headers, json=message_payload)
    
    if response.ok:
        return jsonify({"success": True}), 200
    else:
        return jsonify({"success": False, "message": response.text}), response.status_code

# Define the status page endpoint
@app.route('/status')
def status():
    return render_template('status.html', message='The server is up and running!')


if __name__ == "__main__":
    app.run()