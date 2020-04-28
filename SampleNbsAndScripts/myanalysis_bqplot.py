#  %%
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime
import plotly.graph_objects as go

mpl.rcParams['lines.linewidth'] = 4.0
default_figsize=[16, 9]

#  %% [markdown]
# **********************************************************************************************************
# # Setup
# 1. Read in the covid-19-data from nytimes for state and county (https://github.com/nytimes/covid-19-data)
# 2. Pull in a city density table
# 3. Pull in a state density table
# 4. Identify list of states, counties and cities to graph
# **********************************************************************************************************
#  %%
state_cov_data = pd.read_csv('us-states.csv')
county_cov_data = pd.read_csv('us-counties.csv')

population_city_density = pd.read_csv('city_density.csv')
population_city_density = population_city_density.rename(columns={'City': 'citystate', 'Population Density (Persons/Square Mile)': 'density', '2016 Population': 'population', 'Land Area (Square Miles)': 'area'} )
population_city_density[['city', 'state']] = population_city_density.citystate.str.split(', ', expand=True)

population_state_density = pd.read_csv('state_density.csv')
population_state_density = population_state_density.rename(columns={'State': 'state', 'Density': 'density', 'Pop': 'population', 'LandArea': 'area'})

county_cities_east = [
    ['New York', 'New York City', ['New York']],
    ['New Jersey', 'Bergen', ['Newark', 'Jersey City']],
    ['Massachusetts', 'Suffolk', ['Boston']],
    ['South Carolina', 'Charleston', ['Charleston']],
    ['Florida', 'Miami-Dade', ['Miami']],
    ['Florida', 'Broward', ['Fort Lauderdale']],
    ['Florida', 'Duval', ['Jacksonville']]
]
county_cities_west = [
    ['New York', 'New York City', ['New York']],
    ['Washington', 'King', ['Seattle']],
    ['Washington', 'Snohomish', ['Everett']],
    ['California', 'Los Angeles', ['Los Angeles']],
    ['California', 'San Francisco', ['San Francisco']],
    ['California', 'San Diego', ['San Diego']],
    ['Texas', 'Harris', ['Houston']],
    ['Texas', 'Bexar', ['San Antonio']],
    ['Texas', 'Dallas', ['Dallas']],
    ['Texas', 'Travis', ['Austin']],
    ['Arizona', 'Maricopa', ['Phoenix']]
]

county_cities_midwest = [
    ['New York', 'New York City', ['New York']],
    ['Illinois', 'Cook', ['Chicago']],
    ['Louisiana', 'Orleans', ['New Orleans']],
    ['Ohio', 'Cuyahoga', ['Cleveland']],
    ['Michigan', 'Wayne', ['Detroit']],
    ['Indiana', 'Hamilton', ['Carmel']],
    ['Pennsylvania', 'Philadelphia', ['Philadelphia']]
]

county_cities_east_map = pd.DataFrame(county_cities_east, columns = ['state', 'county', 'cities'])
county_cities_west_map = pd.DataFrame(county_cities_west, columns = ['state', 'county', 'cities'])
county_cities_midwest_map = pd.DataFrame(county_cities_midwest, columns = ['state', 'county', 'cities'])

states_east = county_cities_east_map.state.unique()
states_west = county_cities_west_map.state.unique()
states_midwest = county_cities_midwest_map.state.unique()
states = np.unique(np.concatenate((states_east, states_midwest, states_west)))

# %% [markdown]
# **********************************************************************************************************
# # New cases per day
# This trend line is a moving average of new cases over time.
# **********************************************************************************************************
# %%

def movingaverage(values, window):
    weights = np.repeat(1.0, window)/window
    sma = np.convolve(values, weights, 'valid')
    return sma

def plotnewcases(plot, state='US'):
    if (state == 'US'):
        total_cases_by_date = state_cov_data.groupby('date').sum()
        minimum_cases = 100
    else:
        total_cases_by_date = state_cov_data[state_cov_data.state == state].groupby('date').sum()
        minimum_cases = 15

    total_cases_by_date = total_cases_by_date.reset_index()
    total_cases_by_date = total_cases_by_date[total_cases_by_date.cases > minimum_cases]
    delta_cases = total_cases_by_date.cases.to_numpy()[1:] - total_cases_by_date.head(len(total_cases_by_date)-1).cases.to_numpy()[0:]

    delta_cases_ma = movingaverage(delta_cases, 7)
    df = pd.DataFrame(delta_cases_ma, columns=['new'])
    df['days'] = df.index

    if (plot == None):
        plot = go.Figure()
        plot.add_trace(go.Scatter(x=df.days, y=df.new, mode='lines', name=state, line = { 'width': 4 }))
        return plot
    else:
        plot.add_trace(go.Scatter(x=df.days, y=df.new, mode='lines', name=state))
        return plot

plot = plotnewcases(None)

for state in states:
    plotnewcases(plot, state)

plot.update_layout(
    title = {
        'text': datetime.now().strftime('%x') + ' Newly reported cases per day trend',
        'x': 0.5,
        'xanchor': 'center'
    },
    width = 1200,
    height = 800,
    xaxis_title = 'Days',
    yaxis_title = 'New Cases'
    )

plot.show()

