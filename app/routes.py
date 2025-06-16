from flask import Blueprint, render_template, request
from .services.geolocation_service import get_coordinates_nominatim
from .services.weather_service import fetch_weather_data

# Khởi tạo Blueprint
main = Blueprint('main', __name__)

@main.route('/')
def home():
    return render_template('index.html')

@main.route('/about')
def about():
    return render_template('about.html')

@main.route('/weather',  methods=["GET","POST"])
def weather():
    coords = None
    weather = None
    if request.method == "POST":
        city_name = request.form.get("city")
        coords = get_coordinates_nominatim(city_name)
        if coords:
            lat = coords["lat"]
            lon = coords["lon"]
            weather = fetch_weather_data(lat, lon)

    return render_template('weather.html', coords=coords, weather=weather)
