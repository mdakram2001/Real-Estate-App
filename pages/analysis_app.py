import streamlit as st
import pandas as pd
import plotly_express as px
import pickle
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(page_title="Plots Analysis")
st.title("Analytics")

df = pd.read_csv("datasets/dataviz_1.csv")
feature_text = pickle.load(open("datasets/feature_text.pkl", "rb"))

group_df =df.groupby("sector").mean(numeric_only=True)[['price','price_per_sqft','built_up_area','latitude','longitude']]

fig = px.scatter_map(group_df, lat="latitude", lon="longitude", color="price_per_sqft", size="built_up_area", color_continuous_scale=px.colors.cyclical.IceFire, zoom=10, map_style="open-street-map")

st.plotly_chart(fig,use_container_width=True)

st.header("Word Cloud")

wordcloud = WordCloud(width = 800, height = 800, 
                      background_color ='white', 
                      stopwords = set(['s']),  # Any stopwords you'd like to exclude
                      min_font_size = 10).generate(feature_text)

fig = plt.figure(figsize = (8, 8), facecolor = None) 
plt.imshow(wordcloud, interpolation='bilinear') 
plt.axis("off") 
plt.tight_layout(pad = 0) 
st.pyplot(fig)


st.header("Area vs Price")
property_type = st.selectbox("Select Property Type", ['flat', 'house'])
if property_type == 'flat':
    fig1 = px.scatter(df[df['property_type'] == 'flat'], x="built_up_area", y="price", color="bedRoom")
    st.plotly_chart(fig1,use_container_width=True)
else:
    fig1 = px.scatter(df[df['property_type'] == 'house'], x="built_up_area", y="price", color="bedRoom")
    st.plotly_chart(fig1,use_container_width=True)


st.header("BHK Pie Chart")
sector = st.selectbox("Select Sector", df['sector'].unique().tolist())
fig2 = px.pie(df[df['sector'] == sector], names='bedRoom', title='Pie Chart')
st.plotly_chart(fig2,use_container_width=True)


st.header("BHK Price Comparision")
fig3 = px.box(df[df["bedRoom"]<=4], x='bedRoom', y='price')
st.plotly_chart(fig3,use_container_width=True)



st.header("Side by Side Distribution")
fig4 = plt.figure(figsize=(10,4))
sns.histplot(
    df[df["property_type"] == 'house']['price'],
    kde=True,
    label='House'
)
sns.histplot(
    df[df["property_type"] == 'flat']['price'],
    kde=True,
    label='Flat'
)
plt.legend()
st.pyplot(fig4)