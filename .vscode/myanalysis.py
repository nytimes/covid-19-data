# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'
# %%
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


# %%
statedata = pd.read_csv('../us-states.csv')
countydata = pd.read_csv('../us-counties.csv')

# %%
def doplottotalcases(state, county = 'all'):
    if county == 'all':
        data = statedata[statedata.state == state][['date', 'cases']]
    else:
        data = countydata[countydata.state == state][['date', 'cases', 'county']]
        data = data[countydata.county == county][['date', 'cases']]

    data = data[data.cases >= starting_cases]
    if len(data['cases']):
        data_asarray = data.cases.values
        ax.set_xlim(0, max(data_asarray.size, ax.get_xlim()[1]))
        ax.set_ylim(0, max(data['cases'].max(), ax.get_ylim()[1]))
        if (county == 'all'):
            ax.plot(data_asarray, label=state)
        else:
            ax.plot(data_asarray, label=county + ',  ' + state)


# %%
starting_cases = 1000
fig = plt.figure(figsize=(14,10))
ax = fig.add_axes([0,0,1,1])
ax.set_title('Growth of cases with starting case count = ' + str(starting_cases))
ax.set_xlabel('Days since hitting starting case count')
ax.set_ylabel('Cases')

interesting_states = pd.Series([
    'Washington',
    'New York',
    'Florida',
    'California',
    'New Jersey',
    'Ohio',
    'Florida',
    'Oregon',
    'Michigan',
    'Illinois'
    ])

for s in np.sort(statedata[statedata.state.isin(interesting_states)].state.unique()):
    doplottotalcases(s)

ax.legend()

# %%

starting_cases = 200
fig = plt.figure(figsize=(14,10))
ax = fig.add_axes([0,0,1,1])
ax.set_title('Growth of cases with starting case count = ' + str(starting_cases))
ax.set_xlabel('Days since hitting starting case count')
ax.set_ylabel('Cases')

doplottotalcases('New York', 'New York City')
doplottotalcases('New York', 'Rockland')
doplottotalcases('New York', 'Suffolk')
doplottotalcases('New York', 'Westchester')
doplottotalcases('California', 'Los Angeles')
doplottotalcases('Louisiana', 'Orleans')
doplottotalcases('California', 'San Francisco')
doplottotalcases('Washington', 'King')
doplottotalcases('Washington', 'Snohomish')
doplottotalcases('Illinois', 'Cook')
doplottotalcases('Ohio', 'Cuyahoga')
doplottotalcases('New Jersey', 'Bergen')


ax.legend()

# %%
starting_cases = 1000
fig = plt.figure(figsize=(14,10))
ax = fig.add_axes([0,0,1,1])
ax.set_title('Growth per capita with starting case count = ' + str(starting_cases))
ax.set_xlabel('Days since hitting starting case count')
ax.set_ylabel('Cases per capita')
ax.set_ylim(0, 0.000001)
def doplotpercapita(fulldata, state, population):
    data = fulldata[fulldata.state == state][['date', 'cases']]
    data = data[data.cases >= starting_cases]
    data.cases = data.cases / population
    if len(data['cases']):
        data_asarray = data.cases.values
        ax.set_xlim(0, max(data_asarray.size, ax.get_xlim()[1]))
        ax.set_ylim(0, max(data['cases'].max(), ax.get_ylim()[1]))
        ax.plot(data_asarray, label=state)

doplotpercapita(statedata, 'New York', 19453561)
doplotpercapita(statedata, 'Washington', 7614893)
doplotpercapita(statedata, 'New Jersey', 8882190)
doplotpercapita(statedata, 'Colorado', 5758736)
doplotpercapita(statedata, 'California', 39512223)
doplotpercapita(statedata, 'Oregon', 4217737)
doplotpercapita(statedata, 'Louisiana', 4648794)
doplotpercapita(statedata, 'Florida', 21477737)
doplotpercapita(statedata, 'Illinois', 12671821)
doplotpercapita(statedata, 'Michigan', 9986857)
doplotpercapita(statedata, 'Ohio',11689100)

ax.legend()




# # %%
# def doplotbydate(fulldf, date, state):
#     statedata = fulldf[fulldf.state == state][['date', 'cases']]
#     data = data[data.date >= date]
#     doplot(data, state)

# def doplotbymincases(fulldf, min, state):
#     data = fulldf[fulldf.state == state][['date', 'cases']]
#     data = data[data.cases >= min]
#     data.sort_values('cases', 0, True, True)
#     doplot(data, state)

# def doplot(fulldf, state):
#     plt.figure(figsize=(14,10))
#     data_asarray = fulldf.cases.values
#     plt.yscale('log')
#     plt.xlabel('date')
#     plt.ylabel('cases')
#     plt.plot(data_asarray, label=state)
#     plt.legend()


# # %%
# date = '2020-03-15'
# minimum_cases = 100
# doplotbymincases(data, minimum_cases, 'New York')
# doplotbymincases(data, minimum_cases, 'New Jersey')
# doplotbymincases(data, minimum_cases, 'Washington')
# doplotbymincases(data, minimum_cases, 'Ohio')
# doplotbymincases(data, minimum_cases, 'California')
# doplotbymincases(data, minimum_cases, 'Illinois')
# doplotbymincases(data, minimum_cases, 'Michigan')
# doplotbymincases(data, minimum_cases, 'Florida')
# doplotbymincases(data, minimum_cases, 'Oregon')
# doplotbymincases(data, minimum_cases, 'Rhode Island')


# %%


