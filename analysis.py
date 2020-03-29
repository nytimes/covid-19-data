import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

caseThreshold = 100

countyData = pd.read_csv('us-counties.csv', header=0)
statePopulationData = pd.read_csv('populations.csv', header=0)

#join state populations w/ county data
pd.DataFrame.merge(countyData, statePopulationData, left_on='state', right_on='state_name') = countyData

print(countyData.head())
