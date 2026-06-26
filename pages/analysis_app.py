import streamlit as st
import pandas as pd
import plotly.express as px
import pickle
from wordcloud import WordCloud
import matplotlib.pyplot as plt

# 1. Page Configuration
st.set_page_config(
    page_title="Gurgaon Real Estate Analytics",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. Inject CSS Style for Premium Dashboard
st.markdown("""
<style>
    /* Custom Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', sans-serif;
    }
    
    /* Header Styling */
    .header-title {
        font-size: 2.8rem;
        font-weight: 800;
        background: linear-gradient(135deg, #3B82F6 0%, #10B981 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.25rem;
        padding-top: 1rem;
    }
    
    .header-subtitle {
        color: #6B7280;
        font-size: 1.1rem;
        margin-bottom: 2rem;
        font-weight: 400;
    }
    
    /* Section Headings */
    .section-title {
        font-size: 1.25rem;
        font-weight: 700;
        color: #1F2937;
        margin-bottom: 1.2rem;
        padding-bottom: 0.4rem;
        border-bottom: 2px solid #E5E7EB;
    }
    
    /* Metric Card Custom Styling */
    [data-testid="metric-container"] {
        background-color: #FFFFFF;
        border: 1px solid #E5E7EB;
        padding: 1.25rem;
        border-radius: 12px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05), 0 2px 4px -1px rgba(0, 0, 0, 0.03);
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }
    
    [data-testid="metric-container"]:hover {
        transform: translateY(-2px);
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.08), 0 4px 6px -2px rgba(0, 0, 0, 0.04);
        border-color: #3B82F6;
    }
</style>
""", unsafe_allow_html=True)

# 3. Cache and Load Data assets
@st.cache_data
def load_data():
    dataframe = pd.read_csv("datasets/dataviz_1.csv")
    feat_text = pickle.load(open("datasets/feature_text.pkl", "rb"))
    return dataframe, feat_text

try:
    df, feature_text = load_data()
except Exception as e:
    st.error(f"Failed to load dashboard dataset: {e}")
    st.stop()

# 4. Sidebar Panel
with st.sidebar:
    st.markdown("### 📈 Analytics Dashboard")
    st.info("""
    Explore market trends, spatial valuations, BHK distributions, and key features in the Gurgaon real estate market.
    """)
    st.markdown("""
    **🔍 Data Scope:**
    - Records: **3,329** listings
    - Columns: **21** attributes
    - Visualizations: Interactive Plotly engines
    """)
    st.markdown("---")
    st.caption("Gurgaon Real Estate Analytics App © 2026")

# 5. Header Title
st.markdown("<div class='header-title'>Gurgaon Property Analytics Dashboard</div>", unsafe_allow_html=True)
st.markdown("<div class='header-subtitle'>Explore pricing distributions, geographic valuations, features representation, and dimensions.</div>", unsafe_allow_html=True)

# 6. Overall Summary Metrics Card Panel
m1, m2, m3, m4 = st.columns(4)
with m1:
    st.metric(label="Total Properties Loaded", value=f"{len(df):,}")
with m2:
    st.metric(label="Average Price", value=f"₹ {df['price'].mean():.2f} Cr")
with m3:
    st.metric(label="Avg Price / Sq.Ft.", value=f"₹ {df['price_per_sqft'].mean():,.0f}")
with m4:
    st.metric(label="Avg Built Up Area", value=f"{df['built_up_area'].mean():,.0f} sq.ft.")

st.markdown("<br>", unsafe_allow_html=True)

# 7. Setup Interactive Tabs
tab1, tab2, tab3, tab4 = st.tabs([
    "🌍 Sector Geography", 
    "📈 Price vs Area Trends", 
    "📊 BHK Insights", 
    "🏷️ Keywords & Distributions"
])

# Tab 1: Geographic Map Visualization
with tab1:
    st.markdown("<div class='section-title'>Gurgaon Sectors Geographic Price Index</div>", unsafe_allow_html=True)
    st.caption("Hover over markers to view details. Marker size reflects average built up area; color represents average price per sqft.")
    
    group_df = df.groupby("sector").mean(numeric_only=True)[['price','price_per_sqft','built_up_area','latitude','longitude']].reset_index()
    
    fig_map = px.scatter_map(
        group_df, 
        lat="latitude", 
        lon="longitude", 
        color="price_per_sqft", 
        size="built_up_area", 
        color_continuous_scale=px.colors.cyclical.IceFire, 
        zoom=10, 
        map_style="open-street-map",
        hover_name="sector",
        hover_data={"price_per_sqft": ":,.0f", "built_up_area": ":,.0f", "price": ":.2f"},
        labels={"price_per_sqft": "Price per Sq.Ft.", "built_up_area": "Built Up Area (sq.ft.)"}
    )
    fig_map.update_layout(
        margin={"r":0,"t":10,"l":0,"b":0},
        height=550
    )
    st.plotly_chart(fig_map, use_container_width=True)

# Tab 2: Dimension / Price Scatter Plot
with tab2:
    st.markdown("<div class='section-title'>Built Up Area vs Price Distribution</div>", unsafe_allow_html=True)
    
    col_sel_prop, _ = st.columns([1, 2])
    with col_sel_prop:
        property_type_filter = st.selectbox("Select Property Type", ['flat', 'house'], key="prop_type_select")
        
    filtered_df = df[df['property_type'] == property_type_filter]
    
    fig_scatter = px.scatter(
        filtered_df, 
        x="built_up_area", 
        y="price", 
        color="bedRoom",
        color_continuous_scale=px.colors.sequential.Viridis,
        labels={"built_up_area": "Built Up Area (Sq.Ft.)", "price": "Price (Cr)", "bedRoom": "No. of Bedrooms (BHK)"},
        hover_data=["society", "sector", "price_per_sqft"],
        title=f"Built Up Area vs Price: {property_type_filter.upper()}"
    )
    fig_scatter.update_layout(
        height=500,
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        margin=dict(t=50, b=50, l=50, r=50)
    )
    fig_scatter.update_xaxes(showgrid=True, gridcolor='#E5E7EB')
    fig_scatter.update_yaxes(showgrid=True, gridcolor='#E5E7EB')
    st.plotly_chart(fig_scatter, use_container_width=True)

# Tab 3: BHK Insights
with tab3:
    st.markdown("<div class='section-title'>BHK Layout Distribution & Pricing Analysis</div>", unsafe_allow_html=True)
    
    col_pie, col_box = st.columns(2, gap="large")
    
    with col_pie:
        st.subheader("BHK Proportion by Sector")
        sector_filter = st.selectbox("Select Sector Location", sorted(df['sector'].unique().tolist()), key="sector_select")
        
        sector_df = df[df['sector'] == sector_filter]
        if not sector_df.empty:
            fig_pie = px.pie(
                sector_df, 
                names='bedRoom', 
                title=f'BHK Breakdown in {sector_filter.title()}',
                color_discrete_sequence=px.colors.qualitative.Safe
            )
            fig_pie.update_layout(height=400, margin=dict(t=40, b=40, l=40, r=40))
            st.plotly_chart(fig_pie, use_container_width=True)
        else:
            st.info("No records found for this sector.")
            
    with col_box:
        st.subheader("BHK Price Ranges comparison")
        st.caption("Evaluating values for standard 1 to 4 BHK configurations.")
        
        fig_box = px.box(
            df[df["bedRoom"] <= 4], 
            x='bedRoom', 
            y='price',
            color='bedRoom',
            color_discrete_sequence=px.colors.qualitative.Pastel,
            labels={"bedRoom": "BHK Configuration", "price": "Price (Cr)"},
            title='BHK Price Spread'
        )
        fig_box.update_layout(
            height=400,
            showlegend=False,
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            margin=dict(t=40, b=40, l=40, r=40)
        )
        fig_box.update_yaxes(showgrid=True, gridcolor='#E5E7EB')
        st.plotly_chart(fig_box, use_container_width=True)

# Tab 4: Word Cloud and Density Plot
with tab4:
    st.markdown("<div class='section-title'>Key Features & Price Density Distributions</div>", unsafe_allow_html=True)
    
    col_wc, col_hist = st.columns(2, gap="large")
    
    with col_wc:
        st.subheader("Amenities & Description Word Cloud")
        st.caption("Common terms used to list properties in the dataset.")
        
        wordcloud = WordCloud(
            width=800, 
            height=600, 
            background_color='white', 
            stopwords=set(['s']),  
            min_font_size=10
        ).generate(feature_text)
        
        fig_wc = plt.figure(figsize=(8, 6), facecolor='white') 
        plt.imshow(wordcloud, interpolation='bilinear') 
        plt.axis("off") 
        plt.tight_layout(pad=0) 
        st.pyplot(fig_wc)
        plt.close(fig_wc)
        
    with col_hist:
        st.subheader("Density: Houses vs Flats Price Spread")
        st.caption("Interactive comparison of pricing peaks between houses and apartments.")
        
        fig_hist = px.histogram(
            df, 
            x="price", 
            color="property_type", 
            marginal="box",
            barmode="overlay", 
            opacity=0.7, 
            color_discrete_map={"flat": "#3B82F6", "house": "#10B981"},
            labels={"price": "Price (in Cr)", "property_type": "Property Type"},
            title="Price Distribution Histogram"
        )
        fig_hist.update_layout(
            height=450,
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            margin=dict(t=40, b=40, l=40, r=40)
        )
        fig_hist.update_xaxes(showgrid=True, gridcolor='#E5E7EB')
        fig_hist.update_yaxes(showgrid=True, gridcolor='#E5E7EB')
        st.plotly_chart(fig_hist, use_container_width=True)