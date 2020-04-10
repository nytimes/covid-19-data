import json
import csv


def states_population_parse():
    # Open file

    with open("states_population.csv") as csvfile:
        csvData = csv.reader(csvfile, delimiter=",", quotechar="|")

        jsonData = {}
        # iterate through csv
        for row in csvData:  # iterate through the rows of the csv
            fips = int(row[0])
            state = row[1]
            census = int(row[2])
            estimated = int(row[3])
            jsonData[state] = {"name": state, "census": census, "estimated": estimated}

    with open("state-population.json", "r+") as jsonfile:
        json.dump(jsonData, jsonfile)


states_population_parse()
