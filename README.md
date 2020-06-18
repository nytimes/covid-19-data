# Coronavirus (Covid-19) Data in the United States

**NEW:** We are publishing the data behind our [excess deaths tracker](https://www.nytimes.com/interactive/2020/04/21/world/coronavirus-missing-deaths.html) in order to provide researchers and the public with a better record of the true toll of the pandemic. This data is compiled from official national and municipal data for 24 countries. See the data and documentation in the [excess-deaths/](excess-deaths/) directory.

---

[ [U.S. Data](us.csv) ([Raw CSV](https://raw.githubusercontent.com/nytimes/covid-19-data/master/us.csv)) | [U.S. State-Level Data](us-states.csv) ([Raw CSV](https://raw.githubusercontent.com/nytimes/covid-19-data/master/us-states.csv)) | [U.S. County-Level Data](us-counties.csv) ([Raw CSV](https://raw.githubusercontent.com/nytimes/covid-19-data/master/us-counties.csv)) ]

The New York Times is releasing a series of data files with cumulative counts of coronavirus cases in the United States, at the state and county level, over time. We are compiling this time series data from state and local governments and health departments in an attempt to provide a complete record of the ongoing outbreak.

Since late January, The Times has tracked cases of coronavirus in real time as they were identified after testing. Because of the widespread shortage of testing, however, the data is necessarily limited in the picture it presents of the outbreak.

We have used this data to power our [maps](https://www.nytimes.com/interactive/2020/us/coronavirus-us-cases.html) and [reporting](https://www.nytimes.com/coronavirus) tracking the outbreak, and it is now being made available to the public in response to requests from researchers, scientists and government officials who would like access to the data to better understand the outbreak.

The data begins with the first reported coronavirus case in Washington State on Jan. 21, 2020. We will publish regular updates to the data in this repository. 

## Live and Historical Data

We are providing two sets of data with cumulative counts of coronavirus cases and deaths: one with our most current numbers for each geography and another with historical data showing the tally for each day for each geography.

The historical data files are at the top level of the directory and contain data up to, but not including the current day. The live data files are in the [live/](live/) directory.

A key difference between the historical and live files is that the numbers in the historical files are the final counts at the end of each day, while the live files have figures that may be a partial count released during the day but cannot necessarily be considered the final, end-of-day tally..

The historical and live data are released in three files, one for each of these geographic levels: U.S., states and counties.
 
Each row of data reports the cumulative number of coronavirus cases and deaths based on our best reporting up to the moment we publish an update. Our counts include both laboratory confirmed and probable cases using [criteria](https://int.nyt.com/data/documenthelper/6908-cste-interim-20-id-01-covid-19/85d47e89b637cd643d50/optimized/full.pdf) that were developed by states and the federal government. Not all geographies are reporting probable cases and yet others are providing confirmed and probable as a single total. Please [read here](https://github.com/nytimes/covid-19-data/blob/master/PROBABLE-CASES-NOTE.md) for a full discussion of this issue.

We do our best to revise earlier entries in the data when we receive new information. If a county is not listed for a date, then there were zero reported confirmed cases and deaths.

State and county files contain [FIPS codes](https://www.census.gov/quickfacts/fact/note/US/fips), a standard geographic identifier, to make it easier for an analyst to combine this data with other data sets like a map file or population data.

Download all the data or clone this repository by clicking the green "Clone or download" button above.

---

### Historical Data

#### U.S. National-Level Data

The daily number of cases and deaths nationwide, including states, U.S. territories and the District of Columbia, can be found in the [us.csv](us.csv) file.  ([Raw CSV file here.](https://raw.githubusercontent.com/nytimes/covid-19-data/master/us.csv))

```
date,cases,deaths
2020-01-21,1,0
...
```

#### State-Level Data

State-level data can be found in the [states.csv](us-states.csv) file. ([Raw CSV file here.](https://raw.githubusercontent.com/nytimes/covid-19-data/master/us-states.csv))

```
date,state,fips,cases,deaths
2020-01-21,Washington,53,1,0
...
```

#### County-Level Data

County-level data can be found in the [counties.csv](us-counties.csv) file. ([Raw CSV file here.](https://raw.githubusercontent.com/nytimes/covid-19-data/master/us-counties.csv))

```
date,county,state,fips,cases,deaths
2020-01-21,Washington,Snohomish,53061,1,0
...
```

In some cases, the geographies where cases are reported do not map to standard county boundaries. See the list of [geographic exceptions](#geographic-exceptions) for more detail on these.

---

### Live Data

The files in the [live/](live/) directory are also available at three geographic levels and contain all the fields the historical data files have, but with only data for the current day. We try to update these files multiple times per day. 

Because these are updated throughout the day, they can have inconsistent counts, are more likely to contain errors, and should be considered less reliable than the historical data. Different areas of the country update at different times and our data collection process can move at a different pace as well.

In addition to the columns that are in the historical files, these files also include new columns that include detail on the number of confirmed and probable cases, separately.

In the live files, the case and death fields have the following definitions:

* **cases**: The total number of cases of Covid-19, including both confirmed and probable.
* **deaths**: The total number of deaths from Covid-19, including both confirmed and probable.
* **confirmed_cases**: The number of laboratory confirmed Covid-19 cases only, or blank if not available.
* **confirmed_deaths**: The number of laboratory confirmed Covid-19 deaths only, or blank if not available.
* **probable_cases**: The number of probable Covid-19 cases only, or blank if not available.
* **probable_deaths**: The number of probable Covid-19 deaths only, or blank if not available.

We understand this breakout would also be valuable historically, and are working toward providing that. Please bear with us as we roll out this new and more complicated data.

The live data can be found in files at the U.S. level in the [us.csv](live/us.csv) file, at the state level in the [states.csv](live/us-states.csv) file, and at the county level in the [counties.csv](live/us-counties.csv) file.


## Methodology and Definitions

The data is the product of dozens of journalists working across several time zones to monitor news conferences, analyze data releases and seek clarification from public officials on how they categorize cases. 

It is also a response to a fragmented American public health system in which overwhelmed public servants at the state, county and territorial level have sometimes struggled to report information accurately, consistently and speedily. On several occasions, officials have corrected information hours or days after first reporting it. At times, cases have disappeared from a local government database, or officials have moved a patient first identified in one state or county to another, often with no explanation. In those instances, which have become more common as the number of cases has grown, our team has made every effort to update the data to reflect the most current, accurate information while ensuring that every known case is counted.

When the information is available, we count patients where they are being treated, not necessarily where they live.

In most instances, the process of recording cases has been straightforward. But because of the patchwork of reporting methods for this data across more than 50 state and territorial governments and hundreds of local health departments, our journalists sometimes had to make difficult interpretations about how to count and record cases.

For those reasons, our data will in some cases not exactly match with the information reported by states and counties. Those differences include these cases: When the federal government arranged flights to the United States for Americans exposed to the coronavirus in China and Japan, our team recorded those cases in the states where the patients subsequently were treated, even though local health departments generally did not. When a resident of Florida died in Los Angeles, we recorded her death as having occurred in California rather than Florida, though officials in Florida counted her case in their own records. And when officials in some states reported new cases without immediately identifying where the patients were being treated, we attempted to add information about their locations later, once it became available.

* Confirmed Cases

Confirmed cases and deaths are counts of individuals whose coronavirus infections were confirmed by a laboratory test and reported by a federal, state, territorial or local government agency.

The number of cases includes all cases, including those who have since recovered or died.

* "Probable" Cases and Deaths

Probable cases and deaths count individuals who did not have a confirmed test but were evaluated using criteria developed by states and the federal government.

On April 5, the Council of State and Territorial Epidemiologists Centers [advised states](https://int.nyt.com/data/documenthelper/6908-cste-interim-20-id-01-covid-19/85d47e89b637cd643d50/optimized/full.pdf) to include both confirmed cases, based on laboratory testing, and probable cases, based on specific criteria for symptoms and exposure. The Centers for Disease Control adopted these definitions and national CDC data began including confirmed and probable cases on April 14.

Some governments continue to report only confirmed cases, while others are reporting both confirmed and probable numbers. And there is also another set of governments that are reporting the two types of numbers combined without providing a way to separate the confirmed from the probable.

Please see the Geographic Exceptions section below for more details on specific areas, with the understanding that this changes frequently.

* Dates

For each date, we show the cumulative number of confirmed cases and deaths as reported that day in that county or state. All cases and deaths are counted on the date they are first announced.

Each date includes all cases and deaths announced that day through midnight Eastern Time. As the West Coast and Hawaii tend to release all of their new data early enough in the day.

* Declining Counts

In some cases, the number of cases or deaths for a state or county will decline. This can occur when a state or county corrects an error in the number of cases or deaths they've reported in the past, or when a state moves cases from one county to another. When we are able, we will historically revise counts for all impacted dates. In other cases, this will be reflected in a single-day drop in the number of cases or deaths.

* Counties

In some instances, we report data from multiple counties or other non-county geographies as a single county. For instance, we report a single value for New York City, comprising the cases for New York, Kings, Queens, Bronx and Richmond Counties. In these instances the FIPS code field will be empty. (We may assign FIPS codes to these geographies in the future.) See the list of [geographic exceptions](#geographic-exceptions). 

Cities like St. Louis and Baltimore that are administered separately from an adjacent county of the same name are counted separately.

* “Unknown” Counties

Many state health departments choose to report cases separately when the patient’s county of residence is unknown or pending determination. In these instances, we record the county name as “Unknown.” As more information about these cases becomes available, the cumulative number of cases in “Unknown” counties may fluctuate.

Sometimes, cases are first reported in one county and then moved to another county. As a result, the cumulative number of cases may change for a given county.

### Geographic Exceptions

* New York

All cases for the five boroughs of New York City (New York, Kings, Queens, Bronx and Richmond counties) are assigned to a single area called New York City. There is a large jump in the number of deaths on April 6th due to switching from data from New York City to data from New York state for deaths. We are not currently including the probable deaths reported by New York City.

For all New York state counties, starting on April 8th we are reporting deaths by place of fatality instead of residence of individual. There were no new deaths reported by the state on April 17th or April 18th.

* Georgia

Starting April 12th, our case count excludes cases labeled by the state as "Non-Georgia Resident" leading to a one day drop in cases. These cases were previously included as cases with "Unknown" county.

* Alabama

Alabama's numbers for April 17th contained an [error](https://twitter.com/ALPublicHealth/status/1251531524958289920) in reporting of lab test results that the state is working to correct. The number of deaths drops on April 23rd for an unknown reason.

* Kansas City, Mo.

Four counties (Cass, Clay, Jackson and Platte) overlap the municipality of Kansas City, Mo. The cases and deaths that we show for these four counties are only for the portions exclusive of Kansas City. Cases and deaths for Kansas City are reported as their own line.

* Alameda County, Calif.

Counts for Alameda County include cases and deaths from Berkeley and the Grand Princess cruise ship.

* Douglas County, Neb.

Counts for Douglas County include cases brought to the state from the Diamond Princess cruise ship.

* Chicago

All cases and deaths for Chicago are reported as part of Cook County.

* Guam

Counts for Guam include cases reported from the USS Theodore Roosevelt.

* Puerto Rico

On April 21, the territory's health department revised their number of cases downward, saying they had been double counting some coronavirus patients in official reports, leading to a higher number of cases reported than actually confirmed. 

Additionally, from approximately April 12th through April 18th, the count of deaths for Puerto Rico include some probable Covid-19 related deaths that were not lab-confirmed. Starting April 19th these have been removed. We will revise the numbers for the 12th to 18th as possible.

* North Dakota

On May 25, North Dakota annoucned that due to a laboratory equipment malfunction they were removing 82 positive results from their total case count, pending a retest of the samples.

* Connecticut

On May 27, Connecticut [announced](https://portal.ct.gov/Office-of-the-Governor/News/Press-Releases/2020/05-2020/Governor-Lamont-Coronavirus-Update-May-27) announced that they were removing 356 positive cases, which were determined to be duplicates, from their total case count.

The number of deaths reported by the state in four counties on June 1 was anomalously high and several deaths are removed in the data for June 2.

* Louisiana

On May 29, Louisiana announced that due to a technical error they would not have an update on the number of total cases that day.

On June 13, Louisiana reported an additional 560 backlogged cases from multiple labs and facilities from between April 25 and June 9.

On June 16, Louisiana reported an additional 148 backlogged cases, the majority of which date back to mid-April.

* Massachusetts

On April 24, Massachusetts reported the results of a large number of backlogged tests performed by Quest Diagnostics dating back to April 13, leading to a large one day jump in the number of total cases.

* Texas

On June 16, Texas reported an additional 1,476 backlogged cases from prison inmates in Anderson and Brazoria counties.

* Washington

On June 17, Washington began removing from their totals deaths where Covid-19 was not a factor, for instance homicides, overdoses, suicides and car accidents. Four deaths from King County and three from Yakima county that were due to homicide, suicide or overdose were removed.

#### Probable Cases and Deaths

* Colorado

Numbers reflect the combined number of lab-confirmed and probable cases and deaths as reported by the state. On April 25th, the state revised downward the number of deaths after removing "about 29 duplicates" from the number of "probable deaths" included in the total.

* Hawaii

Numbers reflect the combined number of lab-confirmed and probable cases and deaths as reported by the state.

* Illinois

On June 8, Illinois started reporting probable cases and deaths in their data. We are including these cases and deaths in our total numbers for the state.

* Louisiana

The total cases number and total deaths number include only lab-confirmed cases and deaths. The state is reporting the deaths of probable Covid-19 cases separately from their total number of deaths statewide and in each parish, and we are including those deaths in our total number of deaths for the state.

* Massachusetts

On June 1, Massachusetts started reporting probable cases and deaths in their data. The total number of cases and deaths on that day include probable cases and deaths going back to March 1, leading to a large one day jump in the totals.

* Michigan

On June 1, we began recording probable cases and deaths reported by Michigan's county and regional health districts and adding them to the individual county and statewide totals. On June 5, the state also started to report probable cases and deaths statewide, leading to a jump in total cases and deaths.

* Ohio

The state reports lab-confirmed and probable cases and deaths separately at the state level but combine lab-confirmed and probable cases and deaths at the county level. Our statewide and county numbers combine both case types.

* Pennsylvania

The total cases number includes lab-confirmed and probable cases starting around April 16th, but the deaths number does not include probable deaths, except for on April 21st and April 22nd when it does.

* Virginia

The state reports lab-confirmed and probable cases and deaths separately at the state level but combine lab-confirmed and probable cases and deaths at the county level. Our statewide and county numbers combine both case types.

* Puerto Rico

Our number of cases for Puerto Rico includes the results of serological cases in their total number of cases, we believe this more closely matches the definition of probable cases than confirmed cases as reported elsewhere. Our number of deaths is only deaths with a confirmed test.

## License and Attribution

In general, we are making this data publicly available for broad, noncommercial public use including by medical and public health researchers, policymakers, analysts and local news media.

If you use this data, you must attribute it to “The New York Times” in any publication. If you would like a more expanded description of the data, you could say “Data from The New York Times, based on reports from state and local health agencies.”

If you use it in an online presentation, we would appreciate it if you would link to our U.S. tracking page at [https://www.nytimes.com/interactive/2020/us/coronavirus-us-cases.html](https://www.nytimes.com/interactive/2020/us/coronavirus-us-cases.html).

If you use this data, please let us know at covid-data@nytimes.com.

See our [LICENSE](LICENSE) for the full terms of use for this data.

This license is co-extensive with the Creative Commons Attribution-NonCommercial 4.0 International license, and licensees should refer to that license ([CC BY-NC](https://creativecommons.org/licenses/by-nc/4.0/legalcode)) if they have questions about the scope of the license.


## Contact Us

If you have questions about the data or licensing conditions, please contact us at:

covid-data@nytimes.com


## Contributors

Mitch Smith, Karen Yourish, Sarah Almukhtar, Keith Collins, Danielle Ivory and Amy Harmon have been leading our U.S. data collection efforts.

Data has also been compiled by Jordan Allen, Jeff Arnold, Aliza Aufrichtig, Mike Baker, Robin Berjon, Matthew Bloch, Nicholas Bogel-Burroughs, Maddie Burakoff, Christopher Calabrese, Andrew Chavez, Robert Chiarito, Carmen Cincotti, Alastair Coote, Matt Craig, John Eligon, Tiff Fehr, Andrew Fischer, Matt Furber, Rich Harris, Lauryn Higgins, Jake Holland, Will Houp, Jon Huang, Danya Issawi, Jacob LaGesse, Hugh Mandeville, Patricia Mazzei, Allison McCann, Jesse McKinley, Miles McKinley, Sarah Mervosh, Andrea Michelson, Blacki Migliozzi, Steven Moity, Richard A. Oppel Jr., Jugal K. Patel, Nina Pavlich, Azi Paybarah, Sean Plambeck, Carrie Price, Scott Reinhard, Thomas Rivas, James G. Robinson, Michael Robles, Alison Saldanha, Alex Schwartz, Libby Seline, Shelly Seroussi, Rachel Shorey, Anjali Singhvi, Charlie Smart, Ben Smithgall, Steven Speicher, Michael Strickland, Albert Sun, Thu Trinh, Tracey Tully, Maura Turcotte, Miles Watkins, Phil Wells, Jeremy White, Josh Williams, Jin Wu and Yanxing Yang.