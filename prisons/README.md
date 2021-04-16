# Tracking Covid-19 in Prisons, Jails and Detention Facilities

From March 2020 until the end of March 2021, The New York Times collected data about coronavirus infections, deaths and testing for state and federal prisons; immigration detention centers; juvenile detention facilities; local, regional and reservation jails; and those in the custody of the U.S. Marshals Service.

The Times gathered information about infections, deaths, facility populations and tests administered to inmates and correctional officers for 2,805 facilities, and systemwide totals for the same data. 

The Times’s data collection effort also gathered health and demographic information about people in correctional institutions and detention centers. 

This population represented a particularly vulnerable group of people who were at far higher risk of coronavirus infection than members of the general public. We have used this data to [look at the impact of the virus in prisons](https://www.nytimes.com/interactive/2021/04/10/us/covid-prison-outbreak.html), and are now making it public to help researchers, scientists and the general public better understand these outbreaks.

## Data

Data on individual facilities can be found in the **[facilities.csv](facilities.csv)** file. ([Raw CSV](https://raw.githubusercontent.com/nytimes/covid-19-data/master/prisons/facilities.csv))

```
nyt_id,facility_name,facility_type,facility_city,facility_county,facility_county_fips,facility_state,facility_lng,facility_lat,latest_inmate_population,max_inmate_population_2020,total_inmate_cases,total_inmate_deaths,total_officer_cases,total_officer_deaths,note
F3EFE858,Alex City Work Release prison,Low-security work release,Alex City,Coosa,01037,Alabama,-86.0090148,32.9045073,188,,77,0,17,0,
...
```

The fields have the following definitions:

* **nyt_id**: A unique identifier we may use to match future data to this data set.  
* **facility_name**: The name of the facility.  
* **facility_type**: The type of facility.  
* **facility_city**: The city where this facility is located.  
* **facility_county**: The county where this facility is located.  
* **facility_county_fips**: The county FIPS code of the county.  
* **facility_state**: The state where the facility is located.   
* **facility_lng** and **facility_lat**: The longitude and latitude of the facility.  
* **latest_inmate_population**: The most recent number of inmates at the facility.  
* **max_inmate_population_2020**: The maximum number of inmates at the facility reported at any time from March 2020 through March 2021.  
* **total_inmate_cases**: Total number of cases of Covid-19 reported among inmates from the beginning of the pandemic through the end of March 2021.  
* **total_inmate_deaths**: Total number of inmates who were reported to have died of Covid-19 from the beginning of the pandemic through the end of March 2021.  
* **total_officer_cases**: Total number of cases of Covid-19 reported among correctional officers working at the facility from the beginning of the pandemic through the end of March 2021.  
* **total_officer_deaths**: Total number of correctional officers who worked at the facility who were reported to have died of Covid-19 from the beginning of the pandemic through the end of March 2021.  
* **note**: Any notes important for the interpretation of data on this facility.  


Data on states and prison and detention systems can be found in the **[systems.csv](systems.csv)** file. ([Raw CSV](https://raw.githubusercontent.com/nytimes/covid-19-data/master/prisons/systems.csv))

```
state,inmate_tests,total_inmate_cases,total_inmate_deaths,latest_inmate_population,max_inmate_population_2020,total_officer_cases,total_officer_deaths
Alabama,15505,1601,64,19144,21900,1019,3
...
```

* **system**: The state of the prison system, or other system of detention facilities. For states, the data is reported only for state prisons, not for federal facilities or county jails within the state.  
* **inmate_tests**: The total number of P.C.R. tests conducted on inmates from the beginning of the pandemic through the end of March 2021.  
* **total_inmate_cases**: Total number of cases of Covid-19 reported among inmates in that system from the beginning of the pandemic through the end of March 2021.  
* **total_inmate_deaths**: Total number of inmates in that system who were reported to have died of Covid-19 from the beginning of the pandemic through the end of March 2021.  
* **latest_inmate_population**: The most recent total number of inmates through the system.  
* **max_inmate_population_2020**: The maximum number of inmates in the system from May 2020 through March 2021.  
* **total_officer_cases**: Total number of cases of Covid-19 reported among correctional officers working in the system from the beginning of the pandemic through the end of March 2021.  
* **total_officer_deaths**: Total number of correctional officers working in the system who were reported to have died of Covid-19 from the beginning of the pandemic through the end of March 2021.  


## Methodology

There was no uniform national reporting system for Covid-19 in correctional systems, and state prison systems and local jails sometimes stopped releasing data without explanation.
Some of the data was collected from websites overseen by state and federal prison systems and Immigration and Customs Enforcement. When the data was not publicly available, The Times collected the information through direct inquiries and public records requests, and from data presented at news conferences and meetings of county or state officials.

In cases in which states did not release mortality statistics, The Times used coroners’ reports, medical records provided by families and reports from investigative agencies, including state attorneys general. When state health departments or other state agencies possessed more complete data sets on mortality and infections in state prisons, The Times used the most complete data.

To determine the number of infections in local jails, The Times used internet searches for known cases, and then confirmed the figures with jailers, sheriff’s departments, or local government or health department officers. In cases in which jails declined to provide data, The Times acquired infection numbers and deaths via public records requests.

Infection data for all facilities almost certainly represents an undercount because of a lack of testing. Many state prisons systems have tested inmates several times. But during the first five months of the pandemic, inmates from multiple state prison systems told Times reporters that they had been sick with coronavirus-like symptoms but had never been tested.
 
### Cases and deaths

The information counts unique infections. If an inmate or detainee tested positive multiple times, the case is listed only once.

If an inmate who had an infection was transferred to another facility, the infection was recorded with the institution where the infection was first detected.    

System-wide data is up to date as of March 31, 2020, while facility-level data may be older. 
Some state prison systems, the federal prison system and ICE did not regularly provide facility-level data for inmate infections or disclose the number of tests conducted on inmates or correctional staff members. In those situations, the data represents the most recent facility-level numbers available.

For these reasons, systemwide counts of infections and deaths are typically higher than a sum of the facility-level data in each system. 

State prison systems in Nebraska, Texas and Pennsylvania stopped providing cumulative numbers of infections at the facility level in favor of providing only the number of current infections, making it difficult to ascertain the true cumulative total of cases. Case counts for facilities in these systems represent the highest known cumulative total, but are likely undercounts. The state prison systems that provided only current case totals said they did not keep a cumulative total of inmate infections.

Oklahoma stopped providing facility-level infection data in late February. Facility-level data for Oklahoma represents the latest release.

Some government agencies have removed facilities from their public reporting over the course of the pandemic. The Times data includes those facilities with the most recent number of infections disclosed by the agency. 

Infections in correctional settings in Puerto Rico, Guam and the U.S. Virgin Islands were included in cumulative totals.

Most of the jail figures are cumulative totals as of March 2021. In some cases, however, jails stopped reporting infection information. In those cases, The Times used the most recent cumulative figure. 

Many local jails have tested relatively few of their inmates. A significant number of jails released ill inmates without including them in their infection counts. In situations in which Times journalists were able to determine the number of those released while infected, those counts were included in the total for the facility. 

Two county jails in Pennsylvania are counting the same 18 infected inmates among their numbers. The infected inmates tested positive at the Huntingdon County jail in Huntingdon, Pa., but were later transferred to the Centre County jail in Bellefonte, Pa. The total infections listed at each jail include the 18 infected inmates, but these 18 infections are counted only once in the cumulative total of all jail infections. 

Some jail systems, including New York City, did not provide facility-level infection numbers, but only city- or county-wide totals. In some circumstances, that included four or more different local jails. 

Additionally, New York City and other jurisdictions did not provide the cumulative number of inmate infections but only current infections. Because it was impossible to determine whether current cases had been among the previously disclosed cumulative totals, The Times did not increase its cumulative count unless it was surpassed by the count of those currently infected. For that reason, the cumulative total in some jails and jail systems is likely to be higher than The Times’s total. 
 
### Testing

The data does not include facility-level testing numbers because the total number of coronavirus tests administered in each facility often was not provided, although most states provided cumulative totals of tests for their systems. Arkansas and Montana combined staff and inmate test numbers, so it was not possible to determine how many inmates had been tested in those states. Nevada stopped providing statewide inmate testing data in the summer of 2020. 

Some states that did provide cumulative testing totals reduced without explanation the number of tests they said they had administered. The data represents the highest number of tests each state had said it had administered.
 
### Population

State and federal facility population figures include both the most recent available and the highest number of inmates housed in each facility for the period from March 2020 through March 2021, based on information from prisons when available. Population data was not available for all facilities. 

In states that housed a portion of their prison population in another state, prisoners were counted among inmate populations from their home prison state.

## License and Attribution

This data is licensed under the same terms as our [Coronavirus Data in the United States data](https://github.com/nytimes/covid-19-data). In general, we are making this data publicly available for broad, noncommercial public use, including by medical and public health researchers, policymakers, analysts and local news media.

If you use this data, you must attribute it to “The New York Times” in any publication.

If you use it in an online presentation, we would appreciate it if you would link to our graphic discussing these results [https://www.nytimes.com/interactive/2021/04/10/us/covid-prison-outbreak.html](https://www.nytimes.com/interactive/2021/04/10/us/covid-prison-outbreak.html).

If you use this data, please let us know at covid-data@nytimes.com.

See our [LICENSE](https://github.com/nytimes/covid-19-data/blob/master/LICENSE) for the full terms of use for this data.

## Contact Us

If you have questions about the data or licensing conditions, please contact us at:

covid-data@nytimes.com

## Contributors

Eddie Burkhalter, Izzy Colón, Brendon Derr, Lazaro Gamio, Rebecca Griesbach, Ann Hinga Klein, Danya Issawi, Jacob LaGesse, K.B. Mensah, Derek M. Norman, Savannah Redl, Chloe Reynolds, Emily Schwing, Libby Seline, Rachel Sherman, Maura Turcotte and Timothy Williams.
