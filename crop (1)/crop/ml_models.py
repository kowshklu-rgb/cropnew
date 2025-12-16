import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.preprocessing import LabelEncoder
import pickle
import os

CROPS = ['Rice', 'Wheat', 'Maize', 'Cotton', 'Sugarcane', 'Groundnut', 'Soybean', 
         'Sunflower', 'Tomato', 'Potato', 'Onion', 'Chilli', 'Cabbage', 'Cauliflower',
         'Carrot', 'Beans', 'Peas', 'Cucumber', 'Watermelon', 'Mango']

SOIL_TYPES = ['Clay', 'Loam', 'Sandy', 'Silt', 'Clay Loam', 'Sandy Loam']
SEASONS = ['Kharif (Monsoon)', 'Rabi (Winter)', 'Zaid (Summer)']
CROP_DURATIONS = ['Short-term (< 4 months)', 'Long-term (> 4 months)']

GROWTH_STAGES = ['Seedling', 'Vegetative', 'Flowering', 'Fruiting/Grain Filling', 'Maturity']

ORGANIC_FERTILIZERS = {
    'Seedling': {'name': 'Vermicompost', 'rate': '2-3 kg/10 sq.m', 'method': 'Mix with soil before transplanting'},
    'Vegetative': {'name': 'Neem Cake + Cow Dung', 'rate': '500g neem cake + 5kg cow dung/10 sq.m', 'method': 'Side dressing around plants'},
    'Flowering': {'name': 'Fish Emulsion + Bone Meal', 'rate': '2L fish emulsion + 200g bone meal/10 sq.m', 'method': 'Dilute and apply as foliar spray'},
    'Fruiting/Grain Filling': {'name': 'Seaweed Extract + Wood Ash', 'rate': '1L seaweed + 500g wood ash/10 sq.m', 'method': 'Foliar application and soil drench'},
    'Maturity': {'name': 'Compost Tea', 'rate': '5L/10 sq.m', 'method': 'Light soil application to maintain nutrients'}
}

NON_ORGANIC_FERTILIZERS = {
    'Seedling': {'name': 'DAP (Di-Ammonium Phosphate)', 'rate': '100-150g/10 sq.m', 'method': 'Apply in furrows before planting'},
    'Vegetative': {'name': 'Urea + MOP', 'rate': '150g Urea + 100g MOP/10 sq.m', 'method': 'Split application - broadcast and irrigate'},
    'Flowering': {'name': 'NPK 10-26-26', 'rate': '200g/10 sq.m', 'method': 'Side dressing near root zone'},
    'Fruiting/Grain Filling': {'name': 'Potassium Sulphate + Micronutrients', 'rate': '150g KSO4 + foliar micro spray/10 sq.m', 'method': 'Soil application + foliar spray'},
    'Maturity': {'name': 'Light NPK 0-0-50', 'rate': '100g/10 sq.m', 'method': 'Minimal application for final growth'}
}

