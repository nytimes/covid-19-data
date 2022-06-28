# %% [markdown]
#  * Reference Sites
#      * https://github.com/greazer/covid-19-data
#      * https://www.mercurynews.com/2020/04/08/how-california-has-contained-coronavirus-and-new-york-has-not/
#      * https://www.cdc.gov/nchs/covid19/covid-19-mortality-data-files.htm
#      * https://data.cdc.gov/NCHS/Provisional-COVID-19-Death-Counts-by-Sex-Age-and-S/9bhg-hcku
#      * https://healthdata.gov/dataset/covid-19-reported-patient-impact-and-hospital-capacity-state-timeseries

# %%
import time
t0 = time.perf_counter()

import sys
IN_COLAB = 'google.colab' in sys.modules
IN_AZUREML = 'azureml' in sys.modules

# %%
# DID YOU SET covid_ftp_pw?
import os
os.environ['covid_ftp_pw'] = ''

# %%
if IN_COLAB:
    from google.colab import drive
    drive.mount('/content/drive')

# %%
import os
from IPython.core.display import display, HTML
if (os.name == 'nt'):
    basefolder = os.getcwd() + '\\'
elif IN_COLAB:
    basefolder = os.getcwd() + '/drive/MyDrive/Colab Notebooks/covid-19-data-1/SampleNbsAndScripts/'
elif IN_AZUREML:
    basefolder = os.getcwd() + '/../'
else: 
    basefolder = os.getcwd() + '/'

print('basefolder = ' + basefolder)
#display(HTML(F'<H1>Hello from <span style="color:{color};">' + str.upper(os.name) + '</span>!!!!</H1>'))

# %%
import pandas as pd
import numpy as np
from datetime import datetime
import plotly.graph_objects as go
import plotly
import plotly.io as pio
from plotly.subplots import make_subplots
from sodapy import Socrata

default_line_thickness=2
default_width = 1280
default_height = 800
default_plot_color = 'rgba(0, 0, 0, 0)'
default_grid_color = 'rgba(225, 225, 225, 255)'

# %%
webpage_folder = basefolder + 'webpage/'
if not os.path.exists(webpage_folder):
    os.mkdir(webpage_folder)

html_graphs = open(webpage_folder + "CovidAnalysis.html",'w',)
html_graphs.write('''
<html><head>
<style>
div {margin-left:50px; margin-right:5%; font-family: \"Verdana\"}
table {margin-left: 50px; margin-right:5%; float:left}
tr {text-align: center}
a {font-family: \"Verdana\"}
img {width: 500px}
</style></head><body>\n
''')
html_graphs.write('<div><h1>Data as of ' + datetime.now().strftime('%m/%d/%y')+ '<br/></h1>')
#html_graphs.write('<div style=\'margin:50px\'><h1>Data as of 04/25/2020<br/></h1>')
html_graphs.write('''
Please wait to load all the graphs. This page is not setup to be fast loading. :)<br/><br/>
</div>
''')

instructions = '''
<div>
    <h2> Things you can do on each graph </h2>
    <ul>
    <li> Hover your mouse over a trend line to find which location it refers to.
    <li> Single click on a location <b>in the legend</b> to show and hide that location's trend line.
    <li> Double click on a location <b>in the legend</b> to show only that location OR show ALL locations in that graph.
    <li> Click and drag on a graph to zoom into a particular area.
    </ul>

    <h2> Data Sources </h2>
    <ul> 
    <li> Covid-19 cases and deaths data from https://github.com/nytimes/covid-19-data.
    <li> Population and Land Area data from random places I found information from the internet. Most was sourced via US Census data and tend to be at least 10 years old.
    </ul> 
</div>
'''

html_graphs.write(instructions)

# %% [markdown]
#  **********************************************************************************************************
#  # Setup
#  1. Read in the covid-19-data from nytimes for state and county (https://github.com/nytimes/covid-19-data)
#  2. Pull in a city density table
#  3. Pull in a state density table
#  4. Identify list of states, counties and cities to graph
#  **********************************************************************************************************

# %%
datafolder = basefolder

#state_cov_data = pd.read_csv(datafolder + 'us-states.csv')
state_cov_data = pd.read_csv('https://github.com/nytimes/covid-19-data/blob/master/us-states.csv?raw=true')
county_cov_data = pd.read_csv('https://github.com/nytimes/covid-19-data/blob/master/us-counties.csv?raw=true')

# Perf hack, see https://stackoverflow.com/questions/14737566/pandas-performance-issue-need-help-to-optimize/42589287#42589287
county_cov_data['state'] = county_cov_data['state'].astype('category')
county_cov_data['county'] = county_cov_data['county'].astype('category')

# https://stackoverflow.com/questions/14737566/pandas-performance-issue-need-help-to-optimize/42589287#42589287
county_cov_data['state'] = county_cov_data['state'].astype('category')
county_cov_data['county'] = county_cov_data['county'].astype('category')

population_county = pd.read_csv(datafolder + 'county-population-2013.csv')
population_county.loc[population_county.state == 'Louisiana'] = population_county[population_county.state == 'Louisiana'].replace(regex=[' Parish'], value='')
population_county.drop(columns={'Core_Based_Statistical_Area'}, inplace=True)
population_county.rename(columns={'population2013': 'population'}, inplace=True)
population_county['key'] = population_county.county + ',' + population_county.state
population_county.drop_duplicates(subset='key', inplace=True)
population_county.index = population_county.key


