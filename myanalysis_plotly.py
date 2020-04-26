# %% [markdown]
# * Update 04/25/2020
# * Update 04/19/2020 - Added plotly graphs
# * Update 04/15/2020
# * Update 04/14/2020
# * Update 04/13/2020 - Added new cases trend graphs to the start and reordered the graphs (again) to tell a better story as to how the analysis progressed.
# * Update 04/12/2020
# * Update 04/11/2020
# * Update 04/10/2020
# * Updated 04/09/2020 - From what I'm seeing on these graphs, all the cities and states I show here are showing flattening -- except New York, LA and Chicago, with NY still being the worst and not improving at all. At least it's no longer growing exponentially I guess.
# * Looks like the press is starting to ask some of the same questions I'm asking with this analysis:
#     * https://www.mercurynews.com/2020/04/08/how-california-has-contained-coronavirus-and-new-york-has-not/
# * I moved the graphs that negate the effects of city population density to the top, since that's mostly what I've been interested in seeing.
#  %%
import time
t0 = time.clock()

#  %%
import pandas as pd
import numpy as np
from datetime import datetime
import plotly.graph_objects as go
import plotly

default_line_thickness=2
default_width = 1280
default_height = 800
default_plot_color = 'rgba(0, 0, 0, 0)'
default_grid_color = 'rgba(225, 225, 225, 255)'

webpage_folder = 'webpage/'
html_graphs = open(webpage_folder + "CovidAnalysis.html",'w',)
html_graphs.write("<html><head><style>div {margin:5%; font-family: \"Verdana\"}</style></head><body>"+"\n")
html_graphs.write('<div style=\'margin:50px\'><h1>Data as of ' + datetime.now().strftime('%m/%d/%y')+ '<br/></h1>')
html_graphs.write('''
Please wait to load all the graphs. This page is not setup to be fast loading. :)<br/><br/>
Also be aware that you can now can single click on a location in the legend to show and hide that
location in the graph. If you double click, you will hide all other locations, except for the one you
double clicked.
</div>''')
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
    ['Pennsylvania', 'Philadelphia', ['Philadelphia']],
    ['Georgia', 'Fulton', ['Atlanta']],
    ['Tennessee', 'Davidson', ['Nashville']]
]

county_cities_east_map = pd.DataFrame(county_cities_east, columns = ['state', 'county', 'cities'])
county_cities_west_map = pd.DataFrame(county_cities_west, columns = ['state', 'county', 'cities'])
county_cities_midwest_map = pd.DataFrame(county_cities_midwest, columns = ['state', 'county', 'cities'])

states_east = county_cities_east_map.state.unique()
states_west = county_cities_west_map.state.unique()
states_midwest = county_cities_midwest_map.state.unique()
states = pd.unique(np.concatenate((states_east, states_midwest, states_west)))

# %% [markdown]
# **********************************************************************************************************
# # New cases per day
# **********************************************************************************************************
# %%
def movingaverage(values, window):
    weights = np.repeat(1.0, window)/window
    sma = np.convolve(values, weights, 'valid')
    return sma

def plotnewcases(row, state='US'):
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

    fig.add_trace(
        go.Scatter(x=df.days, y=df.new, mode='lines', name=state, line = { 'width': default_line_thickness },
        hovertemplate='new cases: %{y:,.0f}<br>day: %{x}')
    )

row = 1
layout = go.Layout(
        title = 'New cases for US',
        plot_bgcolor = default_plot_color,
        xaxis_gridcolor = default_grid_color,
        yaxis_gridcolor = default_grid_color,
        width=default_width,
        height=default_height,
        xaxis_title='Days since 100 cases were hit',
        yaxis_title='New cases'
)
fig = go.Figure(layout=layout)
plotnewcases(row)

fig.show()
plotly.offline.plot(fig, filename=webpage_folder + 'Chart_'+str(row)+'.html',auto_open=False)
html_graphs.write('''
<br/><br/><div>
<h1>New cases per day</h1><br/>
This trend line is a moving average of new cases over time. First for the US overall then by state (not all are represented here, just ones I found most interesting.
</div>''')
html_graphs.write("  <object data=\""+'Chart_'+str(row)+'.html'+"\" width=" + str(default_width * 1.10) + " height=" + str(default_height* 1.10) + "\"></object>"+"\n")


#############################

