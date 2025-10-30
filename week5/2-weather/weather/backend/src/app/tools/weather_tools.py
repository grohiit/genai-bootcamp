import json
import requests
from strands import tool

@tool
def convert_temperature(temperature: float, from_unit: str, to_unit: str) -> str:
    """
    Convert temperature between Fahrenheit and Celsius.
    
    Args:
        temperature: The temperature value to convert.
        from_unit: The unit to convert from ('F' for Fahrenheit or 'C' for Celsius).
        to_unit: The unit to convert to ('F' for Fahrenheit or 'C' for Celsius).
    
    Description:
        Converts temperature values between Fahrenheit and Celsius scales.
        Supports conversions in both directions (F->C and C->F).
    """
    try:
        from_unit = from_unit.upper()
        to_unit = to_unit.upper()
        
        if from_unit not in ['F', 'C'] or to_unit not in ['F', 'C']:
            return f"Invalid unit. Use 'F' for Fahrenheit or 'C' for Celsius."
        
        if from_unit == to_unit:
            return f"{temperature}°{from_unit} = {temperature}°{to_unit}"
        
        if from_unit == 'F' and to_unit == 'C':
            # Fahrenheit to Celsius: (F - 32) * 5/9
            converted = (temperature - 32) * 5 / 9
            return f"{temperature}°F = {converted:.2f}°C"
        
        if from_unit == 'C' and to_unit == 'F':
            # Celsius to Fahrenheit: (C * 9/5) + 32
            converted = (temperature * 9 / 5) + 32
            return f"{temperature}°C = {converted:.2f}°F"
        
    except Exception as e:
        return f"Error converting temperature: {str(e)}"

@tool
def get_current_weather(city: str) -> str:
    """
    Get current weather for a single city using wttr.in.
    
    Args:
        city: City name to fetch weather for (e.g., 'Paris').
    
    Description:
        Returns current weather for a single city using wttr.in in a one-line format.
    """
    try:
        # Fetch weather data from wttr.in with format=4 for one-line response
        response = requests.get(
            f"https://wttr.in/{city}", params={"format": "4"}, timeout=10
        )
        response.raise_for_status()
        return response.text.strip()
    except Exception:
        return f"Weather data for {city} is currently unavailable."

@tool
def get_weather_forecast(city: str) -> str:
    """
    Get weather forecast for a single city using wttr.in.
    
    Args:
        city: City name to fetch weather forecast for (e.g., 'Paris').
    
    Description:
        Returns raw JSON weather forecast data for future dates which the LLM can use
        to generate forecasts. The data includes multiple days of forecast information.
    """
    try:
        # Fetch weather forecast data from wttr.in with JSON format
        response = requests.get(
            f"https://wttr.in/{city}", params={"format": "j1"}, timeout=10
        )
        response.raise_for_status()
        data = response.json()
        
        # Return raw JSON as string for LLM to process
        return json.dumps(data, indent=2)
    except Exception:
        return f"Weather forecast data for {city} is currently unavailable."
