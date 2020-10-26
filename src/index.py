import csv
#
# Utils
# -----------------------------------------------------------------------

def numeral(value):
    return f'{value:,}'

def read_csv(path, row_parser):
    """Reads a CSV file from path with a method to intake rows"""
    output = {}

    with open(path) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        index = 0

        for row in csv_reader:
            if index != 0:
                row_parser(index, row, output)
            index += 1

    return output

# States Data
# -----------------------------------------------------------------------

def intake_state_row(index, row, states):
    date, state, fips, cases, deaths = row

    if state not in states:
        states[state] = [
            {
                "cases_cumulative": 0,
                "deaths_cumulative": 0
            }
        ]

    last_entry = states[state][-1]

    states[state].append({
        "date": date,
        "cases": int(cases) - last_entry["cases_cumulative"],
        "cases_cumulative": int(cases),
        "deaths": int(deaths) - last_entry["deaths_cumulative"],
        "deaths_cumulative": int(deaths)
    })

def intake_states():
    states = read_csv('./us-states.csv', intake_state_row)

    with open('./processed/us-states.csv', 'w', newline='\n') as csvfile:
        writer = csv.writer(csvfile, delimiter=',',
                                quotechar='|', quoting=csv.QUOTE_MINIMAL)
        writer.writerow(('state', 'date', 'cases', 'cases_cumulative', 'deaths', 'deaths_cumulative'))

        for state in states:
            del states[state][0]

            for day in states[state]:
                date, cases, cases_cumulative, deaths, deaths_cumulative = day.values()
                writer.writerow((state, date, cases, cases_cumulative, deaths, deaths_cumulative))

# Census Data
# -----------------------------------------------------------------------

def intake_census_row(index, row, output):
    if index == 1 or index >= 6:
        state = row[4] # NAME
        population = int(row[16]) # POPESTIMATE2019
        print(f'{state}: {numeral(population)}')

def intake_census():
    read_csv('./rkd-us-census.csv', intake_census_row)

# Program
# -----------------------------------------------------------------------

if __name__ == "__main__":
    intake_states()
    # intake_census()