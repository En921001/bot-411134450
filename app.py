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

#訊息傳遞區塊
##### 基本上程式編輯都在這個function #####
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    message = event.message.text  # Correct the variable assignment

    if re.match('今天是我的生日', message):  # Matching "今天是我的生日"
        # Send a birthday greeting image and text message
        image_message = ImageSendMessage(
            original_content_url='https://dw-media.dotdotnews.com/dams/product/image/202409/03/66d6a924e4b05e1238102462.png',  # Your birthday image URL
            preview_image_url='https://dw-media.dotdotnews.com/dams/product/image/202409/03/66d6a924e4b05e1238102462.png'  # Your image preview URL
        )
        # Send the birthday message image
        line_bot_api.reply_message(event.reply_token, image_message)
        
        # Send "生日快樂" text message
        text_message = TextSendMessage(text="生日快樂")  
        line_bot_api.reply_message(event.reply_token, text_message)
    
    else:
        # Reply with the original message if it's not "今天是我的生日"
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=message))

#主程式
import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)




