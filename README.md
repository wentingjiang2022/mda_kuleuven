# Explain mortality of heatwaves - A study on Europe

The goal of the project is to investigate why some countries suffer more in heatwave than others. We define the cost of the heatwave here as the total number of deaths from the heatwave. The period of investigation is from 2003 to 2023, because ...

In order to utilize the various indicators from Eurostat, we narrow down the Europe region.

In this project, a variety of tools and libraries have been utilized to facilitate the successful execution of tasks. These tools include **Pandas** and  **NumPy** for data manipulation and analysis within the Python programming environment. Additionally, the **Matplotlib** library has been employed for visualizations. For the realm of machine learning, the project makes use of **Scikit-Learn (sklearn)** for data mining and analysis. For streamlined yet informative statistical graphics, **Seaborn** emerges as a **prominent** choice, built upon the foundations of Matplotlib. The integration of **Plotly Express** further enhances the project's visualizations by enabling the creation of interactive displays. Lastly, the **SHAP** library finds its place, introducing the capacity to interpret machine learning models.

## Table of Contents

- [Background](#project-title-and-description)
- [Folder Structures](#folder)
- [Installation](#installation)
- [Data](#data)
  - [Heatwave](#heatwave)
  - [Weather Features](#weather-features)
    - [Extracting List of Countries and Capitals](#extracting-list-of-countries-and-capitals)
  - [Eurostat Data](#eurostat-data)
- [Results and Visualizations](#results-and-visualizations)
- [Additional Documentation](#additional-documentation)
- [Project Status](#project-status)

## Background

Heatwaves create a large impact on the society.
According to xx, some important factors are relevant for the mortality, such as child, elder, etc.

## Folder Structures

```
dash_app
|-- application.py
data
|-- raw_data
|-- processed_data
notebooks
|-- data_exploration.ipynb
|-- modeling.ipynb
|-- utils
images
|-- plot1.png
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
  - utils: a folder to store Python scripts for specific tasks or functions used in the project.
  
- **images**: Contains some highlighted images in the notebooks.
  - `feature_importance.png`: Image showcasing what factors are important for the model.
  
## Installation

Explain how to set up the project environment and install any dependencies. This might involve using a `requirements.txt` file or a `conda` environment file.

## Data

Three main datasets were used for the analysis, namely, Heatwave Records, Historical Weather for different countries, and Eurostat Data that indicate the country-level social-economic information.

### Heatwave 

The heatwave information is extracted from the xx database, by filtering the range of years, geographic location, and disaster type. Some columns have incomplete information, and therefore, we limit to the most relevant columns which do not information.

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

## Results and Visualizations

### Sample

From the dynamic image below, we can see how the impact of heatwave changes over time.
![Demo GIF](images/sample.gif)

## Additional Documentation

More detailed information about the project can be assessed from the [report](https://www.overleaf.com/4741585141rpxkgzttqrvv) and the [slide deck](https://docs.google.com/presentation/d/1s_Lrp2qbuxrJJsyitHEKRXocIdoAaR0XmclfKdeL9F0/edit?usp=sharing).

## Project Status

THe project has been completed as part of the Modern Data Analytics course in academic year 2022-23 at KU Leuven. The repository is not actively maintained.
