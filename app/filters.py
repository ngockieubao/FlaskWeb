from datetime import datetime

def format_time(value):
    try:
        dt = datetime.fromisoformat(value)
        return dt.strftime('%-I:%M %p')  # "6:00 AM"
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
