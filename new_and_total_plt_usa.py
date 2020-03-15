import os

import pandas as pd
import matplotlib.pyplot as plt
plt.rcParams.update({'font.size': 14})
plt.style.use('dark_background')


usa_new_cases_csv = r'C:\Users\andrew\Documents\covid19\output\CSVs\usa_new_cases.csv'
show_figure = True
save_figure = True

usa_new_cases = pd.read_csv(usa_new_cases_csv)
usa_new_cases['Date'] = pd.to_datetime(usa_new_cases.Date, format=r'%Y-%m-%d')
# usa_new_cases = usa_new_cases.set_index('Date')

fig, ax = plt.subplots(figsize=(13, 6))
bar_container = ax.bar(usa_new_cases.Date, usa_new_cases.NewCases, color='#feffb3')
line = ax.plot(usa_new_cases.Date, usa_new_cases.Confirmed, color='#fa8174')
ax.legend(
    (line[0], bar_container[0]), ('Confirmed Cases', 'New Cases'),
    loc='upper left'
)
plt.title('New and Confirmed COVID-19 Cases in the USA')
ax.set_xlabel('Date')
ax.set_ylabel('Number of Cases')
fig.tight_layout()

if show_figure:
    plt.show()

if save_figure:
    png_path = os.path.abspath(os.path.join(
        os.path.dirname(usa_new_cases_csv),
        '..',
        'PNGs',
        'usa_new_and_confirmed.png'
    ))
    fig.savefig(png_path)
