# Explain mortality of heatwaves - A study on Europe

The goal of the project is to investigate why some countries suffer more in heatwave than others. We define the cost of the heatwave here as the total number of deaths from the heatwave. The period of investigation is from 1985 to 2022 due to the availability of the disaster data.

In order to utilize the various indicators from Eurostat, we narrow down the Europe region.

The deployed app on AWS can be accessed [here](http://heatwave-factors.eu-west-3.elasticbeanstalk.com/).

## Table of Contents

- [Background](#background)
- [Folder](#folder)
- [Installation](#installation)
- [Data](#data)
  - [Heatwave](#heatwave)
  - [Weather](#weather)
    - [Extracting List of Countries and Capitals](#extracting-list-of-countries-and-capitals)
  - [Eurostat Data](#eurostat-data)
- [Additional Documentation](#additional-documentation)
- [Project Status](#project-status)

## Background

Heatwaves create a large impact on the society.
According to [EarthData](https://www.earthdata.nasa.gov/learn/pathfinders/disasters/extreme-heat-data-pathfinder), some important factors are relevant for the mortality, such as child, elder, etc.

## Folder

```
dash_app
|-- application.py
|-- random_forest_model.pkl
|-- (CSV files for web app go here, but not listed explicitly)
data
|-- raw_data
|-- processed_data
notebooks
|-- data_exploration.ipynb
|-- data_processing_model.ipynb
|-- prepare_web_app_data.ipynb
|-- utils
images
|-- (Images from the modelling notebook go here, but not listed explicitly)
README.md
requirements.txt
.gitignore
```
- **dash_app**: Contains the app related codes.
  
- **data**: Contains the raw and processed datasets used in the project.
  - `raw_data`: The original datasets before any preprocessing.
  - `processed_data`: The dataset after data cleaning and preprocessing.
  
- **notebooks**: Includes Jupyter notebooks for data analysis, modeling, and visualization.
  - `data_exploration.ipynb`: Notebook exploring the dataset and visualizing key insights.
  - `data_processing_model.ipynb`: Notebook containing feature generataion and machine learning model development.
  - `prepare_web_app_data.ipynb`: Notebook processing additional data to be used in the web app
  - `utils`: a folder to store Python scripts for specific tasks or functions used in the project.
  
- **images**: Contains some highlighted images in the notebooks.

## Installation

The environment can be set using a `requirements.txt` file.

## Data

Three main datasets were used for the analysis, namely, Heatwave Records, Historical Weather for different countries, and Eurostat Data that indicate the country-level social-economic information.

### Heatwave 

The heatwave information is extracted from the international disaster database [EM-DAT](https://www.emdat.be/), by filtering the range of years, geographic location, and disaster type. Some columns have incomplete information, and therefore, we limit to the most relevant columns which do not information.

### Weather 

The following resource is used to extract historical weather data from the [Open-Meteo API](https://open-meteo.com/en/docs/historical-weather-api).

#### Extracting List of Countries and Capitals

In order to match a certain country's weather information for a specific time, we used the capital city of the country to query the weather data. This has some drawbacks if the actual heatwave location is far away from the capital. However, this greatly simplifies the need for extensive data harmonization.

The list of countries and their capitals are extracted from the provided URL: [List of Countries and Capitals](http://techslides.com/list-of-countries-and-capitals).

### Eurostat Data

Here are the Eurostat sources for various indicators used in the analysis:

- **Population**: [Eurostat - Population](https://ec.europa.eu/eurostat/databrowser/view/DEMO_PJAN/default/table?lang=en)
  - CSV File: `population.csv`

- **Poverty**: [Eurostat - Poverty](https://ec.europa.eu/eurostat/databrowser/view/SDG_01_10/default/table?lang=en)
  - CSV File: `poverty.csv`

- **Housing Deprivation**: [Eurostat - Housing Deprivation](https://ec.europa.eu/eurostat/databrowser/view/SDG_11_11/default/table?lang=en)
  - CSV File: `housing_deprive.csv`

- **GDP**: [Eurostat - GDP](https://ec.europa.eu/eurostat/databrowser/view/SDG_08_10/default/table?lang=en)
  - CSV File: `gdp.csv`

- **Forest Area**: [Eurostat - Forest Area](https://ec.europa.eu/eurostat/databrowser/product/view/SDG_15_10)
  - CSV File: `forest.csv`

- **Elderly Population Percentage**: [Eurostat - Elderly Percentage](https://ec.europa.eu/eurostat/databrowser/view/TPS00028/default/table?lang=en)
  - CSV File: `elder.csv`

- **Child Population**: [Eurostat - Child Population](https://ec.europa.eu/eurostat/databrowser/view/yth_demo_010/default/table?lang=en)
  - CSV File: `population.csv`

- **Disabled Population, Assistance Needed**: [Eurostat - Disabled](https://ec.europa.eu/eurostat/databrowser/view/hlth_dpeh130/default/table?lang=en)
  - CSV File: `disabled.csv`

- **Unemployment**: [Eurostat - Unemployment](https://ec.europa.eu/eurostat/databrowser/product/view/SDG_08_40)
  - CSV File: `unemployment.csv`

## Additional Documentation

More detailed information about the project can be assessed from the [report](https://www.overleaf.com/read/rxvpzncftxkw) and the [slide deck](https://docs.google.com/presentation/d/1sA2jl_Rk2eRyNfLJIeVu0cI9nGPfiJaITWnXJ5g3eT4/edit?usp=sharing).

## Project Status

THe project has been completed as part of the Modern Data Analytics course in academic year 2022-23 at KU Leuven. The repository is not actively maintained.
