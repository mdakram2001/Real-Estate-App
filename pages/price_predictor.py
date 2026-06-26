import streamlit as st
import pandas as pd
import numpy as np
import pickle
import time

# 1. Page Configuration
st.set_page_config(
    page_title="Gurgaon Real Estate Price Predictor",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. Inject Custom CSS for Premium Styling
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
        background: linear-gradient(135deg, #4F46E5 0%, #7C3AED 100%);
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
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    
    /* Result Display Card */
    .result-container {
        background: linear-gradient(135deg, #4F46E5 0%, #7C3AED 100%);
        padding: 2.2rem;
        border-radius: 16px;
        color: white;
        text-align: center;
        box-shadow: 0 10px 30px rgba(124, 58, 237, 0.25);
        margin-top: 2rem;
        animation: slideUp 0.6s cubic-bezier(0.16, 1, 0.3, 1);
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    .result-title {
        font-size: 1.1rem;
        text-transform: uppercase;
        letter-spacing: 2px;
        margin-bottom: 0.6rem;
        font-weight: 600;
        opacity: 0.9;
    }
    
    .result-price {
        font-size: 3.5rem;
        font-weight: 800;
        margin-bottom: 0.6rem;
        text-shadow: 0 2px 8px rgba(0,0,0,0.15);
        letter-spacing: -1px;
    }
    
    .result-footer {
        font-size: 0.95rem;
        opacity: 0.85;
        font-style: italic;
    }
    
    /* Animation Keyframes */
    @keyframes slideUp {
        from {
            opacity: 0;
            transform: translateY(24px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    /* Premium Estimate Button Styling */
    div.stButton > button:first-child {
        background: linear-gradient(135deg, #4F46E5 0%, #7C3AED 100%);
        color: white;
        font-weight: 700;
        font-size: 1.15rem;
        border: none;
        padding: 0.8rem 2rem;
        border-radius: 12px;
        box-shadow: 0 4px 14px rgba(124, 58, 237, 0.3);
        transition: all 0.3s ease;
        width: 100%;
        margin-top: 1rem;
    }
    
    div.stButton > button:first-child:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(124, 58, 237, 0.45);
        color: white !important;
        border: none;
    }
    
    div.stButton > button:first-child:active {
        transform: translateY(1px);
    }
</style>
""", unsafe_allow_html=True)

# 3. Load Data & ML Pipeline
@st.cache_resource
def load_assets():
    with open('datasets/df.pkl', 'rb') as f:
        dataframe = pickle.load(f)
    with open('datasets/pipeline.pkl', 'rb') as f:
        pipeline = pickle.load(f)
    return dataframe, pipeline

try:
    df, pdf = load_assets()
except Exception as e:
    st.error(f"Error loading datasets/models: {e}")
    st.stop()

# 4. Sidebar Content
with st.sidebar:
    st.markdown("### 🏢 Gurgaon Valuation Engine")
    st.info("""
    This intelligent model estimates house and flat prices in Gurgaon based on multiple property characteristics.
    """)
    st.markdown("""
    **🚀 Technical Highlights:**
    - Model: **Random Forest Regressor**
    - Features utilized: 12 key attributes
    - Log-Target Transform for improved residual behavior
    """)
    st.markdown("---")
    st.caption("Gurgaon Real Estate Analytics App © 2026")

# 5. Header Section
st.markdown("<div class='header-title'>Gurgaon Home Valuation Engine</div>", unsafe_allow_html=True)
st.markdown("<div class='header-subtitle'>Enter details below to predict the estimated price range of your property.</div>", unsafe_allow_html=True)

# 6. Inputs Form split into 3 Columns
col1, col2, col3 = st.columns(3, gap="large")

with col1:
    st.markdown("<div class='section-title'>🏠 Property Core Specs</div>", unsafe_allow_html=True)
    
    property_type = st.selectbox(
        'Property Type', 
        ['flat', 'house'],
        format_func=lambda x: "🏢 Flat / Apartment" if x == 'flat' else "🏡 Independent House",
        help="Select if the property is a flat in a residential complex or a standalone house."
    )
    
    sector = st.selectbox(
        "Location Sector", 
        sorted(df['sector'].unique().tolist()),
        help="Select the specific sector in Gurgaon."
    )
    
    area = float(st.number_input(
        "Built Up Area (Sq. Ft.)",
        min_value=100.0,
        max_value=25000.0,
        value=1500.0,
        step=50.0,
        help="Enter the total built-up area of the property in square feet."
    ))
    
    property_age = st.selectbox(
        "Property Age / Possession Status", 
        sorted(df['agePossession'].unique().tolist()),
        help="The age of the property or its construction status."
    )

with col2:
    st.markdown("<div class='section-title'>📐 Space & Layout</div>", unsafe_allow_html=True)
    
    bedroom_options = sorted(df['bedRoom'].unique().tolist())
    bedroom = float(st.selectbox(
        "No. of Bedrooms (BHK)", 
        options=bedroom_options,
        index=bedroom_options.index(3.0) if 3.0 in bedroom_options else 0,
        format_func=lambda x: f"{int(x)} BHK" if x.is_integer() else f"{x} BHK",
        help="Total number of bedrooms in the property."
    ))
    
    bathroom_options = sorted(df['bathroom'].unique().tolist())
    bathroom = float(st.selectbox(
        "No. of Bathrooms", 
        options=bathroom_options,
        index=bathroom_options.index(3.0) if 3.0 in bathroom_options else 0,
        format_func=lambda x: f"{int(x)}" if x.is_integer() else f"{x}",
        help="Total number of bathrooms in the property."
    ))
    
    balcony = st.selectbox(
        "No. of Balconies", 
        sorted(df['balcony'].unique().tolist()),
        help="Number of balconies attached to the property."
    )
    
    floor_category = st.selectbox(
        "Floor Level Category", 
        sorted(df['floor_category'].unique().tolist()),
        help="Vertical category (e.g., Higher, Medium, Lower floors)."
    )

with col3:
    st.markdown("<div class='section-title'>✨ Premium & Comfort</div>", unsafe_allow_html=True)
    
    furnishing_type = st.selectbox(
        "Furnishing Status", 
        sorted(df['furnishing_type'].unique().tolist()),
        format_func=lambda x: x.title(),
        help="Select whether the property is Furnished, Semifurnished or Unfurnished."
    )
    
    luxury_category = st.selectbox(
        "Luxury Segment", 
        sorted(df['luxury_category'].unique().tolist()),
        format_func=lambda x: f"{x} Luxury",
        help="The luxury tier based on apartment/society specifications."
    )
    
    servant_room_label = st.selectbox(
        "Servant Room", 
        ["No", "Yes"],
        help="Is there a dedicated servant room/toilet?"
    )
    servant_room = 1.0 if servant_room_label == "Yes" else 0.0
    
    store_room_label = st.selectbox(
        "Store Room", 
        ["No", "Yes"],
        help="Is there a dedicated store room?"
    )
    store_room = 1.0 if store_room_label == "Yes" else 0.0

st.markdown("<br>", unsafe_allow_html=True)

# 7. Valuation Execution & Presentation
if st.button("Estimate Property Value"):
    with st.spinner("Analyzing market dynamics & predicting property value..."):
        time.sleep(0.7) # Micro-interaction delay for premium feel
        
        columns = [
            'property_type', 'sector', 'bedRoom', 'bathroom', 'balcony', 
            'agePossession', 'built_up_area', 'servant room', 'store room',
            'furnishing_type', 'luxury_category', 'floor_category'
        ]
        
        data = [[
            property_type, sector, bedroom, bathroom, balcony, 
            property_age, area, servant_room, store_room, 
            furnishing_type, luxury_category, floor_category
        ]]

        input_df = pd.DataFrame(data, columns=columns)

        try:
            # Predict log price and exponentiate to original scale
            base_price = np.expm1(pdf.predict(input_df))[0]
            
            # Predict range interval (+/- 0.22 Cr)
            low = max(0.01, round(base_price - 0.22, 2))
            high = round(base_price + 0.22, 2)
            
            # Render styled results card
            st.markdown(f"""
            <div class="result-container">
                <div class="result-title">Estimated Market Valuation</div>
                <div class="result-price">₹ {low:.2f} Cr - ₹ {high:.2f} Cr</div>
                <div class="result-footer">Predicted price ranges are based on active model estimations for properties in {sector}</div>
            </div>
            """, unsafe_allow_html=True)
            
        except Exception as pred_err:
            st.error(f"Prediction Error: {pred_err}. Please check your inputs.")