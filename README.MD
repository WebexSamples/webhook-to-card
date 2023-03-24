# Webhook to Adaptive Card for Webex Integration

This is a sample Python application that demonstrates how to receive a webhook and convert the data into an adaptive card that is posted into a Webex space by a Webex bot.

## Prerequisites

- Python 3.6+
- Flask
- Requests
- Adaptive Card JSON schema

## Getting Started

1. Clone this repository.
2. Install the required packages by running `pip install -r requirements.txt`.
3. Rename .env.example to .env and replace the variables with your own values
   - `WEBEX_ACCESS_TOKEN`: Your Webex bot access token.
   - `WEBEX_ROOM_ID`: The ID of the Webex room where the adaptive card will be posted.
4. Start the application by running `python app.py`.
5. Send a POST request to the `/webhook` endpoint with a JSON payload that contains the data for the adaptive card.

   Example:

```
curl -X POST -H "Content-Type: application/json" -d @webhook-payload.json http://localhost:5000/webhook
```

6. The application will parse the JSON payload, generate an adaptive card, and post it into the Webex room specified by `WEBEX_ROOM_ID`.

## Acknowledgements

This sample application was created using the following resources:

- [Webex API Documentation](https://developer.webex.com/docs/api/getting-started)
- [Adaptive Cards Documentation](https://adaptivecards.io/)
- [ChatGPT](https://chat.openai.com)
