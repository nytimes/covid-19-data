import csv
#
# Utils
# -----------------------------------------------------------------------

def numeral(value):
    return f'{value:,}'

def read_csv(path, row_parser):
    """Reads a CSV file from path with a method to process rows"""
    output = {}

    with open(path) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        # index = 0

        for index, row in enumerate(csv_reader):
            if index != 0:
                row_parser(index, row, output)
            # index += 1

    return output

# States Data
# -----------------------------------------------------------------------

def process_states():
    states = read_csv('./us-states.csv', process_state_row)

    with open('./processed/us-states.csv', 'w', newline='\n') as csvfile:
        writer = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        writer.writerow(('state', 'date', 'cases', 'cases_cumulative', 'deaths', 'deaths_cumulative'))

        for state in states:
            del states[state][0]

            for day in states[state]:
                date, cases, cases_cumulative, deaths, deaths_cumulative = day.values()
                writer.writerow((state, date, cases, cases_cumulative, deaths, deaths_cumulative))

def process_state_row(index, row, output):
    date, state, fips, cases, deaths = row

    if state not in output:
        output[state] = [
            {
                "cases_cumulative": 0,
                "deaths_cumulative": 0
            }
        ]

    last_entry = output[state][-1]

    output[state].append({
        "date": date,
        "cases": int(cases) - last_entry["cases_cumulative"],
        "cases_cumulative": int(cases),
        "deaths": int(deaths) - last_entry["deaths_cumulative"],
        "deaths_cumulative": int(deaths)
    })

# Census Data
# -----------------------------------------------------------------------

def process_census():
    populations = read_csv('./rkd-us-census.csv', process_census_row)

    with open('./processed/us-state-populations.csv', 'w', newline='\n') as csvfile:
        writer = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        writer.writerow(('state', 'population'))

        for state in populations:
            print(f'{state}: {numeral(populations[state])}')
            writer.writerow((state, populations[state]))

def process_census_row(index, row, output):
    if index == 1 or index >= 6:
        state = row[4] # NAME
        population = int(row[16]) # POPESTIMATE2019
        output[state] = population

# Program
# -----------------------------------------------------------------------

if __name__ == "__main__":
    process_states()
    process_census()