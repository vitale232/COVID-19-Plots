from datetime import date, datetime
import os
import re

import matplotlib.pyplot as plt
plt.rcParams.update({'font.size': 14})
plt.style.use('dark_background')
import pandas as pd

from abbreviations import state_abbreviations


plot_states = ['Washington', 'New York', 'California', 'Massachusetts', 'Florida']
plot_countries = ['USA', 'France', 'Germany', 'Canada', 'South Korea', 'Italy']
countries_start_date = date(2020, 2, 19)
daily_reports_dir = r'C:\Users\andrew\Documents\covid19\data\COVID-19\csse_covid_19_data\csse_covid_19_daily_reports'
output_csv = r'C:\Users\andrew\Documents\covid19\output\CSVs\usa.csv'
save_figure = True
show_figure = False
save_all_new_cases = True

csv_dir = os.path.dirname(output_csv)
if not os.path.exists(csv_dir):
    os.makedirs(csv_dir)

png_dir = os.path.join(
    os.path.dirname(os.path.dirname(output_csv)),
    'PNGs'
)

if not os.path.exists(png_dir):
    os.makedirs(png_dir)

cummulative_output_csv = os.path.join(
    csv_dir,
    os.path.basename(output_csv).replace('.csv', '_cases.csv')
)

# Loop through the CSV directory and grab each CSV with a date
date_regex = re.compile(r'^\d{2}-\d{2}-\d{4}.csv$')
daily_csvs = os.listdir(daily_reports_dir)
countries = pd.DataFrame([[]])
for csv in daily_csvs:
    if not date_regex.match(csv):
        print(f'Skipping {csv}')
        continue
    print(f'Processing {csv}')
    
    # Subset the countries of potential interest. Likely to change
    df = pd.read_csv(os.path.join(daily_reports_dir, csv))
    daily_countries = df.loc[df['Country/Region'].isin([
        'US', 'China', 'Mainland China', 'Germany',
        'France', 'Italy', 'Canada', 'South Korea'
    ])].copy()
    cases_date = datetime.strptime(csv.replace('.csv', ''), r'%m-%d-%Y').date()
    daily_countries['Date'] = cases_date
    if not daily_countries.empty:
        countries = countries.append(daily_countries)

usa = countries.loc[countries['Country/Region'] == 'US']
china = countries.loc[countries['Country/Region'].isin(['China', 'Mainland China'])]
france = countries.loc[countries['Country/Region'] == 'France']
germany = countries.loc[countries['Country/Region'] == 'Germany']
italy = countries.loc[countries['Country/Region'] == 'Italy']
canada = countries.loc[countries['Country/Region'] == 'Canada']
south_korea = countries.loc[countries['Country/Region'] == 'South Korea']

usa.to_csv(output_csv)

# Examine the US cases. Zero start out to appease Jamie
zero_start = pd.DataFrame(
    [
        [datetime(2020, 1, 10).date(), 0, 0, 0],
        [datetime(2020, 1, 21).date(), 0, 0, 0],
    ],
    columns=['Date', 'Confirmed', 'Deaths', 'Recovered',]
).set_index(keys='Date')

usa_cases = usa[['Date', 'Confirmed', 'Deaths', 'Recovered']].groupby(['Date']).sum().append(zero_start)
usa_cases.sort_index()
usa_cases.to_csv(cummulative_output_csv)

ax = usa_cases.plot(figsize=(13, 7), title='COVID-19 in the USA', lw=2)
ax.set_xlabel('Date')
ax.set_ylabel('Number of Cases')

if save_figure:
    output_figure = os.path.join(
        png_dir,
        os.path.basename(output_csv).replace('.csv', '.png')
    )
    fig = ax.get_figure()
    fig.savefig(output_figure)

if show_figure:
    plt.show()


# Select out all of the US states. Province/Region is formatted all kinds of ways,
# so try to get the State Name or SN abbreviation, and transform it to a State Name
## Plot 5 hottest US states as of today
usa_by_state = usa.copy()
split_state = usa['Province/State'].str.split(', ', expand=True).values.tolist()
state = []
for row in split_state:
    if all(map(pd.isnull, row)):
        state.append(None)
        continue
    elif any(map(pd.isnull, row)):
        state.append(row[0])
    else:
        try:
            row = [val.strip() for val in row]
            row = [val.replace('.', '') for val in row]
            state.append(state_abbreviations[row[1]])
        except Exception as exc:
            try:
                if re.search(r'princess', row[1].lower()):
                    state.append('Diamond Princess')
                else:
                    state.append(None)
            except Exception as exc2:
                print(f'EXCEPTION : {type(exc2).__name__} : ROW: {row}')
                state.append(None)

