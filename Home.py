import streamlit as st

# 1. Page Configuration
st.set_page_config(
    page_title="Gurgaon Real Estate Portal",
    page_icon="🗺️",
    layout="wide"
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
        background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
        padding: 3.5rem;
        border-radius: 20px;
        color: white;
        text-align: center;
        margin-bottom: 2.5rem;
        box-shadow: 0 10px 25px rgba(30, 60, 114, 0.15);
    }
    
    .hero-title {
        font-size: 3rem;
        font-weight: 800;
        letter-spacing: -0.5px;
        margin-bottom: 0.75rem;
    }
    
    .hero-subtitle {
        font-size: 1.25rem;
        opacity: 0.9;
        font-weight: 300;
        max-width: 800px;
        margin: 0 auto;
        line-height: 1.5;
    }
    
    /* Feature Card Styling */
    .feature-card {
        background: white;
        border: 1px solid #e2e8f0;
        border-radius: 16px;
        padding: 2rem;
        text-align: center;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
        transition: all 0.3s ease;
        height: 100%;
    }
    
    .feature-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04);
        border-color: #2a5298;
    }
    
    .feature-icon {
        font-size: 2.5rem;
        margin-bottom: 1rem;
    }
    
    .feature-name {
        font-size: 1.35rem;
        font-weight: 700;
        color: #1e293b;
        margin-bottom: 0.75rem;
    }
    
    .feature-desc {
        font-size: 0.95rem;
        color: #64748b;
        line-height: 1.6;
        margin-bottom: 1.5rem;
    }
    
    .navigation-badge {
        display: inline-block;
        background-color: #eff6ff;
        color: #1d4ed8;
        font-weight: 600;
        font-size: 0.85rem;
        padding: 0.4rem 1rem;
        border-radius: 30px;
        border: 1px solid #bfdbfe;
    }
    
    /* Statistics Card Styling */
    .stat-card {
        background: #f8fafc;
        border: 1px solid #e2e8f0;
        border-radius: 12px;
        padding: 1.5rem;
        text-align: center;
    }
    
    .stat-num {
        font-size: 2.2rem;
        font-weight: 800;
        color: #2a5298;
        margin-bottom: 0.25rem;
    }
    
    .stat-label {
        font-size: 0.95rem;
        color: #475569;
        font-weight: 500;
    }
</style>
""", unsafe_allow_html=True)

# 3. Sidebar Configuration
with st.sidebar:
    st.markdown("### 🗺️ Portal Navigation")
    st.info("Select any analytics, recommender, or prediction module from the sidebar list to get started.")
    st.markdown("---")
    st.markdown("### 💡 Help & Usage")
    st.caption("""
    1. Navigation: Click options on the top-left sidebar.
    2. Inputs: Forms accept drop-downs or numbers.
    3. Outputs: Powered by standard backend models & geocoded coordinates.
    """)
    st.caption("Gurgaon Real Estate Portal © 2026")

# 4. Hero Welcome Block
st.markdown("""
<div class="hero-container">
    <div class="hero-title">Gurgaon Real Estate Analytics Portal</div>
    <div class="hero-subtitle">Interactive machine learning tools, spatial intelligence insights, and similarity-based recommendations.</div>
</div>
""", unsafe_allow_html=True)

# 5. Features Grid
col1, col2, col3 = st.columns(3, gap="large")

with col1:
    st.markdown("""
    <div class="feature-card">
        <div class="feature-icon">🏢</div>
        <div class="feature-name">Housing Valuation Engine</div>
        <p class="feature-desc">Input property details (area, location, layouts, age) and predict standard market valuation ranges powered by Random Forest ML models.</p>
        <div class="navigation-badge">👈 Select "price_predictor"</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="feature-card">
        <div class="feature-icon">📈</div>
        <div class="feature-name">Property Analytics Dashboard</div>
        <p class="feature-desc">Explore pricing distributions, geographic valuations on interactive maps, BHK proportions, and sector-wise dimensions.</p>
        <div class="navigation-badge">👈 Select "analysis_app"</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="feature-card">
        <div class="feature-icon">🤝</div>
        <div class="feature-name">Smart Recommender System</div>
        <p class="feature-desc">Find apartments based on geographical radius searches or find similar properties using cosine similarity vector scoring models.</p>
        <div class="navigation-badge">👈 Select "recommender"</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br><br>", unsafe_allow_html=True)

# 6. Portal Summary Statistics
st.markdown("### 📊 Portal Key Performance Metrics")

s1, s2, s3 = st.columns(3)
with s1:
    st.markdown("""
    <div class="stat-card">
        <div class="stat-num">3,500+</div>
        <div class="stat-label">Properties Geocoded & Processed</div>
    </div>
    """, unsafe_allow_html=True)
with s2:
    st.markdown("""
    <div class="stat-card">
        <div class="stat-num">100+</div>
        <div class="stat-label">Gurgaon Sectors Covered</div>
    </div>
    """, unsafe_allow_html=True)
with s3:
    st.markdown("""
    <div class="stat-card">
        <div class="stat-num">~90%</div>
        <div class="stat-label">Valuation Pipeline Accuracy</div>
    </div>
    """, unsafe_allow_html=True)