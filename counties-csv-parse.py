import json
import csv


# Open csv file
with open("us-counties.csv") as csvfile:
    csvData = csv.reader(csvfile, delimiter=",", quotechar="|")

    jsonData = {}  # create new dict to store the info
    for row in csvData:  # iterate through csv
        date = row[0]
        if (
            date != "date"
        ):  # check the contents of the date column to make sure it's not the first row
            county = row[1]
            state = row[2]
            fips = row[3]
            cases = int(row[4])
            deaths = int(row[5])
            if (
                state in jsonData.keys()
            ):  # check to see if the state exists already in the dict
                if (
                    county in jsonData[state]["counties"].keys()
                ):  # check to see if the county exists in the state already
                    dataLength = len(jsonData[state]["counties"][county]["data"])
                    previousData = jsonData[state]["counties"][county]["data"][
                        dataLength - 1
                    ]  # get the data from the previous entry for that county
                    newCases = (
                        cases - previousData["cases"]
                    )  # calculate the difference between the current and previous day for cases
                    newDeaths = (
                        deaths - previousData["deaths"]
                    )  # calculate the difference between the current and previous day for deaths
                    jsonData[state]["counties"][county]["data"].append(
                        {
                            "date": date,
                            "cases": cases,
                            "deaths": deaths,
                            "newCases": newCases,
                            "newDeaths": newDeaths,
                        }
                    )  # add the information into the data array
                else:  # if the county doesn't exist, create it
                    jsonData[state]["counties"][county] = {
                        "name": county,
                        "fips": fips,
                        "firstCase": date,
                        "data": [
                            {
                                "date": date,
                                "cases": cases,
                                "deaths": deaths,
                                "newCases": 0,
                                "newDeaths": 0,
                            }
                        ],
                    }
            else:  # if the state doesn't exist, create it
                jsonData[state] = {
                    "state": state,
                    "counties": {
                        county: {
                            "name": county,
                            "fips": fips,
                            "firstCase": date,
                            "data": [
                                {
                                    "date": date,
                                    "cases": cases,
                                    "deaths": deaths,
                                    "newCases": 0,
                                    "newDeaths": 0,
                                }
                            ],
                        }
                    },
                }
    with open("us-counties.json", "r+") as jsonfile:
        json.dump(jsonData, jsonfile)