usa_by_state['State'] = state
usa_by_state.dropna(inplace=True)
usa_by_state = usa_by_state.loc[~usa_by_state['Province/State'].str.contains('Princess')]

state_cases_group = usa_by_state[
    ['Date', 'Confirmed', 'Recovered', 'Deaths', 'State']
].groupby(['Date', 'State']).sum()

state_cases = state_cases_group.reset_index()
state_cases.to_csv(os.path.join(
    csv_dir,
    'usa_state_cases.csv'
))

hot_spots = state_cases.loc[
    state_cases['State'].isin(plot_states), ['Date', 'Confirmed', 'State']
].groupby(['Date', 'State']).sum()
state_cases.to_csv(os.path.join(
    csv_dir,
    'usa_hot_spots.csv'
))

fig2, hotspot_ax2 = plt.subplots(figsize=(13, 7))
hot_spots.unstack().plot(ax=hotspot_ax2, title='COVID-19 in Select US States', lw=2)
hotspot_ax2.set_xlabel('Date')
hotspot_ax2.set_ylabel('Number of Cases')
fig2.tight_layout()

if show_figure:
    plt.show()

if save_figure:
    hotspot_figure = os.path.join(
        png_dir,
        'usa_hot_spots.csv'.replace('.csv', '.png')
    )
    hotspotfig = hotspot_ax2.get_figure()
    hotspotfig.savefig(hotspot_figure)


## New Cases by state
state_dfs = [
    state_cases.loc[state_cases['State'] == state][['Date', 'State', 'Confirmed', 'Recovered', 'Deaths']]
    for state in state_cases.State.unique()
]

new_cases_dfs = []
for state_df in state_dfs:
    state_df['NewCases'] = state_df.Confirmed.diff()
    new_cases_dfs.append(state_df)

new_cases = pd.concat(new_cases_dfs)
new_cases_csv = os.path.join(
    csv_dir,
    'states_new_cases.csv'
)
if save_all_new_cases:
    new_cases.to_csv(new_cases_csv, index=False)
else:
    new_cases.loc[new_cases.State.isin(plot_states)].to_csv(new_cases_csv, index=False)

new_cases = new_cases.loc[new_cases.State.isin(plot_states)].set_index(['Date', 'State'])[['NewCases']]
new_cases_fig, new_cases_ax = plt.subplots(figsize=(13, 7))
new_cases.unstack().plot(ax=new_cases_ax, title='New COVID-19 Cases in Select States', lw=2)
new_cases_ax.set_xlabel('Date')
new_cases_ax.set_ylabel('Number of New Cases')
new_cases_fig.tight_layout()

if show_figure:
    plt.show()

if save_figure:
    new_cases_png = os.path.join(
        png_dir,
        os.path.basename(new_cases_csv).replace('.csv', '.png')
    )
    new_cases_fig = new_cases_ax.get_figure()
    new_cases_fig.savefig(new_cases_png)


## New cases for the US
usa_new_cases = usa[['Date', 'Confirmed', 'Recovered', 'Deaths']].groupby('Date').sum()
usa_new_cases['NewCases'] = usa_new_cases.Confirmed.diff()

usa_new_cases_csv = os.path.join(
    csv_dir,
    'usa_new_cases.csv'
)
usa_new_cases.to_csv(usa_new_cases_csv)

usa_new_cases = usa_new_cases[['NewCases']]
usa_new_cases_fig, usa_new_cases_ax = plt.subplots(figsize=(13, 7))
usa_new_cases.plot(ax=usa_new_cases_ax, title='New COVID-19 Cases in USA', lw=2, color='red')
usa_new_cases_ax.set_xlabel('Date')
usa_new_cases_ax.set_ylabel('Number of New Cases')
usa_new_cases_fig.tight_layout()

if show_figure:
    plt.show()

if save_figure:
    usa_new_cases_png = os.path.join(
        png_dir,
        'usa_new_cases.png'
    )
    usa_new_cases_fig = usa_new_cases_ax.get_figure()
    usa_new_cases_fig.savefig(usa_new_cases_png)

# China/US new cases. China is a few orders of magnitude higher (or reported as such),
# so this graphs not super useful unless you can interact via matplotlib
china_new_cases = china[['Date', 'Confirmed', 'Recovered', 'Deaths']].groupby('Date').sum()
china_new_cases['NewCases'] = china_new_cases.Confirmed.diff()

