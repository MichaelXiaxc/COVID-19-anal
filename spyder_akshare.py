''' akshare data collecter'''
'''https://www.akshare.xyz/zh_CN/latest/data/event/event.html'''


import akshare as ak
import pandas 

covid_19_China_daily = ak.covid_19_163(indicator = "中国实时数据")

covid_19_China_history = ak.covid_19_163(indicator = "中国历史时点数据")

covid_19_China_history_total = ak.covid_19_163(indicator = "中国历史累计数据")

covid_19_global_history = ak.covid_19_163(indicator = "世界历史时点数据")

covid_19_global_history_total = ak.covid_19_163(indicator = "世界历史累计数据")

covid_19_all_area_history_total = ak.covid_19_163(indicator = "全球所有国家及地区累计数据")

#covid_19_city_SH_history = ak.covid_19_hist_city(city = "上海市")

#covid_19_history_all = ak.covid_19_history()




covid_19_China_daily.to_csv("covid_19_China_daily.csv")

covid_19_China_history.to_csv("covid_19_China_daily.csv")

covid_19_China_history_total.to_csv("covid_19_China_history_total.csv")

covid_19_global_history.to_csv("covid_19_global_history.csv")

covid_19_global_history_total.to_csv("covid_19_global_history_total.csv")

covid_19_all_area_history_total.to_csv("covid_19_all_area_history_total.csv")

#covid_19_history_all.to_csv("covid_19_history.csv")

#covid_19_city_SH_history.to_csv("covid_19_city_SH_history.csv")