row += 1
layout = go.Layout(
        title = 'New cases by state',
        plot_bgcolor = default_plot_color,
        xaxis_gridcolor = default_grid_color,
        yaxis_gridcolor = default_grid_color,
        width=default_width,
        height=default_height,
        xaxis_title='Days since 15 cases were hit',
        yaxis_title='New cases'
)

fig = go.Figure(layout=layout)
for state in states:
    plotnewcases(row, state)

fig.show()
plotly.offline.plot(fig, filename=webpage_folder + 'Chart_'+str(row)+'.html',auto_open=False)
html_graphs.write("  <object data=\""+'Chart_'+str(row)+'.html'+"\" width=" + str(default_width * 1.10) + " height=" + str(default_height* 1.10) + "\"></object>"+"\n")

# %% [markdown]
# **********************************************************************************************************
# # State Totals
# **********************************************************************************************************
# %%
def plottotalcases(row, state, county = 'all'):
    if county == 'all':
        data = state_cov_data[state_cov_data.state == state][['date', 'cases']]
    else:
        data = county_cov_data[county_cov_data.state == state][['date', 'cases', 'county']]
        data = data[county_cov_data.county == county][['date', 'cases']]

    data = data[data.cases >= starting_cases]
    if len(data['cases']):
        data.index = [x for x in range(0, len(data))]

        if (county == 'all'):
            fig.add_trace(
                go.Scatter(x=data.index, y=data.cases, mode='lines', name=state, line = { 'width': default_line_thickness },
                hovertemplate='total cases: %{y:,.0f}<br>day: %{x}')
            )
        else:
            fig.add_trace(
                go.Scatter(x=data.index, y=data.cases, mode='lines', name=county + ', ' + state, line = { 'width': default_line_thickness },
                hovertemplate='total cases: %{y:,.0f}<br>day: %{x}')
            )

row += 1
starting_cases = 1000
layout = go.Layout(
        title = 'Total cases by state after hitting ' + str(starting_cases) + ' cases',
        plot_bgcolor = default_plot_color,
        xaxis_gridcolor = default_grid_color,
        yaxis_gridcolor = default_grid_color,
        width=default_width,
        height=default_height,
        xaxis_title='Days since ' + str(starting_cases) + ' cases were hit',
        yaxis_title='Total cases'
)

fig = go.Figure(layout=layout)
for s in states:
    plottotalcases(row, s)

fig.show()
plotly.offline.plot(fig, filename=webpage_folder + 'Chart_'+str(row)+'.html',auto_open=False)
html_graphs.write('''
<br/><br/><div>
<h1>State and County Total cases</h1>
</div>''')
html_graphs.write("  <object data=\""+'Chart_'+str(row)+'.html'+"\" width=" + str(default_width * 1.10) + " height=" + str(default_height* 1.10) + "\"></object>"+"\n")

#  %% [markdown]
# **********************************************************************************************************
# # County Totals
# **********************************************************************************************************
row += 1
starting_cases = 225
layout = go.Layout(
        title = 'Total cases by county after hitting ' + str(starting_cases) + ' cases',
        plot_bgcolor = default_plot_color,
        xaxis_gridcolor = default_grid_color,
        yaxis_gridcolor = default_grid_color,
        width=default_width,
        height=default_height,
        xaxis_title='Days since ' + str(starting_cases) + ' cases were hit',
        yaxis_title='Total cases'
)
fig = go.Figure(layout=layout)

for dataset in [county_cities_east_map, county_cities_midwest_map, county_cities_west_map]:
    starting_cases = 225
    for p in dataset.itertuples():
        plottotalcases(row, p.state, p.county)

fig.show()
plotly.offline.plot(fig, filename=webpage_folder + 'Chart_'+str(row)+'.html',auto_open=False)
html_graphs.write("  <object data=\""+'Chart_'+str(row)+'.html'+"\" width=" + str(default_width * 1.10) + " height=" + str(default_height* 1.10) + "\"></object>"+"\n")

#  %% [markdown]
# **********************************************************************************************************
# # State cases adjusted for population
# **********************************************************************************************************
#  %%
def stateplotpercapita(row, state):
    data = state_cov_data[state_cov_data.state == state][['date', 'cases']]
    data = data[data.cases >= starting_cases]
    state_population = population_state_density[population_state_density.state == state]
    if len(state_population):
        data.index = [x for x in range(0, len(data))]
        plotdata = (data.cases / state_population.population.values[0]) * 1000
        if len(data['cases']):
            fig.add_trace(
                go.Scatter(x=data.index, y=plotdata, mode='lines', name=state, line = { 'width': default_line_thickness },
                hovertemplate='cases per 1000: %{y:,.0f}<br>day: %{x}')
            )

