# -*- coding: utf-8 -*-
"""
Created on Tue Jun 28 01:53:23 2022

@author: User
"""

import numpy as np
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt

bron = pd.read_csv("生育率.csv")
year = list(bron['year'])
boy = list(bron['bronboy'])
girl = list(bron['brongirl'])

chinese_font = matplotlib.font_manager.FontProperties(fname="C:\Windows\Fonts\kaiu.ttf")
x = np.arange(11)
width = 0.4
plt.bar(x-0.2,boy,width,tick_label=year,label='Boy')
plt.bar(x+0.2,girl,width,tick_label=year,label='Girl')

plt.legend()
plt.suptitle('男女分別出生統計',fontsize=25,fontproperties=chinese_font)  #圖表標題
plt.xlabel('年分',fontproperties=chinese_font,fontsize=15)        #X軸名稱
plt.ylabel('千分率(‰)',fontproperties=chinese_font,fontsize=15)        #Y軸名稱
plt.savefig("男女分別出生數.jpg")
# plt.show()
