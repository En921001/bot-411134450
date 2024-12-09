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

app = Flask(__name__)

# 必須放上自己的Channel Access Token
line_bot_api = LineBotApi('VCuOHttt9t9s0wFQNL0xCazF2VzVyirr4oUAnVoKssR6q4xcZZJYayNIZmYNwI1dZOyKf3d+6Jfs9/1PyYEZ0pCz5OlmaH69Zn4Ov8+o8HZyOz5F6rM0bgPPdAb3z/dTzmYQT3OUQdv01TNc2ig24AdB04t89/1O/w1cDnyilFU=')

# 必須放上自己的Channel Secret
handler = WebhookHandler('d7b01a847f2e887fcb0427584630dc86')

line_bot_api.push_message('Uffbc7888e974d392e9d5c273b7cd5cb6', TextSendMessage(text='您好,目前時間是 2024/10/10 14:00 ，請問需要什麼服務呢?'))

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

    # 根據用戶輸入的訊息進行判斷並回應
    if user_message == "天氣":
        reply_message = "請稍等，我幫您查詢天氣資訊！"
    else:
        reply_message = "很抱歉，我目前無法理解這個內容。"

    # 回覆用戶訊息
    line_bot_api.reply_message(event.reply_token, TextSendMessage(text=reply_message))

#訊息傳遞區塊
##### 基本上程式編輯都在這個function #####
#@handler.add(MessageEvent, message=TextMessage)
#def handle_message(event):
    #message = TextSendMessage(text=event.message.text)
    #line_bot_api.reply_message(event.reply_token,message)

#主程式
import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
