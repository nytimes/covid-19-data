#  %%
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime

mpl.rcParams['lines.linewidth'] = 4.0
default_figsize=[12, 9]

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
]
county_cities_west = [
    ['New York', 'New York City', ['New York']],
    ['Washington', 'King', ['Seattle']],
    ['Washington', 'Snohomish', ['Everett']],
    ['California', 'Los Angeles', ['Los Angeles']],
    ['California', 'San Francisco', ['San Francisco']],
]

county_cities_midwest = [
    ['New York', 'New York City', ['New York']],
    ['Illinois', 'Cook', ['Chicago']],
    ['Louisiana', 'Orleans', ['New Orleans']],
    ['Ohio', 'Cuyahoga', ['Cleveland']],
    ['Michigan', 'Wayne', ['Detroit']],
    ['Indiana', 'Hamilton', ['Carmel']]
]

county_cities_east_map = pd.DataFrame(county_cities_east, columns = ['state', 'county', 'cities'])
county_cities_west_map = pd.DataFrame(county_cities_west, columns = ['state', 'county', 'cities'])
county_cities_midwest_map = pd.DataFrame(county_cities_midwest, columns = ['state', 'county', 'cities'])

states_east = county_cities_east_map.state.unique()
states_west = county_cities_west_map.state.unique()
states_midwest = county_cities_midwest_map.state.unique()

#  %%
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
        ax.set_ylim(0, ax.get_ylim()[1] * 1.01)

        if (county == 'all'):
            ax.plot(data_asarray, label=state)
        else:
            ax.plot(data_asarray, label=county + ',  ' + state)

# %% [markdown]
# **********************************************************************************************************
# # State Totals
# **********************************************************************************************************
# %%
for dataset in [states_east, states_midwest, states_west]:
    starting_cases = 1000
    fig = plt.figure(figsize=default_figsize)
    ax = fig.add_axes([0,0,1,1])
    ax.set_title('Total state cases with starting case count = ' + str(starting_cases) + ' Date: ' + datetime.now().strftime('%x'))
    ax.set_xlabel('Days since hitting ' + str(starting_cases) + ' cases')
    ax.set_ylabel('Cases')
    plt.setp(ax.lines)

    for s in dataset:
        plottotalcases(s)

    ax.legend()

#  %% [markdown]
# **********************************************************************************************************
# # County Totals
# **********************************************************************************************************
for dataset in [county_cities_east_map, county_cities_midwest_map, county_cities_west_map]:
    starting_cases = 200
    fig = plt.figure(figsize=default_figsize)
    ax = fig.add_axes([0,0,1,1])
    ax.set_title('Total county cases with starting case count = ' + str(starting_cases) + ' Date: ' + datetime.now().strftime('%x'))
    ax.set_xlabel('Days since hitting ' + str(starting_cases) + ' cases')
    ax.set_ylabel('Cases')

    for p in dataset.itertuples():
        plottotalcases(p.state, p.county)

    ax.legend()

#  %% [markdown]
# **********************************************************************************************************
# # State cases adjusted for population
# To better get a sense of how different states may be handling the virus outbreak, you can
# adjust the graphs to account for the number of people who live in each state. A state that has
# 100,000 people vs 8,000,000 people will obviously look far better with regard to total cases
# because they have 80x less people. By factoring in the population of a state, this is difference
# is accounted for.
#
# This graph indicates that New York, New Jersey, and Louisiana, are getting far more cases per day
# than the other states, regardless of how many people live in each state.
# **********************************************************************************************************
#  %%
for dataset in [states_east, states_midwest, states_west]:
    starting_cases = 1000
    fig = plt.figure(figsize=default_figsize)
    ax = fig.add_axes([0,0,1,1])
    ax.set_title(datetime.now().strftime('%x') + ' State cases adjusted for population\nStarting case count = ' + str(starting_cases))
    ax.set_xlabel('Days since hitting ' + str(starting_cases) + ' cases')
    ax.set_ylabel('Cases adjusted for state population')
    ax.set_ylim(0, 0.0001)

    def stateplotpercapita(state):
        data = state_cov_data[state_cov_data.state == state][['date', 'cases']]
        data = data[data.cases >= starting_cases]
        state_population = population_state_density[population_state_density.state == state]
        if len(state_population):
            plotdata = data.cases / state_population.population.values[0]
            if len(data['cases']):
                    data_asarray = plotdata.values
                    ax.set_xlim(0, max(data_asarray.size, ax.get_xlim()[1]))
                    ax.set_ylim(0, max(data_asarray.max(), ax.get_ylim()[1]))
                    ax.set_ylim(0, ax.get_ylim()[1] * 1.01)
                    ax.set_yticklabels([''])
                    ax.plot(data_asarray, label=state)
                    lastindex = len(data_asarray) - 1
                    ax.annotate(str(data.cases.max()) + ' cases', xy=(lastindex + .1, data_asarray[lastindex]))

    for s in dataset:
        stateplotpercapita(s)

    ax.legend()