# %%
population_city_density = pd.read_csv(datafolder + 'city_density.csv')
population_city_density = population_city_density.rename(columns={'City': 'citystate', 'Population Density (Persons/Square Mile)': 'density', '2016 Population': 'population', 'Land Area (Square Miles)': 'area'} )
population_city_density[['city', 'state']] = population_city_density.citystate.str.split(', ', expand=True)

population_state_density = pd.read_csv(datafolder + 'state_density.csv')
population_state_density = population_state_density.rename(columns={'State': 'state', 'Density': 'density', 'Pop': 'population', 'LandArea': 'area'})

# Create a state abbreviation to full name mapping dataframe.
state_abbrev = pd.read_csv(datafolder + 'StateAbbrev.csv')
state_abbrev.index = state_abbrev.abbrev
state_abbrev.drop(columns='abbrev', inplace=True)

# Get the land area table for county, split the 'county, SS' column into two.
county_land_area = pd.read_csv(datafolder + 'LandAreaCounties.csv')
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


# %%
county_density['key'] = county_density.county + ',' + county_density.state
county_density['area'] = county_density.key.map(county_land_area.land_area)
county_density['population'] = county_density.key.map(population_county.population)


# %%
county_density['density'] = county_density.population / county_density.area
county_density.dropna(subset=['density'], inplace=True)
county_density.drop_duplicates(subset= ['county', 'state'], inplace=True)


