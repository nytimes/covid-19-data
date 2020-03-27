#!/bin/bash

# This is a BASH (actually, Posix SH) script to make a JSON file from
# the CSV file for county data which The New York Times has provided
# at https://github.com/nytimes/covid-19-data/
#
# This script needs POSIX-compatible UNIX-like tools (Linux, MacOS,
# Windows with Cygwin) and the "git" tool to pull the data from
# upstream
#
# This script outputs JSON on the standard output
# The JSON is in this form:
# {state name}.{county name}.{date}.deaths
# {state name}.{county name}.{date}.cases

REPO="$1"
if [ -z "$REPO" ] ; then
        REPO="https://github.com/nytimes/covid-19-data/"
fi

DIR=$( echo $REPO | cut -f5 -d/ )
if [ ! -e "$DIR" ] ; then
        git clone $REPO > /dev/null 2>&1
fi
cd $DIR
git pull origin master > /dev/null 2>&1
cp us-counties.csv ../data.csv
cd ..

cat data.csv | awk -F, '
  BEGIN {
        print "{"
  }

  /202/ {
    date = $1
    county = $2
    state = $3
    fips = $4
    cases = $5
    deaths = $6

    if(stateCounty[state "," county] == 0) {
        if(states[state]) {
                states[state] = states[state] "," county
        } else {
                states[state] = county
        }
    }
    if(stateCounty[state "," county]) {
        stateCounty[state "," county] = stateCounty[state "," county] "," date
    } else {
        stateCounty[state "," county] = date
    }
    scd = "\"cases\": " cases ", \"deaths\": " deaths
    stateCountyDate[state "," county "," date] = scd
  }

  END {
        for(state in states) {
            if(snext) {print ","} else {snext=1}
            print "\t\"" state "\": {"
            split(states[state],counties)
            for(num in counties) {
                if(cnext) {print ","} else {cnext=1}
                county = counties[num]
                print"\t\t\"" county "\" : {"
                split(stateCounty[state "," county],countyDates)
                for(dindex in countyDates) {
                    if(dnext) {print ","} else {dnext=1}
                    date = countyDates[dindex]
                    print "\t\t\t\"" date "\" : {"
                    print "\t\t\t\t" stateCountyDate[state "," county "," date]
                    printf("\t\t\t}")
                }
                dnext = 0
                printf("\n\t\t}")
            }
            cnext = 0
            printf("\n\t}")
        }
        print ""
        print "}"
  }
'
