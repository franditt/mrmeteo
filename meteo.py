import requests
import json
import os
from pydub import AudioSegment

# Set your WeatherAPI key here
API_KEY = 'api_key'
LATITUDE = '10.42'
LONGITUDE = '-0.71'

# Define directory where local language audio files are stored
AUDIO_DIR = 'audio_fragments'

# Function to simplify condition text
def parse_condition_text(text):
    text = text.lower()
    quantity = 'light'
    if 'moderate' in text:
        quantity = 'moderate'
    elif 'heavy' in text:
        quantity = 'heavy'
    event = 'rain' if 'rain' in text else 'wind' if 'wind' in text else None
    return quantity, event

# Fetch weather data from WeatherAPI
def fetch_weather():
    url = f'http://api.weatherapi.com/v1/forecast.json?key={API_KEY}&q={LATITUDE},{LONGITUDE}&days=2'
    response = requests.get(url)
    return response.json()

# Generate audio forecast
def generate_forecast_audio(data, day_offset=1):
    forecast_day = data['forecast']['forecastday'][day_offset]['day']
    condition_text = forecast_day['condition']['text']
    quantity, event = parse_condition_text(condition_text)
    
    if not event:
        print("No relevant weather event found.")
        return

    day_phrase = ['today', 'tomorrow', 'day_after'][day_offset]
    audio_files = [f"{AUDIO_DIR}/there_will_be.mp3", 
                   f"{AUDIO_DIR}/{quantity}.mp3", 
                   f"{AUDIO_DIR}/{event}.mp3", 
                   f"{AUDIO_DIR}/on_{day_phrase}.mp3"]

    # Combine audio fragments
    combined = AudioSegment.empty()
    for file in audio_files:
        if os.path.exists(file):
            combined += AudioSegment.from_mp3(file)
        else:
            print(f"Missing audio file: {file}")
    
    output_path = f"forecast_{day_phrase}.mp3"
    combined.export(output_path, format="mp3")
    print(f"Forecast audio saved to {output_path}")

# Main execution
if __name__ == '__main__':
    weather_data = fetch_weather()
    generate_forecast_audio(weather_data, day_offset=1)  # Tomorrow
