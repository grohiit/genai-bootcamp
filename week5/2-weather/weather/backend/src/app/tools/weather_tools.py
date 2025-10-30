import requests
from typing import Optional
from pydantic import BaseModel, Field
from strands import tool


class CityWeatherInput(BaseModel):
    city: str = Field(
        default="Paris",
        description="City name to fetch weather for (e.g., 'Paris').",
    )


@tool(
    name="weather_report_tool",
    description=(
        "Returns current weather for a single city using wttr.in. "
        "Defaults to Paris if no city is provided."
    ),
)
def weather_report_tool(input_data: CityWeatherInput) -> str:
    """Get weather for a single city using wttr.in."""
    city = input_data.city
    
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
