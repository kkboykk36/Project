# -*- coding: utf-8 -*-
"""
Created on Tue Jun 28 05:06:14 2022

@author: User
"""

import pandas as pd
import matplotlib
import matplotlib.pyplot as plt

bron = pd.read_csv("生育率.csv")
year = list(bron['year'])
tot_boy = list(bron['tot_boy'])
tot_girl = list(bron['tot_girl'])

chinese_font = matplotlib.font_manager.FontProperties(fname="C:\Windows\Fonts\kaiu.ttf")
plt.plot(year,tot_boy,'b-o',label='Boy')
plt.plot(year,tot_girl,'r-o',label='Girl')
plt.xlabel("年分",fontproperties=chinese_font,fontsize=15)
plt.ylabel("千分率",fontproperties=chinese_font,fontsize=15)
plt.legend(loc = "best", fontsize=10)
plt.suptitle('總生育率',fontsize=25,fontproperties=chinese_font)
plt.grid(True)
plt.savefig("總生育率.jpg")
