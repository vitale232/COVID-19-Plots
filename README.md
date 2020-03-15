# About

This repo is just some quick plots I threw together regarding [COVID-19](https://www.health.ny.gov/diseases/communicable/coronavirus/), which is commonly referred to as Coronavirus in the USA.

The true heroes here are the fine folks at Johns Hopkins that have an awesome [dashboard](https://gisanddata.maps.arcgis.com/apps/opsdashboard/index.html#/bda7594740fd40299423467b48e9ecf6) and a [GitHub Repo](https://github.com/CSSEGISandData/COVID-19) of all their data.

# Figures

The figures below are generated in the `./parse_and_plot.py` file. Python was managed using Anaconda. The conda env is output to the `./environment.yml` file.

There is a distinction in these figures between "Total Cases" and "New Cases". **Total cases** is the total number of confirmed cases of COVID-19 for the reporting area as of a given date. The **new cases** are newly identified cases in the reporting area as of a given date.

## New and Total Cases USA and Italy

### USA and Italy

![Total New and Confirmed Cases of COVID-19 in the USA and Italy](./output/PNGs/italy_usa_new_and_confirmed.png?raw=true "Total New and Confirmed Cases of COVID-19 in the USA and Italy")

### USA
![Total New and Confirmed Cases of COVID-19 in USA](./output/PNGs/usa_new_and_confirmed.png?raw=true "Total New and Confirmed Cases of COVID-19 in USA")

### Italy
![Total New and Confirmed Cases of COVID-19 in Italy](./output/PNGs/italy_new_and_confirmed.png?raw=true "Total New and Confirmed Cases of COVID-19 in Italy")

## Total Cases

![Total Cases of COVID-19 in select US States](./output/PNGs/usa_hot_spots.png?raw=true "Total Cases of COVID-19 in select US States")

![Total confirmed, recovered, and fatal cases of COVID-19 in the USA](./output/PNGs/usa.png?raw=true "Total confirmed, recovered, and fatal cases of COVID-19 in the USA")

## New Cases

![New cases of COVID-19 in select countries](./output/PNGs/countries_new_cases.png?raw=true "New cases of COVID-19 in select countries")

![New cases of COVID-19 in select US States](./output/PNGs/states_new_cases.png?raw=true "New cases of COVID-19 in select US States")

![New cases of COVID-19 in China and the USA](./output/PNGs/usa_china_new_cases.png?raw=true "New cases of COVID-19 in China and the USA")
