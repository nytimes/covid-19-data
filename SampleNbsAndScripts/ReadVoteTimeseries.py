# %%
from pandas.io.json import json_normalize 
import json
with open('timeseries.json') as f:
    vote_data = json.load(f)
vote_df = json_normalize(vote_data['timeseries'])
vote_df['trumpd.total_votes'] = round(vote_df['vote_shares.trumpd'] * vote_df['votes'])
vote_df['bidenj.total_votes'] = round(vote_df['vote_shares.bidenj'] * vote_df['votes'])

deltas = vote_df['trumpd.total_votes'][1:] - vote_df.head(len(vote_df)-1)['trumpd.total_votes'].to_numpy()[0:]
vote_df['trump_gains'] = 0
vote_df['trump_gains'][1:] = deltas

deltas = vote_df['bidenj.total_votes'][1:] - vote_df.head(len(vote_df)-1)['bidenj.total_votes'].to_numpy()[0:]
vote_df['biden_gains'] = 0
vote_df['biden_gains'][1:] = deltas


# %%
import matplotlib.pyplot as plt


totals_trump_asarray = vote_df['trumpd.total_votes'].values
totals_biden_asarray = vote_df['bidenj.total_votes'].values


fig = plt.figure(figsize=(14,10))
ax = fig.add_axes([0,0,1,1])
ax.set_xlim(0, max(vote_df.shape[0], ax.get_xlim()[1]))
ax.set_ylim(0, max(vote_df['trumpd.total_votes'].max(), ax.get_ylim()[1]))
ax.set_ylabel('Votes (in millions)')
ax.plot(totals_trump_asarray, label='Trump')
ax.plot(totals_biden_asarray, label='Biden')
ax.legend()

# %%
