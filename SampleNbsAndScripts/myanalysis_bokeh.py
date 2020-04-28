#  %%
import pandas as pd
import numpy as np
from datetime import datetime
from bokeh.plotting import figure
from bokeh.models import HoverTool, LinearColorMapper, CategoricalColorMapper
from bokeh.io import output_notebook, show
from bokeh.palettes import Spectral11
from bokeh.transform import factor_cmap

default_width=2
output_notebook()

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

def plotnewcases(row, state='US', color='none'):
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

    p.line('days', 'new', source=df,
        line_width=default_width,
        legend_label=state,
        color=color)
    return df

hover = HoverTool(
    tooltips=[
        ('day', '$index'),
        ('new cases', '@new{0,0}')
    ]
)
p = figure(width=800, height=500, tools=[hover])

row = 1
for state, color in zip(states, Spectral11):
    plotnewcases(row, state, color)

show(p)

