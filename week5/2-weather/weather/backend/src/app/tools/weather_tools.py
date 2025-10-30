import requests
from strands import tool

@tool
def get_weather_tool(city: str) -> str:
    """
    Get weather for a single city using wttr.in.
    
    Args:
        city: City name to fetch weather for (e.g., 'Paris').
    
    Description:
        Returns current weather for a single city using wttr.in.
        Defaults to Paris if no city is provided.
    """
    # Fetch weather data from wttr.in
    response = requests.get(
        f"https://wttr.in/{city}", params={"format": "j1"}, timeout=10
    )
    response.raise_for_status()
    data = response.json()
    
    # Format the weather report
    try:
        current = data["current_condition"][0]
        temp_c = current.get("temp_C")
        feels_c = current.get("FeelsLikeC")
        desc = (current.get("weatherDesc") or [{"value": ""}])[0]["value"]
        wind_kph = current.get("windspeedKmph")
        wind_dir = current.get("winddir16Point") or ""
        humidity = current.get("humidity")
        return (
            f"Weather in {city}: {desc.lower()}, {temp_c}°C (feels like {feels_c}°C). "
            f"Winds {wind_dir} at {wind_kph} km/h, humidity {humidity}%."
        )
    except Exception:
        return f"Weather data for {city} is currently unavailable."
