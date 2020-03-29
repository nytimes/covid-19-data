import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

#global inputs
input_geographies =[['San Francisco', 'California'],['Santa Clara', 'California'],['San Mateo', 'California'],['Marin', 'California'],['Contra Costa', 'California'],['Alameda', 'California'],['Los Angeles', 'California']]
comparison_metric = 'cases'
index_on_case_threshold = True
case_threshold = 10

def filter (county, state):
	areaName = county + ", " + state 
	masterData = pd.read_csv('masterData.csv', header=0)
	filterData = masterData[(masterData['county'] == county) & (masterData['state'] == state)].drop(columns=['fips','state_population'])
	filterData['cases_per_K'] = filterData['cases'] / (filterData['county_population'] / 1000)
	filterData['deaths_per_K'] = filterData['deaths'] / (filterData['county_population'] / 1000)
	if index_on_case_threshold == True:
		filterData = filterData[filterData['cases'] >= case_threshold]
	filterData = filterData[comparison_metric].reset_index(drop=True)
	filterData = filterData.to_frame().rename(columns={'cases': areaName})
	return filterData

filteredData=[]

for geo in input_geographies:
	filteredData.append(filter(geo[0],geo[1]))

outputData = pd.DataFrame()

for geoFilterData in filteredData:
	outputData = outputData.merge(geoFilterData,how='outer',left_index=True,right_index=True)

outputData.to_csv('plot_data.csv')
