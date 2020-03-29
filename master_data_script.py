import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

caseThreshold = 50
bayAreaCounties = ['San Francisco', 'Santa Clara', 'San Mateo', 'Marin', 'Contra Costa', 'Alameda']

covidData = pd.read_csv('data/us-counties.csv', header=0)
statePopulationData = pd.read_csv('data/state_populations.csv', header=0)
countyPopulationData = pd.read_csv('data/county_populations.csv', header=0)

#clean county population data
countyPopulationData[['county','state']]=countyPopulationData.county_name.str.split(" County, ",expand=True)
countyPopulationData = countyPopulationData.drop(columns=['county_name','2010','2011','2012','2013','2014','2015','2016','2017','2018'])
countyPopulationData.county = countyPopulationData.county.str.replace(".","").replace("St","St.")

#join covid w/ state populations
#print(len(covidData))
masterData = pd.merge(covidData, statePopulationData, on='state').rename(columns={"population": "state_population"})

#join master w/ county populations
#print(len(masterData))
masterData = pd.merge(masterData, countyPopulationData, on=['state','county']).rename(columns={"2019": "county_population"})
masterData.county_population = masterData.county_population.str.replace(",","").astype(int)

#print to csv
masterData.to_csv("masterData.csv", index_label="index")

##analysis 1: Bay Area vs. Non Bay Area, raw counts

#filter for CA
#californiaData = masterData[masterData['state'] == 'California']

#filter to bayArea and notBayArea
#bayAreaData = californiaData[(californiaData['county'] == 'San Francisco') | (californiaData['county'] == 'San Mateo') | (californiaData['county'] == 'Marin') | (californiaData['county'] == 'Contra Costa') | (californiaData['county'] == 'Alameda') | (californiaData['county'] == 'Santa Clara')]
#outsideBayAreaData = californiaData[(californiaData['county'] != 'San Francisco') & (californiaData['county'] != 'San Mateo') & (californiaData['county'] != 'Marin') & (californiaData['county'] != 'Contra Costa') & (californiaData['county'] != 'Alameda') & (californiaData['county'] != 'Santa Clara')]

#group and aggregate
#bayAreaData = bayAreaData.groupby('date').agg({'cases': np.sum, 'deaths' : np.sum, 'county_population' : np.sum})
#outsideBayAreaData = outsideBayAreaData.groupby('date').agg({'cases': np.sum, 'deaths' : np.sum, 'county_population' : np.sum})

#filter by case count
#bayAreaData = bayAreaData[bayAreaData['cases'] >= caseThreshold]
#outsideBayAreaData = outsideBayAreaData[outsideBayAreaData['cases'] >= caseThreshold]