# %%
interesting_locations_east = [
    ['Connecticut', '', [], False],
    ['Delaware', '', [], False],
    ['District of Columbia', 'District of Columbia', ['District of Columbia'], False],
    ['Maine', '', [], False],
    ['Maryland', '', [], False],
    ['Massachusetts', 'Suffolk', ['Boston'], False],
    ['New Hampshire', '', [], False],
    ['New Jersey', 'Bergen', ['Newark', 'Jersey City'], True],
    ['New York', 'Bronx', ['New York'], True],
    ['New York', 'Brooklyn', ['New York'], True],
    ['New York', 'Kings', ['New York'], True],
    ['New York', 'Manhattan', ['New York'], True],
    ['New York', 'New York City', ['New York'], True],
    ['New York', 'Queens', ['New York'], True],
    ['New York', 'Staten Island', ['New York'], True],
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

#FOR DEBUGGING ONLY 
#interesting_states = interesting_states[interesting_states['state'].isin(['Washington', 'New York'])]

interesting_locations = pd.concat([interesting_locations_east_df, interesting_locations_west_df, interesting_locations_midwest_df, interesting_locations_south_df])
interesting_locations.reset_index(inplace=True)


# %%
population_by_age = pd.read_csv(datafolder + 'nc-est2019-agesex-res.csv')

client = Socrata("data.cdc.gov", None)
results = client.get("9bhg-hcku", limit=10000)
covid_by_age = pd.DataFrame.from_records(results)
#covid_by_age = pd.read_csv(datafolder + 'Provisional_COVID-19_Death_Counts_by_Sex__Age__and_State.csv')

indexNames = covid_by_age[  (covid_by_age.age_group == '18-29 years')
                | (covid_by_age.age_group == '30-49 years')
                | (covid_by_age.age_group == '50-64 years') ].index
covid_by_age.drop(indexNames , inplace=True)

# %%

df = covid_by_age[(covid_by_age.state == 'United States') & (covid_by_age.sex == 'All Sexes') & (covid_by_age.group == 'By Total')]
df = df.assign(PopulationRaw=int(0))
df.loc[df.age_group=='All Ages', 'PopulationRaw'] = int(population_by_age.POPESTIMATE2019[(population_by_age.SEX == 0) & (population_by_age.AGE == 999)])
df.loc[df.age_group=='Under 1 year', 'PopulationRaw'] = int(population_by_age.POPESTIMATE2019[(population_by_age.SEX == 0) & (population_by_age.AGE == 0)])
df.loc[df.age_group=='0-17 years', 'PopulationRaw'] = int(population_by_age.POPESTIMATE2019[(population_by_age.SEX == 0) & (population_by_age.AGE <= 17)].sum())
df.loc[df.age_group=='1-4 years', 'PopulationRaw'] = int(population_by_age.POPESTIMATE2019[(population_by_age.SEX == 0) & (population_by_age.AGE >= 1) & (population_by_age.AGE <= 4)].sum())
df.loc[df.age_group=='5-14 years', 'PopulationRaw'] = int(population_by_age.POPESTIMATE2019[(population_by_age.SEX == 0) & (population_by_age.AGE >= 5) & (population_by_age.AGE <= 14)].sum())
df.loc[df.age_group=='15-24 years', 'PopulationRaw'] = int(population_by_age.POPESTIMATE2019[(population_by_age.SEX == 0) & (population_by_age.AGE >= 15) & (population_by_age.AGE <= 24)].sum())
df.loc[df.age_group=='25-34 years', 'PopulationRaw'] = int(population_by_age.POPESTIMATE2019[(population_by_age.SEX == 0) & (population_by_age.AGE >= 25) & (population_by_age.AGE <= 34)].sum())
df.loc[df.age_group=='30-39 years', 'PopulationRaw'] = int(population_by_age.POPESTIMATE2019[(population_by_age.SEX == 0) & (population_by_age.AGE >= 30) & (population_by_age.AGE <= 39)].sum())
df.loc[df.age_group=='35-44 years', 'PopulationRaw'] = int(population_by_age.POPESTIMATE2019[(population_by_age.SEX == 0) & (population_by_age.AGE >= 35) & (population_by_age.AGE <= 44)].sum())
df.loc[df.age_group=='40-49 years', 'PopulationRaw'] = int(population_by_age.POPESTIMATE2019[(population_by_age.SEX == 0) & (population_by_age.AGE >= 40) & (population_by_age.AGE <= 49)].sum())
df.loc[df.age_group=='45-54 years', 'PopulationRaw'] = int(population_by_age.POPESTIMATE2019[(population_by_age.SEX == 0) & (population_by_age.AGE >= 45) & (population_by_age.AGE <= 54)].sum())
df.loc[df.age_group=='55-64 years', 'PopulationRaw'] = int(population_by_age.POPESTIMATE2019[(population_by_age.SEX == 0) & (population_by_age.AGE >= 55) & (population_by_age.AGE <= 64)].sum())
df.loc[df.age_group=='65-74 years', 'PopulationRaw'] = int(population_by_age.POPESTIMATE2019[(population_by_age.SEX == 0) & (population_by_age.AGE >= 65) & (population_by_age.AGE <= 74)].sum())
df.loc[df.age_group=='75-84 years', 'PopulationRaw'] = int(population_by_age.POPESTIMATE2019[(population_by_age.SEX == 0) & (population_by_age.AGE >= 75) & (population_by_age.AGE <= 84)].sum())
df.loc[df.age_group=='85 years and over', 'PopulationRaw'] = int(population_by_age.POPESTIMATE2019[(population_by_age.SEX == 0) & (population_by_age.AGE >= 85) & (population_by_age.AGE < 999)].sum())

df = df.assign(Population=df.PopulationRaw.map(lambda n: '{:,}'.format(n)))
df = df.assign(ChanceOfDeathByCOVIDRaw = (df.covid_19_deaths.astype(int) / df.PopulationRaw))
df = df.assign(ChanceOfDeathByPneumoniaRaw = (df.pneumonia_deaths.astype(int) / df.PopulationRaw))
df = df.assign(ChanceOfDeathByPneumonia = df['ChanceOfDeathByPneumoniaRaw'].map(lambda n: 'none' if n==0 else '1 in {:,}'.format(round(1/n))))
df = df.assign(ChanceOfDeathByCOVID = df['ChanceOfDeathByCOVIDRaw'].map(lambda n: 'none' if n==0 else '1 in {:,}'.format(round(1/n))))
df = df.assign(ChanceOfDeathByFluRaw = (df.influenza_deaths.astype(int) / df.PopulationRaw))
df = df.assign(ChanceOfDeathByFlu = df['ChanceOfDeathByFluRaw'].map(lambda n: 'none' if n==0 else '1 in {:,}'.format(round(1/n))))
df = df.assign(ChanceOfDeathOtherThanCOVIDRaw = (df.total_deaths.astype(int) - (df.covid_19_deaths.astype(int) + df.pneumonia_deaths.astype(int) + df.influenza_deaths.astype(int))) / df.PopulationRaw)
df = df.assign(ChanceOfDeathOtherThanCOVID = df['ChanceOfDeathOtherThanCOVIDRaw'].map(lambda n: '1 in {:,}'.format(round(1/n))))
df = df.assign(ChanceOfLivingAfterCOVIDRaw = 1 - df['ChanceOfDeathByCOVIDRaw'])
df = df.assign(ChanceOfLivingAfterCOVID = df['ChanceOfLivingAfterCOVIDRaw'].map(lambda n: '{:.4%}'.format(n)))
df = df.assign(TimesWorseThan25to34 = df['ChanceOfDeathByCOVIDRaw'].map(lambda n: '{0}x'.format(round(n / df.loc[7, 'ChanceOfDeathByCOVIDRaw'], 0))))

fig = go.Figure(data=[go.Table(
    header=dict(values=['Age group', 'Deaths by COVID-19 Alone', 'Population', 'Chance Of Living Through COVID-19 Alone', 'Chance Of Death By COVID-19 Alone', 'Chance Of Death By PneumoniaAlone', 'Chance Of Death By Flu Alone', 'Chance Of Death Not By COVID-19, Pneumonia or Flu', 'Risk factor compared to 25-34 year olds'],
                fill_color='paleturquoise',
                align='center'),
    cells=dict(values=[df.age_group, df.covid_19_deaths, df['Population'], df['ChanceOfLivingAfterCOVID'], df['ChanceOfDeathByCOVID'], df['ChanceOfDeathByPneumonia'], df['ChanceOfDeathByFlu'], df['ChanceOfDeathOtherThanCOVID'], df['TimesWorseThan25to34']],
               fill_color='lavender',
               align='right'))
])

fig.update_layout(
    title = 'Death Analysis by Age Group (from CDC stats)',
    plot_bgcolor = default_plot_color,
    width=default_width,
    height=default_height * .75,
)

fig.show()
plotly.offline.plot(fig, filename=webpage_folder + 'DeathRiskTable.html',auto_open=False)
html_graphs.write('''
<br/><br/><div>
<h1>Death Risks by Age Group</h1><br/>
</div>
''')
html_graphs.write("  <object data=\""+'DeathRiskTable.html'+"\" width=" + str(default_width * 1.10) + " height=" + str(default_height* 1.10) + "\"></object>"+"\n")

# %%
def movingaverage(df, window):
    if len(df) > window:
        values = df['diff'].to_numpy()
        weights = np.repeat(1.0, window)/window
        sma = np.convolve(values, weights, 'valid')
        df['diff'][window-1:] = sma
    return df

def generate_delta_df(state, county, column):
    if (state == 'all'):
        totals_by_date = state_cov_data.groupby('date').sum()
    elif (county == 'all'):
        totals_by_date = state_cov_data[state_cov_data.state == state].groupby('date').sum()
    else:
        totals_by_date = county_cov_data[(county_cov_data.state == state) & (county_cov_data.county == county)].groupby('date').sum()

    deltas = totals_by_date[column].to_numpy()[1:] - totals_by_date.head(len(totals_by_date)-1)[column].to_numpy()[0:]
    totals_by_date['diff'] = 0
    if deltas.size > 0:
        totals_by_date['diff'][1:] = deltas
        totals_by_date.loc[totals_by_date['diff'] < 0] = 0
    return totals_by_date

def plotmovingaverage(deltas_df, nameOfplot, hover_template, show_by_default=True):
    if (len(deltas_df) > 0):
        df_with_ma = movingaverage(deltas_df, 7)

        if (show_by_default):
            visible = True
        else:
            visible = 'legendonly'

        fig.add_trace(
            go.Scatter(x=df_with_ma.index.to_numpy(), y=df_with_ma['diff'], mode='lines', name=nameOfplot, line = { 'width': default_line_thickness },
            hovertemplate=hover_template, visible=visible)
        )


# %% [markdown]
# **********************************************************************************************************
# # New Cases and Deaths in US
# **********************************************************************************************************
# %%
row = 1
fig = make_subplots(specs=[[{"secondary_y": True}]])
total_new_cases_by_date = generate_delta_df("all", "", "cases")
total_deaths_by_date = generate_delta_df("all", "", "deaths")
plotmovingaverage(total_new_cases_by_date, 'new cases', 'new cases: %{y:,.0f}<br>day: %{x}')
plotmovingaverage(total_deaths_by_date, 'deaths', 'deaths: %{y:,.0f}<br>day: %{x}')

cases_by_date = state_cov_data.groupby('date').sum()
mortality_by_date = cases_by_date['deaths'][14:] / cases_by_date['cases'][:]
mortality_by_date.dropna(inplace=True)
fig.add_trace(
    go.Scatter(x=mortality_by_date.index, y=mortality_by_date.values, mode='lines', name='mortality rate', line = { 'width': default_line_thickness }),
    secondary_y=True
)
fig.update_layout(
    title = 'New cases, daily deaths, and 2-week mortality for US',
    plot_bgcolor = default_plot_color,
    xaxis_gridcolor = default_grid_color,
    yaxis_gridcolor = default_grid_color,
    width=default_width,
    height=default_height,
    xaxis_title='Days',
    yaxis_title='New cases & daily deaths'
)
fig.update_yaxes(title_text="2-week mortality rate", secondary_y=True)
fig.show()

plotly.offline.plot(fig, filename=webpage_folder + 'Chart_'+str(row)+'.html',auto_open=False)
html_graphs.write('''
<br/><br/><div>
<h1>New cases, Daily Deaths and 2-week Mortality for US</h1><br/>
This is a combination plot showing a 7 day moving average of number of new cases per day, number of deaths per day, 
and a 2-week mortality rate for the US overall. Note that the scale for the mortality rate appears along the right hand side of the graph, 
while the scale for cases and deaths is along the left.<br/>
<br/>
The 2-week mortality rate is calculated by taking the total number of deaths that occurred by each date, and dividing it by the total number of new cases that occurred
2 weeks earlier. Therefore, the desired line should be trending downward indicating that the number of deaths compared against the number of cases found is going down. 
This could be due to more people being tested and testing as positive while the absolute mortality of covid-19 stays constant, but it also could be due to better treatment 
of those infected. Note that a .03 mortality rate is believed to be about 30x higher than that of influenza. But also remember that disregarding age, a .03 mortality rate 
implies that if you are infected, you have a 97% chance of surviving. <br/>
<br/>
</div>\n<div>\n
''')
html_graphs.write("  <object data=\""+'Chart_'+str(row)+'.html'+"\" width=" + str(default_width * 1.10) + " height=" + str(default_height* 1.10) + "\"></object>"+"\n")


# %% [markdown]
# **********************************************************************************************************
# # New cases by state
# **********************************************************************************************************
# %%
row += 1
layout = go.Layout(
        title = 'New cases by state',
        plot_bgcolor = default_plot_color,
        xaxis_gridcolor = default_grid_color,
        yaxis_gridcolor = default_grid_color,
        width=default_width,
        height=default_height,
        xaxis_title='Days',
        yaxis_title='New cases'
)

fig = go.Figure(layout=layout)

# Show all states by default.
for index, state in interesting_states.iterrows():
    total_new_cases_by_date = generate_delta_df(state.state, 'all', 'cases')
    plotmovingaverage(total_new_cases_by_date, state.state, 'new cases: %{y:,.0f}<br>day: %{x}')

fig.show()
plotly.offline.plot(fig, filename=webpage_folder + 'Chart_'+str(row)+'.html',auto_open=False)
html_graphs.write('''
<h1>New Cases and Deaths by State</h1>\n
''')
html_graphs.write("  <object data=\""+'Chart_'+str(row)+'.html'+"\" width=" + str(default_width * 1.10) + " height=" + str(default_height* 1.10) + "\"></object>"+"\n")


# %% [markdown]
# **********************************************************************************************************
# # Daily Deaths by state
# **********************************************************************************************************
# %%
row += 1
layout = go.Layout(
        title = 'Daily deaths by state',
        plot_bgcolor = default_plot_color,
        xaxis_gridcolor = default_grid_color,
        yaxis_gridcolor = default_grid_color,
        width=default_width,
        height=default_height,
        xaxis_title='Days',
        yaxis_title='Deaths'
)

fig = go.Figure(layout=layout)

# Show all states by default.
for index, state in interesting_states.iterrows():
    total_deaths_by_date = generate_delta_df(state.state, 'all', 'deaths')
    plotmovingaverage(total_deaths_by_date, state.state, 'deaths: %{y:,.0f}<br>day: %{x}')

fig.show()
plotly.offline.plot(fig, filename=webpage_folder + 'Chart_'+str(row)+'.html',auto_open=False)
html_graphs.write("  <object data=\""+'Chart_'+str(row)+'.html'+"\" width=" + str(default_width * 1.10) + " height=" + str(default_height* 1.10) + "\"></object>"+"\n")


# %% [markdown]
# **********************************************************************************************************
# # New cases by interesting county
# **********************************************************************************************************
# %%
row += 1
layout = go.Layout(
        title = 'New cases by interesting county',
        plot_bgcolor = default_plot_color,
        xaxis_gridcolor = default_grid_color,
        yaxis_gridcolor = default_grid_color,
        width=default_width,
        height=default_height,
        xaxis_title='Days',
        yaxis_title='New cases'
)

fig = go.Figure(layout=layout)
for index, r in interesting_locations.iterrows():
    if (r.county != ''):
        total_new_cases_by_date = generate_delta_df(r.state, r.county, 'cases')
        plotmovingaverage(total_new_cases_by_date, r.state + ', ' + r.county, 'new cases: %{y:,.0f}<br>day: %{x}', r.show_by_default)

fig.show()
plotly.offline.plot(fig, filename=webpage_folder + 'Chart_'+str(row)+'.html',auto_open=False)
html_graphs.write('''
<h1>New Cases and Deaths in Locations Interesting to Me</h1>\n
''')
html_graphs.write("  <object data=\""+'Chart_'+str(row)+'.html'+"\" width=" + str(default_width * 1.10) + " height=" + str(default_height* 1.10) + "\"></object>"+"\n")


# %% [markdown]
# **********************************************************************************************************
# # Daily deaths by interesting county
# **********************************************************************************************************
# %%
row += 1
layout = go.Layout(
        title = 'Daily deaths by interesting county',
        plot_bgcolor = default_plot_color,
        xaxis_gridcolor = default_grid_color,
        yaxis_gridcolor = default_grid_color,
        width=default_width,
        height=default_height,
        xaxis_title='Days',
        yaxis_title='New cases'
)

fig = go.Figure(layout=layout)
for index, r in interesting_locations.iterrows():
    if (r.county != ''):
        total_deaths_by_date = generate_delta_df(r.state, r.county, 'deaths')
        plotmovingaverage(total_deaths_by_date, r.state + ', ' + r.county, 'deaths: %{y:,.0f}<br>day: %{x}', r.show_by_default)

fig.show()
plotly.offline.plot(fig, filename=webpage_folder + 'Chart_'+str(row)+'.html',auto_open=False)
html_graphs.write("  <object data=\""+'Chart_'+str(row)+'.html'+"\" width=" + str(default_width * 1.10) + " height=" + str(default_height* 1.10) + "\"></object>"+"\n")
html_graphs.write("\n</div>\n")

# %%
if IN_COLAB or IN_AZUREML: 
  #%pip install plotly==4.7.1 I don't think we need to downgrade plotly. 
  !wget https://github.com/plotly/orca/releases/download/v1.2.1/orca-1.2.1-x86_64.AppImage -O /usr/local/bin/orca 
  !chmod +x /usr/local/bin/orca 
  !apt-get install xvfb libgtk2.0-0 libgconf-2-4
  #import plotly.graph_objects as go

# %% [markdown]
# **********************************************************************************************************
# # Do all states & counties
# **********************************************************************************************************
# %%
html_graphs.write('''
<div>
<h1>State New Cases and Death Breakdowns</h1>\n
</div>
''')

#plotly.io.orca.config.executable = 'C:/Users/jimg/AppData/Local/Programs/orca/orca.exe'
for index, s in interesting_states.iterrows():

    layout = go.Layout(
            title = s.state + ' State new cases and new deaths',
            plot_bgcolor = default_plot_color,
            xaxis_gridcolor = default_grid_color,
            yaxis_gridcolor = default_grid_color,
            width=default_width,
            height=default_height,
            xaxis_title='Days',
            yaxis_title='New Cases / New Deaths'
    )

    fig = make_subplots(specs=[[{"secondary_y": True}]])
    total_new_cases_by_date = generate_delta_df(s.state, 'all', 'cases')
    total_deaths_by_date = generate_delta_df(s.state, 'all', 'deaths')
    plotmovingaverage(total_new_cases_by_date, s.state + ' new cases', 'cases: %{y:,.0f}<br>day: %{x}')
    plotmovingaverage(total_deaths_by_date, s.state + ' deaths', 'deaths: %{y:,.0f}<br>day: %{x}')

    cases_by_date = state_cov_data[state_cov_data.state == s.state].groupby('date').sum()
    mortality_by_date = cases_by_date['deaths'][14:] / cases_by_date['cases'][:]
    mortality_by_date.dropna(inplace=True)
    fig.add_trace(
        go.Scatter(x=mortality_by_date.index, y=mortality_by_date.values, mode='lines', name='mortality rate', line = { 'width': default_line_thickness }),
        secondary_y=True
    )

    fig.update_layout(
        title = s.state + ' State new cases, daily deaths, and 2-week mortality',
        plot_bgcolor = default_plot_color,
        xaxis_gridcolor = default_grid_color,
        yaxis_gridcolor = default_grid_color,
        width=default_width,
        height=default_height,
        xaxis_title='Days',
        yaxis_title='New cases & daily deaths'
    )
    fig.update_yaxes(title_text="2-week mortality rate", secondary_y=True)

    basename_new_cases_all=s.state + '_new_cases'
    pio.write_image(fig, webpage_folder + basename_new_cases_all + '.jpg')
    plotly.offline.plot(fig, filename=webpage_folder + basename_new_cases_all + '.html', auto_open=False)
    state_chunk_file = s.state + '_new_chunk.html'
    state_chunk_graphs = open(webpage_folder + state_chunk_file,'w',)
    state_chunk_graphs.write("<object data=\"" + basename_new_cases_all + ".html\" width=" + str(default_width * 1.10) + " height=" + str(default_height* 1.10) + "\"></object>"+"\n")

    layout = go.Layout(
            title = s.state + ' State new cases by county',
            plot_bgcolor = default_plot_color,
            xaxis_gridcolor = default_grid_color,
            yaxis_gridcolor = default_grid_color,
            width=default_width,
            height=default_height,
            xaxis_title='Days',
            yaxis_title='New cases'
    )
    fig = go.Figure(layout=layout)

    for index, c in population_county[population_county.state == s.state].iterrows():
        total_new_cases_by_county = generate_delta_df(s.state, c.county, 'cases')
        plotmovingaverage(total_new_cases_by_county, c.county,'')

    basename_new_cases_by_county=s.state + '_new_cases_by_county'
    pio.write_image(fig, webpage_folder + basename_new_cases_by_county + '.jpg')
    plotly.offline.plot(fig, filename=webpage_folder + basename_new_cases_by_county + '.html', auto_open=False)
    state_chunk_graphs.write("<object data=\"" + basename_new_cases_by_county + ".html\" width=" + str(default_width * 1.10) + " height=" + str(default_height* 1.10) + "\"></object>"+"\n")

    layout = go.Layout(
            title = s.state + ' State deaths by county',
            plot_bgcolor = default_plot_color,
            xaxis_gridcolor = default_grid_color,
            yaxis_gridcolor = default_grid_color,
            width=default_width,
            height=default_height,
            xaxis_title='Days',
            yaxis_title='Deaths'
    )
    fig=go.Figure(layout=layout)

    for index, c in population_county[population_county.state == s.state].iterrows():
        total_deaths_by_date = generate_delta_df(s.state, c.county, 'deaths')
        plotmovingaverage(total_deaths_by_date, c.county,'')

    basename_deaths_by_county=s.state + '_deaths_by_county'
    pio.write_image(fig, webpage_folder + basename_deaths_by_county + '.jpg')
    plotly.offline.plot(fig, filename=webpage_folder + basename_deaths_by_county + '.html', auto_open=False)
    state_chunk_graphs.write("<object data=\"" + basename_deaths_by_county + ".html\" width=" + str(default_width * 1.10) + " height=" + str(default_height* 1.10) + "\"></object>"+"\n")
    state_chunk_graphs.close()

    main_page_entry = f'''
<a target='_blank' href='{state_chunk_file}'>
  <table style="border-color: black; border-width: 1px; border-style: solid;">
    <tr><td colspan="2">{s.state}</td></tr>
    <tr><td rowspan="2"><img src='{basename_new_cases_all}.jpg'/></td><td style="width: 200px; height: 200px; margin: 0px; padding: 0px;"><img style="width:200px;" src='{basename_new_cases_by_county}.jpg'/></td></tr>
    <tr><td style="width: 200px; height: 200px; margin: 0px; padding: 0px;"><img style="width: 200px;" src='{basename_deaths_by_county}.jpg'/></td></tr>
  </table>
</a>\n
'''
    html_graphs.write(main_page_entry)

html_graphs.write('<div style=\"clear:both\"></div>')

# %% [markdown]
#  **********************************************************************************************************
#  # State Totals
#  **********************************************************************************************************
# %%
def plottotalcases(state, county = 'all', show_by_default=True):
    if county == 'all':
        data = state_cov_data[state_cov_data.state == state][['date', 'cases']].groupby('date').sum()
    else:
        data = county_cov_data[county_cov_data.state == state][['date', 'cases', 'county']].groupby('date').sum()

    if len(data['cases']):

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
        title = 'Total cases by state',
        plot_bgcolor = default_plot_color,
        xaxis_gridcolor = default_grid_color,
        yaxis_gridcolor = default_grid_color,
        width=default_width,
        height=default_height,
        xaxis_title='Date',
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

# %% [markdown]
# **********************************************************************************************************
# # County Totals
# **********************************************************************************************************
# %%
row += 1
starting_cases = 200
layout = go.Layout(
        title = 'Total cases by county',
        plot_bgcolor = default_plot_color,
        xaxis_gridcolor = default_grid_color,
        yaxis_gridcolor = default_grid_color,
        width=default_width,
        height=default_height,
        xaxis_title='Date',
        yaxis_title='Total cases'
)
fig = go.Figure(layout=layout)

for index, r in interesting_locations.iterrows():
    plottotalcases(r.state, r.county, r.show_by_default)

fig.show()
plotly.offline.plot(fig, filename=webpage_folder + 'Chart_'+str(row)+'.html',auto_open=False)
html_graphs.write("  <object data=\""+'Chart_'+str(row)+'.html'+"\" width=" + str(default_width * 1.10) + " height=" + str(default_height* 1.10) + "\"></object>"+"\n")

# %% [markdown]
#  **********************************************************************************************************
#  # State cases adjusted for population
#  **********************************************************************************************************
# %%
def stateplotpercapita(state, show_by_default):
    data = state_cov_data[state_cov_data.state == state][['date', 'cases']].groupby('date').sum()
    state_population = population_state_density[population_state_density.state == state]
    if len(state_population):
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
        title = 'Total state cases per 1,000',
        plot_bgcolor = default_plot_color,
        xaxis_gridcolor = default_grid_color,
        yaxis_gridcolor = default_grid_color,
        width=default_width,
        height=default_height,
        xaxis_title='Date',
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

# %% [markdown]
# **********************************************************************************************************
# # County cases adjusted for population
# **********************************************************************************************************
# %%
def countyplotpercapita(state, county, show_by_default):
    data = county_cov_data[county_cov_data.state == state][['date', 'cases', 'county']].groupby('date').sum()
    county_population = population_county[(population_county.state == state) & (population_county.county == county)]
    if len(county_population):
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
        title = 'Total county cases per 1,000 people',
        plot_bgcolor = default_plot_color,
        xaxis_gridcolor = default_grid_color,
        yaxis_gridcolor = default_grid_color,
        width=default_width,
        height=default_height,
        xaxis_title='Date',
        yaxis_title='Total cases per 1,000 people'
)
fig=go.Figure(layout=layout)

