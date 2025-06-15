import requests

def get_coordinates_nominatim(city_name):
    url = "https://nominatim.openstreetmap.org/search"
    params = {
        "q": city_name,
        "format": "json",
        "limit": 1
    }
    headers = {
        "User-Agent": "FlaskWeatherApp/1.0 (youremail@example.com)"  # Nominatim bắt buộc phải có
    }

    response = requests.get(url, params=params, headers=headers)
    data = response.json()

    if not data:
        return None

    lat = float(data[0]["lat"])
    lon = float(data[0]["lon"])
    display_name = data[0]["display_name"]
    print(lat, lon, display_name)

    return {
        "lat": lat,
        "lon": lon,
        "display_name": display_name
    }
