import json
import csv


def states_parse():
    # Open file
    with open("us-states.csv") as csvfile:
        csvData = csv.reader(csvfile, delimiter=",", quotechar="|")

        jsonData = {
            "national": {
                "cases": 0,
                "deaths": 0,
                "firstCase": "",
                "firstDeath": "",
                "lastDate": "",
            },
            "states": {},
        }
        # iterate through csv
        for row in csvData:  # iterate through the rows of the csv
            date = row[0]
            if date != "date":  # check to make sure it's not the first row
                jsonData["national"]["lastDate"] = date
                state = row[1]
                fips = int(row[2])
                cases = int(row[3])
                deaths = int(row[4])

                if jsonData["national"]["cases"] == 0 and cases != 0:
                    jsonData["national"]["firstCase"] = date
                if jsonData["national"]["deaths"] == 0 and deaths != 0:
                    jsonData["national"]["firstDeath"] = date

                if (
                    state in jsonData["states"]
                ):  # if the item already exists in the dict
                    dataLength = len(jsonData["states"][state]["data"])
                    previousData = jsonData["states"][state]["data"][dataLength - 1]
                    newCases = cases - previousData["cases"]
                    newDeaths = deaths - previousData["deaths"]
                    jsonData["states"][state]["data"].append(
                        {
                            "date": date,
                            "cases": cases,
                            "deaths": deaths,
                            "newCases": newCases,
                            "newDeaths": newDeaths,
                        }
                    )
                    jsonData["states"][state]["deaths"] = deaths
                    jsonData["states"][state]["cases"] = cases
                    if (
                        "firstDeath" not in jsonData["states"][state].keys()
                        and deaths != 0
                    ):
                        jsonData["states"][state]["firstDeath"] = date

                    jsonData["national"]["cases"] = (
                        jsonData["national"]["cases"] + newCases
                    )
                    jsonData["national"]["deaths"] = (
                        jsonData["national"]["deaths"] + newDeaths
                    )

                else:  # if the item doesn't exist
                    if deaths != 0:  # if there are deaths in the first record
                        jsonData["states"][state] = {
                            "name": state,
                            "fips": fips,
                            "firstCase": date,
                            "cases": cases,
                            "firstDeath": date,
                            "deaths": deaths,
                            "data": [
                                {
                                    "date": date,
                                    "cases": cases,
                                    "deaths": deaths,
                                    "newCases": 0,
                                    "newDeaths": deaths,
                                }
                            ],
                        }
                        jsonData["national"]["cases"] = (
                            jsonData["national"]["cases"] + cases
                        )
                        jsonData["national"]["deaths"] = (
                            jsonData["national"]["deaths"] + deaths
                        )
                    else:  # if there are no deaths in the first record
                        jsonData["states"][state] = {
                            "name": state,
                            "fips": fips,
                            "firstCase": date,
                            "cases": cases,
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
                        jsonData["national"]["cases"] = (
                            jsonData["national"]["cases"] + cases
                        )

        with open("us-states.json", "r+") as jsonfile:
            json.dump(jsonData, jsonfile)
