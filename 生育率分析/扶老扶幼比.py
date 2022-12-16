# -*- coding: utf-8 -*-
"""
Created on Wed Jun 29 01:17:44 2022

@author: User
"""

import pandas as pd
import matplotlib
import matplotlib.pyplot as plt

data_o = pd.read_csv("扶老比.csv")
data_y = pd.read_csv("扶幼比.csv")
year = list(data_o['year'])
rate_o = list(data_o['old_rate'])
rate_y = list(data_y['young_rate'])


fig, ax1 = plt.subplots()  #fig畫布物件  ax1 =subplots畫布上的物件
chinese_font = matplotlib.font_manager.FontProperties(fname="C:\Windows\Fonts\kaiu.ttf")
ax1.set_xlabel('年分',fontproperties=chinese_font,fontsize=15)
ax1.plot(year,rate_o,'r-o',label='Old')
ax1.plot(year,rate_y,'b-o',label='Young')
ax1.set_ylabel('比率',color='r',fontproperties=chinese_font,fontsize=15)
ax1.tick_params('y', colors='r')
ax1.legend(loc = "upper center", fontsize=10)
plt.suptitle('扶老扶幼比',fontsize=20,fontproperties=chinese_font)
plt.grid(True)

fig.savefig("扶老扶幼比.jpg")