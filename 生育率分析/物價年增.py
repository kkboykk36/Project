# -*- coding: utf-8 -*-
"""
Created on Wed Jun 29 23:35:41 2022

@author: User
"""

# -*- coding: utf-8 -*-
"""
Created on Wed Jun 29 15:17:52 2022

@author: AlenChang
"""

import pandas as pd
import matplotlib
import matplotlib.pyplot as plt

data = pd.read_csv("物價.csv")
data = data.fillna(0)

year = list(data['年月'])
tot_rate_y = list(data['總指數年增率'])
non_food_rate_y = list(data['總指數(不含食物)年增率'])
non_vga_rate_y = list(data['總指數(不含蔬菜水果)年增率'])


fig = plt.figure(figsize=(25,10))
chinese_font = matplotlib.font_manager.FontProperties(fname="C:\Windows\Fonts\kaiu.ttf")
plt.xlabel('年分',fontproperties=chinese_font,fontsize=30)
plt.plot(year,tot_rate_y,'r-o',label='Tot_Rate')
plt.plot(year,non_food_rate_y,'b-*',label='Non_Food_Rate')
plt.plot(year,non_vga_rate_y,'g-^',label='Non_Vga_Rate')
plt.ylabel('比率',fontproperties=chinese_font,fontsize=30)
plt.tick_params(axis='y', labelsize=20)    #設定標籤大小
plt.xticks(rotation=90)   #設定標籤方向(逆時針)
plt.grid(True)
plt.legend(loc = "upper left", fontsize=25)
plt.suptitle('物價指數年增率',fontsize=40,fontproperties=chinese_font)
fig.savefig("物價指數年增率.jpg")