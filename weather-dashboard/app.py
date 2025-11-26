from flask import Flask, render_template, jsonify
from google.cloud import storage
import json
import os
import re
from datetime import datetime,timezone
from dotenv import load_dotenv
load_dotenv()


try:
    from google import genai
    ai_available = True
except ImportError:
    ai_available = False



app = Flask(__name__)

storage_client = storage.Client()
BUCKET_NAME = "mishka-cme-project-weather-data" 


def get_latest_files(bucket_name):
    """Return the most recent weather JSON file for each city."""
    bucket = storage_client.bucket(bucket_name)
    blobs = list(bucket.list_blobs())

    latest_files = {}  # {city: (blob_name, timestamp)}

    # ✅ Pattern for files like weather_Mumbai_20251028_123000.json
    pattern = re.compile(r"weather_([\w\s-]+)_([0-9]{8}_[0-9]{6})\.json")

    for blob in blobs:
        match = pattern.match(blob.name)
        if match:
            city, timestamp = match.groups()
            if city not in latest_files or timestamp > latest_files[city][1]:
                latest_files[city] = (blob.name, timestamp)

    return [v[0] for v in latest_files.values()]


@app.route('/')
def home():
    """Homepage listing most recent files."""
    latest_files = get_latest_files(BUCKET_NAME)
    return render_template('weather.html', files=latest_files)



def generate_weather_mood(city, data):
    """Generate a natural, fun mood description using Vertex AI."""
  
    if not ai_available:
        return "Google GenAI SDK not installed."

    try:
        # Initialize GenAI client
        client = genai.Client(
            vertexai=True,
            project="mishka-cme-project",  # ✅ Your actual GCP project ID
            location="us-central1"
        )    


        prompt = f"""
        You are a friendly and expressive weather assistant. 
        Based on the following weather data, write a short, fun, and natural one-liner describing the mood, feeling, or activity that suits the weather.

        Weather data:
        City: {city}
        Condition: {data.get('weather')}
        Temperature: min {data.get('temp_min')}°C, max {data.get('temp_max')}°C
        Humidity: {data.get('humidity')}%
        Cloudiness: {data.get('clouds')}%
        Wind Speed: {data.get('wind_speed')} m/s
        Sunrise: {data.get('sunrise')}
        Sunset: {data.get('sunset')}

        Guidelines:
        - Be descriptive, expressive, and culturally relatable (like a friend commenting on the weather).
        - If it’s raining, mention cozy vibes like chai, pakoras, or music.
        - If it’s cold or snowy, mention blankets, hot drinks, or snuggling.
        - If it’s hot, mention the discomfort, craving for ice cream, or staying indoors.
        - If it’s breezy or mildly cloudy, mention going for a walk, enjoying the view, or outdoor fun.
        - Keep it to one or two sentences. Make it feel warm and conversational.
        - Avoid repeating exact temperature numbers — focus on the feeling.

        Output only the sentence.
        """

        response = client.models.generate_content(
              model="gemini-2.0-flash",
              contents=prompt
        )
        return response.text.strip() if response and response.text else "No mood generated."
    except Exception as e:
        return f"AI generation failed: {e}"


@app.route('/latest_data')
def latest_data():
    """Return parsed and filtered JSON data from most recent weather files."""
    latest_files = get_latest_files(BUCKET_NAME)
    bucket = storage_client.bucket(BUCKET_NAME)

    result = {}
    latest_time = None

    for filename in latest_files:
        blob = bucket.blob(filename)
        data = json.loads(blob.download_as_text())

        # ✅ Extract city name and timestamp
        match = re.match(r"weather_(\w+)_([0-9]{8}_[0-9]{6})\.json", filename)
        if match:
            city, timestamp = match.groups()
            if latest_time is None or timestamp > latest_time:
                latest_time = timestamp
        else:
            city = data.get("name", filename)

        sys_data = data.get("sys", {})
        sunrise_unix = sys_data.get("sunrise")
        sunset_unix = sys_data.get("sunset")

        sunrise = (
            datetime.fromtimestamp(sunrise_unix,tz=timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
            if sunrise_unix
            else "N/A"
        )

        sunset = (
            datetime.fromtimestamp(sunset_unix, tz=timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
            if sunset_unix
            else "N/A"
        )
        

        temp_min = data.get("main", {}).get("temp_min")
        temp_max = data.get("main", {}).get("temp_max")
        humidity = data.get("main", {}).get("humidity")
        wind_speed = data.get("wind", {}).get("speed")
        clouds = data.get("clouds", {}).get("all")

# Add units only if value exists
        filtered = {
            "weather": data.get("weather", [{}])[0].get("description", "N/A"),
            "temp_min": f"{temp_min} °C" if temp_min is not None else "N/A",
            "temp_max": f"{temp_max} °C" if temp_max is not None else "N/A",
            "humidity": f"{humidity}%" if humidity is not None else "N/A",
            "wind_speed": f"{wind_speed} m/s" if wind_speed is not None else "N/A",
            "clouds": f"{clouds}%" if clouds is not None else "N/A",
            "sunrise": sunrise,
            "sunset": sunset,
        }

        result[city] = filtered


        insight = generate_weather_mood(city, filtered)
        filtered["mood"] = insight



        if latest_time:
            latest_time_str = datetime.strptime(latest_time, "%Y%m%d_%H%M%S")
            latest_time_formatted = latest_time_str.strftime("%Y-%m-%d %H:%M:%S")
        else:
            latest_time_formatted = "N/A"



    return jsonify({
        "latest_time": latest_time_formatted,
        "data": result
    })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
