from datetime import date, datetime, timedelta
import os
import math

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()
plt.rcParams.update({'font.size': 14})
plt.style.use('dark_background')


plot_states = ['Washington', 'New York', 'California', 'Massachusetts', 'Florida', 'New Jersey', 'Connecticut']
show_figure = True
save_figure = True
start_date = datetime(2020, 3, 1)
raw_usa_states_csv = os.path.abspath(os.path.join(
    os.path.dirname(__file__),
    '..',
    'output',
    'CSVs',
    'usa_state_cases.csv'
))
png_dir = os.path.abspath(os.path.join(
    os.path.dirname(__file__),
    '..',
    'output',
    'PNGs',
))

start_time = datetime.now()

print(f'\nRunning script : {os.path.abspath(__file__)}')
print(f'Start time     : {start_time}')
print(f'Showing plots  : {show_figure}')
print(f'Saving plots   : {save_figure}')

states = pd.read_csv(raw_usa_states_csv, index_col=0)
states = states.rename(columns={
    col: col.lower() for col in states.columns
})
states.date = pd.to_datetime(states.date)
states = states.sort_values(by=['state', 'date'])
states['new_cases'] = 0
states['new_deaths'] = 0

for state_name in set(states.state.values.tolist()):
    states.loc[states.state == state_name, 'new_cases'] = states.loc[states.state == state_name, 'confirmed'].diff()
    states.loc[states.state == state_name, 'new_deaths'] = states.loc[states.state == state_name, 'deaths'].diff()

df_fig1 = states.loc[(states.state.isin(plot_states)) & (states.date >= start_date)]
df_fig1 = df_fig1.set_index(['date', 'state'])

fig1, ax1 = plt.subplots(figsize=(13, 7))
df_fig1.new_deaths.unstack().plot(ax=ax1, title='COVID-19 New Deaths in Select US States', lw=2)
ax1.set_xlabel('Date')
ax1.set_ylabel('Number of Deaths')
fig1.tight_layout()

if show_figure:
    plt.show()

if save_figure:
    output_figure = os.path.join(
        png_dir,
        'usa_states_new_deaths.png'
    )
    fig = ax1.get_figure()
    fig.savefig(output_figure)
