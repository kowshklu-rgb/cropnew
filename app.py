from flask import Flask, request, jsonify
import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
import pickle

app = Flask(__name__)

# Load the model and scaler
with open('model.pkl', 'rb') as file:
    model = pickle.load(file)

with open('scaler.pkl', 'rb') as file:
    scaler = pickle.load(file)

crop_dict = {
    'rice': 1, 'maize': 2, 'jute': 3, 'cotton': 4, 'coconut': 5,
    'papaya': 6, 'orange': 7, 'apple': 8, 'muskmelon': 9, 'watermelon': 10,
    'grapes': 11, 'mango': 12, 'banana': 13, 'pomegranate': 14,
    'lentil': 15, 'blackgram': 16, 'mungbean': 17, 'mothbeans': 18,
    'pigeonpeas': 19, 'kidneybeans': 20, 'chickpea': 21, 'coffee': 22,
    'groundnut': 23, 'wheat': 24, 'onion': 25, 'barley': 26, 'clover': 27,
    'oats': 28
}

soil_dict = {
    'Clayey': 1, 'Sandy': 2, 'Loam': 3, 'Silty': 4, 'Peaty': 5,
    'Saline': 6, 'Red': 7, 'Black': 8, 'Alluvial': 9
}

season_dict = {
    'Kharif': 1, 'Rabi': 2
}

def recommendation(N, P, K, temperature, humidity, ph, rainfall, soil, prev_crop, prev_duration, rec_duration, season):
    soil_num = soil_dict.get(soil, -1)
    prev_crop_num = crop_dict.get(prev_crop.lower(), -1)
    season_num = season_dict.get(season, -1)
    prev_duration_num = 1 if prev_duration.lower() == 'long' else 0
    rec_duration_num = 1 if rec_duration.lower() == 'long' else 0

    if soil_num == -1 or prev_crop_num == -1 or season_num == -1:
        return "Invalid input for soil type, previous crop, or season."

    features = np.array([[N, P, K, temperature, humidity, ph, rainfall, soil_num, prev_crop_num, prev_duration_num, season_num, rec_duration_num]]).astype(float)
    features = scaler.transform(features)

    prediction = model.predict(features)
    recommended_crop = next((name for name, num in crop_dict.items() if num == prediction[0]), None)

    if recommended_crop:
        return recommended_crop.capitalize()
    else:
        return "Unable to recommend a proper crop."

@app.route('/index', methods=['POST'])
def get_recommendation():
    try:
        data = request.get_json()
        N = float(data['N'])
        P = float(data['P'])
        K = float(data['K'])
        temperature = float(data['temperature'])
        humidity = float(data['humidity'])
        ph = float(data['ph'])
        rainfall = float(data['rainfall'])
        soil = data['soil']
        prev_crop = data['prev_crop']
        prev_duration = data['prev_duration']
        rec_duration = data['rec_duration']
        season = data['season']

        result = recommendation(N, P, K, temperature, humidity, ph, rainfall, soil, prev_crop, prev_duration, rec_duration, season)
        return jsonify({'recommendation': result})
    except Exception as e:
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True)