#  %% [markdown]
# **********************************************************************************************************
# # State cases adjusted for population density
#
# Each state has a population and an area in which this population lives. *Pretend* for a moment that Texas only has 100,000
# people total. Also *pretend* that Rhode Island has 100,000 people. However, you also know that the
# land area of Rhode Island is much, much smaller than that of Texas. So, if Rhode Island gets 5,000 cases of the virus
# and Texas also gets 5,000 case, then you can say with high confidence that the people in Texas are likely completely
# ignoring advice to keep a minimum distance from others. I mean how else could they have the same number of cases as Rhode Island
# where the same number of people are packed together?

# This graph removes this consideration from the comparison between states. As you can see, New Jersey is doing far worse than
# than Ohio, Washington and California.
# **********************************************************************************************************
#  %%
for dataset in [states_east, states_midwest, states_west]:
    starting_cases = 200
    fig = plt.figure(figsize=default_figsize)
    ax = fig.add_axes([0,0,1,1])
    ax.set_title(datetime.now().strftime('%x') + ' State cases adjusted for population density\nStarting case count = ' + str(starting_cases))
    ax.set_xlabel('Days since hitting ' + str(starting_cases) + ' cases')
    ax.set_ylabel('Cases adjusted for state population density')
    ax.set_ylim(0, 0)

    def stateplotbydensity(state):
        data = state_cov_data[state_cov_data.state == state][['date', 'cases']]
        data = data[data.cases >= starting_cases]
        state_density = population_state_density[population_state_density.state == state]
        if len(state_density):
            plotdata = data.cases / state_density.density.values[0]
            if len(data['cases']):
                data_asarray = plotdata.values
                ax.set_xlim(0, max(data_asarray.size, ax.get_xlim()[1]))
                ax.set_ylim(0, max(data_asarray.max(), ax.get_ylim()[1]))
                ax.set_ylim(0, ax.get_ylim()[1] * 1.01)
                ax.set_yticklabels([''])
                ax.plot(data_asarray, label=state)
                lastindex = len(data_asarray) - 1
                ax.annotate(str(data.cases.tail(1).values[0]) + ' cases', xy=(lastindex + .1, data_asarray[lastindex]))


    for s in dataset:
        stateplotbydensity(s)

    ax.legend()

#  %% [markdown]
# **********************************************************************************************************
# # City cases adjusted for population density
# Ohhhh, but I hear you say... Well the area of California is far larger than than of New York. Therefore, the population
# density of California can EASILY be lower than that of New York, so this skews the results to make California look better.
# In addition, each state likely has a hotspot city and in those cities the population density may be FAR higher and thus
# far more likely to spread a virus in the city's immediate area than the state overall.
# In other words the population density of Los Angeles is probably FAR higher than that of California overall, so ranking
# by state-wide density isn't really a good way to compare a physically large state like California to a much smaller state
# like NY or Ohio.
#
# Ok, then lets look at individual cities in each of the states!
#
# This graph shows that even though Detroit Michigan's population density is around 5x less than that of New York City,
# the number of virus cases is growing there far faster than even New York and New Orleans (which both suck!). I'd be much
# more worried if I lived in Detroit right now.
#
# Note that Cleveland and Seattle, and Los Angeles are pretty flat, which is good.
# **********************************************************************************************************
#  %%
for dataset in [county_cities_east_map, county_cities_midwest_map, county_cities_west_map]:
    starting_cases = 20
    fig = plt.figure(figsize=default_figsize)
    ax = fig.add_axes([0,0,1,1])
    ax.set_title(datetime.now().strftime('%x') + ' City cases adjusted for population density\nStarting case count = ' + str(starting_cases))
    ax.set_xlabel('Days since hitting ' + str(starting_cases) + ' cases')
    ax.set_ylabel('Cases adjusted for population density')
    ax.set_ylim(0, 0.0001)

    def cityplotbydensity(state, city):
        county = 'not found'
        for x in dataset.itertuples():
            if city in x.cities and state == x.state:
                county = x.county

        data = county_cov_data[county_cov_data.state == state][county_cov_data.county == county][['date', 'cases']]
        data = data[data.cases >= starting_cases]
        city_density = population_city_density[population_city_density.state == state][population_city_density.city == city]
        if (len(city_density)):
            plotdata = data.cases / city_density.density.values[0]
            if len(data['cases']):
                data_asarray = plotdata.values
                ax.set_xlim(0, max(data_asarray.size, ax.get_xlim()[1]))
                ax.set_ylim(0, max(data_asarray.max(), ax.get_ylim()[1]))
                ax.set_ylim(0, ax.get_ylim()[1] * 1.01)
                ax.set_yticklabels([''])
                ax.plot(data_asarray, label=city + ', ' + state + ' (' + str(city_density.density.values[0]) + ' people/mi^2)')
                lastindex = len(data_asarray) - 1
                ax.annotate(str(data.cases.tail(1).values[0]) + ' cases', xy=(lastindex + .1, data_asarray[lastindex]))

    for p in dataset.itertuples():
        for c in p.cities:
            cityplotbydensity(p.state, c)

    ax.legend()

