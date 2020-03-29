
import numpy as np
from matplotlib import pyplot as plt
from scipy import stats
import pandas as pd
from ipdb import set_trace


def calc_daily_rates(daily_values):
    new_ratio = np.roll(daily_values, -1) / daily_values
    new_ratio = new_ratio[:-1]
    raw_rates = np.log(new_ratio)
    return raw_rates


def running_gmean(in_rates, n):
     n_samples = in_rates.shape[0]
     g_means = [stats.gmean(in_rates[i:i + n]) for i in range(n_samples - n + 1)]
     return np.array(g_means)


def plot_gmean_rates(cases_list, location, filename=False):
    raw_rates = calc_daily_rates(cases_list)
    #avg3 = running_gmean(raw_rates, 3)
    avg5 = running_gmean(raw_rates, 5)
    days = range(len(raw_rates))
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.plot(days, raw_rates ,c='b', label='Daily growth rates', fillstyle='none')
    #ax.plot(days[1:-1], avg3 ,c='r', label='3 day moving growth rate average', fillstyle='none')
    ax.plot(days[2:-2], avg5 ,c='g', label='5 day moving growth rate average', fillstyle='none')
    ax.set(xlabel='days', title='Geometric Moving Avg for COVID-19 Daily Case Growth Rate in ' + location)
    ax.grid()
    plt.legend(loc=2)
    if not filename:
        plt.show()
    else:
        plt.savefig(filename)



#usa_cases =

#utah_cases =

if __name__ == '__main__':
    peru_cases = [6, 7, 9, 11, 17, 22, 38, 43, 71, 86, 117,
                145, 234, 263, 318, 363, 395, 416, 480, 580, 635, 671]

    df = pd.read_csv('./us-states.csv')
    plot_gmean_rates(peru_cases, 'Peru', filename='./Plots/Peru.png')

    usa_cases = df[df['date'] >= '2020-03-01'].groupby('date')['cases'].sum()
    plot_gmean_rates(usa_cases, 'USA', filename='./Plots/USA.png')

    df = df[df['date'] >= '2020-03-01']

    for state in df['state'].unique():
        vals = df[df['state']==state].cases.to_numpy()
        plot_gmean_rates(vals, state, filename='./Plots/' + state + '.png')

    utah = df[df['state']=='Utah'].cases.to_numpy()

