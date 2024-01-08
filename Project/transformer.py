import os
import sys
import time
import json
import requests
import pandas as pd
from selenium import webdriver
import numpy as np
from geopy.geocoders import Nominatim
from geopy.distance import geodesic


def Transformer(data):
    data = pre_processing_precise_location(data)
    data = pre_processing_distance_from_city_center(data)
    data = pre_processing_asking_price(data)
    data['asking_price_per_million'] = ''
    data['asking_price_per_million'] = data['asking_price'] / 1000000
    data.drop(['asking_price'],axis=1,inplace=True)
    data = pre_processing_typeProperty(data)
    data = pre_rpocessing_typeOfForm(data)
    data = pre_processing_type(data)
    data = pre_processing_rooms(data)
    data = pre_processing_size(data)
    data = pre_processing_tomtarea(data)
    data['size'] = data['size'] / 100
    data['tomtarea'] = data['tomtarea'] / 10000
    data = pre_processing_bisize(data)
    data['bisize'] = data['bisize'] / 100
    data = preprocessing_cost(data)
    data['cost_per_year_x1000'] = ''
    data['cost_per_year_x1000'] = data['cost']
    data['cost_per_year_x1000'] = data['cost_per_year_x1000'] / 1000
    data.drop(['cost'],axis=1,inplace=True)
    data = pre_processing_buildarea(data)
    data['buildArea'] = data['buildArea'] / 1000
    data.rename(columns={'size': 'size_x100'}, inplace=True)
    data.rename(columns={'bisize': 'bisize_x100'}, inplace=True)
    data.rename(columns={'tomtarea': 'tomtarea_x10000'}, inplace=True)
    data.rename(columns={'year': 'year_x1000'}, inplace=True)
    data.fillna(0, inplace=True)
    i = 0
    if((data['size_x100']).iloc[i] != 0) or (data['bisize_x100'].iloc[i] != 0):
        data['price_per_m2'].iloc[i] = data['asking_price_per_million'].iloc[i]*1000000 / (data['size_x100'].iloc[i]*100 + data['bisize_x100'].iloc[i]*100)   
    data['price_per_m2_x10000'] = ''
    data['price_per_m2_x10000'] = data['price_per_m2'] / 10000
    data.drop(['price_per_m2'],axis=1,inplace=True)
    data = pre_processing_uteplats(data)
    data = pre_processing_balkong(data)
    data = pre_processing_elevator(data)
    data = pre_processing_floor(data)
    data = pre_processing_transform(data)
    print(data.head())
    return data
    


def get_coordinates(location_name):
    geolocator = Nominatim(user_agent="my_geocoder")
    location = geolocator.geocode(location_name)
    if location:
        return location.latitude, location.longitude
    else:
        return None
def calculate_distance(origin, destination):
    origin_coords = get_coordinates(origin)
    destination_coords = get_coordinates(destination)
    if origin_coords and destination_coords:
        distance = geodesic(origin_coords, destination_coords).kilometers
        return distance
    else:
        return None
    
def pre_processing_precise_location(row_example):
    row_example['precise_location'] = ''
    c = row_example['area'].iloc[0]
    c = c.split(' ')
    c = c[0] + ' ' + c[1] + ' ' + c[2]
    row_example['precise_location'] = c
    row_example.drop(['area'], axis = 1, inplace = True)
    return row_example

def pre_processing_distance_from_city_center(row_example):    
    row_example['precise_location'] 
    row_example['distance_from_city_center'] = ''
    i = 0
    #divide row_example dataframe in 25 different dataframes
    a = calculate_distance(row_example['precise_location'].iloc[i], 'Stockholm, Sweden')
    if(a != None):
        row_example['distance_from_city_center'].iloc[i] = a
    if(a == None):
        a = calculate_distance(row_example['precise_location'].iloc[i], 'Stockholm, Sweden')
        if(a != None):
            row_example['distance_from_city_center'].iloc[i] = a
        if(a == None):
            d = row_example['precise_location'].iloc[i]
            d = d.replace('/', ' ')
            a = calculate_distance(d, 'Stockholm, Sweden')
            if(a != None):
                row_example['distance_from_city_center'].iloc[i] = a
            if(a == None):
                d = d.split(' ')
                x = ''
                for c in range(len(d)):
                    if c == 0:
                        continue
                    x = x + d[c] + ' '
                a = calculate_distance(x, 'Stockholm, Sweden')
                if(a != None):
                    row_example['distance_from_city_center'].iloc[i] = a
                elif(a == None):
                    a = row_example['precise_location'].iloc[i]
                    a = a.split(' ')
                    a = a[-2:]
                    a = a[0] + ' ' + a[1]
                    distance = calculate_distance(a, 'Stockholm, Sweden')
                    print('iteration' + ' ' , i)
                    if(distance == None):
                        row_example['distance_from_city_center'].iloc[i] = 'not found'
                    else:
                        row_example['distance_from_city_center'].iloc[i] = distance
    return row_example

