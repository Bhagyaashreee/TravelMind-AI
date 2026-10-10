import requests


def get_weather(city: str):
    geocode_url = "https://geocoding-api.open-meteo.com/v1/search"

    geocode_params = {
        "name": city,
        "count": 1,
        "language": "en",
        "format": "json",
    }

    location_response = requests.get(
        geocode_url,
        params=geocode_params,
        timeout=10,
    )

    location_response.raise_for_status()

    location_data = location_response.json()

    if not location_data.get("results"):
        return {
            "error": f"Could not find location: {city}"
        }

    location = location_data["results"][0]

    latitude = location["latitude"]
    longitude = location["longitude"]

    weather_url = "https://api.open-meteo.com/v1/forecast"

    weather_params = {
        "latitude": latitude,
        "longitude": longitude,
        "current": (
            "temperature_2m,"
            "relative_humidity_2m,"
            "precipitation,"
            "wind_speed_10m"
        ),
        "daily": (
            "temperature_2m_max,"
            "temperature_2m_min,"
            "precipitation_probability_max,"
            "weather_code"
        ),
        "forecast_days": 4,
        "timezone": "auto",
    }

    weather_response = requests.get(
        weather_url,
        params=weather_params,
        timeout=10,
    )

    weather_response.raise_for_status()

    weather_data = weather_response.json()

    return {
        "city": location["name"],
        "country": location.get("country"),
        "latitude": latitude,
        "longitude": longitude,
        "current": weather_data.get("current"),
        "daily": weather_data.get("daily"),
    }