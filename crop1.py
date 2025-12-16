import requests
import pandas as pd
import time
import random

WEATHER_API_KEY = "721a6db02b65413ba71154158250503"
YOUR_TOMORROW_API_KEY = "FLBkm7DWYVU9vKix9yMqMgtQxpcTZERG"

LOCATIONS = [
    {"city": "Bangalore", "lat": 12.9716, "lon": 77.5946},
    {"city": "Mumbai", "lat": 19.0760, "lon": 72.8777},
    {"city": "Pune", "lat": 18.5204, "lon": 73.8567},
] * 50
CSV_FILE = "weather_data.csv"

SEASONS = ["Kharif", "Rabi"]
SOIL_TYPES = ["Clayey", "Sandy", "Loamy"]
PREVIOUS_CROPS = ["Corn", "Soybean", "Cotton", "Barley"]
DURATION_TYPES = ["short", "long"]

def fetch_weather_weatherapi(location):
    url = f"http://api.weatherapi.com/v1/current.json?key={WEATHER_API_KEY}&q={location['city']}"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        return {
            "Temperature": data['current']['temp_c'],
            "Humidity": data['current']['humidity'],
            "Rainfall": data['current']['precip_mm']
        }
    return None

def fetch_weather_tomorrow(location):
    url = f"https://api.tomorrow.io/v4/weather/realtime?location={location['lat']},{location['lon']}&apikey={YOUR_TOMORROW_API_KEY}"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        return {
            "Temperature": data['data']['values']['temperature'],
            "Humidity": data['data']['values']['humidity'],
            "Rainfall": data['data']['values'].get('precipitationIntensity', 0)
        }
    return None

# Main function to fetch data
def fetch_weather(location, i):
    data1 = fetch_weather_weatherapi(location)
    data2 = fetch_weather_tomorrow(location)

    if data1 and data2:
        temperature = round((data1["Temperature"] + data2["Temperature"]) / 2, 2)
        humidity = round((data1["Humidity"] + data2["Humidity"]) / 2, 2)
        rainfall = round((data1["Rainfall"] + data2["Rainfall"]) / 2, 2)

        return {
            "Location": location["city"],
            "Temperature": temperature,
            "Humidity": humidity,
            "Rainfall": rainfall,
            "pH": round(6 + (humidity / 100), 2),
            "N": round(50 + (temperature / 2), 2),
            "P": round(30 + (humidity / 3), 2),
            "K": round(40 + (rainfall / 4), 2),
            "Soil_Type": SOIL_TYPES[i % len(SOIL_TYPES)],
            "Previous_Crop": PREVIOUS_CROPS[i % len(PREVIOUS_CROPS)],
            "Previous_Duration": DURATION_TYPES[i % len(DURATION_TYPES)],
            "Recommended_Duration": DURATION_TYPES[(i + 1) % len(DURATION_TYPES)],
            "Season": SEASONS[i % len(SEASONS)]
        }
    return None

# Collect weather data
weather_data = []
for i, location in enumerate(LOCATIONS):
    print(f"Fetching data for {location['city']} ({i+1}/{len(LOCATIONS)})...")
    data = fetch_weather(location, i)

    if data:
        weather_data.append(data)

    if (i + 1) % 50 == 0:
        print("Pausing for 60 seconds to avoid rate limits...")
        time.sleep(60)
    else:
        time.sleep(1)

# Save data to CSV
df = pd.DataFrame(weather_data)
df.to_csv(CSV_FILE, index=False)
print(f"Weather data for {len(df)} locations saved to {CSV_FILE}")