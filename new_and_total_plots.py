from datetime import date
import os

import pandas as pd
import matplotlib.pyplot as plt
plt.rcParams.update({'font.size': 14})
plt.style.use('dark_background')


# usa_new_cases_csv = r'C:\Users\andrew\Documents\covid19\output\CSVs\usa_new_cases.csv'
raw_usa_states_csv = r'C:\Users\andrew\Documents\covid19\output\CSVs\usa.csv'
world_new_cases_csv = r'C:\Users\andrew\Documents\covid19\output\CSVs\countries_new_cases.csv'
show_figure = False
save_figure = True
start_date = date(2020, 1, 22)

raw_states = pd.read_csv(raw_usa_states_csv)
raw_states = raw_states.loc[~raw_states['Province/State'].str.contains('Princess')]

usa_new_cases = raw_states[
    ['Date', 'Confirmed', 'Recovered', 'Deaths']
].groupby('Date').sum()
usa_new_cases['NewCases'] = usa_new_cases.Confirmed.diff()

usa_new_cases['Date'] = pd.to_datetime(usa_new_cases.Date, format=r'%Y-%m-%d')
# usa_new_cases = usa_new_cases.set_index('Date')

fig1, ax1 = plt.subplots(figsize=(13, 6))
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


world_new_cases = pd.read_csv(world_new_cases_csv)
world_new_cases['Date'] = pd.to_datetime(world_new_cases.Date, format=r'%Y-%m-%d')

italy = world_new_cases.loc[world_new_cases['Country'] == 'Italy']
italy = pd.concat([
    italy,
    pd.DataFrame([[
        start_date, 'Italy', 0, 0, 0, 0
    ]],
    columns=['Date', 'Country', 'Confirmed', 'Deaths', 'NewCases', 'Recovered'])
])
italy['Date'] = pd.to_datetime(italy.Date)
italy = italy.sort_values(by='Date')

fig2, ax2 = plt.subplots(figsize=(13, 6))
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
fig3, ax3 = plt.subplots(figsize=(13, 6))
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