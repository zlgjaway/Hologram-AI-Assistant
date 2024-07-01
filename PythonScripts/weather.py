import requests_cache
import pandas as pd
from retry_requests import retry
from geopy import Nominatim
from datetime import datetime

class Weather:
    timestamp = 1609459200
    url = "https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true&daily=uv_index_max&forecast_days=3"
    
    def __init__(self):
        self.cache_session = requests_cache.CachedSession('.cache', expire_after=3600)
        self.retry_session = retry(self.cache_session, retries=5, backoff_factor=0.2)
        locator = Nominatim(user_agent="myGeocoder")
        self.__location = "Melbourne, AU"
        loc = locator.geocode(self.__location)
        self.lat = loc.latitude
        self.long = loc.longitude
        print(self.__location)

    def uv_index(self, uvi: float) -> str:
        """Returns a message depending on the UV Index provided."""
        if uvi <= 2.9:
            return "The Ultraviolet level is low, no protection is required."
        elif 3.0 <= uvi < 6.0:
            return "The Ultraviolet level is medium, skin protection is required."
        elif 6.0 <= uvi < 8.0:
            return "The Ultraviolet level is high, skin protection is required."
        elif 8.0 <= uvi < 11.0:
            return "The Ultraviolet level is very high, extra skin protection is required."
        else:
            return "The Ultraviolet level is extremely high, caution is advised and extra skin protection is required."

    @property
    def forecast(self):
        url = self.url.format(lat=self.lat, lon=self.long)
        response = self.retry_session.get(url)
        if response.status_code == 200:
            data = response.json()
            current_weather = data['current_weather']
            temperature = current_weather['temperature']
            time = current_weather['time']
            uv_index_max = data['daily']['uv_index_max'][0]
            
            print(f"Time: {time}")
            print(f"Temperature: {temperature}°C")
            print(f"UV Index: {uv_index_max}")
            print(self.uv_index(uv_index_max))
        else:
            print(f"Failed to retrieve data: {response.status_code}")

# Demo
myweather = Weather()
myweather.forecast