MULTI_CROP_COMBINATIONS = {
    'Rice': {
        'companions': ['Azolla (green manure)', 'Fish (Integrated farming)'],
        'spacing_main': '20x15 cm',
        'spacing_companion': 'Continuous cover / 1 fish per 2 sq.m',
        'benefits': 'Nitrogen fixation, additional protein source, pest control',
        'irrigation': 'Maintain 5-7 cm water depth, drain before harvest'
    },
    'Maize': {
        'companions': ['Beans', 'Pumpkin', 'Squash'],
        'spacing_main': '60x25 cm',
        'spacing_companion': 'Beans: between rows, Pumpkin: 2m apart at field edges',
        'benefits': 'Three Sisters method - nitrogen fixation, ground cover, vertical space use',
        'irrigation': 'Drip irrigation every 3-4 days, 2-3 L per plant'
    },
    'Sugarcane': {
        'companions': ['Onion', 'Garlic', 'Coriander', 'Potato'],
        'spacing_main': '90x45 cm',
        'spacing_companion': 'Inter-row planting at 15cm spacing',
        'benefits': 'Early income, weed suppression, efficient land use',
        'irrigation': 'Furrow irrigation weekly, companions benefit from residual moisture'
    },
    'Cotton': {
        'companions': ['Groundnut', 'Soybean', 'Black gram'],
        'spacing_main': '90x60 cm',
        'spacing_companion': '30x10 cm between cotton rows',
        'benefits': 'Nitrogen fixation, soil health, additional oil/pulse income',
        'irrigation': 'Alternate row irrigation, 5-7 day interval'
    },
    'Tomato': {
        'companions': ['Basil', 'Marigold', 'Carrot', 'Onion'],
        'spacing_main': '60x45 cm',
        'spacing_companion': 'Basil: 30cm from tomato, Marigold: border planting',
        'benefits': 'Pest repellent, pollinator attraction, flavor enhancement',
        'irrigation': 'Drip irrigation daily, 1.5-2 L per plant'
    },
    'Wheat': {
        'companions': ['Mustard', 'Chickpea', 'Lentil'],
        'spacing_main': '22.5 cm row spacing',
        'spacing_companion': 'Every 4th row or border planting',
        'benefits': 'Additional oilseed/pulse crop, biodiversity, risk distribution',
        'irrigation': 'Flood irrigation at critical stages (CRI, jointing, flowering)'
    },
    'Potato': {
        'companions': ['Beans', 'Cabbage', 'Marigold', 'Horseradish'],
        'spacing_main': '60x20 cm',
        'spacing_companion': 'Beans in alternate rows, Marigold as border',
        'benefits': 'Pest deterrent, space optimization, soil nitrogen',
        'irrigation': 'Ridge irrigation every 7-10 days, avoid waterlogging'
    },
    'Groundnut': {
        'companions': ['Sunflower', 'Maize', 'Sorghum'],
        'spacing_main': '30x10 cm',
        'spacing_companion': 'Tall crops at 2:6 or 2:8 row ratio',
        'benefits': 'Windbreak, additional oilseed income, erosion control',
        'irrigation': 'Sprinkler or drip, maintain soil moisture 50-60%'
    },
    'Onion': {
        'companions': ['Carrot', 'Lettuce', 'Beet', 'Tomato'],
        'spacing_main': '15x10 cm',
        'spacing_companion': 'Alternating beds or rows',
        'benefits': 'Pest confusion, efficient space use, harvest timing diversity',
        'irrigation': 'Light frequent irrigation, drip preferred'
    },
    'Cabbage': {
        'companions': ['Celery', 'Onion', 'Dill', 'Chamomile'],
        'spacing_main': '45x45 cm',
        'spacing_companion': 'Border and inter-row planting',
        'benefits': 'Pest repellent, beneficial insect attraction',
        'irrigation': 'Consistent moisture, drip or sprinkler every 2-3 days'
    }
}

def generate_training_data(n_samples=2000):
    np.random.seed(42)
    
    data = {
        'N': np.random.uniform(0, 140, n_samples),
        'P': np.random.uniform(5, 145, n_samples),
        'K': np.random.uniform(5, 205, n_samples),
        'temperature': np.random.uniform(8, 45, n_samples),
        'humidity': np.random.uniform(14, 100, n_samples),
        'ph': np.random.uniform(3.5, 10, n_samples),
        'soil_type': np.random.choice(SOIL_TYPES, n_samples),
        'season': np.random.choice(SEASONS, n_samples),
        'crop_duration': np.random.choice(CROP_DURATIONS, n_samples),
        'previous_crop': np.random.choice(CROPS + ['Fallow'], n_samples)
    }
    
    crops = []
    yields = []
    
    for i in range(n_samples):
        n, p, k = data['N'][i], data['P'][i], data['K'][i]
        temp, hum, ph = data['temperature'][i], data['humidity'][i], data['ph'][i]
        soil = data['soil_type'][i]
        season = data['season'][i]
        duration = data['crop_duration'][i]
        
        if temp > 25 and hum > 60 and season == 'Kharif (Monsoon)':
            if n > 80 and soil in ['Clay', 'Clay Loam']:
                crop = 'Rice'
            elif n > 60 and p > 40:
                crop = 'Maize'
            else:
                crop = 'Cotton'
        elif temp < 25 and season == 'Rabi (Winter)':
            if n > 100 and ph > 6:
                crop = 'Wheat'
            elif p > 60:
                crop = 'Potato'
            else:
                crop = 'Peas'
        elif season == 'Zaid (Summer)':
            if temp > 30:
                crop = 'Watermelon'
            elif hum < 50:
                crop = 'Sunflower'
            else:
                crop = 'Cucumber'
        else:
            if soil in ['Sandy', 'Sandy Loam'] and temp > 20:
                crop = 'Groundnut'
            elif k > 100:
                crop = 'Sugarcane'
            elif duration == 'Short-term (< 4 months)':
                crop = np.random.choice(['Tomato', 'Onion', 'Cabbage', 'Carrot'])
            else:
                crop = np.random.choice(['Mango', 'Sugarcane', 'Cotton'])
        
        base_yield = 25
        yield_val = base_yield + (n/10) + (p/15) + (k/20) - abs(ph - 6.5) * 3
        yield_val += np.random.normal(0, 5)
        yield_val = max(10, min(60, yield_val))
        
        crops.append(crop)
        yields.append(yield_val)
    
    data['crop'] = crops
    data['yield'] = yields
    
    return pd.DataFrame(data)

