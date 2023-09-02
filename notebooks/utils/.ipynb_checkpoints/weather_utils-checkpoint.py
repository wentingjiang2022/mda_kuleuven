#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import requests
import pandas as pd
import calendar

def query_temperatures(lat, lon, start_date, end_date):
    url = "https://archive-api.open-meteo.com/v1/archive"
    
    params = {
        "latitude": lat,
        "longitude": lon,
        "start_date": start_date.strftime('%Y-%m-%d'),
        "end_date": end_date.strftime('%Y-%m-%d'),
        "daily": "temperature_2m_max",
        "timezone": "Europe/Berlin"
    }
    
    response = requests.get(url, params=params)

    if response.status_code == 200:
        data = response.json()
        temperatures = data.get('daily', {}).get('temperature_2m_max', [])[:-1]
        return temperatures
    else:
        print("Request failed with status code:", response.status_code)
        return []

def count_temperatures_above_threshold(temperatures, threshold):
    count = 0
    for temp in temperatures:
        if temp > threshold:
            count += 1
    return count

def create_country_coordinates_dict(capitals, two_to_three_iso, relevant_iso):
    df_capitals = pd.DataFrame(capitals)
    df_capitals_eu = df_capitals[df_capitals['ContinentName'] == 'Europe']

    df_capitals_eu['ISO'] = df_capitals_eu['CountryCode'].map(two_to_three_iso)

    df_coordinates = df_capitals_eu[~df_capitals_eu['ISO'].isna()][['CapitalLatitude', 'CapitalLongitude', 'ISO']]

    df_coordinates_filtered = df_coordinates[df_coordinates['ISO'].isin(relevant_iso)]
    country_dict = df_coordinates_filtered.set_index('ISO').to_dict(orient='index')
    return country_dict

def create_dates(row):
    year = row['Start Year']
    month = int(row['Start Month'])
    _, last_day = calendar.monthrange(year, month)
    
    start_date = pd.to_datetime(f'{year}-{month:02d}-01')
    end_date = pd.to_datetime(f'{year}-{month:02d}-{last_day:02d}')
    
    return start_date, end_date

