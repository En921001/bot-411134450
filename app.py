# -*- coding: utf-8 -*-

# 載入 LineBot 所需要的套件
from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import TextMessage, TextSendMessage, StickerSendMessage, MessageEvent
import re

app = Flask(__name__)

# 必須放上自己的 Channel Access Token
line_bot_api = LineBotApi('uCsEQcK8/n0y6Ry7nNYY2LTMIWRlKRP5Pc5skuVxHUK0kGHPdeMJOGKu6yDC++Mcf0ECgMF2F4mbuFI09sUWo75OU0QFVGNDohhmmY2mQIMizGkTLEkU5gUvWABAdBy0VQjZLQFDCZQ6wrCgfP5fgQdB04t89/1O/w1cDnyilFU=')

# 必須放上自己的 Channel Secret
handler = WebhookHandler('0b346da981e91dd30f384a1d8cd46b39')

# 用戶啟動後，主動發送消息
line_bot_api.push_message('Uc9bf2374d88a474691d2827c396900f0', TextSendMessage(text='你可以開始了'))

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

# 訊息處理區塊
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    user_message = event.message.text  # 用戶發送的訊息
    
    # 根據用戶輸入的內容進行判斷
    if user_message == "心情好":
        # 這裡的貼圖ID是「笑臉貼圖」的 ID，可以根據需要更換
        sticker_message = StickerSendMessage(
            package_id='11537',  # 包含笑臉貼圖的 package_id
            sticker_id='52002734'  # 笑臉貼圖的 sticker_id
        )
        line_bot_api.reply_message(event.reply_token, sticker_message)
    elif user_message == "心情不好":
        # 這裡的貼圖ID是「哭泣貼圖」的 ID，可以根據需要更換
        sticker_message = StickerSendMessage(
            package_id='446',  # 包含哭泣貼圖的 package_id
            sticker_id='2088'  # 哭泣貼圖的 sticker_id
        )
        line_bot_api.reply_message(event.reply_token, sticker_message)
    else:
        # 如果用戶輸入其他訊息，回覆文本訊息
        reply_message = f"你說的是: {user_message}，但是我不太懂這個意思。"
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=reply_message))

# 主程式
import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
