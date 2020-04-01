import json
import csv


# Open file
with open("us-states.csv") as csvfile:
    csvData = csv.reader(csvfile, delimiter=",", quotechar="|")

    with open("us-states.json", "r+") as jsonfile:
        jsonData = json.load(jsonfile)
        jsonfile.close()
        # iterate through csv
        for row in csvData:
            date = row[0]
            if date != "date":
                state = row[1]
                fips = int(row[2])
                cases = int(row[3])
                deaths = int(row[4])
                if fips in jsonData.keys():
                    dataLength = len(jsonData[state]["data"])
                    previousData = jsonData[state]["data"][dataLength - 1]
                    newCases = cases - previousData["cases"]
                    newDeaths = deaths - previousData["deaths"]
                    jsonData[state]["data"].append(
                        {
                            "date": date,
                            "cases": cases,
                            "deaths": deaths,
                            "newCases": newCases,
                            "newDeaths": newDeaths,
                        }
                    )
                else:
                    jsonData[state] = {
                        "name": state,
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
        with open("us-states.json", "r+") as jsonfile:
            json.dump(jsonData, jsonfile)