for index, r in interesting_locations.iterrows():
    countyplotpercapita(r.state, r.county, r.show_by_default)

fig.show()
plotly.offline.plot(fig, filename=webpage_folder + 'Chart_'+str(row)+'.html',auto_open=False)
html_graphs.write("  <object data=\""+'Chart_'+str(row)+'.html'+"\" width=" + str(default_width * 1.10) + " height=" + str(default_height* 1.10) + "\"></object>"+"\n")

# %% [markdown]
#  **********************************************************************************************************
#  # State cases adjusted for population density
#  **********************************************************************************************************
# %%
def stateplotbydensity(state, show_by_default):
    data = state_cov_data[state_cov_data.state == state][['date', 'cases']].groupby('date').sum()
    state_density = population_state_density[population_state_density.state == state]
    if len(state_density):
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
        title = 'Total state cases factoring in population density',
        plot_bgcolor = default_plot_color,
        xaxis_gridcolor = default_grid_color,
        yaxis_gridcolor = default_grid_color,
        width=default_width,
        height=default_height,
        xaxis_title='Date',
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

# %% [markdown]
#  **********************************************************************************************************
#  # County cases adjusted for population density
#  **********************************************************************************************************
# %%
def countyplotbydensity(county, state, show_by_default):
    data = county_cov_data[(county_cov_data.county == county) & (county_cov_data.state == state)][['date', 'cases']].groupby('date').sum()
    density = county_density[(county_density.county == county) & (county_density.state == state)]
    if len(density):
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
        title = 'Total county cases factoring in population density',
        plot_bgcolor = default_plot_color,
        xaxis_gridcolor = default_grid_color,
        yaxis_gridcolor = default_grid_color,
        width=default_width,
        height=default_height,
        xaxis_title='Date',
        yaxis_title='Total density adjusted cases'
)
fig=go.Figure(layout=layout)