row += 1
starting_cases = 1000
layout = go.Layout(
        title = 'Total state cases per 1,000 people after hitting ' + str(starting_cases) + ' cases',
        plot_bgcolor = default_plot_color,
        xaxis_gridcolor = default_grid_color,
        yaxis_gridcolor = default_grid_color,
        width=default_width,
        height=default_height,
        xaxis_title='Days since ' + str(starting_cases) + ' cases were hit',
        yaxis_title='Total cases per 1000 people'
)
fig=go.Figure(layout=layout)

for dataset in [states_east, states_midwest, states_west]:
    for s in dataset:
        stateplotpercapita(row, s)
fig.show()
plotly.offline.plot(fig, filename=webpage_folder + 'Chart_'+str(row)+'.html',auto_open=False)
html_graphs.write('''
<br/><br/><div>
<h1>State cases adjusted for population</h1><br/>
To better get a sense of how different states may be handling the virus outbreak, you can
adjust the graphs to account for the number of people who live in each state. A state that has
100,000 people vs 8,000,000 people will obviously look far better with regard to total cases
because they have 80x less people. By factoring in the population of a state, this is difference
is accounted for.
</div>''')
html_graphs.write("  <object data=\""+'Chart_'+str(row)+'.html'+"\" width=" + str(default_width * 1.10) + " height=" + str(default_height* 1.10) + "\"></object>"+"\n")

#  %% [markdown]
# **********************************************************************************************************
# # State cases adjusted for population density
# **********************************************************************************************************
#  %%
def stateplotbydensity(row, state):
    data = state_cov_data[state_cov_data.state == state][['date', 'cases']]
    data = data[data.cases >= starting_cases]
    state_density = population_state_density[population_state_density.state == state]
    if len(state_density):
        data.index = [x for x in range(0, len(data))]
        plotdata = (data.cases / state_density.density.values[0])
        if len(data['cases']):
            lastindex = len(data) - 1
            fig.add_trace(
                go.Scatter(x=data.index, y=plotdata, mode='lines', name=state, line = { 'width': default_line_thickness },
                hovertemplate='density adjusted cases: %{y:,.0f}<br>day: %{x}')
            )

row += 1
starting_cases = 225
layout = go.Layout(
        title = 'Total state trend after hitting ' + str(starting_cases) + ' cases factoring out population density',
        plot_bgcolor = default_plot_color,
        xaxis_gridcolor = default_grid_color,
        yaxis_gridcolor = default_grid_color,
        width=default_width,
        height=default_height,
        xaxis_title='Days since ' + str(starting_cases) + ' cases were hit',
        yaxis_title='Total density adjusted cases'
)
fig=go.Figure(layout=layout)

for dataset in [states_east, states_midwest, states_west]:
    for s in dataset:
        stateplotbydensity(row, s)
fig.show()
plotly.offline.plot(fig, filename=webpage_folder + 'Chart_'+str(row)+'.html',auto_open=False)
html_graphs.write('''
<br/><br/><div>
<h1>State cases adjusted for population density</h1><br/>
Each state has a population and an area in which this population lives. *Pretend* for a moment that Texas only has 100,000
people total. Also *pretend* that Rhode Island has 100,000 people. However, you also know that the
land area of Rhode Island is much, much smaller than that of Texas. So, if Rhode Island gets 5,000 cases of the virus
and Texas also gets 5,000 case, then you can say with high confidence that the people in Texas are likely completely
ignoring advice to keep a minimum distance from others. I mean how else could they have the same number of cases as Rhode Island
where the same number of people are packed together?<br/>
<br/>
This graph removes this consideration from the comparison between states. As you can see, New Jersey is doing far worse than
than Ohio, Washington and California.
</div>''')
html_graphs.write("  <object data=\""+'Chart_'+str(row)+'.html'+"\" width=" + str(default_width * 1.10) + " height=" + str(default_height* 1.10) + "\"></object>"+"\n")

