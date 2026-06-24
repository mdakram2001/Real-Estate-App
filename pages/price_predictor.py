import streamlit as st
import pandas as pd
import numpy as np
import pickle

st.set_page_config(page_title="Real Housing")

with open('datasets/df.pkl', 'rb') as file:
    df = pickle.load(file)
with open('datasets/pipeline.pkl', 'rb') as file:
    pdf = pickle.load(file)


st.header("Estimate the Price")

property_type = st.selectbox('Property Type', ['flat', 'house'])
sector = st.selectbox("Sector", sorted(df['sector'].unique().tolist()))
bedroom = float(st.selectbox("No. of Bedrooms", sorted(df['bedRoom'].unique().tolist())))
bathroom = float(st.selectbox("No. of Bathrooms", sorted(df['bathroom'].unique().tolist())))
balcony = st.selectbox("No. of Balconies", sorted(df['balcony'].unique().tolist()))
property_age = st.selectbox("Property Age", sorted(df['agePossession'].unique().tolist()))
area = float(st.number_input("Built Up Area"))
servant_room = float(st.selectbox("Servant Room", [0.0 , 1.0]))
store_room = float(st.selectbox("Store Room", [0.0 , 1.0]))
furnishing_type = st.selectbox("Furnishing Type", sorted(df['furnishing_type'].unique().tolist()))
luxury_category = st.selectbox("Luxury Category", sorted(df['luxury_category'].unique().tolist()))
floor_category = st.selectbox("Floor Categoty", sorted(df['floor_category'].unique().tolist()))


if st.button("Estimate"):
    columns = ['property_type', 'sector', 'bedRoom', 'bathroom', 'balcony', 'agePossession', 'built_up_area', 'servant room', 'store room','furnishing_type', 'luxury_category', 'floor_category']
    data = [[property_type, sector, bedroom, bathroom, balcony, property_age, area, servant_room, store_room, furnishing_type, luxury_category, floor_category]]

    df = pd.DataFrame(data, columns=columns)

    base_price = np.expm1(pdf.predict(df))[0]
    low = round(base_price - 0.22, 2)
    high = round(base_price + 0.22 , 2)

    st.text("The price should be between {} Cr and {} Cr".format(low, high))