for index, r in interesting_locations.iterrows():
    countyplotbydensity(r.county, r.state, r.show_by_default)
fig.show()
plotly.offline.plot(fig, filename=webpage_folder + 'Chart_'+str(row)+'.html',auto_open=False)
html_graphs.write("  <object data=\""+'Chart_'+str(row)+'.html'+"\" width=" + str(default_width * 1.10) + " height=" + str(default_height* 1.10) + "\"></object>"+"<br/>\n")

# Do all states & counties
for index, s in interesting_states.iterrows():
    starting_cases = 5
    layout = go.Layout(
            title = s.state + ' State county cases factoring in population density',
            plot_bgcolor = default_plot_color,
            xaxis_gridcolor = default_grid_color,
            yaxis_gridcolor = default_grid_color,
            width=default_width,
            height=default_height,
            xaxis_title='Date',
            yaxis_title='Total density adjusted cases'
    )
    fig=go.Figure(layout=layout)

    for index, r in county_density[county_density.state == s.state].iterrows():
        countyplotbydensity(r.county, r.state, True)

    basename=s.state + '_by_density'
    pio.write_image(fig, webpage_folder + basename + '.jpg')
    plotly.offline.plot(fig, filename=webpage_folder + basename + '.html', auto_open=False)
    html_graphs.write("<a target='_blank' href='" + basename + ".html'><table><tr><td>" + s.state + "</td></tr><tr><td><img src='" + basename + ".jpg'/></td></tr></table></a>\n")