class CropRecommendationModel:
    def __init__(self):
        self.model = RandomForestClassifier(n_estimators=200, max_depth=15, random_state=42)
        self.label_encoders = {}
        self.is_trained = False
    
    def train(self, df):
        categorical_cols = ['soil_type', 'season', 'crop_duration', 'previous_crop']
        df_encoded = df.copy()
        
        for col in categorical_cols:
            self.label_encoders[col] = LabelEncoder()
            df_encoded[col] = self.label_encoders[col].fit_transform(df[col])
        
        self.crop_encoder = LabelEncoder()
        y = self.crop_encoder.fit_transform(df['crop'])
        
        feature_cols = ['N', 'P', 'K', 'temperature', 'humidity', 'ph', 
                       'soil_type', 'season', 'crop_duration', 'previous_crop']
        X = df_encoded[feature_cols]
        
        self.model.fit(X, y)
        self.is_trained = True
        self.feature_cols = feature_cols
    
    def predict(self, input_data):
        if not self.is_trained:
            return None
        
        df = pd.DataFrame([input_data])
        for col in ['soil_type', 'season', 'crop_duration', 'previous_crop']:
            if col in self.label_encoders:
                try:
                    df[col] = self.label_encoders[col].transform(df[col])
                except ValueError:
                    df[col] = 0
        
        X = df[self.feature_cols]
        prediction = self.model.predict(X)
        probabilities = self.model.predict_proba(X)[0]
        
        top_indices = np.argsort(probabilities)[-3:][::-1]
        top_crops = self.crop_encoder.inverse_transform(top_indices)
        top_probs = probabilities[top_indices]
        
        return {
            'recommended_crop': self.crop_encoder.inverse_transform(prediction)[0],
            'top_3_crops': list(zip(top_crops, top_probs))
        }

class YieldPredictionModel:
    def __init__(self):
        self.model = RandomForestRegressor(n_estimators=200, max_depth=15, random_state=42)
        self.label_encoders = {}
        self.is_trained = False
    
    def train(self, df):
        categorical_cols = ['soil_type', 'season', 'crop_duration', 'previous_crop', 'crop']
        df_encoded = df.copy()
        
        for col in categorical_cols:
            self.label_encoders[col] = LabelEncoder()
            df_encoded[col] = self.label_encoders[col].fit_transform(df[col])
        
        feature_cols = ['N', 'P', 'K', 'temperature', 'humidity', 'ph', 
                       'soil_type', 'season', 'crop_duration', 'previous_crop', 'crop']
        X = df_encoded[feature_cols]
        y = df['yield']
        
        self.model.fit(X, y)
        self.is_trained = True
        self.feature_cols = feature_cols
    
    def predict(self, input_data):
        if not self.is_trained:
            return None
        
        df = pd.DataFrame([input_data])
        for col in ['soil_type', 'season', 'crop_duration', 'previous_crop', 'crop']:
            if col in self.label_encoders:
                try:
                    df[col] = self.label_encoders[col].transform(df[col])
                except ValueError:
                    df[col] = 0
        
        X = df[self.feature_cols]
        prediction = self.model.predict(X)[0]
        
        return round(prediction, 2)

def get_fertilizer_recommendation(crop, stage, fertilizer_type='organic'):
    if fertilizer_type.lower() == 'organic':
        fert = ORGANIC_FERTILIZERS.get(stage, ORGANIC_FERTILIZERS['Vegetative'])
    else:
        fert = NON_ORGANIC_FERTILIZERS.get(stage, NON_ORGANIC_FERTILIZERS['Vegetative'])
    
    return {
        'crop': crop,
        'stage': stage,
        'type': fertilizer_type,
        'fertilizer_name': fert['name'],
        'application_rate': fert['rate'],
        'application_method': fert['method']
    }

def get_multi_crop_recommendation(main_crop):
    if main_crop in MULTI_CROP_COMBINATIONS:
        return MULTI_CROP_COMBINATIONS[main_crop]
    return None

crop_model = None
yield_model = None

def initialize_models():
    global crop_model, yield_model
    
    df = generate_training_data(2000)
    
    crop_model = CropRecommendationModel()
    crop_model.train(df)
    
    yield_model = YieldPredictionModel()
    yield_model.train(df)
    
    return crop_model, yield_model

def get_models():
    global crop_model, yield_model
    if crop_model is None or yield_model is None:
        initialize_models()
    return crop_model, yield_model
