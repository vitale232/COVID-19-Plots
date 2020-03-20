from datetime import date, datetime, timedelta
import os
import math

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
diminish_date = date(2020, 3, 19)

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

# Trail off the 86% number by 1% each day after diminish_date to simulate increased testing
usa_new_cases = usa_new_cases.reset_index()
zero_days = timedelta(0)
usa_new_cases['Date'] = usa_new_cases.Date.dt.date

days_since = usa_new_cases.Date - diminish_date
days_since[days_since < zero_days] = zero_days
adjustment_percent = days_since.apply(lambda x: 0.86 - (int(x.days) * 0.01))
new_max_estimate = usa_new_cases.Confirmed + usa_new_cases.Confirmed * adjustment_percent


fig1, ax1 = plt.subplots(figsize=(13, 7))
poly_container = ax1.fill_between(
    usa_new_cases.Date,
    usa_new_cases.Confirmed, new_max_estimate,
    color='#fa8174', alpha=0.25
)
bar_container = ax1.bar(usa_new_cases.Date, usa_new_cases.NewCases, color='#feffb3')
confirmed_line = ax1.plot(usa_new_cases.Date, usa_new_cases.Confirmed, color='orange')
max_line = ax1.plot(usa_new_cases.Date, new_max_estimate, color='red')
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
        'usa_new_and_confirmed_estimated_diminishing.png'
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
italy['Date'] = italy.Date.dt.date
italy = italy.loc[italy.Date > date(2020, 1, 25)]
usa = usa_new_cases.copy()
usa = usa.loc[usa.Date > date(2020, 1, 25)]

fig3, ax3 = plt.subplots(figsize=(13, 7))
usa_lines = ax3.plot(usa.Date, usa.Confirmed, color='#81b1d2')
italy_lines = ax3.plot(italy.Date, italy.Confirmed, color='#fa8174')

# The US overtook italy in new cases on 3/19/2020. Iterate through
# the dates and draw the bigger new cases value on the bottom
for day in italy.Date.tolist():
    italy_new_day = italy.loc[italy.Date == day].NewCases.values[0]
    usa_new_day = usa.loc[usa.Date == day].NewCases.values[0]

    if italy_new_day > usa_new_day:
        italy_zorder = 5 # force to bottom
        usa_zorder = 10  # force to top
    else:
        usa_zorder = 5    # force to top
        italy_zorder = 10 # force to bottom

    italy_bars = ax3.bar(day, italy_new_day, color='#fa8174', zorder=italy_zorder)
    usa_bars = ax3.bar(day, usa_new_day, color='#81b1d2', zorder=usa_zorder)

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
print(f'Run time         : {end_time-start_time}\n')
