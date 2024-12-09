# -*- coding: utf-8 -*-

#載入LineBot所需要的套件
import random
from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import *

# Define a list of sticker IDs (Package ID, Sticker ID)
# For example, we use Package ID 1 and Stickers 1 to 10.
sticker_ids = [
    {'package_id': '1', 'sticker_id': '1'},
    {'package_id': '1', 'sticker_id': '2'},
    {'package_id': '1', 'sticker_id': '3'},
    {'package_id': '1', 'sticker_id': '4'},
    {'package_id': '1', 'sticker_id': '5'},
    {'package_id': '1', 'sticker_id': '6'},
    {'package_id': '1', 'sticker_id': '7'},
    {'package_id': '1', 'sticker_id': '8'},
    {'package_id': '1', 'sticker_id': '9'},
    {'package_id': '1', 'sticker_id': '10'}
]

app = Flask(__name__)

# 必須放上自己的Channel Access Token
line_bot_api = LineBotApi('VCuOHttt9t9s0wFQNL0xCazF2VzVyirr4oUAnVoKssR6q4xcZZJYayNIZmYNwI1dZOyKf3d+6Jfs9/1PyYEZ0pCz5OlmaH69Zn4Ov8+o8HZyOz5F6rM0bgPPdAb3z/dTzmYQT3OUQdv01TNc2ig24AdB04t89/1O/w1cDnyilFU=')
# 必須放上自己的Channel Secret
handler = WebhookHandler('d7b01a847f2e887fcb0427584630dc86')

line_bot_api.push_message('Uffbc7888e974d392e9d5c273b7cd5cb6', TextSendMessage(text='你可以開始了'))

# Handle incoming messages
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    # Choose a random sticker from the list
    sticker = random.choice(sticker_ids)
    
    # Create the StickerSendMessage
    sticker_message = StickerSendMessage(
        package_id=sticker['package_id'],
        sticker_id=sticker['sticker_id']
    )
    
    # Send the sticker as a response
    line_bot_api.reply_message(event.reply_token, sticker_message)
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
