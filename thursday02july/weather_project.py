import sys
import requests
from weather_api_key import OPENWEATHER_API_KEY


POSTCODE_ENDPOINT = "https://api.postcodes.io/postcodes/"
OPENWEATHER_ENDPOINT = "https://api.openweathermap.org/data/2.5/weather"


def get_lat_lon(postcode):
    """
    Takes a UK postcode and returns the latitude, longitude, and normalised postcode.
    Uses the Postcodes.io API.
    """

    response = requests.get(POSTCODE_ENDPOINT + postcode)

    if response.status_code != 200:
        raise Exception("Postcode not found. Please check the postcode and try again.")

    data = response.json()
    result = data["result"]

    latitude = result["latitude"]
    longitude = result["longitude"]
    normalised_postcode = result["postcode"]

    return latitude, longitude, normalised_postcode


def get_weather(latitude, longitude):
    """
    Takes latitude and longitude.
    Uses the OpenWeather API key from config.py.
    Returns the current weather data.
    """

    params = {
        "lat": latitude,
        "lon": longitude,
        "appid": OPENWEATHER_API_KEY,
        "units": "metric"
    }

    response = requests.get(OPENWEATHER_ENDPOINT, params=params)

    if response.status_code != 200:
        raise Exception("Could not fetch weather. Check your OpenWeather API key.")

    return response.json()


def display_weather(postcode, weather_data):
    """
    Displays the weather data in a user-friendly format.
    """

    area = weather_data["name"]
    temperature = weather_data["main"]["temp"]
    feels_like = weather_data["main"]["feels_like"]
    humidity = weather_data["main"]["humidity"]
    wind_speed = weather_data["wind"]["speed"]
    description = weather_data["weather"][0]["description"].title()

    print("\n==============================")
    print("      POSTCODE WEATHER")
    print("==============================")
    print(f"Postcode: {postcode}")
    print(f"Nearest Area: {area}")
    print(f"Weather: {description}")
    print(f"Temperature: {temperature}°C")
    print(f"Feels Like: {feels_like}°C")
    print(f"Humidity: {humidity}%")
    print(f"Wind Speed: {wind_speed} m/s")
    print("==============================\n")


def main():
    """
    Main function that runs the postcode weather program.
    """

    if len(sys.argv) < 2:
        print("Usage: python postcode_weather.py <postcode>")
        print("Example: python postcode_weather.py SW1A1AA")
        return

    postcode = " ".join(sys.argv[1:])

    try:
        latitude, longitude, normalised_postcode = get_lat_lon(postcode)
        weather_data = get_weather(latitude, longitude)
        display_weather(normalised_postcode, weather_data)

    except Exception as error:
        print(f"Error: {error}")


if __name__ == "__main__":
    main()