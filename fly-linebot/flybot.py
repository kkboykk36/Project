'''
Pattern name...: flybot.py
Descriptions...: LineBot整合自動搜尋航班票價
Date & Author..: 22/11/11 By Alen

Modify MOD-221114 By Alen 22/11/14 增加互動訊息
'''

from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent,
    TextMessage,
    TextSendMessage,
    PostbackEvent,
    FlexSendMessage
)
import json
import re



app = Flask(__name__)

# Channel Access Token
line_bot_api = LineBotApi('aaVojFnTBTE7+BYR9Y1+AzjrnOvkIgBAW8QxVeqWMqxI4mQKD7nifTQAaPnnY4BJkPRUz/zPdnV7+KK8tqRCYjLDepPHWug/DNk4dtdyKMe+dqi29x312vvMSim4uMnVR5IFpOaNT+ju2qzkCK1woAdB04t89/1O/w1cDnyilFU=')
# Channel Secret
handler = WebhookHandler('9bdeaaf10e10fc84052ea6b2c268db7f')

# 監聽所有來自 /callback 的 Post Request
@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    print(signature)
    print(body) #DEBUG Alen

    # # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'

date = ''

@handler.add(MessageEvent,message = TextMessage)  #handler = 窗口 #當用戶傳送文字消息時的處理
def handle_message(event):
    global date
    msg = event.message.text  #收到使用者訊息

    with open('1階段.json',encoding='utf8') as f:
        flight_message = json.load(f)
        flex_message = FlexSendMessage(
            type=flight_message['type'],
            alt_text=flight_message['altText'],
            contents=flight_message['contents']
            )

    if msg.find('@')!=-1 :
        line_bot_api.reply_message(
        event.reply_token,flex_message)
    #data 為用戶輸入的日期變數，之後用 date 來做爬蟲的時間參數 
    elif re.match('[2022.2023.2024.2025]+-\d{1,2}-\d{1,2}',msg):
        date =event.message.text
        line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text='以記錄您輸入的日期：'+date))
        #TextSendMessage(text='請輸入 @日本機票 來查看日本的重點城市'))
    else:
        line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text='查無相關資訊，欲查詢日本機票請輸入:@日本機票'))

@handler.add(PostbackEvent)
def handle_post_message(event):
    global date
    print(event.postback.data)
    #postback data 找到 HKD(用戶點了HKD之後)
    #這邊呼叫爬蟲def (date , 涵館
    if (event.postback.data.find('HKD')== 0):
        if date == '' :
            line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text='請輸入航班日期(格式:yyyy-mm-dd)!謝謝!'))
        else:
            area = 'HKD'
            fly_message = flight_search(date,area)
            if fly_message =='N':
                line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text='目前沒有該日期航班資訊請重新選擇!謝謝!'))
            else:
                flex_message = FlexSendMessage(
                    type=fly_message['type'],
                    alt_text=fly_message['altText'],
                    contents=fly_message['contents'])
                
                line_bot_api.reply_message(
                event.reply_token,flex_message)
            
    elif (event.postback.data.find('TYOA') == 0):
        if date == '' :
            line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text='請輸入航班日期(格式:yyyy-mm-dd)!謝謝!'))
        else:
            area = 'TYOA'
            # MOD-221114 add By Alen --(S)
            line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text='航班資訊搜尋中請稍後!謝謝~'))
            # MOD-221114 add By Alen --(E)
            fly_message = flight_search(date,area)
            if fly_message =='N':
                line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text='目前沒有該日期航班資訊請重新選擇!謝謝!'))
            else:
                flex_message = FlexSendMessage(
                    type=fly_message['type'],
                    alt_text=fly_message['altText'],
                    contents=fly_message['contents'])
                
                line_bot_api.reply_message(
                event.reply_token,flex_message)
            
    elif (event.postback.data.find('OSAA') == 0):
        if date == '' :
            line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text='請輸入航班日期(格式:yyyy-mm-dd)!謝謝!'))
        else:
            area = 'OSAA'
            fly_message = flight_search(date,area)
            if fly_message =='N':
                line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text='目前沒有該日期航班資訊請重新選擇!謝謝!'))
            else:
                flex_message = FlexSendMessage(
                    type=fly_message['type'],
                    alt_text=fly_message['altText'],
                    contents=fly_message['contents'])
                
                line_bot_api.reply_message(
                event.reply_token,flex_message)
            
    elif (event.postback.data.find('KOJ') == 0):
        if date == '' :
            line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text='請輸入航班日期(格式:yyyy-mm-dd)!謝謝!'))
        else:
            area = 'KOJ'
            fly_message = flight_search(date,area)
            if fly_message =='N':
                line_bot_api.reply_message(
                event.reply_token,
                    TextSendMessage(
                        text='目前沒有該日期航班資訊請重新選擇!謝謝!'))
            else:
                flex_message = FlexSendMessage(
                    type=fly_message['type'],
                    alt_text=fly_message['altText'],
                    contents=fly_message['contents'])
                
                line_bot_api.reply_message(
                event.reply_token,flex_message)
            
    elif (event.postback.data.find('OKA') == 0):
        if date == '' :
            line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text='請輸入航班日期(格式:yyyy-mm-dd)!謝謝!'))
        else:
            area = 'OKA'
            fly_message = flight_search(date,area)
            if fly_message =='N':
                line_bot_api.reply_message(
                event.reply_token,
                    TextSendMessage(text='目前沒有該日期航班資訊請重新選擇!謝謝!'))
            else:
                flex_message = FlexSendMessage(
                    type=fly_message['type'],
                    alt_text=fly_message['altText'],
                    contents=fly_message['contents'])
                
                line_bot_api.reply_message(
                event.reply_token,flex_message)
            
    else:
        pass
    
    date = '' #清空全域變數
              

