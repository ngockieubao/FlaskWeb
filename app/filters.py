from datetime import datetime

def format_time(value):
    try:
        dt = datetime.fromisoformat(value)
        return dt.strftime('%H:%M')  # "17:00"
    except:
        return value

def format_temp(value):
    try:
        temp = round(float(value))
        return int(temp)
    except (ValueError, TypeError):
        return value

def format_weather_code(value):
    try:
        code = round(value, 0)
        return code
    except:
        return value

def weather_icon(code):
    code = int(code)
    if code == 0:
        return "☀️"
    elif code in [1, 2]:
        return "⛅"
    elif code in [3, 45, 48]:
        return "☁️"
    elif code in [51, 61, 63, 80, 81]:
        return "🌧️"
    elif code in [71, 73, 75, 85]:
        return "❄️"
    else:
        return "❓"

def format_timezone(value):
    try:
        return value.decode("utf-8").strip()
    except AttributeError:
        return str(value).strip()
