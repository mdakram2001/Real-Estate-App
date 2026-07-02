import streamlit as st
import pandas as pd
import numpy as np
import pickle
import plotly.express as px
import time

# 1. Page Configuration
st.set_page_config(
    page_title="Gurgaon Real Estate Insights",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. Inject CSS Style for Premium Portal Layout
st.markdown("""
<style>
    /* Custom Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', sans-serif;
    }
    
    /* Hero Banner Styling */
    .hero-container {
        background: linear-gradient(135deg, #1E3A8A 0%, #3B82F6 100%);
        padding: 2.5rem;
        border-radius: 20px;
        color: white;
        text-align: center;
        margin-bottom: 2.5rem;
        box-shadow: 0 10px 25px rgba(30, 58, 138, 0.15);
    }
    
    .hero-title {
        font-size: 2.8rem;
        font-weight: 800;
        letter-spacing: -0.5px;
        margin-bottom: 0.5rem;
    }
    
    .hero-subtitle {
        font-size: 1.15rem;
        opacity: 0.95;
        font-weight: 300;
        max-width: 800px;
        margin: 0 auto;
        line-height: 1.5;
    }
    
    /* Section Headings */
    .section-title {
        font-size: 1.25rem;
        font-weight: 700;
        color: #1E293B;
        margin-top: 1.5rem;
        margin-bottom: 1rem;
        padding-bottom: 0.4rem;
        border-bottom: 2px solid #E2E8F0;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    
    /* Result Display Card */
    .result-container {
        background: linear-gradient(135deg, #1E3A8A 0%, #3B82F6 100%);
        padding: 2.2rem;
        border-radius: 16px;
        color: white;
        text-align: center;
        box-shadow: 0 10px 30px rgba(59, 130, 246, 0.25);
        margin-top: 1rem;
        margin-bottom: 1.5rem;
        border: 1px solid rgba(255, 255, 255, 0.1);
        transition: all 0.3s ease;
    }
    
    .result-title {
        font-size: 1.05rem;
        text-transform: uppercase;
        letter-spacing: 2px;
        margin-bottom: 0.5rem;
        font-weight: 600;
        opacity: 0.9;
    }
    
    .result-price {
        font-size: 3.5rem;
        font-weight: 800;
        margin-bottom: 0.5rem;
        text-shadow: 0 2px 8px rgba(0,0,0,0.15);
        letter-spacing: -1px;
    }
    
    .result-footer {
        font-size: 0.95rem;
        opacity: 0.85;
        font-style: italic;
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
    with open('datasets/coeff.pkl','rb') as f:
        cdf = pickle.load(f)
    return dataframe, pipeline, cdf

try:
    df, pdf, cdf = load_assets()
except Exception as e:
    st.error(f"Error loading datasets/models: {e}")
    st.stop()

# 4. Sidebar Content
with st.sidebar:
    st.markdown("### 📊 Gurgaon Insights Engine")
    st.info("""
    This dashboard provides mathematical transparency into how Gurgaon property prices are calculated.
    """)
    st.markdown("""
    **🚀 Model Insights:**
    - Type: **Log-Linear Regression Model**
    - Target: **Log-price Transform**
    - Valuation is built step-by-step from coefficients (unstandardized logs).
    """)
    st.markdown("---")
    st.markdown("### 🏠 Baseline Case Example")
    st.caption("""
    **1 BHK Flat in Sector 8**
    - Area: 1000 Sq. Ft.
    - Age: Relatively New
    - Furnishing: Unfurnished
    - **Estimated Base: ₹ 0.66 Cr**
    """)
    st.markdown("---")
    st.caption("Gurgaon Real Estate Analytics App © 2026")

# 5. Hero Banner
st.markdown("""
<div class="hero-container">
    <div class="hero-title">Gurgaon Real Estate Insights</div>
    <div class="hero-subtitle">Interactive Model Interpretability Dashboard. See exactly how each property characteristic adds or subtracts value.</div>
</div>
""", unsafe_allow_html=True)

# 6. Layout split into 2 main Columns
col1, col2 = st.columns([1, 1.2], gap="large")

with col1:
    st.markdown("<div class='section-title'>📍 Location & Property Type</div>", unsafe_allow_html=True)
    
    property_type = st.selectbox(
        'Property Type', 
        ['flat', 'house'],
        format_func=lambda x: "🏢 Flat / Apartment" if x == 'flat' else "🏡 Independent House",
    )
    property_type_multi = 1.0 if property_type == 'house' else 0.0
    property_type_calc = (cdf.loc[cdf['feature'] == 'property_type', 'unstd_log_coeff'].values[0])*property_type_multi

    sector = st.selectbox(
        "Location Sector",
        sorted(cdf[cdf['feature'].str.startswith('sector_')]['feature'].str.replace('sector_', '').unique().tolist()),
    )
    sector_calc = cdf.loc[cdf['feature'] == f'sector_{sector}', 'unstd_log_coeff'].values[0]

    st.markdown("<div class='section-title'>📐 Space & Layout Specifications</div>", unsafe_allow_html=True)
    
    area = float(st.number_input(
        "Built Up Area (Sq. Ft.)",
        min_value=100.0,
        max_value=25000.0,
        value=1500.0,
        step=50.0
    ))
    area_calc = cdf.loc[cdf['feature'] == 'built_up_area', 'unstd_log_coeff'].values[0] * area

    bedroom_options = sorted(df['bedRoom'].unique().tolist())
    bedroom = float(st.selectbox(
        "No. of Bedrooms (BHK)", 
        options=bedroom_options,
        index=bedroom_options.index(3.0) if 3.0 in bedroom_options else 0,
        format_func=lambda x: f"{int(x)} BHK" if x.is_integer() else f"{x} BHK"
    ))
    bedroom_calc = cdf.loc[cdf['feature'] == 'bedRoom', 'unstd_log_coeff'].values[0] * bedroom

    bathroom_options = sorted(df['bathroom'].unique().tolist())
    bathroom = float(st.selectbox(
        "No. of Bathrooms",
        options=bathroom_options,
        index=bathroom_options.index(3.0) if 3.0 in bathroom_options else 0,
        format_func=lambda x: f"{int(x)}" if x.is_integer() else f"{x}"
    ))
    bathroom_calc = cdf.loc[cdf['feature'] == 'bathroom', 'unstd_log_coeff'].values[0] * bathroom

    st.markdown("<div class='section-title'>✨ Property Status & Extras</div>", unsafe_allow_html=True)
    
    property_age = st.selectbox(
        "Property Age / Possession Status", 
        sorted(cdf[cdf['feature'].str.startswith('agePossession_')]['feature'].str.replace('agePossession_', '').unique().tolist())
    )
    property_age_calc = cdf.loc[cdf['feature'] == f'agePossession_{property_age}', 'unstd_log_coeff'].values[0]

    furnishing_type = st.selectbox(
        "Furnishing Status", 
        sorted(df['furnishing_type'].unique().tolist()),
        format_func=lambda x: x.title()
    )
    furnishing_multi = 0.0
    if furnishing_type == 'semi-furnished':
        furnishing_multi = 1.0
    elif furnishing_type == 'furnished':
        furnishing_multi = 2.0
    furnishing_calc = cdf.loc[cdf['feature'] == 'furnishing_type', 'unstd_log_coeff'].values[0] * furnishing_multi

    servant_room_label = st.selectbox(
        "Servant Room", 
        ["No", "Yes"]
    )
    servant_room = 1.0 if servant_room_label == "Yes" else 0.0
    servant_room_calc = cdf.loc[cdf['feature'] == 'servant room', 'unstd_log_coeff'].values[0] * servant_room

with col2:
    st.markdown("<div class='section-title'>📈 Live Valuation Breakdown</div>", unsafe_allow_html=True)

    intercept = 0.20188281728471025

    def predict_log_price():
        return (
            intercept
            + property_type_calc
            + sector_calc
            + area_calc
            + property_age_calc
            + bedroom_calc
            + bathroom_calc
            + furnishing_calc
            + servant_room_calc
        )

    price_log = predict_log_price()
    predicted_price = np.expm1(price_log)

    # Render styled result display card
    st.markdown(f"""
    <div class="result-container">
        <div class="result-title">Estimated Property Value</div>
        <div class="result-price">₹ {predicted_price:,.2f} Cr</div>
        <div class="result-footer">Computed instantly from log-linear model coefficients</div>
    </div>
    """, unsafe_allow_html=True)
    
    st.caption(f"Mathematical Log Prediction: **{price_log:.4f}**")

    # Contributions DataFrame construction
    contributions = pd.DataFrame([
        {
            "Feature": "Property Type",
            "Coefficient": cdf.loc[cdf['feature'] == 'property_type', 'unstd_log_coeff'].values[0],
            "Impact (%)": (np.exp(property_type_calc) - 1) * 100,
            "Value": "Independent House" if property_type == 'house' else "Flat / Apartment",
        },
        {
            "Feature": "Location Sector",
            "Coefficient": sector_calc,
            "Impact (%)": (np.exp(sector_calc) - 1) * 100,
            "Value": f"Sector {sector}",
        },
        {
            "Feature": "Built-up Area",
            "Coefficient": cdf.loc[cdf['feature'] == 'built_up_area', 'unstd_log_coeff'].values[0],
            "Impact (%)": (np.exp(area_calc) - 1) * 100,
            "Value": f"{area:,.0f} Sq. Ft.",
        },
        {
            "Feature": "Property Age",
            "Coefficient": property_age_calc,
            "Impact (%)": (np.exp(property_age_calc) - 1) * 100,
            "Value": property_age,
        },
        {
            "Feature": "Bedrooms (BHK)",
            "Coefficient": cdf.loc[cdf['feature'] == 'bedRoom', 'unstd_log_coeff'].values[0],
            "Impact (%)": (np.exp(bedroom_calc) - 1) * 100,
            "Value": f"{int(bedroom)} BHK" if bedroom.is_integer() else f"{bedroom} BHK",
        },
        {
            "Feature": "Bathrooms",
            "Coefficient": cdf.loc[cdf['feature'] == 'bathroom', 'unstd_log_coeff'].values[0],
            "Impact (%)": (np.exp(bathroom_calc) - 1) * 100,
            "Value": f"{int(bathroom)}" if bathroom.is_integer() else f"{bathroom}",
        },
        {
            "Feature": "Furnishing Status",
            "Coefficient": cdf.loc[cdf['feature'] == 'furnishing_type', 'unstd_log_coeff'].values[0],
            "Impact (%)": (np.exp(furnishing_calc) - 1) * 100,
            "Value": furnishing_type.title(),
        },
        {
            "Feature": "Servant Room",
            "Coefficient": cdf.loc[cdf['feature'] == 'servant room', 'unstd_log_coeff'].values[0],
            "Impact (%)": (np.exp(servant_room_calc) - 1) * 100,
            "Value": "Yes" if servant_room == 1.0 else "No",
        }
    ])

    # Visualizing feature impact with Plotly
    chart_df = contributions.copy()
    chart_df["Impact Type"] = chart_df["Impact (%)"].apply(lambda x: "Increases Price" if x >= 0 else "Decreases Price")
    chart_df["Label"] = chart_df.apply(lambda r: f"{r['Feature']} ({r['Value']})", axis=1)
    chart_df_sorted = chart_df.sort_values(by="Impact (%)", ascending=True)

    fig = px.bar(
        chart_df_sorted,
        x="Impact (%)",
        y="Label",
        color="Impact Type",
        orientation="h",
        color_discrete_map={"Increases Price": "#10B981", "Decreases Price": "#EF4444"},
        labels={"Label": "Attribute Value", "Impact (%)": "Price Impact (%)"},
    )
    
    fig.update_layout(
        xaxis=dict(ticksuffix="%"),
        yaxis=dict(title=None),
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=10, r=10, t=30, b=10),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        height=320
    )
    
    st.plotly_chart(fig, use_container_width=True)

    # 2nd Graph: Coefficient vs Features Dependencies
    st.markdown("<div style='font-size: 1.05rem; font-weight: 700; color: #1E293B; margin-top: 1.5rem; margin-bottom: 0.5rem;'>📐 Model Coefficients vs Features dependencies</div>", unsafe_allow_html=True)
    chart_df_coef = chart_df.copy()
    chart_df_coef["Coefficient Type"] = chart_df_coef["Coefficient"].apply(lambda x: "Positive Influence" if x >= 0 else "Negative Influence")
    chart_df_coef = chart_df_coef.sort_values(by="Coefficient", ascending=True)
    
    fig_coef = px.bar(
        chart_df_coef,
        x="Coefficient",
        y="Label",
        color="Coefficient Type",
        orientation="h",
        color_discrete_map={"Positive Influence": "#3B82F6", "Negative Influence": "#F59E0B"},
        labels={"Label": "Attribute Value", "Coefficient": "Coefficient Value (Beta)"},
    )
    
    fig_coef.update_layout(
        xaxis=dict(title="Unstandardized Model Coefficient (Beta)"),
        yaxis=dict(title=None),
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=10, r=10, t=30, b=10),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        height=320
    )
    
    st.plotly_chart(fig_coef, use_container_width=True)




# 7. Bottom LaTeX mathematical explanation
st.markdown("---")
with st.expander("🔬 Model Mathematics & Coefficients Table"):
    st.markdown("""
    ### Log-Linear Model Formula
    The valuation engine is powered by an unstandardized multiple linear regression model that predicts the logarithm of property price:
    """)
    st.latex(r"""
    \log(\text{Price} + 1) = \beta_0 + \sum_{i=1}^{k} \beta_i X_i
    """)
    st.markdown("""
    To retrieve the final price in Crores, we apply the exponential transform:
    """)
    st.latex(r"""
    \text{Price} = e^{\log(\text{Price} + 1)} - 1
    """)
    st.markdown("### Exact Coefficients Table for Current Selection")
    
    # Create details df for display
    details_df = pd.DataFrame([
        {"Feature Variable": "Model Intercept (Baseline)", "Coefficient (Beta)": intercept, "Contribution to Log Price": intercept, "Exponential Factor (Multiplier)": np.exp(intercept)},
        {"Feature Variable": f"property_type (House multiplier)", "Coefficient (Beta)": cdf.loc[cdf['feature'] == 'property_type', 'unstd_log_coeff'].values[0], "Contribution to Log Price": property_type_calc, "Exponential Factor (Multiplier)": np.exp(property_type_calc)},
        {"Feature Variable": f"sector_{sector}", "Coefficient (Beta)": sector_calc, "Contribution to Log Price": sector_calc, "Exponential Factor (Multiplier)": np.exp(sector_calc)},
        {"Feature Variable": "built_up_area", "Coefficient (Beta)": cdf.loc[cdf['feature'] == 'built_up_area', 'unstd_log_coeff'].values[0], "Contribution to Log Price": area_calc, "Exponential Factor (Multiplier)": np.exp(area_calc)},
        {"Feature Variable": f"agePossession_{property_age}", "Coefficient (Beta)": property_age_calc, "Contribution to Log Price": property_age_calc, "Exponential Factor (Multiplier)": np.exp(property_age_calc)},
        {"Feature Variable": "bedRoom", "Coefficient (Beta)": cdf.loc[cdf['feature'] == 'bedRoom', 'unstd_log_coeff'].values[0], "Contribution to Log Price": bedroom_calc, "Exponential Factor (Multiplier)": np.exp(bedroom_calc)},
        {"Feature Variable": "bathroom", "Coefficient (Beta)": cdf.loc[cdf['feature'] == 'bathroom', 'unstd_log_coeff'].values[0], "Contribution to Log Price": bathroom_calc, "Exponential Factor (Multiplier)": np.exp(bathroom_calc)},
        {"Feature Variable": "furnishing_type", "Coefficient (Beta)": cdf.loc[cdf['feature'] == 'furnishing_type', 'unstd_log_coeff'].values[0], "Contribution to Log Price": furnishing_calc, "Exponential Factor (Multiplier)": np.exp(furnishing_calc)},
        {"Feature Variable": "servant room", "Coefficient (Beta)": cdf.loc[cdf['feature'] == 'servant room', 'unstd_log_coeff'].values[0], "Contribution to Log Price": servant_room_calc, "Exponential Factor (Multiplier)": np.exp(servant_room_calc)}
    ])
    
    # Format details dataframe
    details_df["Coefficient (Beta)"] = details_df["Coefficient (Beta)"].map("{:,.6f}".format)
    details_df["Contribution to Log Price"] = details_df["Contribution to Log Price"].map("{:,.6f}".format)
    details_df["Exponential Factor (Multiplier)"] = details_df["Exponential Factor (Multiplier)"].map("{:,.4f}x".format)
    
    st.dataframe(details_df, use_container_width=True, hide_index=True)