from selenium import webdriver
from bs4 import BeautifulSoup
import time

def flight_search(date,area):
    chrome_options = webdriver.ChromeOptions()
    chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
    chrome_options.add_argument("--headless") #無頭模式
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--no-sandbox")
    driver = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"),chrome_options=chrome_options)
    Flight_URL = 'https://www.airpaz.com/zh-tw/flight/search?depDate={}&depAirport=TPE&arrAirport={}&adult=1'.format(date,area)
    driver.get(Flight_URL) #連結網址
    print(Flight_URL)  #背景查看log網址資訊
    # WebDriverWait(driver,10).until(
    #     expected_conditions.presence_of_element_located((By.CLASS_NAME,'choose-flight-button'))
    #     )
    time.sleep(5)
    
    soup = BeautifulSoup(driver.page_source,'html.parser')
    
    company = soup.find_all('span',class_="flight-box-airline-label normal is-block") #航空公司
    flight_departures = soup.find_all('p',class_="departure-airport normal") #出發地
    daparture_times = soup.find_all('div',class_="flight-box-time flight-box-time-departure") #起飛時間
    flight_arrives = soup.find_all('p',class_="arrive-airport normal") #目的地
    arrive_times = soup.find_all('div',class_="flight-box-time flight-box-time-arrival") #抵達時間
    time_consumimgs = soup.find_all('div',class_="flight-box-time flight-stops-wrapper") #飛航時間
    ticket_prices = soup.find_all('p',class_= re.compile("flight-price medium-b*")) #票價
    flight_types = soup.find_all('p',class_="flight-type normal has-text-grey-dark") #直飛or轉機
    logos = soup.find_all('img',class_="flight-box-airline-logo") #航空公司logo
    
    airline_datas = []
    except_list = []
    
    for dep,arr,name,logo,dep_time,consuming,arr_time,price,types in zip(flight_departures,flight_arrives,company,logos,daparture_times,time_consumimgs,arrive_times,ticket_prices,flight_types):
        if len(except_list) == 0:
            for e in range(1):  #因模板數5個 要補足資料不足5筆的情況
                except_list.append(date)
                except_list.append(dep.text.strip())
                except_list.append(arr.text.strip())
                except_list.append(str(' '))
                except_list.append('https://cdn.airpaz.com/images/illustrations/travelProducts.svg')
                except_list.append(str(' '))
                except_list.append(str('請前往網站了解更多!'))
                except_list.append(str(' '))
                except_list.append(str(' '))
                except_list.append(str(' '))
            
        airline_datas.append([date,
                              dep.text.strip(),
                              arr.text.strip(),
                              name.text.strip(),
                              logo.get('src'),
                              dep_time.find('p',class_="flight-box-time-label medium-b").text.strip(),
                              consuming.find('p',class_="flight-box-time-label medium-b").text.strip(),
                              arr_time.find('p',class_="flight-box-time-label medium-b").text.strip(),
                              price.text.strip()[4:-4],
                              types.text.strip()])
        
        
    driver.quit()
    if len(airline_datas) == 0:  #判斷該條件若沒資料則跳出
        return 'N'
    

    with open('2階段.json',encoding='utf-8') as f:
        detail = json.load(f)
        print(len(airline_datas))#背景查看log查看
        print("進入點A")#背景查看log查看
        '''
        確認資料筆數
        '''
        if len(airline_datas) < 5 :
            print("進入點B")#背景查看log查看
            for x in range(5-len(airline_datas)):
                airline_datas.append(except_list)
                
        print(airline_datas)#背景查看log查看
        for i in range(5):
            print(i) #背景查看log查看
            detail['contents']['contents'][i]['header']['contents'][0]['contents'][1]['text'] = airline_datas[i][1]
            detail['contents']['contents'][i]['header']['contents'][1]['contents'][1]['text'] = airline_datas[i][2]
            detail['contents']['contents'][i]['header']['contents'][2]['contents'][1]['text'] = airline_datas[i][3]
            detail['contents']['contents'][i]['hero']['url'] = airline_datas[i][4]
            detail['contents']['contents'][i]['body']['contents'][0]['contents'][0]['text'] = airline_datas[i][5]
            detail['contents']['contents'][i]['body']['contents'][0]['contents'][2]['text'] = airline_datas[i][1]
            detail['contents']['contents'][i]['body']['contents'][1]['contents'][2]['text'] = airline_datas[i][6]
            detail['contents']['contents'][i]['body']['contents'][2]['contents'][0]['text'] = airline_datas[i][7]
            detail['contents']['contents'][i]['body']['contents'][2]['contents'][2]['text'] = airline_datas[i][2]
            detail['contents']['contents'][i]['body']['contents'][3]['contents'][1]['text'] = airline_datas[i][8]
            print(str(i)+"次")
            print(Flight_URL)
            detail['contents']['contents'][i]['footer']['contents'][0]['action']['uri'] = Flight_URL

    return detail
    

import os


if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)

