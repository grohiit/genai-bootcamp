import requests
from typing import List, Optional
from pydantic import BaseModel, Field

try:
    # Prefer the dedicated tools package if available
    from strands_agents_tools.python import PythonTool  # type: ignore
except Exception:  # Fallback for older versions
    # Older versions exposed tools under strands.tools
    from strands.tools import PythonTool  # type: ignore


DEFAULT_CITIES: List[str] = [
    "Paris",
    "London",
    "New York",
    "Tokyo",
    "Sydney",
    "Toronto",
    "Berlin",
    "Mumbai",
    "São Paulo",
    "Cairo",
]


class WeatherReportInput(BaseModel):
    cities: Optional[List[str]] = Field(
        default=None,
        description=("List of city names to include. If omitted, uses default cities."),
    )


def _fetch_city_weather(city: str) -> dict:
    response = requests.get(
        f"https://wttr.in/{city}", params={"format": "j1"}, timeout=10
    )
    response.raise_for_status()
    return response.json()


def _format_tv_script(city_to_weather: List[tuple[str, dict]]) -> str:
    intro = (
        "Good evening! Here's your TV weather report, "
        "covering conditions across the selected cities."
    )

    segments: List[str] = [intro, ""]

    for city, data in city_to_weather:
        try:
            current = data["current_condition"][0]
            temp_c = current.get("temp_C")
            feels_c = current.get("FeelsLikeC")
            desc = (current.get("weatherDesc") or [{"value": ""}])[0]["value"]
            wind_kph = current.get("windspeedKmph")
            wind_dir = current.get("winddir16Point")
            humidity = current.get("humidity")

            segment = (
                f"In {city}, it's {desc.lower()} right now, "
                f"around {temp_c}°C (feels like {feels_c}°C). "
                f"Winds {wind_dir or ''} at about {wind_kph} km/h, "
                f"humidity near {humidity}%."
            )

            # Add a short daytime outlook if available
            today_hours = (data.get("weather") or [{}])[0].get("hourly") or []
            if today_hours:
                noon_blocks = [h for h in today_hours if h.get("time") in {"1200", "1500"}]
                if noon_blocks:
                    noon = noon_blocks[0]
                    noon_desc = (noon.get("weatherDesc") or [{"value": ""}])[0]["value"]
                    noon_temp = noon.get("tempC")
                    segment += f" Later today: {noon_desc.lower()}, near {noon_temp}°C."

            segments.append(segment)
        except Exception:
            segments.append(f"In {city}, weather data is currently unavailable.")

    wrap = (
        "That's the snapshot for now. Stay tuned for updates, and have a great evening!"
    )
    segments.extend(["", wrap])
    return "\n".join(segments)


def generate_weather_report(input_data: WeatherReportInput) -> str:
    cities = input_data.cities or DEFAULT_CITIES

    city_to_weather: List[tuple[str, dict]] = []
    for city in cities:
        try:
            data = _fetch_city_weather(city)
            city_to_weather.append((city, data))
        except Exception:
            city_to_weather.append((city, {}))

    return _format_tv_script(city_to_weather)


weather_report_tool = PythonTool(
    name="weather_report",
    description=(
        "Generates a scripted TV weather report using live data from wttr.in for "
        "any cities provided. Optionally accepts a list of cities; otherwise uses "
        "default major world cities."
    ),
    input_schema=WeatherReportInput,
    handler=generate_weather_report,
)


