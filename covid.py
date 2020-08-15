# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

#county
cook_data=pd.read_csv("us-counties.csv")
inter_cases=cook_data.loc[cook_data["county"]=="Cook"]
county_cases=inter_cases.loc[inter_cases["state"]=="Illinois"]['cases'].values
total_county_cases=county_cases[len(county_cases)-1]
dayscounty=range(len(county_cases))
per_day_county=np.gradient(county_cases/total_county_cases)

#state
ill_data=pd.read_csv("us-states.csv")
state_cases=ill_data.loc[ill_data["state"]=="Illinois"]['cases'].values
total_state_cases=state_cases[len(state_cases)-1]
daysstate=range(len(state_cases))
per_day_state=np.gradient(state_cases/total_state_cases)

plt.plot(dayscounty, (per_day_state-per_day_county))
plt.show()
plt.plot(dayscounty,per_day_county,label="county cases")
plt.plot(daysstate,per_day_state,label="state cases")
#plt.legend()
#plt.show()

#weighted average
days=5
wa_county_cases=[]
wa_state_cases=[]
#print(int((len(per_day_county)-len(per_day_county)%7)/7))
for i in range(int((len(per_day_county)-len(per_day_county)%days)/days)):
    totalc=sum(per_day_county[int(i*days):int(i*days+days)])/days
    wa_county_cases.append(totalc)
    totals=sum(per_day_state[int(i*days):int(i*days+days)])/days
    wa_state_cases.append(totals)
wa_days=np.array(range(len(wa_county_cases)))*days

plt.plot(wa_days,wa_county_cases,label="weighted average county cases per day")
plt.plot(wa_days,wa_state_cases,label="weighted state county cases per day")
plt.legend()
plt.show()



#country
state_data=pd.read_csv("us.csv")
days=range(len(state_data['cases']))
total_cases=state_data['cases'][len(state_data['cases'])-1]
total_deaths=state_data['deaths'][len(state_data['deaths'])-1]
plt.plot((np.gradient(state_data['cases']))/total_cases,label="cases")
plt.plot(np.gradient(state_data['deaths'])/total_deaths,label="deaths")
plt.legend()
plt.show()

