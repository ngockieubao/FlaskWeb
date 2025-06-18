import requests
import openmeteo_requests
import pandas as pd
import requests_cache
from retry_requests import retry


def fetch_weather_data(lat, lon):

    # Setup the Open-Meteo API client with cache and retry on error
    cache_session = requests_cache.CachedSession('.cache', expire_after=3600)
    retry_session = retry(cache_session, retries=5, backoff_factor=0.2)
    openmeteo = openmeteo_requests.Client(session=retry_session)

    # Make sure all required weather variables are listed here
    # The order of variables in hourly or daily is important to assign them correctly below
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": str(lat),
        "longitude": str(lon),
        "daily": ["weather_code", "temperature_2m_max", "temperature_2m_min"],
        "hourly": ["temperature_2m", "weather_code", "relative_humidity_2m", "apparent_temperature", "visibility",
                   "rain", "precipitation_probability"],
        "current": ["temperature_2m", "apparent_temperature", "relative_humidity_2m", "weather_code", "wind_speed_10m"],
        "timezone": "Asia/Bangkok"
    }

    try:
        responses = openmeteo.weather_api(url, params=params)

        # Process first location. Add a for-loop for multiple locations or weather models
        response = responses[0]
        print(f"Coordinates {response.Latitude()}°N {response.Longitude()}°E")
        # print(f"Elevation {response.Elevation()} m asl")
        print(f"Timezone {response.Timezone()}{response.TimezoneAbbreviation()}")
        # print(f"Timezone difference to GMT+0 {response.UtcOffsetSeconds()} s")

        # Current values. The order of variables needs to be the same as requested.
        current = response.Current()
        current_temperature_2m = current.Variables(0).Value()
        current_apparent_temperature = current.Variables(1).Value()
        current_relative_humidity_2m = current.Variables(2).Value()
        current_weather_code = current.Variables(3).Value()
        current_wind_speed_10m = current.Variables(4).Value()

        print(f"Current time {current.Time()}")

        current_data = {
            "temperature_2m": current_temperature_2m,
            "apparent_temperature": current_apparent_temperature,
            "relative_humidity_2m": current_relative_humidity_2m,
            "weather_code": current_weather_code,
            "wind_speed_10m": current_wind_speed_10m,
            "time": pd.to_datetime(current.Time(), unit="s").strftime('%Y-%m-%d %H:%M')
        }

        # Process hourly data. The order of variables needs to be the same as requested.
        hourly = response.Hourly()
        hourly_temperature_2m = hourly.Variables(0).ValuesAsNumpy()
        hourly_weather_code = hourly.Variables(1).ValuesAsNumpy()
        hourly_relative_humidity_2m = hourly.Variables(2).ValuesAsNumpy()
        hourly_apparent_temperature = hourly.Variables(3).ValuesAsNumpy()
        hourly_visibility = hourly.Variables(4).ValuesAsNumpy()
        hourly_rain = hourly.Variables(5).ValuesAsNumpy()
        hourly_precipitation_probability = hourly.Variables(6).ValuesAsNumpy()

        hourly_data = {"date": pd.date_range(
            start=pd.to_datetime(hourly.Time(), unit="s", utc=True),
            end=pd.to_datetime(hourly.TimeEnd(), unit="s", utc=True),
            freq=pd.Timedelta(seconds=hourly.Interval()),
            inclusive="left"
        )}

        hourly_data["temperature_2m"] = hourly_temperature_2m
        hourly_data["weather_code"] = hourly_weather_code
        hourly_data["relative_humidity_2m"] = hourly_relative_humidity_2m
        hourly_data["apparent_temperature"] = hourly_apparent_temperature
        hourly_data["visibility"] = hourly_visibility
        hourly_data["rain"] = hourly_rain
        hourly_data["precipitation_probability"] = hourly_precipitation_probability

        hourly_dataframe = pd.DataFrame(data=hourly_data)

        # Format hourly dataframe to list of dicts
        hourly_formatted = hourly_dataframe.copy()
        hourly_formatted["date"] = hourly_formatted["date"].dt.strftime('%Y-%m-%d %H:%M')
        hourly_data = hourly_formatted.to_dict(orient="records")
        print(hourly_data)

        # Process daily data. The order of variables needs to be the same as requested.
        daily = response.Daily()
        daily_weather_code = daily.Variables(0).ValuesAsNumpy()
        daily_temperature_2m_max = daily.Variables(1).ValuesAsNumpy()
        daily_temperature_2m_min = daily.Variables(2).ValuesAsNumpy()

        daily_data = {"date": pd.date_range(
            start=pd.to_datetime(daily.Time(), unit="s", utc=True),
            end=pd.to_datetime(daily.TimeEnd(), unit="s", utc=True),
            freq=pd.Timedelta(seconds=daily.Interval()),
            inclusive="left"
        )}

        daily_data["weather_code"] = daily_weather_code
        daily_data["temperature_2m_max"] = daily_temperature_2m_max
        daily_data["temperature_2m_min"] = daily_temperature_2m_min

        daily_dataframe = pd.DataFrame(data=daily_data)

        # Format daily dataframe to list of dicts
        daily_formatted = daily_dataframe.copy()
        daily_formatted["date"] = daily_formatted["date"].dt.strftime('%Y-%m-%d')
        daily_data = daily_formatted.to_dict(orient="records")
        print(daily_data)

        return {
            "response": response,
            "current": current_data,
            "hourly": hourly_data,
            "daily": daily_data
        }

    except requests.RequestException as e:
        print(f"[ERROR] Weather API failed: {e}")
        return None
