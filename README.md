# About

This repo is just some quick plots I threw together regarding [COVID-19](https://www.health.ny.gov/diseases/communicable/coronavirus/), which is commonly referred to as Coronavirus in the USA.

The true heroes here are the fine folks at Johns Hopkins that have an awesome [dashboard](https://gisanddata.maps.arcgis.com/apps/opsdashboard/index.html#/bda7594740fd40299423467b48e9ecf6) and a [GitHub Repo](https://github.com/CSSEGISandData/COVID-19) of all their data.

# Figures

There is a distinction in these figures between "Total Cases" and "New Cases". **Total cases** is the total number of confirmed cases of COVID-19 for the reporting area as of a given date. The **new cases** are newly identified cases in the reporting area as of a given date.

The figures below are generated and published in the `./source/automate_make_plots.py` script. Python was managed using Anaconda. The conda env is output to the `./environment.yml` file.

## New and Total Cases USA and Italy

### USA and Italy Cases

![Total New and Confirmed Cases of COVID-19 in the USA and Italy](./output/PNGs/italy_usa_new_and_confirmed.png?raw=true "Total New and Confirmed Cases of COVID-19 in the USA and Italy")

### USA and Italy Deaths

![New and Total COVID-19 Fatalities in Italy and the USA](./output/PNGs/italy_usa_new_and_confirmed_fatalities.png?raw=true "New and Total COVID-19 Fatalities in Italy and the USA")


### USA
![Total New and Confirmed Cases of COVID-19 in USA](./output/PNGs/usa_new_and_confirmed.png?raw=true "Total New and Confirmed Cases of COVID-19 in USA")

There is an early edition article published in *Science*, which estimates undiagnosed cases in China were about 86%.

> "This estimate reveals a very high rate of undocumented infections: 86%. 
> This finding is independently corroborated by the infection rate among foreign 
> nationals evacuated from Wuhan (see supplementary materials)" [Source: Ruiyun Li et al., 2020](https://science.sciencemag.org/content/early/2020/03/13/science.abb3221)

Given the lack of effective COVID-19 testing in the United States, I've made a gross assumption that the same rate of undiagnosed infections could exist in the USA. This is what that looks like:

![New, Confirmed, and Possible COVID-19 Cases in the USA](./output/PNGs/usa_new_and_confirmed_estimated.png?raw=true "New, Confirmed, and Possible COVID-19 Cases in the USA")

Hopefully the United States will start to get a better handle on the testing situation across the country. As that happens, we would expect the total number of cases and new cases to increase daily, but we would also expect the percentage of undiagnosed cases to decrease. To simulate this potential phenomenon, the following graph applies an 86% undocumented infection rate up until 3/19/2020. From that date on, the rate of undocumented infections is decreased by once percentage point.

|    Date    | Rate of Undiagnosed Infections |
|------------|--------------------------------|
| 2020-03-18 | 86%                            |
| 2020-03-19 | 86%                            |
| 2020-03-20 | 85%                            |
| 2020-03-21 | 84%                            |
| 2020-03-22 | 83%                            |
| ...        | ...                            |
| 2020-04-01 | 73%                            |
| ...        | ...                            |
| 2020-06-01 | 0%                             |

*This linear improvement in the rate of undiagnosed infections is not based on any literature, but rather is more of a thought experiment.*

Applying those rates of undiagnosed infections produces the following estimate:

![New, Confirmed, and Possible COVID-19 Cases in the USA Assuming Linear Increase, Descrease in Unidentified Cases](./output/PNGs/usa_new_and_confirmed_estimated_diminishing.png?raw=true "New, Confirmed, and Possible COVID-19 Cases in the USA Assuming Linear Improvement in Testing")

The testing story is still quite complicated across the US. This graphy assumes a linear increase and decrease in undiagnosed cases.

![New, Confirmed, and Possible COVID-19 Cases in the USA Assuming Linear Improvement in Testing](./output/PNGs/usa_new_and_confirmed_estimated_increase_decrease.png?raw=true "New, Confirmed, and Possible COVID-19 Cases in the USA Assuming Linear Increase, Descreas in Testing")

### Italy
![Total New and Confirmed Cases of COVID-19 in Italy](./output/PNGs/italy_new_and_confirmed.png?raw=true "Total New and Confirmed Cases of COVID-19 in Italy")

## Total Cases

![Total Cases of COVID-19 in select US States](./output/PNGs/usa_hot_spots.png?raw=true "Total Cases of COVID-19 in select US States")

![Total confirmed, recovered, and fatal cases of COVID-19 in the USA](./output/PNGs/usa.png?raw=true "Total confirmed, recovered, and fatal cases of COVID-19 in the USA")

## New Cases

![New cases of COVID-19 in select countries](./output/PNGs/countries_new_cases.png?raw=true "New cases of COVID-19 in select countries")

![New cases of COVID-19 in select US States](./output/PNGs/states_new_cases.png?raw=true "New cases of COVID-19 in select US States")

![New cases of COVID-19 in China and the USA](./output/PNGs/usa_china_new_cases.png?raw=true "New cases of COVID-19 in China and the USA")

## New Deaths

![New deaths from COVID-19 in select US States](./output/PNGs/usa_states_new_deaths.png?raw=true "New deaths from COVID=-19 in select US States")