#  %% [markdown]
# **********************************************************************************************************
# # City deaths adjusted for population density
#
# **********************************************************************************************************
#  %%
for dataset in [county_cities_east_map, county_cities_midwest_map, county_cities_west_map]:
    starting_deaths = 1
    fig = plt.figure(figsize=default_figsize)
    ax = fig.add_axes([0,0,1,1])
    ax.set_title(datetime.now().strftime('%x') + ' City deaths adjusted for population density')
    ax.set_xlabel('Days since first death')
    ax.set_ylabel('Deaths adjusted for population density')
    ax.set_ylim(0, 0.0001)

    def cityplotbydensity(state, city):
        county = 'not found'
        for x in dataset.itertuples():
            if city in x.cities and state == x.state:
                county = x.county

        data = county_cov_data[county_cov_data.state == state][county_cov_data.county == county][['date', 'deaths']]
        data = data[data.deaths >= starting_deaths]
        city_density = population_city_density[population_city_density.state == state][population_city_density.city == city]
        if (len(city_density)):
            plotdata = data.deaths / city_density.density.values[0]
            if len(data['deaths']):
                value_array = plotdata.values
                ax.set_xlim(0, max(value_array.size, ax.get_xlim()[1]))
                ax.set_ylim(0, max(value_array.max(), ax.get_ylim()[1]))
                ax.set_ylim(0, ax.get_ylim()[1] * 1.01)
                ax.set_yticklabels([''])
                ax.plot(value_array, label=city + ', ' + state + ' (' + str(city_density.density.values[0]) + ' people/mi^2)')
                lastindex = len(value_array) - 1
                ax.annotate(str(data.deaths.tail(1).values[0]) + ' deaths', xy=(lastindex + .1, value_array[lastindex]))


    for p in dataset.itertuples():
        for c in p.cities:
            cityplotbydensity(p.state, c)

    ax.legend()

# # %% [markdown]
# # **********************************************************************************************************
# # # Use Bokeh for plotting just for kicks
# # **********************************************************************************************************
# #  %%
# import bokeh.plotting as bplt
# import bokeh.models as bmod
# from bokeh.palettes import Dark2_5 as palette
# import itertools
# #  %%
# starting_cases = 1000

# # output to static HTML file
# bplt.output_notebook()

# # create a new plot with a title and axis labels
# fig_bokeh = bplt.figure(title='Total state cases with starting case count = ' + str(starting_cases), x_axis_label='Days since hitting ' + str(starting_cases) + ' cases', y_axis_label='Cases', plot_width=1200, plot_height=1000)
# colors = itertools.cycle(palette)

# def plottotalcases_bokeh(state, county = 'all', color = 'black'):
#     if county == 'all':
#         data = state_cov_data[state_cov_data.state == state][['date', 'cases']]
#     else:
#         data = county_cov_data[county_cov_data.state == state][['date', 'cases', 'county']]
#         data = data[county_cov_data.county == county][['date', 'cases']]

#     data = data[data.cases >= starting_cases]
#     if len(data['cases']):
#         data_asarray = data.cases.values
#         # fig_bokeh.x_range = bmod.Range1d(0, data_asarray.size)
#         # fig_bokeh.y_range = bmod.Range1d(0, data['cases'].max())
#         if (county == 'all'):
#             fig_bokeh.line(data.cases.reset_index().index.tolist(), data_asarray, color=next(colors), line_width=2, legend_label=state)
#         else:
#             fig_bokeh.line(data.cases.reset_index().index.tolist(), data_asarray, color=next(colors), line_width=2, legend_label=county + ',  ' + state)

# # show the results
# for s in states.unique():
#     plottotalcases_bokeh(s)

# bplt.show(fig_bokeh)
# #  %%
# starting_cases = 200

# # output to static HTML file
# bplt.output_notebook()

# # create a new plot with a title and axis labels
# fig_bokeh = bplt.figure(title='Total county cases with starting case count = ' + str(starting_cases), x_axis_label='Days since hitting ' + str(starting_cases) + ' cases', y_axis_label='Cases', plot_width=1200, plot_height=1000)
# colors = itertools.cycle(palette)

# def plottotalcases_bokeh(state, county = 'all', color = 'black'):
#     if county == 'all':
#         data = state_cov_data[state_cov_data.state == state][['date', 'cases']]
#     else:
#         data = county_cov_data[county_cov_data.state == state][['date', 'cases', 'county']]
#         data = data[county_cov_data.county == county][['date', 'cases']]

#     data = data[data.cases >= starting_cases]
#     if len(data['cases']):
#         data_asarray = data.cases.values
#         # fig_bokeh.x_range = bmod.Range1d(0, data_asarray.size)
#         # fig_bokeh.y_range = bmod.Range1d(0, data['cases'].max())
#         if (county == 'all'):
#             fig_bokeh.line(data.cases.reset_index().index.tolist(), data_asarray, color=next(colors), line_width=2, legend_label=state)
#         else:
#             fig_bokeh.line(data.cases.reset_index().index.tolist(), data_asarray, color=next(colors), line_width=2, legend_label=county + ',  ' + state)

# # show the results
# for p in county_cities_map.itertuples():
#     plottotalcases_bokeh(p.state, p.county)

# bplt.show(fig_bokeh)
