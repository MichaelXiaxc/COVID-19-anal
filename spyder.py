'''Web spyder for collecting data of the COVID-19 '''
'''currently useless'''


'''
m     m   mm    mmmm mmmmmmm mmmmmm mmmm  
#  #  #   ##   #"   "   #    #      #   "m
" #"# #  #  #  "#mmm    #    #mmmmm #    #
 ## ##"  #mm#      "#   #    #      #    #
 #   #  #    # "mmm#"   #    #mmmmm #mmm" 
'''

import time
import json
import requests
from datetime import datetime
import pandas as pd
import numpy as np



def Domestic():
    url = 'https://view.inews.qq.com/g2/getOnsInfo?name=disease_h5'
    reponse = requests.get(url=url).json()
    data = json.loads(reponse['data'])
    return data


def Oversea():
    url = 'https://view.inews.qq.com/g2/getOnsInfo?name=disease_foreign'
    reponse = requests.get(url=url).json()
    data = json.loads(reponse['data'])
    return data





domestic = Domestic()
oversea = Oversea()

print(domestic.keys())
print(oversea.keys())


# 提取各地区数据明细
areaTree = domestic['areaTree']
# 查看并分析具体数据
areaTree

# 提取国外地区数据明细
foreignList = oversea['foreignList']
# 查看并分析具体数据
foreignList

china_data = areaTree[0]['children'] 
china_list = []
for a in range(len(china_data)):
    province = china_data[a]['name']  
    confirm = china_data[a]['total']['confirm'] 
    heal = china_data[a]['total']['heal']  
    dead = china_data[a]['total']['dead']  
    nowConfirm = confirm - heal - dead 
    china_dict = {} 
    china_dict['province'] = province  
    china_dict['nowConfirm'] = nowConfirm 
    china_list.append(china_dict) 

china_data = pd.DataFrame(china_list) 
china_data.to_csv("国内疫情.csv", index=False) #存储为csv文件
china_data.head()

world_data = foreignList  
world_list = []  

for a in range(len(world_data)):
    # 提取数据
    country = world_data[a]['name']
    nowConfirm = world_data[a]['nowConfirm']  
    confirm = world_data[a]['confirm']
    dead = world_data[a]['dead']  
    heal = world_data[a]['heal'] 
    # 存放数据
    world_dict = {}
    world_dict['country'] = country
    world_dict['nowConfirm'] = nowConfirm
    world_dict['confirm'] = confirm
    world_dict['dead'] = dead
    world_dict['heal'] = heal
    world_list.append(world_dict)

world_data = pd.DataFrame(world_list)
world_data.to_csv("国外疫情.csv", index=False)
world_data.head()
