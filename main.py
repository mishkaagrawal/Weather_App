import functions_framework
import requests
from google.cloud import storage
import datetime
import os
import json

@functions_framework.cloud_event
def hello_world(cloud_event):
    cities = ["Mumbai", "New York", "London", "Tokyo", "Sydney"]
    api_key = os.environ.get("API_KEY")
    bucket_name = os.environ.get("BUCKET_NAME", "mishka-cme-project-weather-data")

    client = storage.Client()
    bucket = client.bucket(bucket_name)

    results = {}

    for city in cities:
        try:
            url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
            response = requests.get(url)
            data = response.json()

            filename = f"weather_{city}_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            blob = bucket.blob(filename)
            blob.upload_from_string(json.dumps(data))

            results[city] = " Data saved"
        except Exception as e:
            results[city] = f" Failed: {str(e)}"

    print(json.dumps(results))
