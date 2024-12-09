# -*- coding: utf-8 -*-

#載入LineBot所需要的套件
from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *
import re
app = Flask(__name__)

# 必須放上自己的Channel Access Token
line_bot_api = LineBotApi('VCuOHttt9t9s0wFQNL0xCazF2VzVyirr4oUAnVoKssR6q4xcZZJYayNIZmYNwI1dZOyKf3d+6Jfs9/1PyYEZ0pCz5OlmaH69Zn4Ov8+o8HZyOz5F6rM0bgPPdAb3z/dTzmYQT3OUQdv01TNc2ig24AdB04t89/1O/w1cDnyilFU=')
# 必須放上自己的Channel Secret
handler = WebhookHandler('d7b01a847f2e887fcb0427584630dc86')

line_bot_api.push_message('Uffbc7888e974d392e9d5c273b7cd5cb6', TextSendMessage(text='你可以開始了'))

# 監聽所有來自 /callback 的 Post Request
@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'

# Enable logging
logging.basicConfig(level=logging.DEBUG)

# Google Places API Key (replace with your key)
GOOGLE_API_KEY = 'YOUR_GOOGLE_API_KEY'

# Initialize the LINE Bot API
line_bot_api = LineBotApi('YOUR_LINE_CHANNEL_ACCESS_TOKEN')
handler = WebhookHandler('YOUR_LINE_CHANNEL_SECRET')

# Function to search for places using Google Places API
def search_location(query, location="Taiwan", radius=5000):
    # Prepare the Google Places API request URL
    url = f'https://maps.googleapis.com/maps/api/place/textsearch/json?query={query}+in+{location}&radius={radius}&key={GOOGLE_API_KEY}'
    
    # Log the request URL for debugging
    logging.debug(f"Request URL: {url}")
    
    # Send the request to Google Places API
    response = requests.get(url)
    response_data = response.json()
    
    # Log the API response for debugging
    logging.debug(f"API Response: {response_data}")
    
    results = response_data.get('results', [])
    
    # If no results found, return None
    if not results:
        return None
    
    # Extract the first result (you can modify this to handle multiple results)
    place = results[0]
    name = place.get('name', 'Unknown')
    address = place.get('formatted_address', 'No address available')
    latitude = place['geometry']['location']['lat']
    longitude = place['geometry']['location']['lng']
    
    return name, address, latitude, longitude

# Handle incoming messages
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    message = event.message.text  # Get the message text
    logging.debug(f"Received message: {message}")
    
    # If the message contains a location keyword like "公園" or "咖啡廳"
    if re.match(r'公園|咖啡廳', message):  # You can add more keywords to match
        location_data = search_location(message)  # Search using the input message
        
        if location_data:
            name, address, latitude, longitude = location_data
            location_message = LocationSendMessage(
                title=name,
                address=address,
                latitude=latitude,
                longitude=longitude
            )
            line_bot_api.reply_message(event.reply_token, location_message)
        else:
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text="抱歉，沒有找到相關的地點"))
    else:
        # Default behavior if no match
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text="請輸入地名關鍵字 (例如：公園 或 咖啡廳)"))


#主程式
import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)




