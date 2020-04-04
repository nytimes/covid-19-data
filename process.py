import json

from states_csv_parse import states_parse
from counties_csv_parse import counties_parse

#  this is a small function that will take the json files, put them into two objects, and put the objects into a javascript file.


def move_convert():
    states_parse()
    counties_parse()
    with open("us-states.json", "r") as statesJSON:
        statesData = json.load(statesJSON)
        statesJSON.close()
        statesStr = str(statesData)
        with open("us-counties.json", "r") as countiesJSON:
            countiesData = json.load(countiesJSON)
            countiesJSON.close()
            countyStr = str(countiesData)

            fileData = (
                "export const states ="
                + str(statesData)
                + "; export const counties = "
                + countyStr
            )

            with open("./app/js/data.js", "w") as dataFile:
                dataFile.write(fileData)
                dataFile.close()


move_convert()
