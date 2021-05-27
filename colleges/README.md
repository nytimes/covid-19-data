# Tracking Covid-19 at U.S. Colleges and Universities

The New York Times is releasing [counts of Covid-19 cases reported on college and university campuses](https://www.nytimes.com/interactive/2021/us/college-covid-tracker.html) in the United States.

Since late July, we have been conducting a rolling survey of American colleges and universities — including every four-year public institution and every private college that competes in N.C.A.A. sports — to track the number of coronavirus cases reported among students and employees. The survey now includes more than 1,900 colleges. Starting in 2021 the number of cases in 2021 is also included.

This data was most recently updated on May 26, 2021. It may be updated again at a later date.

## Data

Data can be found in the **[colleges.csv](colleges.csv)** file. ([Raw CSV](https://raw.githubusercontent.com/nytimes/covid-19-data/master/colleges/colleges.csv))

```
date,state,county,city,ipeds_id,college,cases,cases_2021,notes
2021-02-26,Alabama,Madison,Huntsville,100654,Alabama A&M University,41,,
…
2021-02-26,Alabama,Jefferson,Birmingham,100663,University of Alabama at Birmingham,2856,570,"Total is known to include one or more cases from a medical school, medical center, teaching hospital, clinical setting or other academic program in health sciences."
```

The fields have the following definitions:

**date**: The date of the last update.  
**state**: The state where the college is located.  
**county**: The county where the college is located.  
**city**: The city where the college is located.  
**ipeds_id**: The Integrated Postsecondary Education Data System (IPEDS) ID number for the college.  
**college**: The name of the college or university.  
**cases**: The total number of reported Covid-19 cases among university students and employees in all fields, including those whose roles as doctors, nurses, pharmacists or medical students put them at higher risk of contracting the virus, since the beginning of the pandemic.  
**cases_2021**: The total number of newly reported Covid-19 cases since Jan. 1, 2021 only.
**notes**: Specific methodological notes that apply to the institution, for example if the count includes cases from a medical unit, and if there is a possibility that duplicate cases have been counted due to the manner in which the institution reports data.   

Colleges and universities that have reported zero cases will be listed with a zero for cases, while colleges which have not reported data will have a blank in the cases field.

## Methodology

Data is based on reports from colleges and government sources and may lag. Cases include those of students, faculty, staff members and other college workers. Colleges and government agencies report this data differently, so exercise caution when comparing institutions. Some colleges declined to provide data, provided partial data or did not respond to inquiries. At some institutions, cases may be spread across multiple campuses. Total cases include confirmed positive cases and probable cases, where available. Colleges occasionally adjust their data downward if new information emerges.

Because colleges report data differently, and because cases continued to emerge even in the months when most campuses were closed, The Times is counting all reported cases since the start of the pandemic for 2020.

With no national tracking system, colleges are making their own rules for how to tally infections. While The Times’s survey is believed to be the most comprehensive account available, it is also a near-certain undercount. Among the colleges contacted by The Times, most published case information online or responded to requests for case numbers, but others did not respond, declined to provide information or only provided partial information. Some colleges reported zero cases. The Times obtained case data through open records requests at several public universities that would not otherwise provide numbers.

Given the disparities in size, reopening plans and transparency among universities, it is not recommended to use this data to make campus-to-campus comparisons. Some colleges subtract cases from their tallies once people recover. Some report only tests performed on campus. Some colleges reported some cases without identifying whether they occurred in 2020 or 2021. Those cases are not included in our totals.

When colleges have noted that an infected person did not have access to campus in the month before testing positive, we have excluded them from our count.

The size of colleges and universities in this data set vary widely, but we have not calculated or published per capita case counts because institutions vary in whether they report cases among faculty and staff and in how the total population of faculty, staff and students are defined.

Because colleges continue to change how they report data, we will not be publishing any historical time series of the number of cases at different points in time. 

## License and Attribution

This data is licensed under the same terms as our [Coronavirus Data in the United States data](https://github.com/nytimes/covid-19-data). In general, we are making this data publicly available for broad, noncommercial public use including by medical and public health researchers, policymakers, analysts and local news media.

If you use this data, you must attribute it to “The New York Times” in any publication. If you would like a more expanded description of the data, you could say “The New York Times survey of U.S. Colleges and Universities”

If you use it in an online presentation, we would appreciate it if you would link to our graphic discussing these results [https://www.nytimes.com/interactive/2021/us/college-covid-tracker.html](https://www.nytimes.com/interactive/2021/us/college-covid-tracker.html).

If you use this data, please let us know at covid-data@nytimes.com.

See our [LICENSE](https://github.com/nytimes/covid-19-data/blob/master/LICENSE) for the full terms of use for this data.

## Contact Us

If you have questions about the data or licensing conditions, please contact us at:

covid-data@nytimes.com

## Contributors

Weiyi Cai, Danielle Ivory, Kirk Semple, Mitch Smith, Alex Lemonides, Lauryn Higgins, Adeel Hassan, Julia Calderone, Jordan Allen, Anne Barnard, Yuriria Avila, Brillian Bao, Elisha Brown, Alyssa Burr, Sarah Cahalan, Matt Craig, Yves De Jesus, Brandon Dupré, Timmy Facciola, Bianca Fortis, Grace Gorenflo, Benjamin Guggenheim, Barbara Harvey, Jacob LaGesse, Alex Lim, Alex Leeds Matthews, Jaylynn Moffat-Mowatt, Ashlyn O’Hara, Laney Pope, Cierra S. Queen, Natasha Rodriguez, Jess Ruderman, Alison Saldanha, Emily Schwing, Sarena Snider, Brandon Thorp, Kristine White, Bonnie G. Wong, Tiffany Wong and John Yoon.