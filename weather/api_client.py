import requests
from django.conf import settings
import constants


class OpenWeatherAPIClient:
    BASE_URL = "https://api.openweathermap.org/data/3.0/onecall"

    def __init__(self):
        self.api_key = constants.OPENWEATHER_API_KEY

    def get_weather_data(self, lat, lon, exclude="minutely,hourly"):
        """
        Fetch weather data for the given latitude and longitude.

        :param lat: Latitude of the location
        :param lon: Longitude of the location
        :param exclude: Comma-separated list of parts to exclude (default is to exclude minutely, hourly data)
        :return: JSON response containing weather data
        """
        params = {
            "lat": lat,
            "lon": lon,
            "exclude": exclude,
            "appid": self.api_key,
            "units": "metric",  # Convert Kelvin to Celsius
        }

        try:
            response = requests.get(self.BASE_URL, params=params)
            response.raise_for_status()  # Raise an exception for bad HTTP status codes
            return response.json()

        except requests.exceptions.RequestException as e:
            print(f"Error fetching weather data: {e}")
            return None