def pre_processing_asking_price(row_example):
    i = 0
    a = row_example['asking_price'].iloc[i]
    a = a.replace('\xa0','')
    a = a.replace('kr','')
    row_example['asking_price'].iloc[i] = float(a)
    return row_example

def pre_processing_typeProperty(row_example):
    lookup_table = pd.read_csv("./lookups/lookup_table_typeProperty.csv")
    i = 0
    a = row_example['typeProperty'].iloc[i]
    row_example['typeProperty'].iloc[i] = lookup_table[lookup_table['typeProperty'] == a]['code'].iloc[0]
    return row_example

def pre_rpocessing_typeOfForm(row_example):
    lookup_table = pd.read_csv("./lookups/lookup_table_typeOfForm.csv")
    i = 0
    a = row_example['typeOfForm'].iloc[i]
    row_example['typeOfForm'].iloc[i] = lookup_table[lookup_table['typeOfForm'] == a]['code'].iloc[0]
    return row_example

def pre_processing_type(row_example):
    lookup_table = pd.read_csv("./lookups/lookup_table_type.csv")
    i = 0
    match row_example['typeProperty'].iloc[i]:
        case '0':
            row_example['type'] = '2'
        case '1':
            row_example['type'] = '2'
        case '2':
            row_example['type'] = '2'
        case '4':
            row_example['type'] = '1'
        case '5':
            row_example['type'] = '0'
        case '6':
            row_example['type'] = '0'
        case '7':
            row_example['type'] = '0'
        case '8':
            row_example['type'] = '3'
        case '9':
            row_example['type'] = '3'
    return row_example

def pre_processing_rooms(row_example):
    i = 0
    b = 0
    c = row_example['rooms'].iloc[i]
    # if c is an integer then do nothing
    if isinstance(c, int):
        b = 1
    else:
        c = c.replace(',','.')
        c = c.replace('rum','')
    row_example['rooms'].iloc[i] = float(c)
    return row_example

def pre_processing_size(row_example):
    i = 0
    a = row_example['size'].iloc[i]
    if isinstance(a, int):
        b = 0
    else:
        a = a.replace(',','.')
        a = a.replace('\xa0','')
        a = a.replace('m²','')
    row_example['size'].iloc[i] = float(a)
    return row_example

def pre_processing_tomtarea(row_example):
    i = 0
    a = row_example['tomtarea'].iloc[i]
    print(a)
    if isinstance(a, float):
        b = 0
    elif isinstance(a, int):
        b = 0
    elif('ha' in a):
        a = a.replace(',','.')
        a = a.replace('\xa0','')
        a = a.replace('ha','')
        a = float(a) * 10000
    else:
        a = a.replace(',','.')
        a = a.replace('\xa0','')
        a = a.replace(' ','')
        a = a.replace('m²','')
        print(a)
    if(a == 'N/A'):
        a = 0
    row_example['tomtarea'].iloc[i] = float(a)
    return row_example

def pre_processing_bisize(row_example):
    i = 0
    a = row_example['bisize'].iloc[i]
    if isinstance(a, float):
        b = 0
    elif isinstance(a, int):
        b = 0
    elif('ha' in a):
        a = a.replace(',','.')
        a = a.replace('\xa0','')
        a = a.replace('ha','')
        a = float(a) * 10000
    else:
        a = a.replace(',','.')
        a = a.replace('\xa0','')
        a = a.replace(' ','')
        a = a.replace('m²','')
    if(a == 'N/A'):
        a = 0
    row_example['bisize'].iloc[i] = float(a)
    return row_example

