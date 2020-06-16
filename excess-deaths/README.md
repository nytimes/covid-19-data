# Excess Deaths During the Coronavirus Pandemic

The New York Times is releasing data that documents the number of deaths from all causes that have occurred during the coronavirus pandemic for 25 countries. We are compiling this time series data from national and municipal health departments, vital statistics offices and other official sources in order to better understand the true toll of the pandemic and provide a record for researchers and the public.

Official Covid-19 death tolls offer a limited view of the impact of the outbreak because they often exclude people who have not been tested and those who died at home. All-cause mortality is widely used by demographers and other researchers to understand the full impact of deadly events, including epidemics, wars and natural disasters. The totals in this data include deaths from Covid-19 as well as those from other causes, likely including people who could not be treated or did not seek treatment for other conditions. 

We have used this data to produce [graphics tracking](https://www.nytimes.com/interactive/2020/04/21/world/coronavirus-missing-deaths.html) [the oubreak’s toll](https://www.nytimes.com/interactive/2020/06/10/world/coronavirus-history.html) and stories about [the United States](https://www.nytimes.com/interactive/2020/05/05/us/coronavirus-death-toll-us.html), [Ecuador](https://www.nytimes.com/2020/04/23/world/americas/ecuador-deaths-coronavirus.html), [Russia](https://www.nytimes.com/2020/05/11/world/europe/coronavirus-deaths-moscow.html), [Turkey](https://www.nytimes.com/2020/04/20/world/middleeast/coronavirus-turkey-deaths.html), [Sweden](https://www.nytimes.com/interactive/2020/05/15/world/europe/sweden-coronavirus-deaths.html) and [other countries](https://www.nytimes.com/2020/05/12/world/americas/latin-america-virus-death.html). We would like to thank a number of demographers and other researchers, listed at the end, who have provided data or helped interpret it.

## Country and City-Level Data

The number of all-cause deaths recorded in each area, by week or month, can be found in the **[deaths.csv](deaths.csv)** file. ([Raw CSV](https://raw.githubusercontent.com/nytimes/covid-19-data/master/excess-deaths/deaths.csv)) For weekly data, the first and last weeks of the year, which are often partial weeks, were excluded.

```
country,placename,frequency,start_date,end_date,year,month,week,deaths,expected_deaths,excess_deaths,baseline
France,,weekly,2020-04-27,2020-05-03,2020,4,18,10498,10357,141,2010-2018 weekly average
```

Some of the data is only available at the city level.

```
country,placename,frequency,start_date,end_date,year,month,week,deaths,expected_deaths,excess_deaths,baseline
Turkey,Istanbul,weekly,2020-04-06,2020-04-12,2020,4,15,2193,1429,764,2018-2019 weekly average
```


The deaths fields have the following definitions:

**deaths**: The total number of confirmed deaths recorded from any cause.
**expected_deaths**: The baseline number of expected deaths, calculated from a historical average. See [expected deaths](#expected-deaths).
**excess_deaths**: The number of deaths minus the expected deaths.

The time fields have the following definitions:

**frequency**: Weekly or monthly, depending on how the data is recorded.
**start_date**: The first date included in the period.
**end_date**: The last date included in the period.
**month**: Numerical month.
**week**: Epidemiological week, which is a standardized way of counting weeks to allow for year-over-year comparisons. Most countries start epi weeks on Mondays, but others vary.
**baseline**: The years used to calculate expected_deaths.

## Methodology

The data is the product of journalists in a number of countries who monitor official data releases and ask government officials for information. We have consulted with demographers, medical officials and local sources to confirm that this data is broadly representative of how many people have died. In some countries, the number of burials, hospital deaths or other factors are used to confirm that the underlying trends are representative.

But mortality data in the middle of a pandemic is not perfect. Many countries have not yet published any data on all-cause mortality. And during a pandemic, normal patterns of death registration may be disrupted, which could lead to changes in how many deaths are captured. 

Most of the countries in this dataset have widespread vital statistics coverage. But many low-income countries have [unreliable death registration systems](https://twitter.com/helleringer143/status/1261868447903948800), making it very difficult to assess their levels of excess mortality. A rough guide to the historical completeness of death registration systems by country is available from the United Nations:
https://unstats.un.org/unsd/demographic-social/crvs/documents/Website_final_coverage.xls

Some countries are publishing mortality data faster than normal in order to understand how mortality is changing. That means data, especially for recent time periods, may be revised. It is usually revised upwards as more deaths are reported.

Expected deaths  for [the United States](https://www.nytimes.com/interactive/2020/05/05/us/coronavirus-death-toll-us.html) were calculated with a simple model based on the number of all-cause deaths from 2015 to 2019 released by the Centers for Disease Control and Prevention, adjusted to account for trends, like population changes, over time.

Our analysis aims to show mortality statistics for as much of the country as possible, but it is limited to those states where mortality data is sufficiently complete.

Some states are so far behind in submitting death certificates to the C.D.C. that the C.D.C. does not recommend relying on their recent death reporting. In Pennsylvania and Ohio, for example, death reporting seems to be lagging far behind the normal rate all year, according to the C.D.C., even though their reporting is usually more timely, so we have excluded data from those states, in addition to Alaska, Connecticut, Louisiana, North Carolina, Puerto Rico, Rhode Island and West Virginia.

See [Data Sources](#data-sources) below for the source of data for each country and city in this dataset.

## Expected Deaths

We have calculated an average number of expected deaths for each area based on historical data for the same time of year. These expected deaths are the basis for our [excess death calculations](https://www.nytimes.com/interactive/2020/04/21/world/coronavirus-missing-deaths.html), which estimate how many more people have died this year than in an average year.

To estimate expected deaths, we fit a linear model to the reported deaths in each country from earlier years to January 2020. The model has two components — a linear time trend to account for demographic changes and a smoothing spline to account for seasonal variation. For countries limited to monthly data, the model includes month as a fixed effect rather than using a smoothing spline. 

The number of expected deaths are not adjusted for how non-Covid-19 deaths may change during the outbreak, which will take some time to figure out. As countries impose control measures, deaths from causes like road accidents and homicides may decline. And people who die from Covid-19 cannot die later from [other causes](https://twitter.com/AndrewNoymer/status/1241620305350549504), which may reduce other causes of death. Both of these factors, if they play a role, would lead these baselines to understate, rather than overstate, the number of excess deaths.

The number of years used in the expected deaths calculation changes depending on what data is available. See Data Sources for the years used to calculate the baselines. 


## Data Sources

**Austria**

Source: [Statistics Austria](http://www.statistik.at/web_de/statistiken/menschen_und_gesellschaft/bevoelkerung/gestorbene/index.html)  
Baseline years: 2015-2019  
Data frequency: weekly  

**Belgium**

Source: Sciensano publishes a [weekly report](https://covid-19.sciensano.be/fr/covid-19-situation-epidemiologique). More historical mortality data is from the [Belgian Mortality Monitoring](https://epistat.wiv-isp.be/momo/) dashboard.  
Baseline years: 2016-2019  
Data frequency: weekly  

**Brazil**

Source: Data for five cities in Brazil — São Paulo, Rio de Janeiro, Fortaleza, Manaus and Recife — is from the [Registro Civil](https://registrocivil.org.br/) and the Ministry of Health.  
Baseline years: 2016-2019  
Data frequency: weekly  

**Denmark**

Source: [Statistics Denmark](https://www.statbank.dk/dodc2)  
Baseline years: 2015-2019  
Data frequency: weekly  

**Ecuador**

Source: [General Direction of Civil Registry](https://www.registrocivil.gob.ec/cifras/)  
Baseline years: 2017-2019. 2019 data is only available for Jan.-April.  
Data frequency: monthly  

**Finland**

Source: [Statistics Finland](https://pxnet2.stat.fi/PXWeb/pxweb/en/Kokeelliset_tilastot/Kokeelliset_tilastot__vamuu_koke/statfin_vamuu_pxt_12ng.px/)  
Baseline years: 2015-2019  
Data frequency: weekly  

**France**

Source: INSEE (2018-2020 data can be found [here](https://www.insee.fr/fr/statistiques/4487988?sommaire=4487854))  
Baseline years: 2010-2019  
Data frequency: weekly  

**Germany**

Source: [Federal Statistics Office](https://www.destatis.de/EN/Themes/Society-Environment/Population/Deaths-Life-Expectancy/_node.html;jsessionid=91286BFEECCABAD3052B72D2C2760F99.internet8732)  
Baseline years: 2016-2019  
Data frequency: weekly  

**Jakarta, Indonesia**

Source: [Jakarta’s Department of Parks and Cemeteries](https://pertamananpemakaman.jakarta.go.id/v140/t15)  
Baseline years: 2010-2019  
Data frequency: monthly burials  

**Israel**

Source: [Population and Immigration Authority](https://www.gov.il/BlobFolder/news/death_stats_2001_2020/he/death_stats_2001_2020.pdf)  
Baseline years: 2015-2019  
Data frequency: monthly  

**Italy**

Source: [The Italian National Institute of Statistics](https://www.istat.it/en/archivio/240106)  
Baseline years: 2015-2019 monthly average. Historical data is only available as a four-year average from January 1 through March 31.  
Data frequency: monthly  

**Netherlands**

Source: [Statistics Netherlands](https://opendata.cbs.nl/#/CBS/en/dataset/70895ENG/table?ts=1588591754264)  
Baseline years: 2016-2019  
Data frequency: weekly  

**Norway**

Source: [Statistics Norway](https://www.ssb.no/statbank/table/07995/)  
Baseline years: 2015-2019  
Data frequency: weekly  

**Peru**

Source: [Mortality Information System](https://www.minsa.gob.pe/defunciones/) (Sinadef) for 2017-2020; Health Ministry for 2016.  
Baseline years: 2017-2019  
Data frequency: monthly  

**Portugal**

Source: Eurostat  
Baseline years: 2015-2019  
Data frequency: weekly  

**Moscow, Russia**

Source: [Moscow City Government](https://data.mos.ru/opendata/7704111479-dinamika-registratsii-aktov-grajdanskogo-sostoyaniya?pageNumber=13&versionNumber=3&releaseNumber=42&fbclid=IwAR23dK1YBLeGipw4UPg4hi_w6cDOE94fuZ0Z7lwx28u-rAZCEoqAAaIQpF8)  
Baseline years: 2015-2019  
Data frequency: monthly  

**Sweden**

Source: [Statistics Sweden](https://www.scb.se/en/About-us/news-and-press-releases/statistics-sweden-to-publish-preliminary-statistics-on-deaths-in-sweden/)  
Baseline years: 2015-2019  
Data frequency: weekly  

**Switzerland**

Source: [Federal Statistics Bureau](https://www.bfs.admin.ch/bfs/fr/home/statistiques/sante/etat-sante/mortalite-causes-deces.html)  
Baseline years: 2016-2019  
Data frequency: weekly  


**Thailand**

Sources: [Bureau of Registration Administration](https://www.cdg.co.th/website/en/industries/government/civil-registration-and-the-national-identification-card-system-the-bureau-of-registration-administration-the-department-of-provincial-administration-2/) [Department of Provincial Administration](https://www.dopa.go.th/main/web_index)
Baseline years: 2015-2019
Data frequency: monthly

**United Kingdom**

Sources: [Office for National Statistics](https://www.ons.gov.uk/peoplepopulationandcommunity/birthsdeathsandmarriages/deaths/datasets/weeklyprovisionalfiguresondeathsregisteredinenglandandwales); [National Records of Scotland](https://www.nrscotland.gov.uk/covid19stats); [Northern Ireland Statistics and Research Agency](https://www.nisra.gov.uk/publications/weekly-deaths).  
Baseline years: 2010-2019  
Data frequency: weekly  


**United States**
Source: [Centers for Disease Control and Prevention](https://www.cdc.gov/nchs/nvss/vsrr/covid_weekly/)
Baseline years: 2015-2019  
Data frequency: weekly  


**Boston, United States**
Source: Massachusetts Department of Public Health
Baseline years: 2015-2019
Data frequency: weekly


**Chicago, United States**
Source: Illinois Department of Public Health
Baseline years: 2017-2019
Data frequency: weekly


**Denver, United States**
Source: Colorado Department of Public Health and Environment
Baseline years: 2017-2019
Data frequency: monthly


**Detroit, United States**
Source: Michigan Department of Health and Human Services
Baseline years: 2017-2019
Data frequency: weekly


**Miami, United States**
Source: Florida Department of Health
Baseline years: 2015-2019
Data frequency: monthly


**New York City, United States**
Source: [Centers for Disease Control and Prevention](https://gis.cdc.gov/grasp/fluview/mortality.html)
Baseline years: 2015-2019
Data frequency: weekly






## Other Collections of All-Cause Mortality Data

[The Human Mortality Database](https://www.mortality.org/) includes recent all-cause deaths collected by demographers at the Max Planck Institute for Demographic Research and other institutions. [The Economist](https://github.com/TheEconomist/covid-19-excess-deaths-tracker) and the [Financial Times](https://github.com/Financial-Times/coronavirus-excess-mortality-data) are also publicly releasing their data on all-cause mortality.

## License and Attribution

This data is licensed under the same terms as our Coronavirus Data in the United States data. In general, we are making this data publicly available for broad, noncommercial public use including by medical and public health researchers, policymakers, analysts and local news media.

If you use this data, you must attribute it to “The New York Times” in any publication. If you would like a more expanded description of the data, you could say “Data from The New York Times, based on reports from national and municipal health agencies.”

If you use it in an online presentation, we would appreciate it if you would link to our graphic tracking  these deaths [https://www.nytimes.com/interactive/2020/04/21/world/coronavirus-missing-deaths.html](https://www.nytimes.com/interactive/2020/04/21/world/coronavirus-missing-deaths.html).

If you use this data, please let us know at covid-data@nytimes.com.

See our [LICENSE](LICENSE) for the full terms of use for this data.

## Contact Us

If you have questions about the data or licensing conditions, please contact us at:

covid-data@nytimes.com


## Contributors

Allison McCann, Jin Wu, Josh Katz and Denise Lu have been leading our data collection efforts. 

Elian Peltier contributed reporting from Paris, Muktita Suhartono from Bangkok, Carlotta Gall from Istanbul, Anatoly Kurmanaev from Caracas, Venezuela, Monika Pronczuk from Brussels, José María León Cabrera from Quito, Ecuador, Irit Pazner from Jerusalem, Mirelis Morales from Lima and Manuela Andreoni from Rio de Janeiro.

Thank you to Stéphane Helleringer, Johns Hopkins University; Tim Riffe, Max Planck Institute for Demographic Research; Lasse Skafte Vestergaard, EuroMOMO; Vladimir Shkolnikov, Max Planck Institute for Demographic Research; Jenny Garcia, Institut National d'Études Démographiques; Tom Moultrie, University of Cape Town; Isaac Sasson, Tel Aviv University; Patrick Gerland, United Nations; S V Subramanian, Harvard University; Paulo Lotufo, University of São Paulo; and Marcelo Oliveira.
