import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

caseThreshold = 100

countyData = pd.read_csv('/data/us-counties.csv', header=0)
statePopulationData = pd.read_csv('/data/state_populations.csv', header=0)

#join state populations w/ county data
countyData = pd.merge(countyData, statePopulationData, on='state').rename(columns={"population": "state_population"})

print(countyData.head())

