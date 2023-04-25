#載入LineBot所需要的模組
from flask import Flask, request, abort
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *
from linebot.models import PostbackAction,URIAction, MessageAction, TemplateSendMessage, ButtonsTemplate,TextSendMessage
from Postgresql import database

app = Flask(__name__)

# 必須放上自己的Channel Access Token
line_bot_api = LineBotApi('DwE27NcztEaf4fIpXJtvGIfVCiWv+77jEYNxxTameVt70Caoo5wQ2d7LwfxoQ7LW3mq+/qbndXjZpWWhoXmbQNSXLY7dZrRvSS2SmPpUAqxW8ZVF5bhLhQq6plgtoYHpdY9G3QoahpJmLeBZrFpG9QdB04t89/1O/w1cDnyilFU=')

# 必須放上自己的Channel Secret
handler = WebhookHandler('59f91d8eb0fe78b17307f5b2f02f62b8')

#推播
line_bot_api.push_message('U62f7334ab2243374de92db45eab6e153', TextSendMessage(text='你可以開始了'))


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
    elif "撿狗roll"==message:
      sendString=foodStraws()
    elif "菜單 reset"==message:
      foodList.clear()
      sendString="菜單已重置，請先新增後再查詢"
    elif "菜單 show"==message:
      sendString=str(foodList)
    elif re.match("菜單\s\+*",message):
      foodList.append(message.split("+")[1].strip())
      sendString="菜單已新增: "+message.split("+")[1].strip()
    elif re.match("^.+天氣",message):
      sendString=weatherReport(message.split("天氣")[0])
    elif re.match("^.+風浪",message):
      sendString=waveReport(message.split("風浪")[0])
    elif "我說" in message and "你說" in message:
      isay=message.split("我說")[1].split("你說")[0]
      usay=message.split("我說")[1].split("你說")[1]
      sendString=learnSpeak(isay,usay)
    elif message in dicAll:
      sendString=dicAll[message]
    elif "DBS" in message:
      profile = line_bot_api.get_profile(event.source.user_id)
      user_name = profile.display_name #使用者名稱
      uid = profile.user_id # 發訊者ID
      key=message.split("@")[1]
      val=message.split("@")[2]
      print(f"name={user_name},key={key},val={val}")
      myDatabase = database(user_name, uid)
      v = myDatabase.add_test(key,val)
      print(f"V={v}")
      if v==True:
        sendString="資料庫新增成功"
      else:
        sendString="資料庫新增失敗"
    elif "群組"==message and event.source.type=="group":
      #要買高級會員才能用，傻眼
      #member_ids_res = line_bot_api.get_group_member_ids(event.source.group_id)
      #sendString=str(member_ids_res.member_ids)+str(member_ids_res.next)
      print(event.source.group_id)
      line_bot_api.reply_message(event.reply_token, TemplateSendMessage(alt_text='ButtonsTemplate',
        template=ButtonsTemplate(
          thumbnail_image_url='https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcT_F7ApoziOFXs9ZpPsvKKkixUFv3Nsab0ppAMoMLfYpg&s',
          title='測試測試',
          text='這是按鈕樣板',
          imageSize='comtain',
          actions=[
            #PostbackAction(
                #label='postback',
                #data='發送 postback'
            #),
            MessageAction(
                label='按我',
                text='我是SB'
            ),
            URIAction(
                label='URL',
                uri='https://developers.line.biz/en/reference/messaging-api/#template-messages'
            )
          ]
        )
      ))
    else:
      sendString=""
      
    
    if sendString!="":
      line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=sendString)
      )

#fun菜單變數
foodList = ["大埔", "石二鍋", "炒飯"]
import random
def foodStraws():
    return foodList[random.randint(0, len(foodList) - 1)]

#fun天氣預報
import requests
def weatherReport(loc="桃園市"):
  url = 'https://opendata.cwb.gov.tw/api/v1/rest/datastore/F-C0032-001?Authorization=CWB-FE106A37-DA13-4687-9965-EE2C546A1C30'
  data = requests.get(url)   # 取得 JSON 檔案的內容為文字
  data_json = data.json()    # 轉換成 JSON 格式
  location = data_json['records']['location']

  loc=loc.replace("台","臺")
  if len(loc)==2:
    loc=loc+"市"

  for i in location:
    if i['locationName']==loc:
      city = i['locationName']    # 縣市名稱
      wx8 = i['weatherElement'][0]['time'][0]['parameter']['parameterName']    # 天氣現象
      maxt8 = i['weatherElement'][2]['time'][0]['parameter']['parameterName']  # 最高溫
      mint8 = i['weatherElement'][4]['time'][0]['parameter']['parameterName']  # 最低溫
      ci8 = i['weatherElement'][3]['time'][0]['parameter']['parameterName']    # 舒適度
      pop8 = i['weatherElement'][1]['time'][0]['parameter']['parameterName']   # 降雨機率
      return f'{city}未來 8 小時{wx8}，最低溫 {maxt8} 度，最高溫 {mint8} 度，降雨機率 {pop8} %'

#fun學說話
dicAll = dict()
def learnSpeak(key,val):
    dictmp = dict()
    dictmp = {key:val}
    dicAll.update(dictmp)
    return 'OK!已學'

#fun風浪
import ssl,json,urllib.request
def waveReport(loc='宜蘭'):
  url = 'https://opendata.cwb.gov.tw/fileapi/v1/opendataapi/F-A0012-001?Authorization=CWB-FE106A37-DA13-4687-9965-EE2C546A1C30&downloadType=WEB&format=JSON'
  context = ssl._create_unverified_context()

  with urllib.request.urlopen(url, context=context) as jsondata:
    #將JSON進行UTF-8的BOM解碼，並把解碼後的資料載入JSON陣列中
    data = json.loads(jsondata.read().decode('utf-8-sig'))

  location = data['cwbopendata']['dataset']['location']

  for i in location:
    if loc in i['locationName']:
      city = i['locationName']    # 縣市名稱
      wx8 = i['weatherElement'][0]['time'][0]['parameter']['parameterName']    # 天氣現象
      maxt8 = i['weatherElement'][1]['time'][0]['parameter']['parameterName']  # 風向 
      mint8 = i['weatherElement'][2]['time'][0]['parameter']['parameterName']  # 風速
      ci8 = i['weatherElement'][2]['time'][0]['parameter']['parameterUnit']    # 風速2
      pop8 = i['weatherElement'][3]['time'][0]['parameter']['parameterName']   # 浪高
      pop9 = i['weatherElement'][4]['time'][0]['parameter']['parameterName']   # 浪型
      return f'{city} 未來一天 {wx8}，\n風向: {maxt8} ，\n風速: {mint8}-{ci8}，\n浪高: {pop8}-{pop9}'
      break



#連資料庫撈--舊
# import psycopg2
# def DBS(SQLstr):
#   conn = psycopg2.connect(database="d9853ut492vfal",
# 						user="unbbvvskdqjxhn",
# 						password="a44a2c39177a46456adc7e1a6bb984c59f904c5d80ca2c1d57c569fc898bafd7",
# 						host="ec2-3-223-242-224.compute-1.amazonaws.com",
# 						port="5432")
#   cursor=conn.cursor()
#   cursor.execute("SELECT * FROM userdata;")#選擇資料表userdata
#   rows = cursor.fetchall() #讀出所有資料
#   cursor.close()
#   res=""
#   for row in rows:   #將讀到的資料全部print出來
#     res+="Data row = (%s, %s, %s)\n" %(str(row[0]), str(row[1]), str(row[2]))
#   return res


#連資料庫撈--render-postgreSQL



#主程式
import os 
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)