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
line_bot_api = LineBotApi('uCsEQcK8/n0y6Ry7nNYY2LTMIWRlKRP5Pc5skuVxHUK0kGHPdeMJOGKu6yDC++Mcf0ECgMF2F4mbuFI09sUWo75OU0QFVGNDohhmmY2mQIMizGkTLEkU5gUvWABAdBy0VQjZLQFDCZQ6wrCgfP5fgQdB04t89/1O/w1cDnyilFU=')
# 必須放上自己的Channel Secret
handler = WebhookHandler('0b346da981e91dd30f384a1d8cd46b39')

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

#訊息傳遞區塊
##### 基本上程式編輯都在這個function #####
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    message = event.message.text  # Correct variable assignment
    if re.match('你好', message):
        # Reply with a sticker
        sticker_message = StickerSendMessage(
            package_id='11537',
            sticker_id='52002738'
        )
        line_bot_api.reply_message(event.reply_token, sticker_message)
    elif re.match('喜歡', message):
        # Reply with both sticker and text
        sticker_message = StickerSendMessage(
            package_id='8515',
            sticker_id='16581253'
        )
        text_message = TextSendMessage(text=message)  # reply with the same message text
        line_bot_api.reply_message(event.reply_token, [sticker_message, text_message])  # send both sticker and text

#主程式
import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
