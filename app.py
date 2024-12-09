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
    message = event.message.text  # Get the message text

    # Define a dictionary with video URLs based on the category
    video_dict = {
        '動作片': {
            'original_content_url': 'https://youtu.be/vrK9VCSslyI',
            'preview_image_url': 'https://hips.hearstapps.com/hmg-prod/images/chris-hemsworth-extraction-2-642a8d4059737.jpg?resize=980:*'
        },
        '動畫': {
            'original_content_url': 'https://youtu.be/p6h57WqRRl8',
            'preview_image_url': 'https://p2.bahamut.com.tw/B/2KU/90/18a976106d462f8f0babd9674b1sd9y5.JPG'
        },
        '紀錄片': {
            'original_content_url': 'https://youtu.be/ohwiy6CfzGc',
            'preview_image_url': 'https://vbmspic.video.friday.tw/STILL/95776/95776_86525_L.jpg'
        }
    }

    # Check if the user input matches a valid movie type
    if message in video_dict:
        video_message = VideoSendMessage(
            original_content_url=video_dict[message]['original_content_url'],
            preview_image_url=video_dict[message]['preview_image_url']
        )
        line_bot_api.reply_message(event.reply_token, video_message)  # Send the video

    else:
        # If the message doesn't match any known category
        error_message = TextSendMessage(text='抱歉，沒有這類型的影片')
        line_bot_api.reply_message(event.reply_token, error_message)  # Send the error message


#主程式
import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)




