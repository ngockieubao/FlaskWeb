from flask import Flask
from app.filters import format_time, weather_icon, format_temp, format_timezone

def create_app():
    app = Flask(__name__)

    # Đăng ký custom filters
    app.jinja_env.filters['format_time'] = format_time
    app.jinja_env.filters['weather_icon'] = weather_icon
    app.jinja_env.filters['format_temp'] = format_temp
    app.jinja_env.filters['format_timezone'] = format_timezone

    # Đăng ký các route từ routes.py
    from .routes import main
    app.register_blueprint(main)

    return app