html_graphs.write('<div style=\"clear:both\"></div>')

# %% [markdown]
#  **********************************************************************************************************
#  # City cases adjusted for population
#  **********************************************************************************************************
# %%
def cityplotpercapita(state, city, show_by_default):
    county = 'not found'
    for index, x in interesting_locations.iterrows():
        if city in x.cities and state == x.state:
            county = x.county

    cov_at_county_level = county_cov_data[county_cov_data.state == state][county_cov_data.county == county][['date', 'cases']].groupby('date').sum()
    city_population = population_city_density[population_city_density.state == state][population_city_density.city == city]
    if (len(city_population)):
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
        title = 'Total city cases per 1,000',
        plot_bgcolor = default_plot_color,
        xaxis_gridcolor = default_grid_color,
        yaxis_gridcolor = default_grid_color,
        width=default_width,
        height=default_height,
        xaxis_title='Date',
        yaxis_title='Total cases per 1,000 people'
)
fig=go.Figure(layout=layout)

for index, r in interesting_locations[~interesting_locations['cities'].apply(tuple).duplicated()].iterrows():
    for c in r.cities:
        cityplotpercapita(r.state, c, r.show_by_default)

fig.show()
plotly.offline.plot(fig, filename=webpage_folder + 'Chart_'+str(row)+'.html',auto_open=False)
html_graphs.write('''
<br/><br/><div>">
<h1>City total cases adjusted for population</h1><br/>
You can do the same types of adjustments as we did for state and county at the city level.
A city that has 100,000 people vs 8,000,000 people will obviously look far better with regard to total cases
because they have 80x less people. By factoring in the population of a city, this is difference
is accounted for.
</div>''')
html_graphs.write("  <object data=\""+'Chart_'+str(row)+'.html'+"\" width=" + str(default_width * 1.10) + " height=" + str(default_height* 1.10) + "\"></object>"+"\n")

