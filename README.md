# Explain mortality of heatwaves - Europe study

The goal of the project is to investigate why some countries suffer more in heatwave than others. We define the cost of the heatwave here as the total number of deaths from the heatwave. The period of investigation is from 2003 to 2023, because ...

In order to utilize the various indicators from Eurostat, we narrow down the Europe region.

Here are some of the key tools and libraries that were used in this project:
- **Pandas**: Data manipulation and analysis library in Python.
- **Matplotlib**: Data visualization library for creating static, interactive, and animated visualizations.
- **NumPy**: Fundamental package for scientific computing with Python.
- **Scikit-Learn (sklearn)**: Machine learning library that provides simple and efficient tools for data mining and data analysis.
- **Seaborn**: Data visualization library based on Matplotlib, offering a high-level interface for creating informative and attractive statistical graphics.
- **Plotly Express**: A library for creating interactive visualizations in Python.
- **SHAP**: A Python library for SHapley Additive exPlanations - a unified framework for interpreting machine learning models.

## Table of Contents

- [Background](#project-title-and-description)
- [Folder Structure](#folder)
- [Installation](#installation)
- [Usage](#usage)
- [Data](#data)
  - [Heatwave](#heatwave)
  - [Weather Features](#weather-features)
    - [Extracting List of Countries and Capitals](#extracting-list-of-countries-and-capitals)
  - [Eurostat Data](#eurostat-data)
- [Features](#features)
- [Results and Visualizations](#results-and-visualizations)
- [Additional Documentation](#additional-documentation)
- [Project Status](#project-status)

## Background

Heatwaves create a large impact on the society.
According to xx, some important factors are relevant for the mortality, such as child, elder, etc.

## Folder Structure
Folder Structure Visualization:

```
data
|-- raw_data.csv
|-- cleaned_data.csv
notebooks
|-- data_exploration.ipynb
|-- modeling.ipynb
scripts
|-- data_preprocessing.py
|-- model_evaluation.py
images
|-- plot1.png
docs
|-- project_summary.pdf
configs
|-- config.yaml
README.md
requirements.txt
.gitignore
```

Here's an overview of the folder structure of this data science project:
- **data**: Contains the raw and processed datasets used in the project.
  - `raw_data.csv`: The original dataset before any preprocessing.
  - `cleaned_data.csv`: The dataset after data cleaning and preprocessing.
  
- **notebooks**: Includes Jupyter notebooks for data analysis, modeling, and visualization.
  - `data_exploration.ipynb`: Notebook exploring the dataset and visualizing key insights.
  - `modeling.ipynb`: Notebook containing machine learning model development.
  
- **scripts**: Stores Python scripts for specific tasks or functions used in the project.
  - `data_preprocessing.py`: Script containing data preprocessing functions.
  - `model_evaluation.py`: Script for evaluating model performance.
  
- **images**: Contains images and visualizations used in the README and notebooks.
  - `plot1.png`: Image showcasing a key visualization.
  
- **docs**: Additional documentation related to the project, if applicable.
  - `project_summary.pdf`: Project summary and key findings.
  
- **configs**: Configuration files or settings used in the project.
  - `config.yaml`: Configuration settings for model hyperparameters.
  
- `README.md`: The main README file that provides an overview of the project.
- `requirements.txt`: List of required Python packages for reproducing the environment.
- `.gitignore`: Specifies files and directories to be ignored by version control.

## Installation

Explain how to set up the project environment and install any dependencies. This might involve using a `requirements.txt` file or a `conda` environment file.

## Usage

Describe how to use your project. If it's a library or tool, provide code examples or usage instructions. If it's an analysis or model, explain how to run the code and interpret the results.

## Data

If your project uses specific datasets, provide information about the data sources, how to obtain the data, and any data preprocessing steps.

### Heatwave 


### Weather Features

The following resource is used to extract historical weather data from the [Open-Meteo API](https://open-meteo.com/en/docs/historical-weather-api).

#### Extracting List of Countries and Capitals

This section explains how to extract a list of countries and their capitals from the provided URL: [List of Countries and Capitals](http://techslides.com/list-of-countries-and-capitals).

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

- **Child Population**: [Eurostat - Child Population](https://ec.europa.eu/eurostat/databrowser/view/yth_demo_010/default/table?lang=en)

- **Disabled Population, Assistance Needed**: [Eurostat - Disabled](https://ec.europa.eu/eurostat/databrowser/view/hlth_dpeh130/default/table?lang=en)

- **Unemployment**: [Eurostat - Unemployment](https://ec.europa.eu/eurostat/databrowser/product/view/SDG_08_40)
- 
## Features

Describe the main features of your project. For a data science project, this could include descriptions of the models, algorithms, or analyses you've conducted.

## Results and Visualizations

Include examples of any key results, visualizations, or insights generated by your project. You can include images, graphs, or links to notebooks.

### Sample

![Demo GIF](SampleGIFImage_40kbmb.gif)

## Additional Documentation

More detailed information about the project can be assessed from the [report](https://www.overleaf.com/4741585141rpxkgzttqrvv) and the [slide deck](https://docs.google.com/presentation/d/1s_Lrp2qbuxrJJsyitHEKRXocIdoAaR0XmclfKdeL9F0/edit?usp=sharing).

## Project Status

THe project has been completed as part of the Modern Data Analytics coursea at KU Leuven. The repository is not actively maintained.
