from datetime import date
import os

import pandas as pd
import matplotlib.pyplot as plt
plt.rcParams.update({'font.size': 14})
plt.style.use('dark_background')


usa_new_cases_csv = r'C:\Users\andrew\Documents\covid19\output\CSVs\usa_new_cases.csv'
world_new_cases_csv = r'C:\Users\andrew\Documents\covid19\output\CSVs\countries_new_cases.csv'
show_figure = False
save_figure = True
start_date = date(2020, 1, 22)

usa_new_cases = pd.read_csv(usa_new_cases_csv)
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
        os.path.dirname(usa_new_cases_csv),
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
        os.path.dirname(usa_new_cases_csv),
        '..',
        'PNGs',
        'italy_new_and_confirmed.png'
    ))
    fig2.savefig(png_path)