import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import Circle, Rectangle, FancyBboxPatch, Polygon
from matplotlib.collections import PatchCollection
from io import BytesIO
from database import init_db, get_db, FarmData, CropHistory
from ml_models import (
    get_models, get_fertilizer_recommendation, get_multi_crop_recommendation,
    CROPS as ML_CROPS, SOIL_TYPES, SEASONS, CROP_DURATIONS, GROWTH_STAGES,
    ORGANIC_FERTILIZERS, NON_ORGANIC_FERTILIZERS, MULTI_CROP_COMBINATIONS
)
from crop_database import (
    EXTENDED_CROPS, CROP_CATEGORIES, EXTENDED_MULTI_CROP_COMBINATIONS,
    CROP_ICONS, get_crop_icon, get_crop_category, CROP_INFO
)

ALL_CROPS = EXTENDED_CROPS
from pdf_generator import (
    generate_crop_recommendation_pdf, generate_fertilizer_pdf,
    generate_multi_crop_pdf, generate_yield_prediction_pdf, generate_farm_overview_pdf
)
import base64

init_db()

st.set_page_config(
    page_title="AgriSmart Pro - Precision Agriculture",
    page_icon="🌾",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
    
    :root {
        --primary-green: #1B5E20;
        --secondary-green: #2E7D32;
        --accent-green: #4CAF50;
        --light-green: #81C784;
        --pale-green: #C8E6C9;
        --background: #F5F7F5;
        --white: #FFFFFF;
        --dark-text: #1A1A1A;
        --gray-text: #666666;
    }
    
    .stApp {
        background: linear-gradient(180deg, #F8FAF8 0%, #E8F5E9 100%);
        font-family: 'Inter', sans-serif;
    }
    
    /* Professional Header */
    .pro-header {
        background: linear-gradient(135deg, #1B5E20 0%, #2E7D32 50%, #388E3C 100%);
        padding: 1.5rem 2rem;
        border-radius: 0 0 20px 20px;
        margin: -1rem -1rem 2rem -1rem;
        box-shadow: 0 4px 20px rgba(27, 94, 32, 0.3);
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    
    .pro-header-left {
        display: flex;
        align-items: center;
        gap: 15px;
    }
    
    .pro-logo {
        font-size: 2.5rem;
    }
    
    .pro-header-title {
        color: white;
        margin: 0;
        font-size: 1.8rem;
        font-weight: 700;
        letter-spacing: -0.5px;
    }
    
    .pro-header-subtitle {
        color: rgba(255,255,255,0.85);
        margin: 0;
        font-size: 0.9rem;
        font-weight: 400;
    }
    
    .pro-header-right {
        display: flex;
        gap: 20px;
        align-items: center;
    }
    
    .pro-stat {
        text-align: center;
        padding: 0.5rem 1rem;
        background: rgba(255,255,255,0.15);
        border-radius: 10px;
    }
    
    .pro-stat-value {
        color: white;
        font-size: 1.2rem;
        font-weight: 700;
    }
    
    .pro-stat-label {
        color: rgba(255,255,255,0.8);
        font-size: 0.7rem;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    /* Navigation Sidebar */
    .nav-container {
        background: white;
        border-radius: 15px;
        padding: 1rem;
        box-shadow: 0 2px 10px rgba(0,0,0,0.05);
        margin-bottom: 1rem;
    }
    
    .nav-header {
        color: #1B5E20;
        font-size: 0.85rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-bottom: 0.8rem;
        padding-bottom: 0.5rem;
        border-bottom: 2px solid #E8F5E9;
    }
    
    /* Cards */
    .pro-card {
        background: white;
        border-radius: 16px;
        padding: 1.5rem;
        box-shadow: 0 2px 12px rgba(0,0,0,0.06);
        border: 1px solid #E8F5E9;
        margin-bottom: 1rem;
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }
    
    .pro-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(0,0,0,0.1);
    }
    
    .pro-card-header {
        display: flex;
        align-items: center;
        gap: 10px;
        margin-bottom: 1rem;
        padding-bottom: 0.8rem;
        border-bottom: 1px solid #E8F5E9;
    }
    
    .pro-card-icon {
        font-size: 1.5rem;
    }
    
    .pro-card-title {
        color: #1B5E20;
        font-size: 1.1rem;
        font-weight: 600;
        margin: 0;
    }
    
    /* Metric Cards */
    .metric-grid {
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 1rem;
        margin-bottom: 1.5rem;
    }
    
    .metric-item {
        background: linear-gradient(135deg, #E8F5E9 0%, #C8E6C9 100%);
        border-radius: 12px;
        padding: 1.2rem;
        text-align: center;
        border-left: 4px solid #4CAF50;
    }
    
    .metric-value {
        font-size: 1.8rem;
        font-weight: 700;
        color: #1B5E20;
    }
    
    .metric-label {
        font-size: 0.8rem;
        color: #666;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    /* Result Boxes */
    .result-success {
        background: linear-gradient(135deg, #C8E6C9 0%, #A5D6A7 100%);
        border-radius: 16px;
        padding: 2rem;
        text-align: center;
        border: 2px solid #81C784;
    }
    
    .result-title {
        color: #1B5E20;
        font-size: 1rem;
        font-weight: 600;
        margin-bottom: 0.5rem;
    }
    
    .result-value {
        color: #1B5E20;
        font-size: 2.5rem;
        font-weight: 800;
    }
    
    /* Multi-crop visual cards */
    .companion-card {
        background: linear-gradient(145deg, #FFFFFF 0%, #F1F8E9 100%);
        border-radius: 12px;
        padding: 1rem;
        margin: 0.5rem 0;
        border-left: 4px solid #8BC34A;
        display: flex;
        align-items: center;
        gap: 12px;
    }
    
    .companion-icon {
        font-size: 2rem;
        background: #E8F5E9;
        padding: 0.5rem;
        border-radius: 10px;
    }
    
    .companion-name {
        font-weight: 600;
        color: #2E7D32;
    }
    
    /* Benefits Cards */
    .benefit-card {
        background: linear-gradient(145deg, #E3F2FD 0%, #BBDEFB 100%);
        border-radius: 12px;
        padding: 1rem;
        margin: 0.5rem 0;
        border-left: 4px solid #2196F3;
    }
    
    .benefit-title {
        font-weight: 600;
        color: #1565C0;
        margin-bottom: 0.3rem;
    }
    
    .benefit-text {
        color: #455A64;
        font-size: 0.9rem;
    }
    
    /* Irrigation Card */
    .irrigation-card {
        background: linear-gradient(145deg, #E1F5FE 0%, #B3E5FC 100%);
        border-radius: 12px;
        padding: 1rem;
        border-left: 4px solid #03A9F4;
    }
    
    /* Spacing Card */
    .spacing-card {
        background: linear-gradient(145deg, #FFF3E0 0%, #FFE0B2 100%);
        border-radius: 12px;
        padding: 1rem;
        border-left: 4px solid #FF9800;
    }
    
    /* Footer */
    .pro-footer {
        background: #1B5E20;
        color: white;
        padding: 1.5rem 2rem;
        margin: 2rem -1rem -1rem -1rem;
        border-radius: 20px 20px 0 0;
    }
    
    .footer-content {
        display: flex;
        justify-content: space-between;
        align-items: center;
        flex-wrap: wrap;
        gap: 1rem;
    }
    
    .footer-left {
        display: flex;
        align-items: center;
        gap: 10px;
    }
    
    .footer-logo {
        font-size: 1.5rem;
    }
    
    .footer-brand {
        font-weight: 600;
        font-size: 1rem;
    }
    
    .footer-tagline {
        font-size: 0.8rem;
        opacity: 0.8;
    }
    
    .footer-center {
        display: flex;
        gap: 2rem;
    }
    
    .footer-link {
        color: rgba(255,255,255,0.9);
        text-decoration: none;
        font-size: 0.85rem;
        transition: color 0.2s;
    }
    
    .footer-right {
        text-align: right;
    }
    
    .footer-copyright {
        font-size: 0.75rem;
        opacity: 0.7;
    }
    
    /* Buttons */
    .stButton > button {
        background: linear-gradient(135deg, #4CAF50 0%, #2E7D32 100%);
        color: white;
        border: none;
        border-radius: 10px;
        padding: 0.75rem 2rem;
        font-weight: 600;
        font-size: 0.95rem;
        box-shadow: 0 4px 15px rgba(76, 175, 80, 0.3);
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(76, 175, 80, 0.4);
    }
    
    /* Download Button */
    .download-btn {
        background: linear-gradient(135deg, #1976D2 0%, #0D47A1 100%);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.5rem 1rem;
        font-weight: 500;
        cursor: pointer;
        display: inline-flex;
        align-items: center;
        gap: 8px;
        text-decoration: none;
    }
    
    /* Section Headers */
    .section-header {
        display: flex;
        align-items: center;
        gap: 10px;
        margin: 1.5rem 0 1rem 0;
        padding-bottom: 0.5rem;
        border-bottom: 2px solid #E8F5E9;
    }
    
    .section-icon {
        font-size: 1.3rem;
    }
    
    .section-title {
        color: #1B5E20;
        font-size: 1.3rem;
        font-weight: 700;
        margin: 0;
    }
    
    /* Hide default Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Slider styling */
    .stSlider > div > div > div > div {
        background: linear-gradient(90deg, #81C784, #4CAF50);
    }
    
    /* Select box styling */
    .stSelectbox > div > div {
        background: white;
        border-radius: 10px;
        border: 1px solid #E8F5E9;
    }
    
    /* Crop category cards */
    .category-card {
        background: white;
        border-radius: 12px;
        padding: 1rem;
        margin-bottom: 0.5rem;
        border-left: 4px solid #4CAF50;
        box-shadow: 0 2px 8px rgba(0,0,0,0.05);
    }
    
    .category-name {
        font-weight: 600;
        color: #1B5E20;
        font-size: 0.95rem;
    }
    
    .category-count {
        color: #666;
        font-size: 0.8rem;
    }
    
    /* Crop grid */
    .crop-grid {
        display: grid;
        grid-template-columns: repeat(auto-fill, minmax(120px, 1fr));
        gap: 0.8rem;
    }
    
    .crop-item {
        background: linear-gradient(145deg, #F1F8E9 0%, #DCEDC8 100%);
        border-radius: 10px;
        padding: 0.8rem;
        text-align: center;
        transition: transform 0.2s;
    }
    
    .crop-item:hover {
        transform: scale(1.05);
    }
    
    .crop-icon {
        font-size: 1.8rem;
        display: block;
        margin-bottom: 0.3rem;
    }
    
    .crop-name {
        font-size: 0.75rem;
        color: #2E7D32;
        font-weight: 500;
    }
    
    /* Growth stage timeline */
    .stage-timeline {
        display: flex;
        justify-content: space-between;
        position: relative;
        padding: 1rem 0;
    }
    
    .stage-item {
        text-align: center;
        flex: 1;
        position: relative;
    }
    
    .stage-dot {
        width: 40px;
        height: 40px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        margin: 0 auto 0.5rem;
        font-size: 1.2rem;
    }
    
    .stage-label {
        font-size: 0.75rem;
        color: #666;
        font-weight: 500;
    }
    
    /* Info boxes */
    .info-box {
        background: linear-gradient(145deg, #FFF8E1 0%, #FFECB3 100%);
        border-radius: 10px;
        padding: 1rem;
        border-left: 4px solid #FFC107;
        margin: 0.5rem 0;
    }
    
    .success-box {
        background: linear-gradient(145deg, #E8F5E9 0%, #C8E6C9 100%);
        border-radius: 10px;
        padding: 1rem;
        border-left: 4px solid #4CAF50;
        margin: 0.5rem 0;
    }
    
    /* Divider */
    .divider {
        height: 2px;
        background: linear-gradient(90deg, #E8F5E9, #81C784, #E8F5E9);
        margin: 1.5rem 0;
        border-radius: 1px;
    }
</style>
""", unsafe_allow_html=True)


def render_header():
    st.markdown("""
    <div class="pro-header">
        <div class="pro-header-left">
            <span class="pro-logo">🌾</span>
            <div>
                <h1 class="pro-header-title">AgriSmart Pro</h1>
                <p class="pro-header-subtitle">Precision Agriculture Platform with AI-Powered Insights</p>
            </div>
        </div>
        <div class="pro-header-right">
            <div class="pro-stat">
                <div class="pro-stat-value">300+</div>
                <div class="pro-stat-label">Crop Varieties</div>
            </div>
            <div class="pro-stat">
                <div class="pro-stat-value">99.77%</div>
                <div class="pro-stat-label">ML Accuracy</div>
            </div>
            <div class="pro-stat">
                <div class="pro-stat-value">12</div>
                <div class="pro-stat-label">Soil Types</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)


def render_footer():
    st.markdown("""
    <div class="pro-footer">
        <div class="footer-content">
            <div class="footer-left">
                <span class="footer-logo">🌾</span>
                <div>
                    <div class="footer-brand">AgriSmart Pro</div>
                    <div class="footer-tagline">Smart Farming, Better Yields</div>
                </div>
            </div>
            <div class="footer-center">
                <span class="footer-link">📊 Data-Driven Decisions</span>
                <span class="footer-link">🤖 AI-Powered Analysis</span>
                <span class="footer-link">📄 PDF Reports</span>
            </div>
            <div class="footer-right">
                <div class="footer-copyright">© 2024 AgriSmart Pro. All Rights Reserved.</div>
                <div class="footer-copyright">Powered by Machine Learning</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)


def get_download_link(buffer, filename, text):
    b64 = base64.b64encode(buffer.getvalue()).decode()
    return f'<a href="data:application/pdf;base64,{b64}" download="{filename}" class="download-btn">📄 {text}</a>'


def main():
    render_header()
    
    with st.sidebar:
        st.markdown('<div class="nav-header">Navigation</div>', unsafe_allow_html=True)
        
        page = st.radio(
            "Select Page",
            ["🏠 Dashboard", "🌾 Crop Advisor", "🧪 Fertilizer Planner", 
             "🌻 Multi-Cropping Hub", "📊 Yield Forecaster", "🚿 Irrigation Manager", 
             "🔄 Rotation Planner", "💰 Economic Analysis", "🐛 Pest & Disease", 
             "📈 Analytics Center", "📚 Crop Library"],
            label_visibility="collapsed"
        )
        
        st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
        
        st.markdown("### 📊 Quick Stats")
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Crops", f"{len(EXTENDED_CROPS)}")
        with col2:
            st.metric("Categories", f"{len(CROP_CATEGORIES)}")
    
    if page == "🏠 Dashboard":
        render_dashboard()
    elif page == "🌾 Crop Advisor":
        render_crop_recommendation()
    elif page == "🧪 Fertilizer Planner":
        render_fertilizer_guide()
    elif page == "🌻 Multi-Cropping Hub":
        render_multi_cropping()
    elif page == "📊 Yield Forecaster":
        render_yield_prediction()
    elif page == "🚿 Irrigation Manager":
        render_irrigation_planner()
    elif page == "🔄 Rotation Planner":
        render_crop_rotation()
    elif page == "💰 Economic Analysis":
        render_economic_analysis()
    elif page == "🐛 Pest & Disease":
        render_pest_disease()
    elif page == "📈 Analytics Center":
        render_farm_overview()
    elif page == "📚 Crop Library":
        render_crop_library()
    
    render_footer()


def render_dashboard():
    st.markdown("""
    <div class="section-header">
        <span class="section-icon">🏠</span>
        <h2 class="section-title">Welcome to AgriSmart Pro</h2>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="metric-grid">
        <div class="metric-item">
            <div class="metric-value">300+</div>
            <div class="metric-label">Crop Varieties</div>
        </div>
        <div class="metric-item">
            <div class="metric-value">20</div>
            <div class="metric-label">Crop Categories</div>
        </div>
        <div class="metric-item">
            <div class="metric-value">99.77%</div>
            <div class="metric-label">ML Accuracy</div>
        </div>
        <div class="metric-item">
            <div class="metric-value">12</div>
            <div class="metric-label">Soil Types</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="pro-card">
            <div class="pro-card-header">
                <span class="pro-card-icon">🌾</span>
                <h3 class="pro-card-title">Crop Recommendation</h3>
            </div>
            <p>AI-powered crop selection based on soil parameters, weather, and historical data. Get personalized recommendations with confidence scores.</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="pro-card">
            <div class="pro-card-header">
                <span class="pro-card-icon">🌻</span>
                <h3 class="pro-card-title">Multi-Cropping System</h3>
            </div>
            <p>Maximize your farm income with companion planting. Visual spacing diagrams and irrigation schedules for optimal yields.</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="pro-card">
            <div class="pro-card-header">
                <span class="pro-card-icon">📄</span>
                <h3 class="pro-card-title">PDF Reports</h3>
            </div>
            <p>Generate professional PDF reports for all your farm data. Export recommendations, schedules, and analytics.</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="section-header">
        <span class="section-icon">📋</span>
        <h2 class="section-title">Crop Categories Overview</h2>
    </div>
    """, unsafe_allow_html=True)
    
    cols = st.columns(4)
    for i, (category, crops) in enumerate(list(CROP_CATEGORIES.items())[:8]):
        with cols[i % 4]:
            st.markdown(f"""
            <div class="category-card">
                <div class="category-name">{category}</div>
                <div class="category-count">{len(crops)} varieties</div>
            </div>
            """, unsafe_allow_html=True)


def render_crop_library():
    st.markdown("""
    <div class="section-header">
        <span class="section-icon">📚</span>
        <h2 class="section-title">Crop Library - 300+ Varieties</h2>
    </div>
    """, unsafe_allow_html=True)
    
    selected_category = st.selectbox("Select Category", list(CROP_CATEGORIES.keys()))
    
    if selected_category:
        crops = CROP_CATEGORIES[selected_category]
        st.markdown(f"### {selected_category} ({len(crops)} varieties)")
        
        cols = st.columns(5)
        for i, crop in enumerate(crops):
            with cols[i % 5]:
                icon = get_crop_icon(crop)
                st.markdown(f"""
                <div class="crop-item">
                    <span class="crop-icon">{icon}</span>
                    <span class="crop-name">{crop}</span>
                </div>
                """, unsafe_allow_html=True)


def render_crop_recommendation():
    st.markdown("""
    <div class="section-header">
        <span class="section-icon">🌾</span>
        <h2 class="section-title">AI Crop Recommendation System</h2>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("Enter your farm parameters to get personalized, AI-powered crop recommendations.")
    
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("#### 🧪 Soil Nutrients")
        nitrogen = st.slider("Nitrogen (N) kg/ha", 0, 140, 50, help="Nitrogen level in soil")
        phosphorus = st.slider("Phosphorus (P) kg/ha", 5, 145, 40, help="Phosphorus level")
        potassium = st.slider("Potassium (K) kg/ha", 5, 205, 40, help="Potassium level")
        ph = st.slider("Soil pH", 3.5, 10.0, 6.5, 0.1, help="Soil acidity/alkalinity")
    
    with col2:
        st.markdown("#### 🌡️ Environment")
        temperature = st.slider("Temperature (°C)", 8, 45, 25)
        humidity = st.slider("Humidity (%)", 14, 100, 60)
        soil_type = st.selectbox("Soil Type", SOIL_TYPES)
        season = st.selectbox("Season", SEASONS)
    
    with col3:
        st.markdown("#### 🌱 Crop Parameters")
        crop_duration = st.selectbox("Duration", CROP_DURATIONS)
        previous_crop = st.selectbox("Previous Crop", ['Fallow'] + ML_CROPS)
    
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    
    if st.button("🔍 Get AI Recommendation", use_container_width=True):
        crop_model, _ = get_models()
        
        input_data = {
            'N': nitrogen, 'P': phosphorus, 'K': potassium,
            'temperature': temperature, 'humidity': humidity, 'ph': ph,
            'soil_type': soil_type, 'season': season,
            'crop_duration': crop_duration, 'previous_crop': previous_crop
        }
        
        result = crop_model.predict(input_data)
        
        if result:
            col1, col2 = st.columns([2, 1])
            
            with col1:
                st.markdown(f"""
                <div class="result-success">
                    <div class="result-title">🎯 Recommended Crop</div>
                    <div class="result-value">{result['recommended_crop']}</div>
                </div>
                """, unsafe_allow_html=True)
                
                st.markdown("#### 📊 Top 3 Recommendations")
                for i, (crop, prob) in enumerate(result['top_3_crops'], 1):
                    prob_percent = prob * 100
                    colors = ['#4CAF50', '#8BC34A', '#CDDC39']
                    st.markdown(f"""
                    <div style="display: flex; align-items: center; margin: 0.5rem 0; padding: 0.5rem; 
                                background: {colors[i-1]}20; border-radius: 8px;">
                        <span style="font-weight: bold; width: 35px; color: {colors[i-1]};">#{i}</span>
                        <span style="flex: 1; font-weight: 500;">{crop}</span>
                        <div style="background: linear-gradient(90deg, {colors[i-1]} {prob_percent}%, #e0e0e0 {prob_percent}%); 
                                    height: 20px; width: 150px; border-radius: 10px;"></div>
                        <span style="margin-left: 10px; font-weight: 600;">{prob_percent:.1f}%</span>
                    </div>
                    """, unsafe_allow_html=True)
            
            with col2:
                labels = [crop for crop, _ in result['top_3_crops']]
                values = [prob for _, prob in result['top_3_crops']]
                
                fig = go.Figure(data=[go.Pie(
                    labels=labels, values=values,
                    hole=0.5,
                    marker_colors=['#4CAF50', '#8BC34A', '#CDDC39']
                )])
                fig.update_layout(
                    showlegend=True,
                    height=280,
                    margin=dict(t=20, b=20, l=20, r=20),
                    paper_bgcolor='rgba(0,0,0,0)',
                    plot_bgcolor='rgba(0,0,0,0)'
                )
                st.plotly_chart(fig, use_container_width=True)
            
            st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
            
            pdf_data = {
                'nitrogen': nitrogen, 'phosphorus': phosphorus, 'potassium': potassium,
                'temperature': temperature, 'humidity': humidity, 'ph': ph,
                'soil_type': soil_type, 'season': season, 'previous_crop': previous_crop,
                'recommended_crop': result['recommended_crop'],
                'top_3_crops': result['top_3_crops']
            }
            pdf_buffer = generate_crop_recommendation_pdf(pdf_data)
            
            st.markdown("### 📄 Export Report")
            st.download_button(
                label="📄 Download PDF Report",
                data=pdf_buffer,
                file_name="crop_recommendation_report.pdf",
                mime="application/pdf"
            )
            
            try:
                db = get_db()
                if db:
                    farm_data = FarmData(
                        nitrogen=nitrogen, phosphorus=phosphorus, potassium=potassium,
                        temperature=temperature, humidity=humidity, ph=ph,
                        soil_type=soil_type, previous_crop=previous_crop, season=season,
                        crop_duration=crop_duration, recommended_crop=result['recommended_crop']
                    )
                    db.add(farm_data)
                    db.commit()
                    db.close()
            except Exception:
                pass


def render_fertilizer_guide():
    st.markdown("""
    <div class="section-header">
        <span class="section-icon">🧪</span>
        <h2 class="section-title">Smart Fertilizer Planner</h2>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        selected_crop = st.selectbox("Select Crop", ALL_CROPS)
    
    with col2:
        fertilizer_type = st.radio("Fertilizer Type", ["Organic", "Non-Organic"], horizontal=True)
    
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    
    st.markdown("### 📅 Growth Stage Timeline")
    
    stage_colors = {
        'Seedling': ('#FFF9C4', '#F57F17', '🌱'),
        'Vegetative': ('#C8E6C9', '#2E7D32', '🌿'),
        'Flowering': ('#F8BBD0', '#C2185B', '🌸'),
        'Fruiting/Grain Filling': ('#FFE0B2', '#E65100', '🍎'),
        'Maturity': ('#D7CCC8', '#5D4037', '🌾')
    }
    
    cols = st.columns(5)
    for i, stage in enumerate(GROWTH_STAGES):
        with cols[i]:
            bg_color, text_color, icon = stage_colors[stage]
            st.markdown(f"""
            <div style="background: {bg_color}; padding: 1rem; border-radius: 12px; 
                        text-align: center; min-height: 90px;">
                <span style="font-size: 2rem;">{icon}</span><br>
                <span style="color: {text_color}; font-weight: 600; font-size: 0.8rem;">{stage}</span>
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    
    fertilizer_data = ORGANIC_FERTILIZERS if fertilizer_type == "Organic" else NON_ORGANIC_FERTILIZERS
    
    for stage in GROWTH_STAGES:
        fert = fertilizer_data[stage]
        bg_color, text_color, icon = stage_colors[stage]
        
        st.markdown(f"""
        <div class="pro-card" style="border-left: 4px solid {text_color};">
            <div style="display: flex; align-items: center; gap: 10px; margin-bottom: 1rem;">
                <span style="font-size: 1.5rem;">{icon}</span>
                <h4 style="margin: 0; color: #1B5E20;">{stage} Stage</h4>
            </div>
            <div style="display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 1rem;">
                <div>
                    <strong style="color: #666;">Fertilizer:</strong><br>
                    <span style="color: #2E7D32; font-weight: 500;">{fert['name']}</span>
                </div>
                <div>
                    <strong style="color: #666;">Application Rate:</strong><br>
                    <span style="color: #2E7D32; font-weight: 500;">{fert['rate']}</span>
                </div>
                <div>
                    <strong style="color: #666;">Method:</strong><br>
                    <span style="color: #2E7D32; font-weight: 500;">{fert['method']}</span>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    
    pdf_data = {
        'crop': selected_crop,
        'fertilizer_type': fertilizer_type,
        'schedule': fertilizer_data
    }
    pdf_buffer = generate_fertilizer_pdf(pdf_data)
    
    st.download_button(
        label="📄 Download Fertilizer Schedule PDF",
        data=pdf_buffer,
        file_name=f"fertilizer_schedule_{selected_crop}.pdf",
        mime="application/pdf"
    )


def render_enhanced_crop_diagram(main_crop, combo):
    fig, ax = plt.subplots(1, 1, figsize=(14, 10))
    ax.set_facecolor('#FAFAFA')
    
    ax.add_patch(Rectangle((0, 0), 500, 420, facecolor='#F5F5DC', edgecolor='#8B4513', linewidth=3))
    
    crop_settings = {
        'Maize': {'main_color': '#FFD54F', 'main_size': 18, 'companion_color': '#81C784', 'emoji': '🌽'},
        'Tomato': {'main_color': '#EF5350', 'main_size': 20, 'companion_color': '#81C784', 'emoji': '🍅'},
        'Rice': {'main_color': '#A5D6A7', 'main_size': 12, 'companion_color': '#64B5F6', 'emoji': '🌾'},
        'Cotton': {'main_color': '#E3F2FD', 'main_size': 22, 'companion_color': '#8BC34A', 'emoji': '☁️'},
        'Sugarcane': {'main_color': '#8BC34A', 'main_size': 15, 'companion_color': '#FFC107', 'emoji': '🎋'},
        'Wheat': {'main_color': '#FFD54F', 'main_size': 10, 'companion_color': '#FFAB91', 'emoji': '🌾'},
        'Potato': {'main_color': '#8D6E63', 'main_size': 16, 'companion_color': '#81C784', 'emoji': '🥔'},
        'Onion': {'main_color': '#CE93D8', 'main_size': 12, 'companion_color': '#FFCC80', 'emoji': '🧅'},
        'Mango': {'main_color': '#FF9800', 'main_size': 30, 'companion_color': '#4CAF50', 'emoji': '🥭'},
        'Banana': {'main_color': '#FFEB3B', 'main_size': 25, 'companion_color': '#8BC34A', 'emoji': '🍌'},
    }
    
    settings = crop_settings.get(main_crop, {
        'main_color': '#81C784', 'main_size': 18, 'companion_color': '#FFB74D', 'emoji': '🌱'
    })
    
    if main_crop in ['Rice']:
        water_rect = Rectangle((10, 10), 480, 350, alpha=0.3, color='#64B5F6')
        ax.add_patch(water_rect)
        
        for i in range(8):
            for j in range(12):
                x, y = j * 38 + 30, i * 42 + 30
                rect = FancyBboxPatch((x-12, y-15), 24, 30, 
                                       boxstyle="round,pad=0.02",
                                       facecolor=settings['main_color'], 
                                       edgecolor='#388E3C', linewidth=1.5)
                ax.add_patch(rect)
        
        for i in range(10):
            for j in range(15):
                x, y = j * 32 + 20, i * 35 + 20
                circle = Circle((x, y), 3, color='#4CAF50', alpha=0.6)
                ax.add_patch(circle)
        
        legend_items = [
            (30, 395, settings['main_color'], '🌾 Rice Paddy (20x15 cm)'),
            (30, 375, '#64B5F6', '💧 Water Level (5-7 cm)'),
            (30, 355, '#4CAF50', '🌿 Azolla Cover'),
        ]
        
    elif main_crop in ['Maize', 'Cotton', 'Sugarcane']:
        row_spacing = 70 if main_crop == 'Maize' else 90
        plant_spacing = 25 if main_crop == 'Maize' else 45
        
        for i in range(5):
            for j in range(7):
                x, y = j * row_spacing + 45, i * 75 + 50
                
                circle = Circle((x, y), settings['main_size'], 
                               color=settings['main_color'], ec='#5D4037', linewidth=2)
                ax.add_patch(circle)
                ax.annotate(settings['emoji'], (x, y), fontsize=14, ha='center', va='center')
        
        for i in range(5):
            for j in range(6):
                x, y = j * row_spacing + 80, i * 75 + 35
                circle = Circle((x, y), 8, color=settings['companion_color'], 
                               ec='#388E3C', linewidth=1.5)
                ax.add_patch(circle)
        
        legend_items = [
            (30, 395, settings['main_color'], f'{settings["emoji"]} {main_crop} (Main Crop)'),
            (30, 375, settings['companion_color'], f'🌿 Companion Crops'),
            (30, 355, '#8D6E63', f'📏 Spacing: {combo.get("spacing_main", "60x25 cm")}'),
        ]
        
    elif main_crop in ['Tomato', 'Chilli']:
        for i in range(5):
            for j in range(7):
                x, y = j * 65 + 50, i * 75 + 55
                
                circle = Circle((x, y), settings['main_size'], 
                               color=settings['main_color'], ec='#C62828', linewidth=2)
                ax.add_patch(circle)
                ax.annotate(settings['emoji'], (x, y), fontsize=16, ha='center', va='center')
        
        for i in range(5):
            for j in range(7):
                x, y = j * 65 + 75, i * 75 + 40
                circle = Circle((x, y), 6, color='#81C784', ec='#388E3C', linewidth=1)
                ax.add_patch(circle)
        
        for j in range(9):
            circle = Circle((j * 52 + 30, 395), 10, color='#FFB74D', ec='#F57C00', linewidth=2)
            ax.add_patch(circle)
            ax.annotate('🌼', (j * 52 + 30, 395), fontsize=10, ha='center', va='center')
        
        legend_items = [
            (30, 415, settings['main_color'], f'{settings["emoji"]} {main_crop} (60x45 cm)'),
            (230, 415, '#81C784', '🌿 Basil (companion)'),
            (400, 415, '#FFB74D', '🌼 Marigold (border)'),
        ]
        
    elif main_crop in ['Mango', 'Coconut', 'Banana']:
        main_spacing = 100 if main_crop == 'Banana' else 150
        
        for i in range(3):
            for j in range(4):
                x, y = j * main_spacing + 80, i * 120 + 80
                
                circle = Circle((x, y), settings['main_size'], 
                               color=settings['main_color'], ec='#5D4037', linewidth=3)
                ax.add_patch(circle)
                ax.annotate(settings['emoji'], (x, y), fontsize=20, ha='center', va='center')
        
        for i in range(4):
            for j in range(5):
                x, y = j * main_spacing * 0.8 + 60, i * 100 + 50
                if not any(abs(x - (jj * main_spacing + 80)) < 40 and abs(y - (ii * 120 + 80)) < 40 
                          for ii in range(3) for jj in range(4)):
                    circle = Circle((x, y), 8, color=settings['companion_color'], 
                                   ec='#388E3C', linewidth=1)
                    ax.add_patch(circle)
        
        legend_items = [
            (30, 395, settings['main_color'], f'{settings["emoji"]} {main_crop} (Main)'),
            (30, 375, settings['companion_color'], '🌱 Intercrops'),
            (30, 355, '#8D6E63', '📏 Multi-tier system'),
        ]
        
    else:
        for i in range(6):
            for j in range(8):
                x, y = j * 55 + 45, i * 60 + 50
                circle = Circle((x, y), settings['main_size'], 
                               color=settings['main_color'], ec='#388E3C', linewidth=2)
                ax.add_patch(circle)
                ax.annotate(settings['emoji'], (x, y), fontsize=12, ha='center', va='center')
        
        for i in range(6):
            for j in range(7):
                x, y = j * 55 + 72, i * 60 + 30
                circle = Circle((x, y), 7, color=settings['companion_color'], 
                               ec='#F57C00', linewidth=1)
                ax.add_patch(circle)
        
        legend_items = [
            (30, 395, settings['main_color'], f'{settings["emoji"]} {main_crop}'),
            (30, 375, settings['companion_color'], '🌸 Companion crops'),
        ]
    
    for x, y, color, text in legend_items:
        ax.add_patch(Rectangle((x - 5, y - 5), 10, 10, color=color, ec='#333'))
        ax.annotate(text, (x + 15, y), fontsize=10, va='center',
                   bbox=dict(boxstyle='round,pad=0.3', facecolor='white', edgecolor='#ddd'))
    
    ax.set_xlim(-10, 510)
    ax.set_ylim(-10, 430)
    ax.set_aspect('equal')
    ax.set_xlabel('Field Width (cm)', fontsize=11, color='#333')
    ax.set_ylabel('Field Length (cm)', fontsize=11, color='#333')
    ax.set_title(f'🌱 Multi-Cropping Layout: {main_crop} with Companions', 
                fontsize=14, fontweight='bold', color='#1B5E20', pad=15)
    ax.grid(True, alpha=0.2, linestyle='--', color='#888')
    
    for spine in ax.spines.values():
        spine.set_color('#8B4513')
        spine.set_linewidth(2)
    
    return fig


def render_multi_cropping():
    st.markdown("""
    <div class="section-header">
        <span class="section-icon">🌻</span>
        <h2 class="section-title">Multi-Cropping Hub</h2>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("Maximize farm income with scientifically-designed companion planting systems.")
    
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    
    available_crops = list(EXTENDED_MULTI_CROP_COMBINATIONS.keys())
    selected_main_crop = st.selectbox("🌱 Select Main Crop", available_crops)
    
    if selected_main_crop:
        combo = EXTENDED_MULTI_CROP_COMBINATIONS[selected_main_crop]
        
        st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
        
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.markdown(f"""
            <div class="pro-card">
                <div class="pro-card-header">
                    <span class="pro-card-icon">{combo.get('icon', '🌱')}</span>
                    <h3 class="pro-card-title">Main Crop: {selected_main_crop}</h3>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("#### 🌿 Companion Crops")
            for companion in combo['companions']:
                st.markdown(f"""
                <div class="companion-card">
                    <span class="companion-icon">🌱</span>
                    <span class="companion-name">{companion}</span>
                </div>
                """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div class="spacing-card">
                <h4 style="color: #E65100; margin-top: 0;">📏 Spacing Requirements</h4>
                <p><strong>Main Crop:</strong> {combo['spacing_main']}</p>
                <p><strong>Companions:</strong> {combo['spacing_companion']}</p>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown(f"""
            <div class="benefit-card">
                <div class="benefit-title">✨ Benefits</div>
                <div class="benefit-text">{combo['benefits']}</div>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown(f"""
            <div class="irrigation-card">
                <h4 style="color: #0277BD; margin-top: 0;">🚿 Irrigation Schedule</h4>
                <p>{combo['irrigation']}</p>
            </div>
            """, unsafe_allow_html=True)
            
            if 'yield_boost' in combo:
                st.markdown(f"""
                <div class="success-box">
                    <h4 style="color: #2E7D32; margin-top: 0;">📈 Expected Yield Boost</h4>
                    <p style="font-size: 1.5rem; font-weight: bold; color: #1B5E20;">{combo['yield_boost']}</p>
                </div>
                """, unsafe_allow_html=True)
        
        st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
        
        st.markdown("### 📐 Visual Crop Spacing Diagram")
        
        fig = render_enhanced_crop_diagram(selected_main_crop, combo)
        st.pyplot(fig)
        plt.close()
        
        st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
        
        pdf_data = {
            'main_crop': selected_main_crop,
            'companions': combo['companions'],
            'spacing_main': combo['spacing_main'],
            'spacing_companion': combo['spacing_companion'],
            'benefits': combo['benefits'],
            'irrigation': combo['irrigation'],
            'yield_boost': combo.get('yield_boost', 'N/A')
        }
        pdf_buffer = generate_multi_crop_pdf(pdf_data)
        
        st.download_button(
            label="📄 Download Multi-Cropping Plan PDF",
            data=pdf_buffer,
            file_name=f"multicrop_plan_{selected_main_crop}.pdf",
            mime="application/pdf"
        )


def render_yield_prediction():
    st.markdown("""
    <div class="section-header">
        <span class="section-icon">📊</span>
        <h2 class="section-title">AI Yield Forecaster</h2>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("#### 🧪 Soil Parameters")
        nitrogen = st.slider("Nitrogen (N)", 0, 140, 60, key="yield_n")
        phosphorus = st.slider("Phosphorus (P)", 5, 145, 50, key="yield_p")
        potassium = st.slider("Potassium (K)", 5, 205, 50, key="yield_k")
        ph = st.slider("pH Level", 3.5, 10.0, 6.5, 0.1, key="yield_ph")
    
    with col2:
        st.markdown("#### 🌡️ Environment")
        temperature = st.slider("Temperature (°C)", 8, 45, 28, key="yield_temp")
        humidity = st.slider("Humidity (%)", 14, 100, 65, key="yield_hum")
        soil_type = st.selectbox("Soil Type", SOIL_TYPES, key="yield_soil")
        season = st.selectbox("Season", SEASONS, key="yield_season")
    
    with col3:
        st.markdown("#### 🌾 Crop Details")
        crop = st.selectbox("Target Crop", ML_CROPS, key="yield_crop")
        crop_duration = st.selectbox("Duration", CROP_DURATIONS, key="yield_dur")
        previous_crop = st.selectbox("Previous Crop", ['Fallow'] + ML_CROPS, key="yield_prev")
    
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    
    if st.button("📈 Predict Yield", use_container_width=True):
        _, yield_model = get_models()
        
        input_data = {
            'N': nitrogen, 'P': phosphorus, 'K': potassium,
            'temperature': temperature, 'humidity': humidity, 'ph': ph,
            'soil_type': soil_type, 'season': season,
            'crop_duration': crop_duration, 'previous_crop': previous_crop,
            'crop': crop
        }
        
        predicted_yield = yield_model.predict(input_data)
        
        if predicted_yield:
            col1, col2, col3 = st.columns([1, 2, 1])
            
            with col2:
                st.markdown(f"""
                <div class="result-success">
                    <div class="result-title">🌾 Predicted Yield</div>
                    <div class="result-value">{predicted_yield} q/ha</div>
                    <p style="margin-top: 0.5rem; color: #388E3C;">For {crop} in {season}</p>
                </div>
                """, unsafe_allow_html=True)
            
            st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
            
            col1, col2 = st.columns(2)
            
            with col1:
                fig = go.Figure(data=[go.Bar(
                    x=['Nitrogen', 'Phosphorus', 'Potassium'],
                    y=[nitrogen, phosphorus, potassium],
                    marker_color=['#4CAF50', '#81C784', '#A5D6A7'],
                    text=[f'{nitrogen}', f'{phosphorus}', f'{potassium}'],
                    textposition='auto'
                )])
                fig.update_layout(
                    title='Current Nutrient Levels (kg/ha)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    plot_bgcolor='rgba(0,0,0,0)',
                    height=300
                )
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                categories = ['N', 'P', 'K', 'pH', 'Humidity']
                current = [nitrogen/140*100, phosphorus/145*100, potassium/205*100, 
                          (ph-3.5)/6.5*100, humidity]
                
                fig = go.Figure(data=go.Scatterpolar(
                    r=current,
                    theta=categories,
                    fill='toself',
                    fillcolor='rgba(76, 175, 80, 0.3)',
                    line_color='#4CAF50'
                ))
                fig.update_layout(
                    polar=dict(radialaxis=dict(visible=True, range=[0, 100])),
                    title='Conditions Overview',
                    paper_bgcolor='rgba(0,0,0,0)',
                    height=300
                )
                st.plotly_chart(fig, use_container_width=True)
            
            pdf_data = {
                'crop': crop, 'predicted_yield': predicted_yield,
                'nitrogen': nitrogen, 'phosphorus': phosphorus, 'potassium': potassium,
                'temperature': temperature, 'humidity': humidity, 'ph': ph,
                'soil_type': soil_type, 'season': season
            }
            pdf_buffer = generate_yield_prediction_pdf(pdf_data)
            
            st.download_button(
                label="📄 Download Yield Report PDF",
                data=pdf_buffer,
                file_name=f"yield_prediction_{crop}.pdf",
                mime="application/pdf"
            )


def render_irrigation_planner():
    st.markdown("""
    <div class="section-header">
        <span class="section-icon">🚿</span>
        <h2 class="section-title">Smart Irrigation Manager</h2>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        crop = st.selectbox("Select Crop", ALL_CROPS, key="irr_crop")
        soil_type = st.selectbox("Soil Type", SOIL_TYPES, key="irr_soil")
        area = st.number_input("Field Area (hectares)", 0.1, 100.0, 1.0, 0.1)
    
    with col2:
        temperature = st.slider("Temperature (°C)", 10, 45, 30, key="irr_temp")
        humidity = st.slider("Humidity (%)", 10, 100, 50, key="irr_hum")
        growth_stage = st.selectbox("Growth Stage", GROWTH_STAGES)
    
    if st.button("💧 Calculate Water Requirements", use_container_width=True):
        base_water = 5.0
        
        temp_factor = 1.4 if temperature > 35 else 1.2 if temperature > 30 else 1.0
        hum_factor = 1.3 if humidity < 40 else 1.1 if humidity < 60 else 0.9
        
        soil_factors = {'Sandy': 1.3, 'Sandy Loam': 1.2, 'Loam': 1.0, 
                       'Silt': 0.95, 'Clay Loam': 0.9, 'Clay': 0.85}
        soil_factor = soil_factors.get(soil_type, 1.0)
        
        stage_factors = {'Germination': 0.5, 'Seedling': 0.7, 'Vegetative': 1.0, 
                        'Flowering': 1.3, 'Fruiting/Grain Filling': 1.2, 
                        'Maturity': 0.6, 'Harvest': 0.3}
        stage_factor = stage_factors.get(growth_stage, 1.0)
        
        daily_water = base_water * temp_factor * hum_factor * soil_factor * stage_factor
        total_water = daily_water * area
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown(f"""
            <div class="metric-item">
                <div class="metric-value">{daily_water:.1f} mm</div>
                <div class="metric-label">Daily per Hectare</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div class="metric-item">
                <div class="metric-value">{total_water:.1f} kL</div>
                <div class="metric-label">Total Daily Volume</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            freq = "Daily" if daily_water > 6 else "Every 2-3 days" if daily_water > 4 else "Every 3-5 days"
            st.markdown(f"""
            <div class="metric-item">
                <div class="metric-value">{freq}</div>
                <div class="metric-label">Irrigation Frequency</div>
            </div>
            """, unsafe_allow_html=True)


def render_crop_rotation():
    st.markdown("""
    <div class="section-header">
        <span class="section-icon">🔄</span>
        <h2 class="section-title">Crop Rotation Planner</h2>
    </div>
    """, unsafe_allow_html=True)
    
    st.info("Plan your crop rotation for optimal soil health and yield sustainability.")
    
    rotation_plans = {
        'Cereal-Legume': ['Rice', 'Wheat', 'Green Gram', 'Rice'],
        'Cash Crop': ['Cotton', 'Wheat', 'Groundnut', 'Cotton'],
        'Vegetable': ['Tomato', 'Cabbage', 'Onion', 'Potato'],
        'Mixed': ['Maize', 'Chickpea', 'Sunflower', 'Wheat'],
    }
    
    plan_type = st.selectbox("Select Rotation Type", list(rotation_plans.keys()))
    
    if plan_type:
        st.markdown(f"### {plan_type} Rotation Plan")
        crops = rotation_plans[plan_type]
        cols = st.columns(4)
        
        for i, crop in enumerate(crops):
            with cols[i]:
                season = ['Kharif', 'Rabi', 'Zaid', 'Kharif'][i]
                icon = get_crop_icon(crop)
                st.markdown(f"""
                <div class="pro-card" style="text-align: center;">
                    <span style="font-size: 2.5rem;">{icon}</span>
                    <h4 style="color: #1B5E20;">{crop}</h4>
                    <p style="color: #666;">Year {i+1} - {season}</p>
                </div>
                """, unsafe_allow_html=True)


def render_economic_analysis():
    st.markdown("""
    <div class="section-header">
        <span class="section-icon">💰</span>
        <h2 class="section-title">Economic Analysis</h2>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        crop = st.selectbox("Select Crop", ALL_CROPS)
        area = st.number_input("Area (hectares)", 0.1, 100.0, 1.0, 0.1)
        expected_yield = st.number_input("Expected Yield (q/ha)", 5.0, 100.0, 30.0, 1.0)
    
    with col2:
        market_price = st.number_input("Market Price (₹/quintal)", 500, 10000, 2000, 100)
        input_cost = st.number_input("Input Cost (₹/hectare)", 5000, 100000, 25000, 1000)
    
    if st.button("📊 Calculate Economics", use_container_width=True):
        total_yield = expected_yield * area
        gross_income = total_yield * market_price
        total_cost = input_cost * area
        net_profit = gross_income - total_cost
        roi = (net_profit / total_cost) * 100 if total_cost > 0 else 0
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Total Yield", f"{total_yield:.1f} q")
        with col2:
            st.metric("Gross Income", f"₹{gross_income:,.0f}")
        with col3:
            st.metric("Net Profit", f"₹{net_profit:,.0f}")
        with col4:
            st.metric("ROI", f"{roi:.1f}%")


def render_pest_disease():
    st.markdown("""
    <div class="section-header">
        <span class="section-icon">🐛</span>
        <h2 class="section-title">Pest & Disease Management</h2>
    </div>
    """, unsafe_allow_html=True)
    
    crop = st.selectbox("Select Crop", ALL_CROPS)
    
    pest_data = {
        'Rice': [('Stem Borer', 'Pheromone traps, Trichogramma release'),
                ('Brown Plant Hopper', 'Avoid excess nitrogen, use resistant varieties'),
                ('Blast', 'Seed treatment, fungicide spray')],
        'Wheat': [('Aphids', 'Neem oil spray, ladybug release'),
                 ('Rust', 'Resistant varieties, fungicide'),
                 ('Termites', 'Chlorpyrifos application')],
        'Tomato': [('Fruit Borer', 'Pheromone traps, Bt spray'),
                  ('Early Blight', 'Crop rotation, fungicide'),
                  ('Whitefly', 'Yellow sticky traps, neem spray')],
    }
    
    pests = pest_data.get(crop, [('General Pests', 'Integrated Pest Management')])
    
    for pest, solution in pests:
        st.markdown(f"""
        <div class="pro-card">
            <h4 style="color: #D32F2F;">🐛 {pest}</h4>
            <p><strong>Management:</strong> {solution}</p>
        </div>
        """, unsafe_allow_html=True)


def render_farm_overview():
    st.markdown("""
    <div class="section-header">
        <span class="section-icon">📈</span>
        <h2 class="section-title">Analytics Center</h2>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="metric-grid">
        <div class="metric-item">
            <div class="metric-value">300+</div>
            <div class="metric-label">Crop Varieties</div>
        </div>
        <div class="metric-item">
            <div class="metric-value">20</div>
            <div class="metric-label">Categories</div>
        </div>
        <div class="metric-item">
            <div class="metric-value">99.77%</div>
            <div class="metric-label">ML Accuracy</div>
        </div>
        <div class="metric-item">
            <div class="metric-value">12</div>
            <div class="metric-label">Soil Types</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 📊 Seasonal Crop Distribution")
        
        fig = go.Figure()
        seasons = ['Kharif', 'Rabi', 'Zaid']
        crops_per_season = [8, 7, 5]
        
        fig.add_trace(go.Bar(
            x=seasons,
            y=crops_per_season,
            marker_color=['#4CAF50', '#2196F3', '#FF9800'],
            text=crops_per_season,
            textposition='auto'
        ))
        fig.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            height=300
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown("### 🥧 Crop Category Distribution")
        
        category_names = list(CROP_CATEGORIES.keys())[:6]
        category_counts = [len(CROP_CATEGORIES[c]) for c in category_names]
        
        fig = go.Figure(data=[go.Pie(
            labels=category_names,
            values=category_counts,
            hole=0.4,
            marker_colors=['#4CAF50', '#81C784', '#A5D6A7', '#C8E6C9', '#E8F5E9', '#F1F8E9']
        )])
        fig.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            height=300
        )
        st.plotly_chart(fig, use_container_width=True)
    
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    
    pdf_data = {
        'total_crops': f'{len(EXTENDED_CROPS)}',
        'soil_types': '12',
        'accuracy': '99.77%',
        'seasons': '4'
    }
    pdf_buffer = generate_farm_overview_pdf(pdf_data)
    
    st.download_button(
        label="📄 Download Farm Overview PDF",
        data=pdf_buffer,
        file_name="farm_overview_report.pdf",
        mime="application/pdf"
    )


if __name__ == "__main__":
    main()
