# %% [markdown]
# * Looks like the press is starting to ask some of the same questions I'm asking with this analysis:
#     * https://www.mercurynews.com/2020/04/08/how-california-has-contained-coronavirus-and-new-york-has-not/
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
html_graphs.write("<html><head><style>div {margin-left:50px; margin-right:5%; font-family: \"Verdana\"}</style></head><body>"+"\n")
html_graphs.write('<div style=\'margin:50px\'><h1>Data as of ' + datetime.now().strftime('%m/%d/%y')+ '<br/></h1>')
#html_graphs.write('<div style=\'margin:50px\'><h1>Data as of 04/25/2020<br/></h1>')
html_graphs.write('''
Please wait to load all the graphs. This page is not setup to be fast loading. :)<br/><br/>

<h2> Things you can do on each graph </h2>
<ul>
<li> Hover your mouse over a trend line to find which location it refers to.
<li> Single click on a location to show and hide that location's trend line.
<li> Double click on a location to show only that location OR show ALL locations in that graph.
</ul>
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

population_county = pd.read_csv('county-population-2013.csv')
population_county.drop(columns={'Core_Based_Statistical_Area'}, inplace=True)
population_county.rename(columns={'population2013': 'population'}, inplace=True)
population_county.index = [population_county.county, population_county.state]

population_city_density = pd.read_csv('city_density.csv')
population_city_density = population_city_density.rename(columns={'City': 'citystate', 'Population Density (Persons/Square Mile)': 'density', '2016 Population': 'population', 'Land Area (Square Miles)': 'area'} )
population_city_density[['city', 'state']] = population_city_density.citystate.str.split(', ', expand=True)

population_state_density = pd.read_csv('state_density.csv')
population_state_density = population_state_density.rename(columns={'State': 'state', 'Density': 'density', 'Pop': 'population', 'LandArea': 'area'})

# Create a state abbreviation to full name mapping dataframe.
state_abbrev = pd.read_csv('StateAbbrev.csv')
state_abbrev.index = state_abbrev.abbrev
state_abbrev.drop(columns='abbrev', inplace=True)

# Get the land area table for county, split the 'county, SS' column into two.
county_land_area = pd.read_csv('LandAreaCounties.csv')
county_density = county_land_area['Areaname'].str.split(', ', n=1, expand=True)
county_density.rename(columns={0: 'county', 1: 'state'}, inplace=True)
county_density.dropna(inplace=True)
county_density.state = county_density.state.map(state_abbrev.state)

county_land_area['county'] = county_density.county
county_land_area['state'] = county_density.state
county_land_area.dropna(inplace=True)
county_land_area['key'] = county_land_area.county + ',' + county_land_area.state
county_land_area.drop_duplicates(subset='key', inplace=True)
county_land_area.index = county_land_area.key
county_land_area.drop(columns={'Areaname', 'county', 'state', 'key'}, inplace=True)

county_density['population'] = population_county.loc[list(county_density.itertuples(name=None, index=False))].population.values
county_density['key'] = county_density.county + ',' + county_density.state
county_density['area'] = county_density.key.map(county_land_area.land_area)
county_density['density'] = county_density.population / county_density.area
county_density.dropna(subset=['density'], inplace=True)
county_density.drop_duplicates(subset= ['county', 'state'], inplace=True)

interesting_locations_east = [
    ['Connecticut', '', [], False],
    ['Delaware', '', [], False],
    ['District of Columbia', 'District of Columbia', ['District of Columbia'], False],
    ['Maine', '', [], False],
    ['Maryland', '', [], False],
    ['Massachusetts', 'Suffolk', ['Boston'], False],
    ['New Hampshire', '', [], False],
    ['New Jersey', 'Bergen', ['Newark', 'Jersey City'], False],
    ['New York', 'Bronx', ['New York'], False],
    ['New York', 'Brooklyn', ['New York'], False],
    ['New York', 'Kings', ['New York'], False],
    ['New York', 'Manhattan', ['New York'], False],
    ['New York', 'New York City', ['New York'], False],
    ['New York', 'Queens', ['New York'], False],
    ['New York', 'Staten Island', ['New York'], False],
    ['Pennsylvania', 'Philadelphia', ['Philadelphia'], False],
    ['Rhode Island', '', [], False],
    ['Vermont', '', [], False],
    ['Virginia', '', [], False],
    ['West Virginia', '', [], False]
]

interesting_locations_west = [
    ['Alaska', '', [], False],
    ['Arizona', 'Maricopa', ['Phoenix'], False],
    ['California', 'Los Angeles', ['Los Angeles'], False],
    ['California', 'San Diego', ['San Diego'], False],
    ['California', 'San Francisco', ['San Francisco'], False],
    ['Colorado', '', [], False],
    ['Hawaii', '', [], False],
    ['Idaho', '', [], False],
    ['Montana', '', [], False],
    ['Nevada', '', [], False],
    ['New Mexico', '', [], False],
    ['Oregon', '', [], False],
    ['Utah', '', [], False],
    ['Washington', 'King', ['Seattle'], True],
    ['Washington', 'Snohomish', ['Everett'], True],
    ['Wyoming', '', [], False],
]

interesting_locations_south = [
    ['Alabama', '', [], False],
    ['Arkansas', '', [], False],
    ['Florida', 'Broward', ['Fort Lauderdale'], False],
    ['Florida', 'Duval', ['Jacksonville'], False],
    ['Florida', 'Miami-Dade', ['Miami'], False],
    ['Georgia', 'Fulton', ['Atlanta'], False],
    ['Louisiana', 'Orleans', ['New Orleans'], False],
    ['Mississippi', '', [], False],
    ['North Carolina', '', [], False],
    ['Oklahoma', '', [], False],
    ['South Carolina', 'Charleston', ['Charleston'], True],
    ['Tennessee', 'Davidson', ['Nashville'], True],
    ['Texas', 'Bexar', ['San Antonio'], False],
    ['Texas', 'Dallas', ['Dallas'], False],
    ['Texas', 'Harris', ['Houston'], False],
    ['Texas', 'Potter', ['Amarillo'], True],
    ['Texas', 'Travis', ['Austin'], False],
]

interesting_locations_midwest = [
    ['Illinois', 'Cook', ['Chicago'], False],
    ['Indiana', 'Hamilton', ['Carmel'], False],
    ['Indiana', 'Marion', ['Indianapolis'], False],
    ['Iowa', 'Polk', ['Des Moines'], True],
    ['Kansas', '', [], False],
    ['Kentucky', 'Muhlenberg', ['Central City'], True],
    ['Michigan', 'Wayne', ['Detroit'], False],
    ['Minnesota', '', [], False],
    ['Missouri', '', [], False],
    ['Nebraska', '', [], False],
    ['North Dakota', '', [], False],
    ['Ohio', 'Cuyahoga', ['Cleveland'], True],
    ['South Dakota', '', [], False],
    ['Wisconsin', 'Milwaukee', ['Milwaukee'], False],
]

interesting_locations_east_df = pd.DataFrame(interesting_locations_east, columns = ['state', 'county', 'cities', 'show_by_default'])
interesting_locations_west_df = pd.DataFrame(interesting_locations_west, columns = ['state', 'county', 'cities', 'show_by_default'])
interesting_locations_midwest_df = pd.DataFrame(interesting_locations_midwest, columns = ['state', 'county', 'cities', 'show_by_default'])
interesting_locations_south_df = pd.DataFrame(interesting_locations_south, columns = ['state', 'county', 'cities', 'show_by_default'])

interesting_states_east = interesting_locations_east_df.sort_values(by='show_by_default').drop_duplicates(subset='state', keep='last')
interesting_states_west = interesting_locations_west_df.sort_values(by='show_by_default').drop_duplicates(subset='state', keep='last')
interesting_states_midwest = interesting_locations_midwest_df.sort_values(by='show_by_default').drop_duplicates(subset='state', keep='last')
interesting_states_south = interesting_locations_south_df.sort_values(by='show_by_default').drop_duplicates(subset='state', keep='last')
interesting_states = pd.concat([interesting_states_east, interesting_states_midwest, interesting_states_west, interesting_states_south])
interesting_states.reset_index(inplace=True)
interesting_states.sort_values(by='state', inplace=True)

interesting_locations = pd.concat([interesting_locations_east_df, interesting_locations_west_df, interesting_locations_midwest_df, interesting_locations_south_df])
interesting_locations.reset_index(inplace=True)

# %% [markdown]
# **********************************************************************************************************
# # New cases per day
# **********************************************************************************************************
# %%
def movingaverage(values, window):
    weights = np.repeat(1.0, window)/window
    sma = np.convolve(values, weights, 'valid')
    return sma

def plotnewcases(state='all', county='all', show_by_default=True):
    if (state == 'all'):
        total_cases_by_date = state_cov_data.groupby('date').sum()
        minimum_cases = 100
    elif (county == 'all'):
        total_cases_by_date = state_cov_data[state_cov_data.state == state].groupby('date').sum()
        minimum_cases = 15
    else:
        total_cases_by_date = county_cov_data[(county_cov_data.state == state) & (county_cov_data.county == county)].groupby('date').sum()
        minimum_cases = 15

    if (len(total_cases_by_date) > 0):
        total_cases_by_date = total_cases_by_date.reset_index()
        total_cases_by_date = total_cases_by_date[total_cases_by_date.cases > minimum_cases]
        delta_cases = total_cases_by_date.cases.to_numpy()[1:] - total_cases_by_date.head(len(total_cases_by_date)-1).cases.to_numpy()[0:]

        delta_cases_ma = movingaverage(delta_cases, 7)
        df = pd.DataFrame(delta_cases_ma, columns=['new'])
        df['days'] = df.index
        df = df[df.new.gt(0).idxmax():]
        df.reset_index(inplace=True)

        if (state != 'all' and county != 'all'):
            name = state + ' - ' + county
        else:
            name = state

        if (show_by_default):
            visible = True
        else:
            visible = 'legendonly'

        fig.add_trace(
            go.Scatter(x=df.days, y=df.new, mode='lines', name=name, line = { 'width': default_line_thickness },
            hovertemplate='new cases: %{y:,.0f}<br>day: %{x}', visible=visible)
        )

row = 1
layout = go.Layout(
        title = 'New cases for US',
        plot_bgcolor = default_plot_color,
        xaxis_gridcolor = default_grid_color,
        yaxis_gridcolor = default_grid_color,
        width=default_width,
        height=default_height,
        xaxis_title='Days since new cases started increasing',
        yaxis_title='New cases'
)
fig = go.Figure(layout=layout)
plotnewcases()

fig.show()
plotly.offline.plot(fig, filename=webpage_folder + 'Chart_'+str(row)+'.html',auto_open=False)
html_graphs.write('''
<br/><br/><div>
<h1>New cases per day</h1><br/>
This trend line is a moving average of new cases over time. First for the US overall then by state (not all are represented here, just ones I found most interesting.
</div>''')
html_graphs.write("  <object data=\""+'Chart_'+str(row)+'.html'+"\" width=" + str(default_width * 1.10) + " height=" + str(default_height* 1.10) + "\"></object>"+"\n")


#############################
# New cases by state
#############################
row += 1
layout = go.Layout(
        title = 'New cases by state',
        plot_bgcolor = default_plot_color,
        xaxis_gridcolor = default_grid_color,
        yaxis_gridcolor = default_grid_color,
        width=default_width,
        height=default_height,
        xaxis_title='Days since new cases started increasing',
        yaxis_title='New cases'
)

fig = go.Figure(layout=layout)
for index, state in interesting_states.iterrows():
    plotnewcases(state.state, 'all', state.show_by_default)

fig.show()
plotly.offline.plot(fig, filename=webpage_folder + 'Chart_'+str(row)+'.html',auto_open=False)
html_graphs.write("  <object data=\""+'Chart_'+str(row)+'.html'+"\" width=" + str(default_width * 1.10) + " height=" + str(default_height* 1.10) + "\"></object>"+"\n")

#############################
# New cases by county
#############################
row += 1
layout = go.Layout(
        title = 'New cases by county',
        plot_bgcolor = default_plot_color,
        xaxis_gridcolor = default_grid_color,
        yaxis_gridcolor = default_grid_color,
        width=default_width,
        height=default_height,
        xaxis_title='Days since new cases started increasing',
        yaxis_title='New cases'
)

fig = go.Figure(layout=layout)
for index, r in interesting_locations.iterrows():
    plotnewcases(r.state, r.county, r.show_by_default)

fig.show()
plotly.offline.plot(fig, filename=webpage_folder + 'Chart_'+str(row)+'.html',auto_open=False)
html_graphs.write("  <object data=\""+'Chart_'+str(row)+'.html'+"\" width=" + str(default_width * 1.10) + " height=" + str(default_height* 1.10) + "\"></object>"+"\n")


# %% [markdown]
# **********************************************************************************************************
# # State Totals
# **********************************************************************************************************
# %%
def plottotalcases(state, county = 'all', show_by_default=True):
    if county == 'all':
        data = state_cov_data[state_cov_data.state == state][['date', 'cases']]
    else:
        data = county_cov_data[county_cov_data.state == state][['date', 'cases', 'county']]
        data = data[county_cov_data.county == county][['date', 'cases']]

    data = data[data.cases >= starting_cases]
    if len(data['cases']):
        data.index = [x for x in range(0, len(data))]

        if (show_by_default):
            visible = True
        else:
            visible = 'legendonly'

        if (county == 'all'):
            fig.add_trace(
                go.Scatter(x=data.index, y=data.cases, mode='lines', name=state, line = { 'width': default_line_thickness },
                hovertemplate='total cases: %{y:,.0f}<br>day: %{x}', visible=visible)
            )
        else:
            fig.add_trace(
                go.Scatter(x=data.index, y=data.cases, mode='lines', name=county + ', ' + state, line = { 'width': default_line_thickness },
                hovertemplate='total cases: %{y:,.0f}<br>day: %{x}', visible=visible)
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
for index, s in interesting_states.iterrows():
    plottotalcases(s.state, 'all', s.show_by_default)

fig.show()
plotly.offline.plot(fig, filename=webpage_folder + 'Chart_'+str(row)+'.html',auto_open=False)
html_graphs.write('''
<br/><br/><div>
<h1>State and County Total cases</h1>
The simplest count is just a total number of cases per state and then per interesting county. Nothing more than what each state is reporting
as new cases on a daily basis.
</div>''')
html_graphs.write("  <object data=\""+'Chart_'+str(row)+'.html'+"\" width=" + str(default_width * 1.10) + " height=" + str(default_height* 1.10) + "\"></object>"+"\n")

###########################
# County Totals
###########################
row += 1
starting_cases = 200
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

for index, r in interesting_locations.iterrows():
    plottotalcases(r.state, r.county, r.show_by_default)

fig.show()
plotly.offline.plot(fig, filename=webpage_folder + 'Chart_'+str(row)+'.html',auto_open=False)
html_graphs.write("  <object data=\""+'Chart_'+str(row)+'.html'+"\" width=" + str(default_width * 1.10) + " height=" + str(default_height* 1.10) + "\"></object>"+"\n")

#  %% [markdown]
# **********************************************************************************************************
# # State cases adjusted for population
# **********************************************************************************************************
#  %%
def stateplotpercapita(state, show_by_default):
    data = state_cov_data[state_cov_data.state == state][['date', 'cases']]
    data = data[data.cases >= starting_cases]
    state_population = population_state_density[population_state_density.state == state]
    if len(state_population):
        data.index = [x for x in range(0, len(data))]
        plotdata = (data.cases / state_population.population.values[0]) * 1000
        if len(data['cases']):
            if (show_by_default):
                visible = True
            else:
                visible = 'legendonly'

            fig.add_trace(
                go.Scatter(x=data.index, y=plotdata, mode='lines', name=state + ' (' + str.format('{0:,}', state_population.population.values[0]) + ' people)', line = { 'width': default_line_thickness },
                hovertemplate='cases per 1000: %{y:,.0f}<br>day: %{x}', visible=visible)
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
        yaxis_title='Total cases per 1,000 people'
)
fig=go.Figure(layout=layout)

for index, s in interesting_states.iterrows():
    stateplotpercapita(s.state, s.show_by_default )

fig.show()
plotly.offline.plot(fig, filename=webpage_folder + 'Chart_'+str(row)+'.html',auto_open=False)
html_graphs.write('''
<br/><br/><div>
<h1>State and County cases adjusted for population</h1><br/>
Total cases is one thing, but to better get a sense of how different states and counties may be handling the virus compared to others,
you can adjust the graphs to account for the number of people who live in each state. A state that has 100,000 people vs
one that has 8,000,000 people should obviously have far fewer total cases because they have 80x less people. By factoring
in the population, a state or county with a low population may show a slope as high as other states with far more people.
This would indicate that the lower population state isn't likely effectively quarantining nearly as much as a higher
population state.
</div>''')
html_graphs.write("  <object data=\""+'Chart_'+str(row)+'.html'+"\" width=" + str(default_width * 1.10) + " height=" + str(default_height* 1.10) + "\"></object>"+"\n")

#################################################
# County cases adjusted for population
#################################################
#  %%
def countyplotpercapita(state, county, show_by_default):
    data = county_cov_data[county_cov_data.state == state][['date', 'cases', 'county']]
    data = data[county_cov_data.county == county][['date', 'cases']]
    data = data[data.cases >= starting_cases]
    county_population = population_county[(population_county.state == state) & (population_county.county == county)]
    if len(county_population):
        data.index = [x for x in range(0, len(data))]
        plotdata = (data.cases / county_population.population.values[0]) * 1000
        if len(data['cases']):
            if (show_by_default):
                visible = True
            else:
                visible = 'legendonly'

            fig.add_trace(
                go.Scatter(x=data.index, y=plotdata, mode='lines', name=county + ', ' + state + ' (' + str.format('{0:,}', county_population.population.values[0]) + ' people)', line = { 'width': default_line_thickness },
                hovertemplate='cases per 1000: %{y:,.0f}<br>day: %{x}', visible=visible)
            )

row += 1
starting_cases = 50
layout = go.Layout(
        title = 'Total county cases per 1,000 people after hitting ' + str(starting_cases) + ' cases',
        plot_bgcolor = default_plot_color,
        xaxis_gridcolor = default_grid_color,
        yaxis_gridcolor = default_grid_color,
        width=default_width,
        height=default_height,
        xaxis_title='Days since ' + str(starting_cases) + ' cases were hit',
        yaxis_title='Total cases per 1,000 people'
)
fig=go.Figure(layout=layout)

for index, r in interesting_locations.iterrows():
    countyplotpercapita(r.state, r.county, r.show_by_default)

fig.show()
plotly.offline.plot(fig, filename=webpage_folder + 'Chart_'+str(row)+'.html',auto_open=False)
html_graphs.write("  <object data=\""+'Chart_'+str(row)+'.html'+"\" width=" + str(default_width * 1.10) + " height=" + str(default_height* 1.10) + "\"></object>"+"\n")

#  %% [markdown]
# **********************************************************************************************************
# # State cases adjusted for population density
# **********************************************************************************************************
#  %%
def stateplotbydensity(state, show_by_default):
    data = state_cov_data[state_cov_data.state == state][['date', 'cases']]
    data = data[data.cases >= starting_cases]
    state_density = population_state_density[population_state_density.state == state]
    if len(state_density):
        data.index = [x for x in range(0, len(data))]
        plotdata = (data.cases / state_density.density.values[0])
        if len(data['cases']):
            lastindex = len(data) - 1
            if (show_by_default):
                visible = True
            else:
                visible = 'legendonly'

            fig.add_trace(
                go.Scatter(x=data.index, y=plotdata, mode='lines', name=state + ' (' + str.format('{0:,}', int(round(state_density.density.values[0],0))) + ' ppl/mi^2)', line = { 'width': default_line_thickness },
                hovertemplate='density adjusted cases: %{y:,.0f}<br>day: %{x}', visible=visible)
            )

row += 1
starting_cases = 200
layout = go.Layout(
        title = 'Total state trend after hitting ' + str(starting_cases) + ' cases factoring in population density',
        plot_bgcolor = default_plot_color,
        xaxis_gridcolor = default_grid_color,
        yaxis_gridcolor = default_grid_color,
        width=default_width,
        height=default_height,
        xaxis_title='Days since ' + str(starting_cases) + ' cases were hit',
        yaxis_title='Total density adjusted cases'
)
fig=go.Figure(layout=layout)

for index, s in interesting_states.iterrows():
    stateplotbydensity(s.state, s.show_by_default)

fig.show()
plotly.offline.plot(fig, filename=webpage_folder + 'Chart_'+str(row)+'.html',auto_open=False)
html_graphs.write('''
<br/><br/><div>
<h1>State cases adjusted for population density</h1><br/>
Each state and county obviously has a population and an area in which this population lives. *Pretend* for a moment that Texas only has 1,000,000
people total. Also *pretend* that Rhode Island has 1,000,000 people. The land area of Rhode Island is much, much smaler than that of Texas. So, if both states
have a total of 5,000 covid-19 cases over the same number of days since the outbreak began in that state, you can say with high confidence that the people
in Texas are likely not effectively managing to stay as safe as they are in Rhode Island.<br/>
<br/>
This graph factors in this consideration for comparison between states and counties
</div>''')
html_graphs.write("  <object data=\""+'Chart_'+str(row)+'.html'+"\" width=" + str(default_width * 1.10) + " height=" + str(default_height* 1.10) + "\"></object>"+"\n")


#  %% [markdown]
# **********************************************************************************************************
# # County cases adjusted for population density
# **********************************************************************************************************
#  %%
def countyplotbydensity(county, state, show_by_default):
    data = county_cov_data[(county_cov_data.county == county) & (county_cov_data.state == state)][['date', 'cases']]
    data = data[data.cases >= starting_cases]
    density = county_density[(county_density.county == county) & (county_density.state == state)]
    if len(density):
        data.index = [x for x in range(0, len(data))]
        plotdata = (data.cases / density.density.values[0])
        if len(data['cases']):
            lastindex = len(data) - 1
            if (show_by_default):
                visible = True
            else:
                visible = 'legendonly'

            fig.add_trace(
                go.Scatter(x=data.index, y=plotdata, mode='lines', name=state + ' - ' + county + ' (' + str.format('{0:,}', int(round(density.density))) + ' ppl/mi^2)', line = { 'width': default_line_thickness },
                hovertemplate='density adjusted cases: %{y:,.0f}<br>day: %{x}', visible=visible)
            )

row += 1
starting_cases = 50
layout = go.Layout(
        title = 'Total county trend after hitting ' + str(starting_cases) + ' cases factoring in population density',
        plot_bgcolor = default_plot_color,
        xaxis_gridcolor = default_grid_color,
        yaxis_gridcolor = default_grid_color,
        width=default_width,
        height=default_height,
        xaxis_title='Days since ' + str(starting_cases) + ' cases were hit',
        yaxis_title='Total density adjusted cases'
)
fig=go.Figure(layout=layout)

for index, r in interesting_locations.iterrows():
    countyplotbydensity(r.county, r.state, r.show_by_default)
fig.show()
plotly.offline.plot(fig, filename=webpage_folder + 'Chart_'+str(row)+'.html',auto_open=False)
html_graphs.write("  <object data=\""+'Chart_'+str(row)+'.html'+"\" width=" + str(default_width * 1.10) + " height=" + str(default_height* 1.10) + "\"></object>"+"\n")

# Do all states
for index, s in interesting_states.iterrows():
    starting_cases = 5
    layout = go.Layout(
            title = s.state + ' State county trends after hitting ' + str(starting_cases) + ' cases factoring in population density',
            plot_bgcolor = default_plot_color,
            xaxis_gridcolor = default_grid_color,
            yaxis_gridcolor = default_grid_color,
            width=default_width,
            height=default_height,
            xaxis_title='Days since ' + str(starting_cases) + ' cases were hit',
            yaxis_title='Total density adjusted cases'
    )
    fig=go.Figure(layout=layout)

    for index, r in county_density[county_density.state == s.state].iterrows():
        countyplotbydensity(r.county, r.state, True)
    # fig.show()
    plotly.offline.plot(fig, filename=webpage_folder + s.state + '_by_density.html', auto_open=False)
    html_graphs.write("<br/><a style=\'margin:50px\' href='" + s.state + "_by_density.html'>" + s.state + "</a>\n")

#  %% [markdown]
# **********************************************************************************************************
# # City cases adjusted for population
# **********************************************************************************************************
#  %%
def cityplotpercapita(state, city, show_by_default):
    county = 'not found'
    for index, x in interesting_locations.iterrows():
        if city in x.cities and state == x.state:
            county = x.county

    cov_at_county_level = county_cov_data[county_cov_data.state == state][county_cov_data.county == county][['date', 'cases']]
    cov_at_county_level = cov_at_county_level[cov_at_county_level.cases >= starting_cases]
    city_population = population_city_density[population_city_density.state == state][population_city_density.city == city]
    if (len(city_population)):
        cov_at_county_level.index = [x for x in range(0, len(cov_at_county_level))]
        plotdata = (cov_at_county_level.cases / city_population.population.values[0]) * 1000
        if len(cov_at_county_level['cases']):
            lastindex = len(cov_at_county_level) - 1
            if (show_by_default):
                visible = True
            else:
                visible = 'legendonly'

            fig.add_trace(
                go.Scatter(x=cov_at_county_level.index, y=plotdata, mode='lines', name=city + ', ' + state + ' (' + str.format('{0:,}', city_population.population.values[0],0) + ' people)', line = { 'width': default_line_thickness },
                    hovertemplate='cases per 1000: %{y:,.3f}<br>day: %{x}', visible=visible)
            )

row += 1
starting_cases = 20
layout = go.Layout(
        title = 'Total city cases per 1,000 people after hitting ' + str(starting_cases) + ' cases',
        plot_bgcolor = default_plot_color,
        xaxis_gridcolor = default_grid_color,
        yaxis_gridcolor = default_grid_color,
        width=default_width,
        height=default_height,
        xaxis_title='Days since ' + str(starting_cases) + ' cases were hit',
        yaxis_title='Total cases per 1,000 people'
)
fig=go.Figure(layout=layout)

for index, r in interesting_locations[~interesting_locations['cities'].apply(tuple).duplicated()].iterrows():
    for c in r.cities:
        cityplotpercapita(r.state, c, r.show_by_default)

fig.show()
plotly.offline.plot(fig, filename=webpage_folder + 'Chart_'+str(row)+'.html',auto_open=False)
html_graphs.write('''
<br/><br/><div>
<h1>City total cases adjusted for population</h1><br/>
You can do the same types of adjustments as we did for state and county at the city level.
A city that has 100,000 people vs 8,000,000 people will obviously look far better with regard to total cases
because they have 80x less people. By factoring in the population of a city, this is difference
is accounted for.
</div>''')
html_graphs.write("  <object data=\""+'Chart_'+str(row)+'.html'+"\" width=" + str(default_width * 1.10) + " height=" + str(default_height* 1.10) + "\"></object>"+"\n")

#  %% [markdown]
# **********************************************************************************************************
# # City total cases adjusted for population density
# **********************************************************************************************************
#  %%
def cityplotbydensity(state, city, show_by_default):
    county = 'not found'
    for index, x in interesting_locations.iterrows():
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
            if (show_by_default):
                visible = True
            else:
                visible = 'legendonly'

            fig.add_trace(
                go.Scatter(x=data.index, y=plotdata, mode='lines', name=city + ', ' + state + ' (' + str.format('{0:,}', int(round(city_density.density.values[0],0))) + ' ppl/mi^2)', line = { 'width': default_line_thickness },
                    hovertemplate='density adjusted cases: %{y:,.3f}<br>day: %{x}', visible=visible)
            )

row += 1
starting_cases = 20
layout = go.Layout(
        title = 'Total city trend after hitting ' + str(starting_cases) + ' cases factoring in population density',
        plot_bgcolor = default_plot_color,
        xaxis_gridcolor = default_grid_color,
        yaxis_gridcolor = default_grid_color,
        width=default_width,
        height=default_height,
        xaxis_title='Days since ' + str(starting_cases) + ' cases were hit',
        yaxis_title='Total density adjusted cases'
)
fig=go.Figure(layout=layout)

for index, r in interesting_locations[~interesting_locations['cities'].apply(tuple).duplicated()].iterrows():
    for c in r.cities:
        cityplotbydensity(r.state, c, r.show_by_default)

fig.show()
plotly.offline.plot(fig, filename=webpage_folder + 'Chart_'+str(row)+'.html',auto_open=False)
html_graphs.write('''
<br/><br/><div>
<h1>City total cases adjusted for population density</h1><br/>
Same trends as described for state cases adjusted for population density, but applied at the city level instead. The intent of
this graph is to discount the consideration that some cities growth rates are so fast because those cities are so densely populated.
This was a common explanation as to why New York was growing so much faster than other cities. Though even when taking density into account,
New York's trend <b>still</b> beats all others, but other cities are much closer!
</div>''')
html_graphs.write("  <object data=\""+'Chart_'+str(row)+'.html'+"\" width=" + str(default_width * 1.10) + " height=" + str(default_height* 1.10) + "\"></object>"+"\n")


#  %% [markdown]
# **********************************************************************************************************
# # City deaths adjusted for population density
# **********************************************************************************************************
#  %%
def citydeathsplotbydensity(state, city, show_by_default):
    county = 'not found'
    for index, x in interesting_locations.iterrows():
        if city in x.cities and state == x.state:
            county = x.county

    data = county_cov_data[county_cov_data.state == state][county_cov_data.county == county][['date', 'deaths']]
    data = data[data.deaths >= starting_deaths]
    city_density = population_city_density[population_city_density.state == state][population_city_density.city == city]
    if (len(city_density)):
        data.index = [x for x in range(0, len(data))]
        plotdata = data.deaths / city_density.density.values[0]
        if len(data['deaths']):
            if (show_by_default):
                visible = True
            else:
                visible = 'legendonly'

            fig.add_trace(
                go.Scatter(x=data.index, y=plotdata.values, mode='lines', name=city + ', ' + state + ' (' + str.format('{0:,}', int(round(city_density.density.values[0],0))) + ' ppl/mi^2)', line = { 'width': default_line_thickness },
                hovertemplate='density adjusted deaths: %{y}<br>day: %{x}', visible=visible)
            )

row += 1
layout = go.Layout(
        title = 'Total city deaths trend after the first death factoring in population density',
        plot_bgcolor = default_plot_color,
        xaxis_gridcolor = default_grid_color,
        yaxis_gridcolor = default_grid_color,
        width=default_width,
        height=default_height,
        xaxis_title='Days since first person died from covid-19',
        yaxis_title='Total density adjusted deaths'
)
fig=go.Figure(layout=layout)
starting_deaths = 1

for index, r in interesting_locations[~interesting_locations['cities'].apply(tuple).duplicated()].iterrows():
    for c in r.cities:
        citydeathsplotbydensity(r.state, c, r.show_by_default)

fig.show()
plotly.offline.plot(fig, filename=webpage_folder + 'Chart_'+str(row)+'.html',auto_open=False)
html_graphs.write('''
<br/><br/><div>
<h1>City <b>deaths</b> adjusted for population density</h1><br/>
See description above concerning cases adjusted for population density. This is the same, but is about deaths, not just cases.
</div>''')
html_graphs.write("  <object data=\""+'Chart_'+str(row)+'.html'+"\" width=" + str(default_width * 1.10) + " height=" + str(default_height* 1.10) + "\"></object>"+"\n")

# %%
html_graphs.write('</body></html')
html_graphs.close()

# %%
print('Total run time: ', time.clock() - t0)





# %%
