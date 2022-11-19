# Cases and Deaths Rolling Averages and Anomalous Days

The data in these files is a different version of the data in our main U.S. cases and deaths [files](https://github.com/nytimes/covid-19-data). Instead of cumulative totals, each file contains the daily number of new cases and deaths, the seven-day rolling average and the seven-day rolling average per 100,000 residents.

This data was reported by dozens of journalists at The Times, drawing from a patchwork of county, state and national government sources. The ever-evolving nature of the coronavirus pandemic meant that the way these officials reported their data was not always consistent. 

In compiling data, we chose to prioritize the accuracy of our cumulative case counts. Because of that, the number of new daily cases may at times appear anomalous because it is derived from the difference in cumulative cases from one day to another. 

In creating our rolling averages, we’ve drawn on our experience reporting coronavirus data since early 2020. Using that editorial judgment and expertise, we elected to exclude certain data points from the calculation of these averages because they would skew county, state or national trends in the data. These instances are listed, as is our best understanding of the reason for the data anomaly. 

All the methodology noted in our description of the main cases and deaths data continues to apply here.

## Rolling Averages

The fields have the following definitions:

* **geoid**: A unique geographic identifier for each place. For counties and states, the final five digits are the same as the FIPS code when possible. In instances where we have assigned a non-standard identifier, the geoid will end in `99[0-9]`.  
* **cases**: The number of new cases of Covid-19 reported that day, including both confirmed and probable.  
* **cases_avg**: The average number of new cases reported over the most recent seven days of data.  
* **cases_avg_per_100k**: The `cases_avg` per 100,000 people.  
* **deaths**: The total number of new deaths from Covid-19 reported that day, including both confirmed and probable.  
* **deaths_avg**: The daily average number of new deaths reported over the most recent period. County-level deaths are averaged over 30 days. State, territory and national deaths are averaged over 7 days.  
* **deaths_avg_per_100k**: The `deaths_avg` per 100,000 people.  

Because many agencies do not report data every day, variation in the schedule on which cases or deaths are reported, such as around holidays, can cause irregular patterns in a simple seven-day trailing average.

To adjust for this in our averages, the number of days included in the average may be extended if there are days within the time range with no data reported. The average is extended to older days until at least seven days of data are included.

If the most recent days have no data reported, then the average is extended further back until seven days worth of data are included. Data reported on a day that follows one or more days with no data reported is assumed to represent multiple days worth of data. In any average, that day and all non-reporting days preceding it are always included together in the average. This may cause some averages to include more than seven days.

For the U.S. national case and death count averages, the average is the sum of the average number of cases and deaths in all states and territories each day. This average may not match the average when calculated from the U.S. case and death total in order to account for irregularly timed case and death reports at the state level.

See the methodology section for a more detailed discussion of how single-day reporting anomalies affect the average.

### U.S. National-Level Data

The daily number of newly reported cases and deaths nationwide, including all states, U.S. territories and the District of Columbia, can be found in the [us.csv](us.csv) file.  ([Raw CSV file here.](https://raw.githubusercontent.com/nytimes/covid-19-data/master/rolling-averages/us.csv))

```
date,geoid,cases,cases_avg,cases_avg_per_100k,deaths,deaths_avg,deaths_avg_per_100k
2020-01-21,USA,1,0.14,0,0,0,0
...
```

### State-Level Data

State-level data can be found in the [states.csv](us-states.csv) file. ([Raw CSV file here.](https://raw.githubusercontent.com/nytimes/covid-19-data/master/rolling-averages/us-states.csv))

```
date,geoid,state,cases,cases_avg,cases_avg_per_100k,deaths,deaths_avg,deaths_avg_per_100k
2020-01-21,USA-53,Washington,1,0.14,0,0,0,0
...
```

### County-Level Data

Recent county-level data can be found in the [us-counties-recent.csv](us-counties-recent.csv) file. ([Raw CSV file here.](https://raw.githubusercontent.com/nytimes/covid-19-data/master/rolling-averages/us-counties-recent.csv))

```
date,geoid,county,state,cases,cases_avg,cases_avg_per_100k,deaths,deaths_avg,deaths_avg_per_100k
2020-01-21,USA-53061,Snohomish,Washington,1,0.14,0.02,0,0,0
...
```

This file contains data only for the last 30 days.

There are now county-level files for each year of the pandemic, like [us-counties-2020.csv](us-counties-2020.csv). To create a single file covering the entire pandemic, combine each annual file.

There is also an older file, [us-counties.csv](us-counties.csv) that contains data starting from the beginning of the pandemic through September 2021. Of note, this counties file is too large to be opened in Excel and too large to continue to be updated on Github. ([Raw CSV file here.](https://raw.githubusercontent.com/nytimes/covid-19-data/master/rolling-averages/us-counties.csv)). 

## Anomalies

The list of anomalous days is in the [anomalies.csv](anomalies.csv) file. ([Raw CSV file here.](https://raw.githubusercontent.com/nytimes/covid-19-data/master/rolling-averages/anomalies.csv))

```
date,end_date,county,state,geoid,type,omit_from_rolling_average,omit_from_rolling_average_on_subgeographies,adjusted_daily_count_for_avg,description
2020-04-06,,New York City,New York,USA-36998,deaths,,,The Times began using deaths reported by the New York State Health Department instead of the city's health department.
...
```

The fields have the following definitions: 

* **date**: The date to which the anomaly applies.  
* **end_date**: For anomalies that span multiple days, the last day to which it applies. Otherwise, left blank.  
* **geoid**: A unique geographic identifier for each place. Use this to match against the file of rolling averages.  
* **type**: Whether the anomaly applies to the data on cases, deaths or both.  
* **omit_from_rolling_average**: This will be `yes` if the data for that day is excluded from the calculation of rolling averages. Otherwise, left blank.  
* **omit_from_rolling_average_on_subgeographies**: This will be `yes` if the data for that day is excluded from the calculation of rolling averages, for all subgeographies, i.e. the counties within a state. Otherwise, left blank.  
* **adjusted_daily_count_for_avg**: If the daily total includes a large known backlog, this is the adjustment to the case or death count used for the purpose of calculating a more accurate current rolling average.  
* **description**: A note explaining the cause for the anomaly, based on data reporting and/or communication with local officials. These explanations appear at the bottom of the geography tracking pages.  

### Anomalies Methodology

The list of anomalies published here is curated and maintained based on our daily review of newly reported case and death counts published each day, and verified by public statements published by health departments either publicly or via press releases, or our own additional reporting and research. It is neither a complete list of all anomalies with Covid data, nor based on any statistical outlier detection.

Identified anomalies are often because of officials making revisions to improve the overall quality of the data they have released. Many small anomalies due to backlogs of cases or minor revisions of previously announced numbers are not included here, particularly at the county level. There are no listed anomalies from very early in the pandemic. When deciding whether to list an anomaly, we judge whether a member of the public would need that note to understand and put in context that day’s case or death count.

When deciding whether to exclude an anomaly from our rolling averages, we use our best judgment of whether including the day in the rolling average would significantly distort the overall trend appearing in the data. Since data fluctuations are common and agencies vary in their typical reporting rhythms, we have found it is not beneficial to use a completely objective standard, and we err toward not removing data from the rolling averages. Factors we consider include: the proportion of anomalous cases or deaths in the daily total, whether the information is relevant to recent trends, and how much delay or variation is typical for a particular data source.

We sometimes remove a day’s numbers from the rolling average at the state level, but not at the county level or vice versa, because county- and state-level data can come from different sources, or a state may provide a more detailed explanation of cases at the state level than it does at the county level.

Population data used to calculate per capita figures comes from the U.S. Census Bureau 2019 population estimate.


## License and Attribution

This data is licensed under the same terms as our [Coronavirus Data in the United States data](https://github.com/nytimes/covid-19-data). In general, we are making this data publicly available for broad, noncommercial public use, including by medical and public health researchers, policymakers, analysts and local news media.

If you use this data, you must attribute it to “The New York Times” in any publication. If you would like a more expanded description of the data, you could say, “Data from The New York Times, based on reports from state and local health agencies.”

For papers following APA format, we recommend the following citation: "The New York Times. (2021). Coronavirus (Covid-19) Data in the United States. Retrieved [Insert Date Here], from https://github.com/nytimes/covid-19-data."

If you use it in an online presentation, we would appreciate it if you would link to our U.S. tracking page at [https://www.nytimes.com/interactive/2020/us/coronavirus-us-cases.html](https://www.nytimes.com/interactive/2020/us/coronavirus-us-cases.html).

If you use this data, please let us know at covid-data@nytimes.com.

See our [LICENSE](https://github.com/nytimes/covid-19-data/blob/master/LICENSE) for the full terms of use for this data.

## Contact Us

If you have questions about the data or licensing conditions, please contact us at:

covid-data@nytimes.com

## Contributors

[The list of contributors is the same as the list for the primary Coronavirus Data in the United States data](https://github.com/nytimes/covid-19-data)
