import streamlit as st
import pickle
import pandas as pd
import numpy as np
import time

# 1. Page Configuration
st.set_page_config(
    page_title="Gurgaon Real Estate Recommender",
    page_icon="🤝",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. Inject CSS Style for Premium Layout
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
        background: linear-gradient(135deg, #EC4899 0%, #8B5CF6 100%);
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
    
    /* Premium Search/Recommend Button Styling */
    div.stButton > button:first-child {
        background: linear-gradient(135deg, #EC4899 0%, #8B5CF6 100%);
        color: white;
        font-weight: 700;
        font-size: 1.15rem;
        border: none;
        padding: 0.8rem 2rem;
        border-radius: 12px;
        box-shadow: 0 4px 14px rgba(139, 92, 246, 0.3);
        transition: all 0.3s ease;
        width: 100%;
        margin-top: 1rem;
    }
    
    div.stButton > button:first-child:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(139, 92, 246, 0.45);
        color: white !important;
        border: none;
    }
    
    div.stButton > button:first-child:active {
        transform: translateY(1px);
    }
</style>
""", unsafe_allow_html=True)

# 3. Load & Cache Similarity Assets
@st.cache_resource
def load_assets():
    loc_df = pickle.load(open('datasets/distance.pkl', 'rb'))
    sim1 = pickle.load(open('datasets/cosine_sim1.pkl', 'rb'))
    sim2 = pickle.load(open('datasets/cosine_sim2.pkl', 'rb'))
    sim3 = pickle.load(open('datasets/cosine_sim3.pkl', 'rb'))
    return loc_df, sim1, sim2, sim3

try:
    location_df, cosine_sim1, cosine_sim2, cosine_sim3 = load_assets()
except Exception as e:
    st.error(f"Error loading recommender datasets: {e}")
    st.stop()

# 4. Recommendation Logic
def recommend_properties_with_scores(property_name, top_n=5):
    cosine_sim_matrix = 0.5 * cosine_sim1 + 0.8 * cosine_sim2 + 1 * cosine_sim3

    # Get the similarity scores for the property using its name as the index
    sim_scores = list(enumerate(cosine_sim_matrix[location_df.index.get_loc(property_name)]))

    # Sort properties based on the similarity scores
    sorted_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)

    # Get the indices and scores of the top_n most similar properties
    top_indices = [i[0] for i in sorted_scores[1:top_n + 1]]
    top_scores = [i[1] for i in sorted_scores[1:top_n + 1]]

    # Retrieve the names of the top properties using the indices
    top_properties = location_df.index[top_indices].tolist()

    # Create a dataframe with the results
    recommendations_df = pd.DataFrame({
        'PropertyName': top_properties,
        'SimilarityScore': top_scores
    })

    return recommendations_df

# Module-level silent run (matching original code behavior)
recommend_properties_with_scores('DLF The Camellias')

# 5. Sidebar Layout
with st.sidebar:
    st.markdown("### 🤝 Smart Recommender")
    st.info("""
    Find properties based on geography and similarity scores using cosine vector math matching dimensions.
    """)
    st.markdown("""
    **🚀 Recommendation Matrix:**
    - Cosine Sim weights: 
      - Locality (0.5)
      - Specs (0.8)
      - Price (1.0)
    """)
    st.markdown("---")
    st.caption("Gurgaon Real Estate Analytics App © 2026")

# 6. Header Banner
st.markdown("<div class='header-title'>Gurgaon Property Recommender System</div>", unsafe_allow_html=True)
st.markdown("<div class='header-subtitle'>Find nearby apartments or search for structurally and financially similar properties.</div>", unsafe_allow_html=True)

# 7. Navigation Tabs
tab1, tab2 = st.tabs([
    "📍 Locality Radius Search", 
    "🏢 Similarity-Based Recommender"
])

# Tab 1: Locality Search
with tab1:
    st.markdown("<div class='section-title'>Select Proximity Parameters</div>", unsafe_allow_html=True)
    
    col_loc, col_rad = st.columns(2, gap="large")
    with col_loc:
        selected_location = st.selectbox(
            'Target Location',
            sorted(location_df.columns.to_list()),
            help="Select the focal property or sector to search around."
        )
    with col_rad:
        radius = st.number_input(
            'Proximity Radius (in Kms)',
            min_value=0.1,
            max_value=50.0,
            value=5.0,
            step=0.5,
            help="Radius limit in kilometers."
        )
        
    if st.button('Search Location Proximity'):
        with st.spinner("Searching nearby coordinates..."):
            time.sleep(0.5)
            # Perform query in meters
            result_ser = location_df[location_df[selected_location] < radius * 1000][selected_location].sort_values()
            
            if not result_ser.empty:
                result_df = pd.DataFrame({
                    "PropertyName": result_ser.index,
                    "DistanceKms": (result_ser.values / 1000).round(2)
                })
                
                st.markdown(f"**Found {len(result_df)} properties within {radius} Kms of {selected_location}:**")
                st.dataframe(
                    result_df,
                    column_config={
                        "PropertyName": st.column_config.TextColumn("Property Name"),
                        "DistanceKms": st.column_config.NumberColumn(
                            "Distance",
                            format="%.2f km",
                            help="Kilometers away from target location"
                        )
                    },
                    use_container_width=True
                )
            else:
                st.warning(f"No properties found within {radius} Kms of {selected_location}.")

# Tab 2: Similarity-Based Recommender
with tab2:
    st.markdown("<div class='section-title'>Recommend Similar Properties</div>", unsafe_allow_html=True)
    
    col_select_apartment = st.columns([2, 1])[0]
    with col_select_apartment:
        selected_appartment = st.selectbox(
            'Select Reference Apartment',
            sorted(location_df.index.to_list()),
            help="Select the property you want recommendations similar to."
        )
        
    if st.button('Calculate Recommendations'):
        with st.spinner("Executing similarity vector scoring..."):
            time.sleep(0.6)
            recommendation_df = recommend_properties_with_scores(selected_appartment)
            
            if not recommendation_df.empty:
                st.markdown(f"**Top recommended properties similar to {selected_appartment}:**")
                st.dataframe(
                    recommendation_df,
                    column_config={
                        "PropertyName": st.column_config.TextColumn("Recommended Property"),
                        "SimilarityScore": st.column_config.ProgressColumn(
                            "Cosine Match Score",
                            help="Normalized vector similarity score (0 to 2.3 scale)",
                            format="%.3f",
                            min_value=0.0,
                            max_value=2.3
                        )
                    },
                    use_container_width=True
                )
            else:
                st.error("Could not compute recommendations for the selected property.")