def preprocessing_cost(row_example):
    i = 0
    a = row_example['cost'].iloc[i]
    if isinstance(a, float):
        b = 0
    elif isinstance(a, int):
        b = 0
    else:
        a = a.replace(',','.')
        a = a.replace('\xa0','')
        a = a.replace('kr/år','')
    
    row_example['cost'].iloc[i] = float(a)
    return row_example

def pre_processing_buildarea(row_example):
    i = 0
    e = row_example['buildArea'].iloc[i]
    if isinstance(e, int):
        b = 0
    elif isinstance(e, float):
        b = 0
    for j in range(1900, 2024):
        intermediate = str(j)
        a = 0
        if intermediate in e:
            e = str(j)
            e = float(e)
            a = 1
            break
    if (a == 0):
        for k in range(0, 100):
            intermediate = str(k)
            if intermediate in e:
                if k < 50:
                    e = '19' + '0' + str(k)
                    e = float(e)
                    break
                else:
                    e = '19' + str(k)
                    e = float(e)
                    break
    if isinstance(e, str):
        e = 0
    row_example['buildArea'].iloc[i] = float(e)
    return row_example

def pre_processing_uteplats(row_example):
    i = 0
    a = row_example['uteplats'].iloc[i]
    if (a != 0):
        a = 1
    row_example['uteplats'].iloc[i] = a
    return row_example

def pre_processing_balkong(row_example):
    i = 0
    a = row_example['balkong'].iloc[i]
    if (a != 'Nej'):
        a = 1
    else:
        a = 0
    row_example['balkong'].iloc[i] = a
    return row_example

def pre_processing_elevator(row_example):
    row_example['elevator'] = ''
    i = 0
    for i in range(len(row_example['floor'])):
        a = row_example['floor'].iloc[i]
        if isinstance(a, int):
            continue
        elif isinstance(a, float):
            continue
        elif isinstance(a, np.int64):
            continue
        if(('hiss finns ej' in a) or ('hiss fins ej' in a)):
            a = 0
            row_example['elevator'].iloc[i] = a
            a = row_example['floor'].iloc[i].replace('hiss finns ej','')
            row_example['floor'].iloc[i] = a
        elif('hiss finns' in a) or ('hiss fins' in a):
            a = 1
            row_example['elevator'].iloc[i] = a
            a = row_example['floor'].iloc[i].replace('hiss finns','')
            row_example['floor'].iloc[i] = a
        else:
            a = 0
            row_example['elevator'].iloc[i] = a
    return row_example

def pre_processing_floor(row_example):
    i = 0
    for i in range(len(row_example['floor'])):
        a = row_example['floor'].iloc[i]
        if isinstance(a, int):
            continue
        elif isinstance(a, float):
            continue
        elif isinstance(a, np.int64):
            continue
        c = a.split('av')
        c[0] = c[0].replace(',','')
        if(len(c) == 2):
            c[1] = c[1].replace(',','')
            a = float(c[0])
            b = float(c[1])
            a = a / b
            a = float(a)
        row_example['floor'].iloc[i] = a
    return row_example

def pre_processing_transform(row_example):
    #remove any commas or strings from the whole dataframe

    row_example = row_example.replace(',','.', regex=True)
    row_example = row_example.replace(' ','', regex=True)
    row_example = row_example.replace('m²','', regex=True)
    row_example = row_example.replace('kr','', regex=True)
    row_example = row_example.replace('rum','', regex=True)
    row_example = row_example.replace('ha','', regex=True)
    row_example = row_example.replace('år','', regex=True)
    row_example = row_example.replace('av','', regex=True)
    row_example = row_example.replace('hiss finns ej','', regex=True)
    row_example = row_example.replace('hiss finns','', regex=True)
    row_example = row_example.replace('hiss fins ej','', regex=True)
    row_example = row_example.replace('hiss fins','', regex=True)
    row_example = row_example.replace('Nej','', regex=True)
    row_example = row_example.replace('Ja','', regex=True)

    #change all strings to zeros
    row_example = row_example.replace('',0, regex=True)

    #remove everything that is string
    row_example = row_example.apply(pd.to_numeric, errors='coerce')
    #filling all the nan values with zeros
    row_example = row_example.fillna(0)
    row_example.drop(['precise_location'],axis=1,inplace=True)
    return row_example