#  %% [markdown]
# **********************************************************************************************************
# # City total cases adjusted for population density
# **********************************************************************************************************
#  %%
def cityplotbydensity(row, state, city):
    county = 'not found'
    for x in dataset.itertuples():
        if city in x.cities and state == x.state:
            county = x.county

    data = county_cov_data[county_cov_data.state == state][county_cov_data.county == county][['date', 'cases']]
    data = data[data.cases >= starting_cases]
    city_density = population_city_density[population_city_density.state == state][population_city_density.city == city]
    if (len(city_density)):
        data.index = [x for x in range(0, len(data))]
        plotdata = data.cases / city_density.density.values[0]
        if len(data['cases']):
            lastindex = len(data) - 1
            fig.add_trace(
                go.Scatter(x=data.index, y=plotdata, mode='lines', name=city + ', ' + state, line = { 'width': default_line_thickness },
                    hovertemplate='density adjusted cases: %{y:,.3f}<br>day: %{x}')
            )

row += 1
starting_cases = 20
layout = go.Layout(
        title = 'Total city trend after hitting ' + str(starting_cases) + ' cases factoring out population density',
        plot_bgcolor = default_plot_color,
        xaxis_gridcolor = default_grid_color,
        yaxis_gridcolor = default_grid_color,
        width=default_width,
        height=default_height,
        xaxis_title='Days since ' + str(starting_cases) + ' cases were hit',
        yaxis_title='Total density adjusted cases'
)
fig=go.Figure(layout=layout)

for dataset in [county_cities_east_map, county_cities_midwest_map, county_cities_west_map]:
    for p in dataset.itertuples():
        for c in p.cities:
            cityplotbydensity(row, p.state, c)

fig.show()
plotly.offline.plot(fig, filename=webpage_folder + 'Chart_'+str(row)+'.html',auto_open=False)
html_graphs.write('''
<br/><br/><div>
<h1>City total cases adjusted for population density</h1><br/>
Same trends as described for state cases adjusted for population density, but applied at the city level instead. The intent of
this graph is to discount the consideration that some cities growth rates are so fast because those cities are so densely populated.
This was a common explanation as to why New York was growing so much faster than other cities.
</div>''')
html_graphs.write("  <object data=\""+'Chart_'+str(row)+'.html'+"\" width=" + str(default_width * 1.10) + " height=" + str(default_height* 1.10) + "\"></object>"+"\n")


#  %% [markdown]
# **********************************************************************************************************
# # City deaths adjusted for population density
# **********************************************************************************************************
#  %%
def citydeathsplotbydensity(row, state, city):
    county = 'not found'
    for x in dataset.itertuples():
        if city in x.cities and state == x.state:
            county = x.county

    data = county_cov_data[county_cov_data.state == state][county_cov_data.county == county][['date', 'deaths']]
    data = data[data.deaths >= starting_deaths]
    city_density = population_city_density[population_city_density.state == state][population_city_density.city == city]
    if (len(city_density)):
        data.index = [x for x in range(0, len(data))]
        plotdata = data.deaths / city_density.density.values[0]
        if len(data['deaths']):
            fig.add_trace(
                go.Scatter(x=data.index, y=plotdata.values, mode='lines', name=city + ', ' + state, line = { 'width': default_line_thickness },
                hovertemplate='density adjusted deaths: %{y}<br>day: %{x}')
            )

row += 1
layout = go.Layout(
        title = 'Total city deaths trend after hitting ' + str(starting_cases) + ' cases factoring out population density',
        plot_bgcolor = default_plot_color,
        xaxis_gridcolor = default_grid_color,
        yaxis_gridcolor = default_grid_color,
        width=default_width,
        height=default_height,
        xaxis_title='Days since first person died from covid-19',
        yaxis_title='Total density adjusted cases'
)
fig=go.Figure(layout=layout)
for dataset in [county_cities_east_map, county_cities_midwest_map, county_cities_west_map]:
    starting_deaths = 1
    for p in dataset.itertuples():
        for c in p.cities:
            citydeathsplotbydensity(row, p.state, c)
fig.show()
plotly.offline.plot(fig, filename=webpage_folder + 'Chart_'+str(row)+'.html',auto_open=False)
html_graphs.write('''
<br/><br/><div>
<h1>City <b>deaths</b> adjusted for population density</h1><br/>
See description above concerning cases adjusted for population density. This is the same, but is about deaths, not just cases.
</div>''')
html_graphs.write("  <object data=\""+'Chart_'+str(row)+'.html'+"\" width=" + str(default_width * 1.10) + " height=" + str(default_height* 1.10) + "\"></object>"+"\n")

html_graphs.write('</body></html')
html_graphs.close()

# %%
print('Total run time: ', time.clock() - t0)





# %%
