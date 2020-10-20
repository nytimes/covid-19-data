import csv

# Utils
# -----------------------------------------------------------------------

def numeral(value):
    return f'{value:,}'

def read_csv(path, row_parser):
    with open(path) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0

        for row in csv_reader:
            if line_count == 0:
                row_parser(line_count, row)
                line_count += 1
            else:
                row_parser(line_count, row)
                line_count += 1

# States Data
# -----------------------------------------------------------------------

states = {}

def get_last_state_entry(state):
    length = len(states[state])
    if (length == 0):
        return {
            "cases_cumulative": 0,
            "deaths_cumulative": 0
        }
    else:
        return states[state][length - 1]

def intake_state_entry(index, row):
    if (index == 0):
        return

    date, state, fips, cases, deaths = row

    if state not in states:
        states[state] = []

    last_entry = get_last_state_entry(state)

    states[state].append({
        "date": date,
        "cases": int(cases) - last_entry["cases_cumulative"],
        "cases_cumulative": int(cases),
        "deaths": int(deaths) - last_entry["deaths_cumulative"],
        "deaths_cumulative": int(deaths)
    })

def intake_states():
    read_csv('./us-states.csv', intake_state_entry)

    for state in states:
        last_entry = get_last_state_entry(state)
        print(f'\n{state}')
        print(f'  as of: {last_entry["date"]}')
        print(f'  total cases: {numeral(last_entry["cases_cumulative"])}')
        print(f'  deaths: {numeral(last_entry["deaths_cumulative"])}')

# Census Data
# -----------------------------------------------------------------------

def intake_census_row(index, row):
    if index == 1 or index >= 6:
        state = row[4] # NAME
        population = int(row[16]) # POPESTIMATE2019
        print(f'{state}: {numeral(population)}')

def intake_census():
    read_csv('./rkd-us-census.csv', intake_census_row)

# Program
# -----------------------------------------------------------------------

intake_states()
intake_census()