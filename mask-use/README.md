# Mask-Wearing Survey Data

The New York Times is releasing estimates of [mask usage](https://www.nytimes.com/interactive/2020/07/17/upshot/coronavirus-face-mask-map.html) by county in the United States.

This data comes from a large number of interviews conducted online by the global data and survey firm Dynata at the request of The New York Times. The firm asked a question about mask use to obtain 250,000 survey responses between July 2 and July 14, enough data to provide estimates more detailed than the state level. (Several states have imposed new mask requirements since the completion of these interviews.)

Specifically, each participant was asked: _How often do you wear a mask in public when you expect to be within six feet of another person?_

This survey was conducted a single time, and at this point we have no plans to update the data or conduct the survey again.

## Data

Data on the estimated prevalence of mask-wearing in counties in the United States can be found in the **[mask-use-by-county.csv](mask-use-by-county.csv)** file. ([Raw CSV](https://raw.githubusercontent.com/nytimes/covid-19-data/master/mask-use/mask-use-by-county.csv))

```
COUNTYFP,NEVER,RARELY,SOMETIMES,FREQUENTLY,ALWAYS
01001,0.053,0.074,0.134,0.295,0.444
01003,0.083,0.059,0.098,0.323,0.436
01005,0.067,0.121,0.12,0.201,0.491
```

The fields have the following definitions:

**COUNTYFP**: The county FIPS code.  
**NEVER**: The estimated share of people in this county who would say **never** in response to the question “How often do you wear a mask in public when you expect to be within six feet of another person?”  
**RARELY**: The estimated share of people in this county who would say **rarely**  
**SOMETIMES**: The estimated share of people in this county who would say **sometimes**  
**FREQUENTLY**: The estimated share of people in this county who would say **frequently**  
**ALWAYS**: The estimated share of people in this county who would say **always**  

## Methodology

To transform raw survey responses into county-level estimates, the survey data was weighted by age and gender, and survey respondents’ locations were approximated from their ZIP codes. Then estimates of mask-wearing were made for each census tract by taking a weighted average of the 200 nearest responses, with closer responses getting more weight in the average. These tract-level estimates were then rolled up to the county level according to each tract’s total population. 

By rolling the estimates up to counties, it reduces a lot of the random noise that is seen at the tract level. In addition, the shapes in the map are constructed from census tracts that have been merged together — this helps in displaying a detailed map, but is less useful than county-level in analyzing the data.

## License and Attribution

This data is licensed under the same terms as our Coronavirus Data in the United States data. In general, we are making this data publicly available for broad, noncommercial public use including by medical and public health researchers, policymakers, analysts and local news media.

If you use this data, you must attribute it to “The New York Times and Dynata” in any publication. If you would like a more expanded description of the data, you could say “Estimates from The New York Times, based on roughly 250,000 interviews conducted by Dynata from July 2 to July 14.”

If you use it in an online presentation, we would appreciate it if you would link to our graphic discussing these results [https://www.nytimes.com/interactive/2020/07/17/upshot/coronavirus-face-mask-map.html](https://www.nytimes.com/interactive/2020/07/17/upshot/coronavirus-face-mask-map.html).

If you use this data, please let us know at covid-data@nytimes.com.

See our [LICENSE](https://github.com/nytimes/covid-19-data/blob/master/LICENSE) for the full terms of use for this data.

## Contact Us

If you have questions about the data or licensing conditions, please contact us at:

covid-data@nytimes.com

## Contributors

Josh Katz, Margot Sanger-Katz and Kevin Quealy.
