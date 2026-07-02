from flask import Flask, request, jsonify, render_template
import requests
from config import OPENWEATHER_API_KEY


app = Flask(__name__)

POSTCODE_ENDPOINT = "https://api.postcodes.io/postcodes/"
OPENWEATHER_ENDPOINT = "https://api.openweathermap.org/data/2.5/weather"


def get_lat_lon(postcode):
    """
    Takes a UK postcode and returns latitude, longitude, and normalised postcode.
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
    Uses OpenWeather API to get current weather data.
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


def simplify_weather(postcode, weather_data):
    """
    Takes raw weather data and returns a cleaner dictionary.
    This makes the API response easier to read.
    """

    description = weather_data["weather"][0]["description"].title()
    icon_code = weather_data["weather"][0]["icon"]

    weather_report = {
        "postcode": postcode,
        "area": weather_data["name"],
        "description": description,
        "temperature": weather_data["main"]["temp"],
        "feels_like": weather_data["main"]["feels_like"],
        "humidity": weather_data["main"]["humidity"],
        "wind_speed": weather_data["wind"]["speed"],
        "icon_url": f"https://openweathermap.org/img/wn/{icon_code}@2x.png"
    }

    return weather_report


def get_weather_by_postcode(postcode):
    """
    Full process:
    postcode -> latitude/longitude -> weather data -> simplified report.
    """

    latitude, longitude, normalised_postcode = get_lat_lon(postcode)
    weather_data = get_weather(latitude, longitude)
    weather_report = simplify_weather(normalised_postcode, weather_data)

    return weather_report


@app.route("/")
def home():
    """
    Frontend homepage.
    User can type a postcode into a form.
    """

    postcode = request.args.get("postcode")

    weather = None
    error = None

    if postcode:
        try:
            weather = get_weather_by_postcode(postcode)
        except Exception as e:
            error = str(e)

    return render_template("index.html", weather=weather, error=error)


@app.route("/weather_api", methods=["GET", "POST"])
def weather_api():
    """
    GET example:
    /weather_api?postcode=EC2Y 4AB

    POST example:
    {
        "postcodes": ["SW1A 1AA", "EC2Y 4AB", "M1 1AE"]
    }
    """

    if request.method == "GET":
        postcode = request.args.get("postcode")

        if not postcode:
            return jsonify({"error": "Please provide a postcode query parameter."}), 400

        try:
            weather_report = get_weather_by_postcode(postcode)
            return jsonify(weather_report), 200

        except Exception as e:
            return jsonify({"error": str(e)}), 400

    if request.method == "POST":
        data = request.get_json()

        if not data or "postcodes" not in data:
            return jsonify({
                "error": "Please send JSON in this format: {'postcodes': ['SW1A 1AA', 'EC2Y 4AB']}"
            }), 400

        postcodes = data["postcodes"]
        results = []

        for postcode in postcodes:
            try:
                weather_report = get_weather_by_postcode(postcode)
                results.append(weather_report)

            except Exception as e:
                results.append({
                    "postcode": postcode,
                    "error": str(e)
                })

        return jsonify({"results": results}), 200


@app.route("/weather_api/<postcode>")
def weather_api_path(postcode):
    """
    Path parameter example:
    /weather_api/EC2Y4AB
    """

    try:
        weather_report = get_weather_by_postcode(postcode)
        return jsonify(weather_report), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 400


if __name__ == "__main__":
    app.run(debug=True)