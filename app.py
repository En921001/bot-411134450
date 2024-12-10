# -*- coding: utf-8 -*-

# 載入LineBot所需要的套件
from flask import Flask, request, abort
from geopy.geocoders import Nominatim
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import *
import os

app = Flask(__name__)

# 必須放上自己的 Channel Access Token
line_bot_api = LineBotApi('+7YfwUC/eTwkZN/ppuj4iMFcqEzyfSz3mkp912pZzYqRl/dQQGSk5CqHUTmyhsxJVbIlHGZ5uaKhpWcBF94m/CLWI7zGkRanEfHwMbbb6wWHrXFfiRaQvYdmGlKcMjcHNSkmyV7W/vYsS7kcoU22dQdB04t89/1O/w1cDnyilFU==')
# 必須放上自己的 Channel Secret
handler = WebhookHandler('0f360f872b791eec9ca40c322452e6a7')

line_bot_api.push_message('Ue846dc373e7a4eb37266340a870b7d0a', TextSendMessage(text='你可以開始了'))

# Geopy Geolocator
geolocator = Nominatim(user_agent="line_bot_location", timeout=10)

# 查詢地名並偏向台灣
def search_location(query):
    """
    使用 Geopy 查詢地名，偏向於台灣地區
    """
    try:
        # 限制搜尋範圍為台灣
        location = geolocator.geocode(query, country_codes="tw", viewbox=((20.5, 119.5), (25.5, 122.5)), bounded=True)
        if location:
            return {
                'address': location.address,
                'latitude': location.latitude,
                'longitude': location.longitude
            }
        else:
            return None
    except Exception as e:
        print(f"Geopy error: {e}")
        return None

# 監聽所有來自 /callback 的 POST Request
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

# 訊息傳遞區塊
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    message = event.message.text
    try:
        # 使用者輸入地名查詢
        location_data = search_location(message)
        if location_data:
            location_message = LocationSendMessage(
                title=message,
                address=location_data['address'],
                latitude=location_data['latitude'],
                longitude=location_data['longitude']
            )
            line_bot_api.reply_message(event.reply_token, location_message)
        else:
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text="找不到對應的位置信息，請嘗試其他關鍵字。"))
    except Exception as e:
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text="系統錯誤，請稍後再試。"))

# 主程式
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
