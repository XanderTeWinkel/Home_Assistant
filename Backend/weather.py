import requests

WINTERSWIJK_LAT = 51.9726
WINTERSWIJK_LON = 6.7181

# Weather code → human readable description
WEATHER_CODE_MAP = {
    0: "Clear sky",
    1: "Mainly clear",
    2: "Partly cloudy",
    3: "Cloudy",
    45: "Fog",
    48: "Depositing rime fog",
    51: "Light drizzle",
    53: "Moderate drizzle",
    55: "Dense drizzle",
    56: "Light freezing drizzle",
    57: "Dense freezing drizzle",
    61: "Slight rain",
    63: "Moderate rain",
    65: "Heavy rain",
    66: "Light freezing rain",
    67: "Heavy freezing rain",
    71: "Slight snow",
    73: "Moderate snow",
    75: "Heavy snow",
    77: "Snow grains",
    80: "Light rain showers",
    81: "Moderate rain showers",
    82: "Violent rain showers",
    85: "Light snow showers",
    86: "Heavy snow showers",
    95: "Thunderstorm",
    96: "Thunderstorm with slight hail",
    99: "Thunderstorm with heavy hail"
}

def fetch_weather(location="winterswijk"):
    """
    Fetch current + hourly weather for Winterswijk.
    Includes timestamps and human-readable weather descriptions.
    """

    if location.lower() == "winterswijk":
        lat, lon = WINTERSWIJK_LAT, WINTERSWIJK_LON
    else:
        lat, lon = WINTERSWIJK_LAT, WINTERSWIJK_LON

    url = (
        "https://api.open-meteo.com/v1/forecast?"
        f"latitude={lat}&longitude={lon}"
        "&current_weather=true"
        "&hourly=temperature_2m,relativehumidity_2m,precipitation"
        "&timezone=Europe%2FAmsterdam"
    )

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()

        current = data.get("current_weather", {})
        hourly = data.get("hourly", {})

        weathercode = current.get("weathercode")
        weather_description = WEATHER_CODE_MAP.get(weathercode, "Unknown")

        return {
            "location": location,
            "temperature": current.get("temperature"),
            "windspeed": current.get("windspeed"),
            "winddirection": current.get("winddirection"),
            "weathercode": weathercode,
            "weather_description": weather_description,
            "time": current.get("time"),

            "hourly": {
                "time": hourly.get("time", []),
                "temperature_2m": hourly.get("temperature_2m", []),
                "humidity": hourly.get("relativehumidity_2m", []),
                "precipitation": hourly.get("precipitation", [])
            }
        }

    except Exception as e:
        return {"error": str(e)}
