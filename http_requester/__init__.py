# import logging
# import requests
# from typing import Optional, Dict, Union, Tuple, Any
# from urllib.parse import urljoin

# logger = logging.getLogger(__name__)


# class WeatherAPIRequester:
#     """Handle HTTP requests to the OpenWeatherMap API."""

#     BASE_URL = "https://api.openweathermap.org/data/2.5/"
#     REQUEST_TIMEOUT = 30  # Longer timeout for weather API

#     def __init__(self, api_key: str):
#         self.api_key = api_key

#     def make_request(
#         self,
#         endpoint: str,
#         method: str = "GET",
#         params: Optional[Dict] = None,
#         headers: Optional[Dict] = None,
#         data: Optional[Union[Dict, bytes]] = None,
#         convert_to_json: bool = True,
#         return_response_object: bool = False,
#     ) -> Tuple[bool, Any]:
#         """
#         Make an HTTP request to the OpenWeatherMap API.

#         Args:
#             endpoint: API endpoint (e.g., 'weather', 'forecast')
#             method: HTTP method (default: GET)
#             params: URL parameters
#             headers: HTTP headers
#             data: Request body data
#             convert_to_json: Whether to convert response to JSON
#             return_response_object: Whether to return the response object

#         Returns:
#             Tuple of (success: bool, result: Union[dict, str, Response])
#         """
#         url = urljoin(self.BASE_URL, endpoint)

#         # Ensure API key is always included in parameters
#         params = params or {}
#         params["appid"] = self.api_key

#         request_params = {"url": url, "timeout": self.REQUEST_TIMEOUT, "params": params}

#         if headers:
#             request_params["headers"] = headers
#         if method != "GET" and data:
#             request_params["data"] = data

#         request_log_context = {
#             "url": url,
#             "method": method,
#             "endpoint": endpoint,
#             "params": str(
#                 {k: v for k, v in params.items() if k != "appid"}
#             ),  # Log params except API key
#         }

#         logger.debug("Making weather API request", extra=request_log_context)

#         try:
#             response = getattr(requests, method.lower())(**request_params)

#         except requests.exceptions.Timeout:
#             logger.error("Weather API request timed out", extra=request_log_context)
#             return False, {"error": "request_timeout"}

#         except requests.exceptions.ConnectionError as exp:
#             logger.exception("Weather API connection failed", extra=request_log_context)
#             if "service not known" in str(exp).lower():
#                 return False, {"error": "service_not_known"}
#             return False, {"error": "connection_error"}

#         except requests.exceptions.RequestException:
#             logger.exception("Weather API request failed", extra=request_log_context)
#             return False, {"error": "request_failed"}

#         except Exception as e:
#             logger.exception(
#                 "Unexpected error during weather API request",
#                 extra={**request_log_context, "error": str(e)},
#             )
#             return False, {"error": "unexpected_error"}

#         success = response.ok
#         response_log_context = {
#             **request_log_context,
#             "success": success,
#             "status_code": response.status_code,
#         }

#         if success:
#             logger.info("Weather API request completed", extra=response_log_context)
#         else:
#             logger.error(
#                 "Weather API request failed",
#                 extra={**response_log_context, "response_text": response.text},
#             )

#         if return_response_object:
#             return success, response

#         if convert_to_json:
#             try:
#                 return success, response.json()
#             except ValueError:
#                 logger.error(
#                     "Failed to parse JSON response", extra=response_log_context
#                 )
#                 return False, {"error": "invalid_json", "text": response.text}

#         return success, response.text

#     def get_current_weather(
#         self, city: str, units: str = "metric"
#     ) -> Tuple[bool, Dict]:
#         """
#         Get current weather for a specific city.

#         Args:
#             city: City name (e.g., 'Mumbai')
#             units: Temperature units ('metric' for Celsius, 'imperial' for Fahrenheit)

#         Returns:
#             Tuple of (success: bool, weather_data: dict)
#         """
#         params = {"q": f"{city},IN", "units": units}  # Restrict to Indian cities
#         return self.make_request("weather", params=params)

#     def get_weather_forecast(
#         self, city: str, units: str = "metric"
#     ) -> Tuple[bool, Dict]:
#         """
#         Get 5-day weather forecast for a specific city.

#         Args:
#             city: City name (e.g., 'Mumbai')
#             units: Temperature units ('metric' for Celsius, 'imperial' for Fahrenheit)

#         Returns:
#             Tuple of (success: bool, forecast_data: dict)
#         """
#         params = {"q": f"{city},IN", "units": units}  # Restrict to Indian cities
#         return self.make_request("forecast", params=params)
