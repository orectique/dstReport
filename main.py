import streamlit as st
import pandas as pd
#import plotly.express as px

st.set_page_config(
    page_title= 'Survey Report',
    page_icon = '📊',
    layout= 'wide'
)

st.title('Report Generation')

body = st.container()

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

    number = st.number_input('Choose Aadhaar Number', min_value=1234567100, max_value = 1234567999, value = 1234567100)
    
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
        


        