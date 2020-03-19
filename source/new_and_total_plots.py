from datetime import date, datetime
import os

import pandas as pd
import matplotlib.pyplot as plt

from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()
plt.rcParams.update({'font.size': 14})
plt.style.use('dark_background')


raw_usa_states_csv = r'C:\Users\andrew\Documents\covid19\output\CSVs\usa.csv'
world_new_cases_csv = r'C:\Users\andrew\Documents\covid19\output\CSVs\countries_new_cases.csv'
show_figure = False
save_figure = True
start_date = date(2020, 1, 22)

start_time = datetime.now()

print(f'\nRunning script : {os.path.abspath(__file__)}')
print(f'Start time     : {start_time}')
print(f'Showing plots  : {show_figure}')
print(f'Saving plots   : {save_figure}')

# Prepare US cases from state data
raw_states = pd.read_csv(raw_usa_states_csv)
raw_states = raw_states.loc[~raw_states['Province/State'].str.contains('Princess')]

usa_new_cases = raw_states[
    ['Date', 'Confirmed', 'Recovered', 'Deaths']
].groupby('Date').sum()

usa_new_cases['NewCases'] = usa_new_cases.Confirmed.diff()

usa_new_cases = usa_new_cases.reset_index()
usa_new_cases['Date'] = pd.to_datetime(usa_new_cases.Date)

usa_new_cases = usa_new_cases[usa_new_cases.Date >= pd.Timestamp(start_date)]

# USA Cases
fig1, ax1 = plt.subplots(figsize=(13, 7))
bar_container = ax1.bar(usa_new_cases.Date, usa_new_cases.NewCases, color='#feffb3')
line = ax1.plot(usa_new_cases.Date, usa_new_cases.Confirmed, color='#fa8174')
ax1.legend(
    (line[0], bar_container[0]), ('Confirmed Cases', 'New Cases'),
    loc='upper left'
)
plt.title('New and Confirmed COVID-19 Cases in the USA')
ax1.set_xlabel('Date')
ax1.set_ylabel('Number of Cases')
fig1.tight_layout()

if show_figure:
    plt.show()

if save_figure:
    png_path = os.path.abspath(os.path.join(
        os.path.dirname(raw_usa_states_csv),
        '..',
        'PNGs',
        'usa_new_and_confirmed.png'
    ))
    fig1.savefig(png_path)

# USA max possible cases assumming 86% undiagnosed cases
max_estimate = usa_new_cases.Confirmed + usa_new_cases.Confirmed * 0.86
fig1, ax1 = plt.subplots(figsize=(13, 7))
poly_container = ax1.fill_between(
    usa_new_cases.Date,
    usa_new_cases.Confirmed, max_estimate,
    color='#fa8174', alpha=0.25
)
bar_container = ax1.bar(usa_new_cases.Date, usa_new_cases.NewCases, color='#feffb3')
confirmed_line = ax1.plot(usa_new_cases.Date, usa_new_cases.Confirmed, color='orange')
max_line = ax1.plot(usa_new_cases.Date, max_estimate, color='red')
ax1.legend(
    (confirmed_line[0], max_line[0], poly_container, bar_container[0]),
    ('Confirmed Cases', 'Estimated Cases (Includes Undiagnosed)', 'Possible Total Cases Range', 'Confirmed New Cases'),
    loc='upper left'
)
plt.title('New, Confirmed, and Possible COVID-19 Cases in the USA')
ax1.set_xlabel('Date')
ax1.set_ylabel('Number of Cases')
fig1.tight_layout()

if show_figure:
    plt.show()

if save_figure:
    png_path = os.path.abspath(os.path.join(
        os.path.dirname(raw_usa_states_csv),
        '..',
        'PNGs',
        'usa_new_and_confirmed_estimated.png'
    ))
    fig1.savefig(png_path)


# Italy cases
world_new_cases = pd.read_csv(world_new_cases_csv)
world_new_cases['Date'] = pd.to_datetime(world_new_cases.Date, format=r'%Y-%m-%d')

italy = world_new_cases.loc[world_new_cases['Country'] == 'Italy']
italy = pd.concat(
    [
        italy,
        pd.DataFrame([[
            start_date, 'Italy', 0, 0, 0, 0
        ]],
        columns=['Date', 'Country', 'Confirmed', 'Deaths', 'NewCases', 'Recovered'])
    ],
    sort=True
)
italy['Date'] = pd.to_datetime(italy.Date)
italy = italy[italy.Date >= pd.Timestamp(start_date)]
italy = italy.sort_values(by='Date')

fig2, ax2 = plt.subplots(figsize=(13, 7))
italy_bar_container = ax2.bar(italy.Date, italy.NewCases, color='#feffb3')
italy_line = ax2.plot(italy.Date, italy.Confirmed, color='#fa8174')
ax2.legend(
    (line[0], bar_container[0]), ('Confirmed Cases', 'New Cases'),
    loc='upper left'
)
plt.title('New and Confirmed COVID-19 Cases in Italy')
ax2.set_xlabel('Date')
ax2.set_ylabel('Number of Cases')
fig2.tight_layout()

if show_figure:
    plt.show()

if save_figure:
    png_path = os.path.abspath(os.path.join(
        os.path.dirname(raw_usa_states_csv),
        '..',
        'PNGs',
        'italy_new_and_confirmed.png'
    ))
    fig2.savefig(png_path)


## Italy and US on same plot
fig3, ax3 = plt.subplots(figsize=(13, 7))
italy_bars = ax3.bar(italy.Date, italy.NewCases, color='#fa8174')
italy_lines = ax3.plot(italy.Date, italy.Confirmed, color='#fa8174')

usa_bars = ax3.bar(usa_new_cases.Date, usa_new_cases.NewCases, color='#81b1d2')
usa_lines = ax3.plot(usa_new_cases.Date, usa_new_cases.Confirmed, color='#81b1d2')
ax3.legend(
    (italy_lines[0], italy_bars[0], usa_lines[0], usa_bars[0]),
    ('Italy Confirmed Cases', 'Italy New Cases', 'USA Confirmed Cases', 'USA New Cases'),
    loc='upper left'
)
plt.title('New and Confirmed COVID-19 Cases in Italy and the USA')
ax3.set_xlabel('Date')
ax3.set_ylabel('Number of Cases')
fig3.tight_layout()

if show_figure:
    plt.show()

if save_figure:
    png_path = os.path.abspath(os.path.join(
        os.path.dirname(raw_usa_states_csv),
        '..',
        'PNGs',
        'italy_usa_new_and_confirmed.png'
    ))
    fig3.savefig(png_path)

end_time = datetime.now()
print(f'\nScript completed : {end_time}')
print(f'Run time         : {end_time-start_time}')
