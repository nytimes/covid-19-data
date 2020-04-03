import plotly.express as px
import numpy as np
import pandas as pd


# load us states into df
file = "us-states.csv"
df = pd.read_csv(file)
df.head()

# create MN df
df_MN = df.loc[(df["state"] == "Minnesota")]

df_MN.head(5)


# import plotly.express as px
# fig = px.bar(df_MN, x='date', y='cases')
# fig.show()

