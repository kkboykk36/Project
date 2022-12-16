from selenium import webdriver #載入webdriver模組
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import re
from datetime import datetime
import time
import json
# from linebot.models import FlexSendMessage


arrAirport = input("請輸入目的地：")
depDate = input('出發日(yyyy/mm/dd)：')
d = datetime.strptime(depDate,'%Y/%m/%d').date()

def flight_search(depDate,arrAirport):
    
    Flight_URL = 'https://www.airpaz.com/zh-tw/flight/search?depDate='+str(d)+'&depAirport=TPE&arrAirport='+arrAirport+'&adult=1'
    browser = webdriver.Chrome(r'C:\Users\AlenChang\Desktop\2接\chromedriver.exe') #建立瀏覽器
    browser.get(Flight_URL) #聯結網址
    WebDriverWait(browser,10).until(
        expected_conditions.presence_of_element_located((By.CLASS_NAME,'choose-flight-button'))
        )
    time.sleep(5)
    
    soup = BeautifulSoup(browser.page_source,'html.parser')
    
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
    
    for dep,arr,name,logo,dep_time,consuming,arr_time,price,types in zip(flight_departures,flight_arrives,company,logos,daparture_times,time_consumimgs,arrive_times,ticket_prices,flight_types):
        
        airline_datas.append([d,
                              dep.text.strip(),
                              arr.text.strip(),
                              name.text.strip(),
                              logo.get('src'),
                              dep_time.find('p',class_="flight-box-time-label medium-b").text.strip(),
                              consuming.find('p',class_="flight-box-time-label medium-b").text.strip(),
                              arr_time.find('p',class_="flight-box-time-label medium-b").text.strip(),
                              price.text.strip()[4:-4],
                              types.text.strip()])
        
    browser.quit()
    
    # print(airline_datas)
    
    with open('2階段.json',encoding='utf-8') as f:
        detail = json.load(f)
        # print(detail['contents']['contents'][1]['body']['contents'][3]['contents'][2]['text'])
        # print(airline_datas[0][7])
        # num = len(airline_datas)
        # if num >= 5:
        for i in range(5):
            detail['contents']['contents'][i]['header']['contents'][0]['contents'][1]['text'] = airline_datas[i][1]
            detail['contents']['contents'][i]['header']['contents'][1]['contents'][1]['text'] = airline_datas[i][2]
            detail['contents']['contents'][i]['header']['contents'][2]['contents'][1]['text'] = airline_datas[i][3]
            detail['contents']['contents'][i]['hero']['url'] = airline_datas[i][4]
            detail['contents']['contents'][i]['body']['contents'][0]['contents'][0]['text'] = airline_datas[i][5]
            detail['contents']['contents'][i]['body']['contents'][0]['contents'][2]['text'] = airline_datas[i][1]
            detail['contents']['contents'][i]['body']['contents'][1]['contents'][2]['text'] = airline_datas[i][6]
            detail['contents']['contents'][i]['body']['contents'][2]['contents'][0]['text'] = airline_datas[i][5]
            detail['contents']['contents'][i]['body']['contents'][2]['contents'][2]['text'] = airline_datas[i][7]
            detail['contents']['contents'][i]['body']['contents'][3]['contents'][1]['text'] = airline_datas[i][2]
            detail['contents']['contents'][i]['footer']['contents'][0]['action']['uri'] = i+1   #先用數字註記 
        
        # print('done')
        # detail_massage = FlexSendMessage.new_from_json_dict(detail)
         
    with open('2階段.json','w',newline='',encoding='utf-8') as f:
          json.dump(detail,f,indent=4,ensure_ascii=False)
          
    print('done')
    # return detail_massage
    
flight_search(depDate,arrAirport)
# Ans = flight_search(depDate,arrAirport)
# print(Ans)