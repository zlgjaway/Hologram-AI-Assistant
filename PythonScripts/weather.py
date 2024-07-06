import requests_cache
from retry_requests import retry
from geopy import Nominatim
from datetime import datetime, timezone
import json

class Weather:
    timestamp = 1609459200
    url = "https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true&daily=uv_index_max&forecast_days=3&daily=sunrise,sunset"
    
    def __init__(self):
        self.cache_session = requests_cache.CachedSession('.cache', expire_after=3600)
        self.retry_session = retry(self.cache_session, retries=5, backoff_factor=0.2)
        geolocator = Nominatim(user_agent="Geocoder")
        self.__location = "Melbourne, AU"
        loc = geolocator.geocode(self.__location)
        self.lat = loc.latitude
        self.long = loc.longitude
        print(f"Location: {self.__location}")

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
    def forecast_today(self):
        try:
            url = self.url.format(lat=self.lat, lon=self.long)
            print(f"Requesting URL: {url}")
            response = self.retry_session.get(url)
            response.raise_for_status()  # Raise an HTTPError for bad responses
            data = response.json()
            print("Data retrieved successfully.")
            
            with open("weather.json", "w") as json_file:
                json.dump(data, json_file, indent=4)
                print("Data written to weather.json successfully.")
            
            current_weather = data['current_weather']
            temperature = current_weather['temperature']
            uv_index_max = data['daily']['uv_index_max'][0]
            sunrise_str = data['daily']['sunrise'][0]
            sunset_str = data['daily']['sunset'][0]

            sunrise = datetime.fromisoformat(sunrise_str)
            sunset = datetime.fromisoformat(sunset_str)
            
            # Convert to UTC timezone if needed
            sunrise_utc = sunrise.astimezone(timezone.utc)
            sunset_utc = sunset.astimezone(timezone.utc)
            
            # Format as string
            sunrise_formatted = sunrise_utc.strftime("%H:%M:%S")
            sunset_formatted = sunset_utc.strftime("%H:%M:%S")

            # Summary Information

            message =( 
                f"Here is the Weather: Today The temperature is: {temperature}°C\n"
                f". Sunrise was at  {sunrise_formatted} \n"
                f" and sunset is at  {sunset_formatted} \n"
                f"UV Index: {uv_index_max} ({self.uv_index(uv_index_max)})"
            )
            return message

        except Exception as e:
            print(f"An error occurred: {e}")
            return "Failed to retrieve weather data."
