# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'
# %%
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


# %%
state_cov_data = pd.read_csv('us-states.csv')
county_cov_data = pd.read_csv('us-counties.csv')

population_city_density = pd.read_csv('city_density.csv')
population_city_density = population_city_density.rename(columns={'City': 'citystate', 'Population Density (Persons/Square Mile)': 'density', '2016 Population': 'population', 'Land Area (Square Miles)': 'area'} )
population_city_density[['city', 'state']] = population_city_density.citystate.str.split(', ', expand=True)

population_state_density = pd.read_csv('state_density.csv')
population_state_density = population_state_density.rename(columns={'State': 'state', 'Density': 'density', 'Pop': 'population', 'LandArea': 'area'})

county_cities = [
    ['New York', 'New York City', ['New York']],
    ['New Jersey', 'Bergen', ['Newark', 'Jersey City']],
    ['Washington', 'King', ['Bellevue', 'Seattle']],
    ['California', 'Los Angeles', ['Los Angeles']],
    ['Illinois', 'Cook', ['Chicago']],
    ['Louisiana', 'Orleans', ['New Orleans']],
    ['Ohio', 'Cuyahoga', ['Cleveland']]
]

county_cities_map = pd.DataFrame(county_cities, columns = ['state', 'county', 'cities'])

def plottotalcases(state, county = 'all'):
    if county == 'all':
        data = state_cov_data[state_cov_data.state == state][['date', 'cases']]
    else:
        data = county_cov_data[county_cov_data.state == state][['date', 'cases', 'county']]
        data = data[county_cov_data.county == county][['date', 'cases']]

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
ax.set_title('Total state cases with starting case count = ' + str(starting_cases))
ax.set_xlabel('Days since hitting ' + str(starting_cases) + ' cases')
ax.set_ylabel('Cases')

for p in county_cities_map.itertuples():
    plottotalcases(p.state)

ax.legend()

# %%

starting_cases = 200
fig = plt.figure(figsize=(14,10))
ax = fig.add_axes([0,0,1,1])
ax.set_title('Total county cases with starting case count = ' + str(starting_cases))
ax.set_xlabel('Days since hitting ' + str(starting_cases) + ' cases')
ax.set_ylabel('Cases')

for p in county_cities_map.itertuples():
    plottotalcases(p.state, p.county)

ax.legend()

# %%
starting_cases = 1000
fig = plt.figure(figsize=(14,10))
ax = fig.add_axes([0,0,1,1])
ax.set_title('State growth per capita with starting case count = ' + str(starting_cases))
ax.set_xlabel('Days since hitting ' + str(starting_cases) + ' cases')
ax.set_ylabel('Cases per capita')
ax.set_ylim(0, 0.0001)

def stateplotpercapita(state):
    data = state_cov_data[state_cov_data.state == state][['date', 'cases']]
    data = data[data.cases >= starting_cases]
    state_population = population_state_density[population_state_density.state == state]
    if len(state_population):
       data.cases = data.cases / state_population.population.values[0]
       if len(data['cases']):
            data_asarray = data.cases.values
            ax.set_xlim(0, max(data_asarray.size, ax.get_xlim()[1]))
            ax.set_ylim(0, max(data['cases'].max(), ax.get_ylim()[1]))
            ax.plot(data_asarray, label=state)

for p in county_cities_map.itertuples():
    stateplotpercapita(p.state)

ax.legend()

# %%
starting_cases = 200
fig = plt.figure(figsize=(14,10))
ax = fig.add_axes([0,0,1,1])
ax.set_title('State cases by population density starting case count = ' + str(starting_cases))
ax.set_xlabel('Days since hitting ' + str(starting_cases) + ' cases')
ax.set_ylabel('Cases by state population density')
ax.set_ylim(0, 0.0001)

def stateplotbydensity(state):
    data = state_cov_data[state_cov_data.state == state][['date', 'cases']]
    data = data[data.cases >= starting_cases]
    state_density = population_state_density[population_state_density.state == state]
    if len(state_density):
        data.cases = data.cases / state_density.density.values[0]
        if len(data['cases']):
            data_asarray = data.cases.values
            ax.set_xlim(0, max(data_asarray.size, ax.get_xlim()[1]))
            ax.set_ylim(0, max(data['cases'].max(), ax.get_ylim()[1]))
            ax.plot(data_asarray, label=state)

for p in county_cities_map.itertuples():
    stateplotpercapita(p.state)

ax.legend()

# %%
starting_cases = 20
fig = plt.figure(figsize=(14,10))
ax = fig.add_axes([0,0,1,1])
ax.set_title('City growth by population density starting case count = ' + str(starting_cases))
ax.set_xlabel('Days since hitting ' + str(starting_cases) + ' cases')
ax.set_ylabel('Cases per population density value')
ax.set_ylim(0, 0.0001)

def cityplotbydensity(state, city):
    county = 'not found'
    for x in county_cities_map.itertuples():
        if city in x.cities and state == x.state:
            county = x.county

    data = county_cov_data[county_cov_data.county == county][['date', 'cases']]
    data = data[data.cases >= starting_cases]
    city_density = population_city_density[population_city_density.state == state][population_city_density.city == city]
    if (len(city_density)):
        data.cases = data.cases / city_density.density.values[0]
        if len(data['cases']):
            data_asarray = data.cases.values
            ax.set_xlim(0, max(data_asarray.size, ax.get_xlim()[1]))
            ax.set_ylim(0, max(data['cases'].max(), ax.get_ylim()[1]))
            ax.plot(data_asarray, label=city + ', ' + state)

for p in county_cities_map.itertuples():
    for c in p.cities:
        cityplotbydensity(p.state, c)

ax.legend()

# %%
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


