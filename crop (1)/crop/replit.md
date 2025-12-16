# AgriSmart Pro - Precision Agriculture Platform

## Overview
A comprehensive precision agriculture web application built with Streamlit that uses machine learning (Random Forest algorithm with 99.77% accuracy) for crop recommendations, yield predictions, and fertilizer guidance. The platform features a professional design with 300+ crop varieties and PDF export capabilities.

## Recent Changes (December 2024)
- **Expanded to 300+ crop varieties** across 21 categories (cereals, pulses, vegetables, fruits, spices, herbs, etc.)
- **Professional redesign** with modern header, footer, and card-based layout
- **Enhanced multi-cropping visuals** with detailed spacing diagrams using matplotlib
- **PDF export functionality** for all reports (crop recommendations, fertilizer schedules, multi-crop plans, yield predictions)
- **New Crop Library page** to browse all varieties by category

## Key Features
- **Crop Advisor**: AI-powered crop selection based on soil parameters (N, P, K, pH), environmental conditions, soil type, previous crop, season, and crop duration
- **Fertilizer Planner**: Organic vs non-organic fertilizer recommendations for each growth stage with PDF export
- **Multi-Cropping Hub**: Compatible crop combinations with enhanced visual spacing diagrams, companion crop cards, and yield boost information
- **Yield Forecaster**: ML-based yield predictions with interactive charts
- **Irrigation Manager**: Water management optimization based on crop, soil, and weather
- **Crop Rotation Planner**: Multi-year rotation planning
- **Economic Analysis**: ROI calculations and profit forecasting
- **Pest & Disease**: Common pest identification and management
- **Analytics Center**: Comprehensive farm health metrics and analytics with PDF reports
- **Crop Library**: Browse 300+ crop varieties across 21 categories

## Project Structure
```
├── app.py                 # Main Streamlit application (professional redesign)
├── database.py            # SQLAlchemy database models and PostgreSQL connection
├── ml_models.py           # Random Forest ML models for predictions
├── crop_database.py       # Extended crop database with 300+ varieties
├── pdf_generator.py       # ReportLab-based PDF report generation
├── pyproject.toml         # Python dependencies
├── attached_assets/       # Training data and research documentation
│   └── crop_recommendation_with_project_*.csv  # ML training data
└── replit.md             # This documentation file
```

## Technical Stack
- **Frontend**: Streamlit with custom CSS (professional green theme)
- **ML**: scikit-learn Random Forest (99.77% accuracy)
- **Database**: PostgreSQL with SQLAlchemy ORM
- **Visualization**: Plotly (interactive charts) and Matplotlib (crop spacing diagrams)
- **PDF Generation**: ReportLab library
- **Data Processing**: Pandas and NumPy

## Database Schema
- **FarmData**: Stores farm parameters and crop recommendations
- **FertilizerRecommendation**: Fertilizer application records
- **MultiCropPlan**: Multi-cropping configurations
- **CropHistory**: Historical crop and yield data

## Crop Categories (21 total, 300+ varieties)
1. Cereals & Grains (20 varieties)
2. Pulses & Legumes (25 varieties)
3. Vegetables - Leafy (25 varieties)
4. Vegetables - Root (25 varieties)
5. Vegetables - Fruit (25 varieties)
6. Vegetables - Cruciferous (9 varieties)
7. Fruits - Tropical (28 varieties)
8. Fruits - Citrus (16 varieties)
9. Fruits - Temperate (19 varieties)
10. Fruits - Berries (15 varieties)
11. Fruits - Melons (12 varieties)
12. Oilseeds (18 varieties)
13. Fiber Crops (12 varieties)
14. Spices (25 varieties)
15. Herbs (19 varieties)
16. Beverage Crops (6 varieties)
17. Sugar Crops (7 varieties)
18. Fodder Crops (14 varieties)
19. Medicinal Crops (18 varieties)
20. Flowers (17 varieties)
21. Nuts (12 varieties)

## Running the Application
```bash
streamlit run app.py --server.port=5000 --server.address=0.0.0.0 --server.headless=true
```

## User Preferences
- Professional green color scheme with modern card-based layout
- Multi-page navigation with sidebar
- Interactive visualizations with Plotly
- Enhanced crop spacing diagrams with matplotlib
- PDF export for all reports
- Organic and non-organic fertilizer options