china_new_cases['Country'] = 'China'
usa_new_cases['Country'] = 'USA'

usa_china_new_cases = pd.concat([
    usa_new_cases.reset_index(),
    china_new_cases.reset_index()
]).set_index([
    'Date', 'Country'
])

usa_china_new_cases_csv = os.path.join(
    csv_dir,
    'usa_china_new_cases.csv'
)
usa_china_new_cases.to_csv(usa_china_new_cases_csv)

usa_china_new_cases = usa_china_new_cases[['NewCases']]
usa_china_new_cases_fig, usa_china_new_cases_ax = plt.subplots(figsize=(13, 7))
usa_china_new_cases.unstack().plot(ax=usa_china_new_cases_ax, title='New COVID-19 Cases in Select Countries', lw=2)
usa_china_new_cases_ax.set_xlabel('Date')
usa_china_new_cases_ax.set_ylabel('Number of New Cases')
usa_china_new_cases_fig.tight_layout()

if show_figure:
    plt.show()

if save_figure:
    usa_china_new_cases_png = os.path.join(
        png_dir,
        os.path.basename(usa_china_new_cases_csv).replace('.csv', '.png')
    )
    usa_china_new_cases_fig = usa_china_new_cases_ax.get_figure()
    usa_china_new_cases_fig.savefig(usa_china_new_cases_png)


# Compare the new cases for the countries idenfied in `plot_countries`
france_new_cases = france[['Date', 'Confirmed', 'Recovered', 'Deaths']].groupby('Date').sum()
france_new_cases['NewCases'] = france_new_cases.Confirmed.diff()

germany_new_cases = germany[['Date', 'Confirmed', 'Recovered', 'Deaths']].groupby('Date').sum()
germany_new_cases['NewCases'] = germany_new_cases.Confirmed.diff()

italy_new_cases = italy[['Date', 'Confirmed', 'Recovered', 'Deaths']].groupby('Date').sum()
italy_new_cases['NewCases'] = italy_new_cases.Confirmed.diff()

canada_new_cases = canada[['Date', 'Confirmed', 'Recovered', 'Deaths']].groupby('Date').sum()
canada_new_cases['NewCases'] = canada_new_cases.Confirmed.diff()

south_korea_new_cases = south_korea[['Date', 'Confirmed', 'Recovered', 'Deaths']].groupby('Date').sum()
south_korea_new_cases['NewCases'] = south_korea_new_cases.Confirmed.diff()


france_new_cases['Country'] = 'France'
usa_new_cases['Country'] = 'USA'
germany_new_cases['Country'] = 'Germany'
italy_new_cases['Country'] = 'Italy'
canada_new_cases['Country'] = 'Canada'
south_korea_new_cases['Country'] = 'South Korea'

countries_new_cases = pd.concat([
    usa_new_cases.reset_index(),
    france_new_cases.reset_index(),
    germany_new_cases.reset_index(),
    italy_new_cases.reset_index(),
    canada_new_cases.reset_index(),
    south_korea_new_cases.reset_index(),
    china_new_cases.reset_index(),
])
countries_new_cases = countries_new_cases.loc[
    countries_new_cases.Country.isin(plot_countries)
]
countries_new_cases = countries_new_cases.loc[
    countries_new_cases.Date >= countries_start_date
]
countries_new_cases = countries_new_cases.set_index(['Date', 'Country'])

countries_new_cases_csv = os.path.join(
    csv_dir,
    'countries_new_cases.csv'
)
countries_new_cases.to_csv(countries_new_cases_csv)

countries_new_cases = countries_new_cases[['NewCases']]
countries_new_cases_fig, countries_new_cases_ax = plt.subplots(figsize=(13, 7))
countries_new_cases.unstack().plot(
    ax=countries_new_cases_ax,
    title='New COVID-19 Cases in Select Countries',
    lw=2
)
countries_new_cases_ax.set_xlabel('Date')
countries_new_cases_ax.set_ylabel('Number of New Cases')
countries_new_cases_fig.tight_layout()

if show_figure:
    plt.show()

if save_figure:
    countries_new_cases_png = os.path.join(
        png_dir,
        os.path.basename(countries_new_cases_csv).replace('.csv', '.png')
    )
    countries_new_cases_fig = countries_new_cases_ax.get_figure()
    countries_new_cases_fig.savefig(countries_new_cases_png)
