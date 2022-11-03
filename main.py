import streamlit as st
import pandas as pd
#import plotly.express as px
import json
import time
import base64
import requests
import numpy as np
import streamlit as st
import plotly.express as px
import matplotlib.pyplot as plt
import plotly.graph_objects as go
from plotly.subplots import make_subplots

st.set_page_config(
    page_title= 'Survey Report',
    page_icon = '📊',
    layout= 'wide'
)

st.title('Report Generation')

body = st.container()

def fetch_FoodGroups():
    url = 'http://115.243.144.151/seed/fetchAllFood.php'
    data_fetched = json.loads(requests.post(url).text)
    data_dict = data_fetched['datalist']
    food_df = pd.DataFrame.from_dict(data_dict)
    food_df.to_csv('data/Dietary.csv', index=False,
                   header=['Aadhaar', 'Date', 'Grains', 'Pulses', 'otherFruits', 'leafy_Vegetables','other_veg', 'Milk', 'Animal', 'Vitamin_A','Nuts', 'Eggs', 'junk'])

def fetch_Anthropometric():
    url = 'http://115.243.144.151/seed/fetchAllAnthropometric.php'
    data_fetched = json.loads(requests.post(url).text)
    data_dict = data_fetched['datalist']
    food_df = pd.DataFrame.from_dict(data_dict)
    food_df.to_csv('data/Anthropometric.csv', index=False,
                   header=['Aadhaar', 'Month', 'Gender', 'Age', 'Height', 'Weight', 'BodyFat', 'MidArm', 'BMI', 'BMR'])


def fetch_Biochemical():
    url = 'http://115.243.144.151/seed/fetchAllBiochemical.php'
    data_fetched = json.loads(requests.post(url).text)
    data_dict = data_fetched['datalist']
    food_df = pd.DataFrame.from_dict(data_dict)
    food_df.to_csv('data/Biochemical.csv', index=False,
                   header=['Aadhaar', 'Month', 'Haemoglobin'])


def fetch_Clinical():
    url = 'http://115.243.144.151/seed/fetchAllClinical.php'
    data_fetched = json.loads(requests.post(url).text)
    data_dict = data_fetched['datalist']
    food_df = pd.DataFrame.from_dict(data_dict)
    food_df.to_csv('data/Clinical.csv', index=False,
                   header=['Aadhaar', 'Month', 'NeckPatches', 'PaleSkin', 'Pellagra', 'WrinkledSkin',
                           'TeethDiscolouration', 'BleedingGums', 'Cavity', 'WeakGums', 'AngularCuts',
                           'InflammedTongue', 'LipCuts', 'MouthUlcer',
                           'BitotSpot', 'Xeropthalmia', 'RedEyes', 'Catract',
                           'HairFall', 'DamagedHair', 'SplitEnds', 'Discolouration',
                           'DarkLines', 'SpoonShapedNails', 'BrokenNails', 'PaleNails','lean','bony','goitre','obesity'])



fetch_FoodGroups()
fetch_Anthropometric()
fetch_Biochemical()
fetch_Clinical()

data1 = pd.read_csv('data/Anthropometric.csv')
data2 = pd.read_csv('data/Dietary.csv')
data3 = pd.read_csv('data/Clinical.csv')
data4 = pd.read_csv('data/Biochemical.csv')

data1['Month Log'] = data1['Month'].apply(lambda x: 'Month 1' if x == '1-2022' else ('Month 2' if x == '2-2022' else None))

data3['Month Log'] = data3['Month'].apply(lambda x: 'Month 1' if x == '1-2022' else ('Month 2' if x == '2-2022' else None))

data4['Month Log'] = data4['Month'].apply(lambda x: 'Month 1' if x == '1-2022' else ('Month 2' if x == '2-2022' else None))

data1.to_csv('data/Anthropometric_Month.csv', index=False)
data3.to_csv('data/Clinical_Month.csv', index=False)
data4.to_csv('data/Biochemical_Month.csv', index=False)

data2['Date'] = pd.to_datetime(data2['Date'], infer_datetime_format=True)
data2['Month'] = data2['Date'].apply(lambda x: 'Month ' + str(x.month - 6))
data2['Day'] = data2['Date'].apply(lambda x: x.day)
data2.to_csv('data/Dietary_Month.csv', index=False)

anthropometric = pd.read_csv('data/Anthropometric_Month.csv')
bioChem = pd.read_csv('data/Biochemical_Month.csv')
clinical = pd.read_csv('data/Clinical_Month.csv')
dietary = pd.read_csv('data/Dietary_Month.csv')




diseases = ['NeckPatches', 'PaleSkin', 'Pellagra',
       'WrinkledSkin', 'TeethDiscolouration', 'BleedingGums', 'Cavity',
       'WeakGums', 'AngularCuts', 'InflammedTongue', 'LipCuts', 'MouthUlcer',
       'BitotSpot', 'Xeropthalmia', 'RedEyes', 'Catract', 'HairFall',
       'DamagedHair', 'SplitEnds', 'Discolouration', 'DarkLines',
       'SpoonShapedNails', 'BrokenNails', 'PaleNails', 'lean', 'bony',
       'goitre', 'obesity']

foods = ['Grains', 'Pulses', 'otherFruits',
       'leafy_Vegetables', 'other_veg', 'Milk', 'Animal', 'Vitamin_A', 'Nuts',
       'Eggs', 'junk']

def foodsTable(month, number):
    dictFood = {}
    table = dietary[(dietary['Aadhaar'] == number) & (dietary['Month'] == month)]
    for food in foods:
        dictFood[food] = [sum(table[food]), len(table), sum(table[food])*100/len(table)]

    df = pd.DataFrame(dictFood, index = ['Days Consumed', 'Days Observed', 'Percentage of Days']).transpose()
    df = df[df['Percentage of Days'] != 0]

    return df


with body:

    number = st.number_input('Choose Aadhaar Number', min_value=1234567100, max_value = 999999999999, value = 1234567100)
    
    if st.button('Generate Report'):
        st.subheader('Report for Aadhaar Number ' + str(number))

        st.write('### Anthropometric Data')

        st.write(anthropometric[anthropometric['Aadhaar'] == number][['Gender', 'Age', 'Height', 'Weight', 'BodyFat', 'MidArm', 'BMI', 'BMR', 'Month Log']].reset_index(drop=True))

        st.write('### Biochemical Data')

        st.write(bioChem[bioChem['Aadhaar'] == number][['Haemoglobin', 'Month Log']].reset_index(drop=True))

        st.write('### Clinical Data')

        st.write('Month 1')
        diseases1 = [disease for disease in diseases if clinical[(clinical['Aadhaar'] == number) & (clinical['Month Log'] == 'Month 1')][disease].reset_index(drop = True)[0] == 1]
        st.write(['None' if len(diseases1) == 0 else i for i in diseases1]) 

        st.write('Month 2')
        diseases2 = [disease for disease in diseases if clinical[(clinical['Aadhaar'] == number) & (clinical['Month Log'] == 'Month 2')][disease].reset_index(drop = True)[0] == 1]
        st.write(['None' if len(diseases2) == 0 else i for i in diseases2])

        st.write('### Dietary Data')
        
        st.write('###### Only food groups consumed are displayed. Absence of group in table implies that it was not consumed in that period.')

        st.write('Month 1')
        st.write(foodsTable('Month 1', number))

        st.write('Month 2')
        st.write(foodsTable('Month 2', number))
        


        