# %% [markdown]
#  **********************************************************************************************************
#  # City total cases adjusted for population density
#  **********************************************************************************************************
# %%
def cityplotbydensity(state, city, show_by_default):
    county = 'not found'
    for index, x in interesting_locations.iterrows():
        if city in x.cities and state == x.state:
            county = x.county

    data = county_cov_data[county_cov_data.state == state][county_cov_data.county == county][['date', 'cases']].groupby('date').sum()
    city_density = population_city_density[population_city_density.state == state][population_city_density.city == city]
    if (len(city_density)):
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
        title = 'Total city cases factoring in population density',
        plot_bgcolor = default_plot_color,
        xaxis_gridcolor = default_grid_color,
        yaxis_gridcolor = default_grid_color,
        width=default_width,
        height=default_height,
        xaxis_title='Date',
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

# %% [markdown]
#  **********************************************************************************************************
#  # City deaths adjusted for population density
#  **********************************************************************************************************
# %%
def citydeathsplotbydensity(state, city, show_by_default):
    county = 'not found'
    for index, x in interesting_locations.iterrows():
        if city in x.cities and state == x.state:
            county = x.county

    data = county_cov_data[county_cov_data.state == state][county_cov_data.county == county][['date', 'deaths']].groupby('date').sum()
    city_density = population_city_density[population_city_density.state == state][population_city_density.city == city]
    if (len(city_density)):
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
        title = 'Total city deaths factoring in population density',
        plot_bgcolor = default_plot_color,
        xaxis_gridcolor = default_grid_color,
        yaxis_gridcolor = default_grid_color,
        width=default_width,
        height=default_height,
        xaxis_title='Date',
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
import os
if (os.environ.get('covid_ftp_pw')):
    import time
    t1 = time.perf_counter()

    import ftplib
    import io
    import pytz
    from datetime import datetime
    from dateutil import parser
    from dateutil.tz import gettz

    ftp = ftplib.FTP('ftp.jimgphotography.com', 'jim@covid.jimgries.com', os.environ['covid_ftp_pw'])

    tzinfos = {'UTC': gettz('UTC')}
    for filename in os.listdir('webpage'):
        localtimestamp = datetime.fromtimestamp(os.stat('webpage/' + filename).st_mtime).replace(tzinfo=pytz.timezone('America/Los_Angeles'))
        try:
            tmp = None
            tmp = ftp.voidcmd('MDTM /' + filename)[4:].strip()+'UTC'
            remotetimestamp = (parser.parse(tmp, tzinfos=tzinfos)).astimezone(pytz.timezone('America/Los_Angeles'))
        except: 
            pass
        if (tmp == None or localtimestamp > remotetimestamp):
            print('Transferring ' + filename)
            with open('webpage/' + filename, 'rb') as fobj:
                ftp.storbinary('STOR ' + filename, fobj)
        else:
            print('Skipping ' + filename)
            print(filename + ' local: ' + localtimestamp.strftime('%c'))
            print(filename + ' remote: ' + remotetimestamp.strftime('%c'))
    ftp.close()
    print('Total file transfer time: ', time.perf_counter() - t1)
else:
    print('Skipped file transfer')

# %%
print('Total run time: ', time.perf_counter() - t0)

# %%
