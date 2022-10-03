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

#推播
#line_bot_api.push_message('U62f7334ab2243374de92db45eab6e153', TextSendMessage(text='你可以開始了'))


# 監聽所有來自 /callback 的 Post Request
@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']
    # get request body as text
    body = request.get_data(as_text=True)
    #app.logger.info("Request body: " + body)
    print("Request body: " + body)

    # handle webhook body
    try:
      handler.handle(body, signature)
    except InvalidSignatureError:
      abort(400)

    return 'OK'

import re
#訊息傳遞區塊
##### 基本上程式編輯都在這個function #####
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    #message = TextSendMessage(text=event.message.text)
    message = event.message.text
    sendString = ""
    #re.match("你是誰",message) -->正則表示式
    if "你是誰"==message:
      sendString="乾你屌事"
    elif "撿狗吃啥"==message:
      sendString=foodStraws()
    elif "撿狗吃啥 reset"==message:
      foodList.clear()
      sendString="菜單已重置，請先新增後再查詢"
    elif re.match("吃啥\s\+*",message):
      foodList.append(message.split("+")[1].strip())
      sendString="菜單已新增: "+message.split("+")[1].strip()
    elif re.match("...天氣",message):
      sendString=weatherReport(message.split("天氣")[0])
    elif "我說" in message and "你說" in message:
      isay=message.split("我說")[1].split("你說")[0]
      usay=message.split("我說")[1].split("你說")[1]
      sendString=learnSpeak(isay,usay)
    elif message in dicAll:
      sendString=dicAll[message]
    elif "這裡有誰"==message and event.source.type=="group":
      print(event.source.group_id)
      member_ids_res = line_bot_api.get_group_member_ids(event.source.group_id)
      sendString=str(member_ids_res.member_ids)+str(member_ids_res.next)
    else:
      sendString=""
      
    
    if sendString!="":
      line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=sendString)
      )

#菜單變數
foodList = ["大埔", "石二鍋", "薩利亞", "米粉湯", "炒飯", "烏龍麵"]
import random
def foodStraws():
    return foodList[random.randint(0, len(foodList) - 1)]

import requests
def weatherReport(loc="桃園市"):
  url = 'https://opendata.cwb.gov.tw/api/v1/rest/datastore/F-C0032-001?Authorization=CWB-FE106A37-DA13-4687-9965-EE2C546A1C30'
  data = requests.get(url)   # 取得 JSON 檔案的內容為文字
  data_json = data.json()    # 轉換成 JSON 格式
  location = data_json['records']['location']
  for i in location:
    if i['locationName']==loc:
      city = i['locationName']    # 縣市名稱
      wx8 = i['weatherElement'][0]['time'][0]['parameter']['parameterName']    # 天氣現象
      maxt8 = i['weatherElement'][2]['time'][0]['parameter']['parameterName']  # 最高溫
      mint8 = i['weatherElement'][4]['time'][0]['parameter']['parameterName']  # 最低溫
      ci8 = i['weatherElement'][3]['time'][0]['parameter']['parameterName']    # 舒適度
      pop8 = i['weatherElement'][1]['time'][0]['parameter']['parameterName']   # 降雨機率
      return f'{city}未來 8 小時{wx8}，最高溫 {maxt8} 度，最低溫 {mint8} 度，降雨機率 {pop8} %'

dicAll = dict()
def learnSpeak(key,val):
    dictmp = dict()
    dictmp = {key:val}
    dicAll.update(dictmp)
    return 'OK!已學'

#主程式
import os 
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)