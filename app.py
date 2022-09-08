#載入LineBot所需要的模組
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
line_bot_api = LineBotApi('DwE27NcztEaf4fIpXJtvGIfVCiWv+77jEYNxxTameVt70Caoo5wQ2d7LwfxoQ7LW3mq+/qbndXjZpWWhoXmbQNSXLY7dZrRvSS2SmPpUAqxW8ZVF5bhLhQq6plgtoYHpdY9G3QoahpJmLeBZrFpG9QdB04t89/1O/w1cDnyilFU=')

# 必須放上自己的Channel Secret
handler = WebhookHandler('59f91d8eb0fe78b17307f5b2f02f62b8')

line_bot_api.push_message('U62f7334ab2243374de92db45eab6e153', TextSendMessage(text='你可以開始了'))


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
    message = TextSendMessage(text=event.message.text)
    line_bot_api.reply_message(event.reply_token,message)

#主程式
import os 
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)