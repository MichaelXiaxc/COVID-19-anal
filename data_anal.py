import numpy
import pandas as pd
import matplotlib.pyplot as plt

#中国数据
covid_data = pd.read_csv("WHO-COVID-19-global-data.csv") #读取数据

CN_covid_data = covid_data[covid_data["Country_code"]=="CN"]

CN_covid_data = CN_covid_data[['Date_reported','Country','New_cases','Cumulative_cases','New_deaths','Cumulative_deaths']]

CN_covid_data.set_index(['Date_reported'],drop = True)

CN_covid_data.to_csv("CN_covid_data.csv") #筛选出中国的疫情数据，另输入进csv数据集中

CN_covid_data.plot()

plt.show()

#美国数据
covid_data = pd.read_csv("WHO-COVID-19-global-data.csv") #读取数据

US_covid_data = covid_data[covid_data["Country_code"]=="US"]

US_covid_data = US_covid_data[['Date_reported','Country','New_cases','Cumulative_cases','New_deaths','Cumulative_deaths']]

US_covid_data.set_index(['Date_reported'],drop = True)

US_covid_data.to_csv("US_covid_data.csv") #筛选出中国的疫情数据，另输入进csv数据集中

US_covid_data.plot()

plt.show()

#其余替换国家码，同理
