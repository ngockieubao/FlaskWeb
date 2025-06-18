from datetime import datetime
from zoneinfo import ZoneInfo


def format_time(value):
    try:
        dt = datetime.fromisoformat(value)

        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=ZoneInfo("UTC"))

        local_dt = dt.astimezone(ZoneInfo("Asia/Bangkok"))
        return local_dt.strftime('%H:%M')
    except Exception:
        return value

def format_date(value):
    try:
        dt = datetime.fromisoformat(value)

        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=ZoneInfo("UTC"))

        local_dt = dt.astimezone(ZoneInfo("Asia/Bangkok"))
        return local_dt.strftime('%Y/%m/%d')
    except Exception:
        return value

def format_round_float_to_int(value):
    try:
        temp = round(float(value))
        return int(temp)
    except (ValueError, TypeError):
        return value

def weather_icon(code):
    code = int(code)
    if code == 0:
        return "☀️"  # Clear sky
    elif code in [1, 2, 3]:
        return "⛅"  # Mainly clear, partly cloudy, and overcast
    elif code in [45, 48]:
        return "🌫️"  # Fog and depositing rime fog
    elif code in [51, 53, 55]:
        return "🌦️"  # Drizzle: Light, moderate, and dense
    elif code in [56, 57]:
        return "🌧️❄️"  # Freezing Drizzle
    elif code in [61, 63, 65]:
        return "🌧️"  # Rain: Slight, moderate, and heavy
    elif code in [66, 67]:
        return "🌧️❄️"  # Freezing Rain
    elif code in [71, 73, 75]:
        return "❄️"  # Snow fall
    elif code == 77:
        return "🌨️"  # Snow grains
    elif code in [80, 81, 82]:
        return "🌦️"  # Rain showers
    elif code in [85, 86]:
        return "🌨️"  # Snow showers
    elif code == 95:
        return "⛈️"  # Thunderstorm
    elif code in [96, 99]:
        return "⛈️❄️"  # Thunderstorm with hail
    else:
        return "❓"  # Unknown code

def format_timezone(value):
    try:
        return value.decode("utf-8").strip()
    except AttributeError:
        return str(value).strip()

def format_visibility(value):
    try:
        res = round(float(value / 1000))
        return int(res)
    except (ValueError, TypeError):
        return value