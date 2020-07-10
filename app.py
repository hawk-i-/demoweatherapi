import pyowm
import time
from flask import Flask, request, json, Response
from os import environ
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)
def get_wtr(location: str, temp_unit: str = 'fahrenheit', wind_unit: str = 'miles_hour'):
    owm = pyowm.OWM(environ.get('OWM_API_KEY')).weather_manager()
    wtr = owm.weather_at_place(location).weather
    return {
        "status": wtr.detailed_status,
        "wind_speed": wtr.wind(wind_unit).get('speed'),
        "wind_deg": wtr.wind(wind_unit).get('deg'),
        "temp": wtr.temperature(temp_unit).get('temp'),
        "temp_feel": wtr.temperature(temp_unit).get('feels_like'),
        "temp_max": wtr.temperature(temp_unit).get('temp_max'),
        "temp_min": wtr.temperature(temp_unit).get('temp_min'),
        "reference_time": time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(wtr.reference_time())),
        "sunset": time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(wtr.sunset_time())),
        "sunrise": time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(wtr.sunrise_time())),
        "wind_unit": wind_unit,
        "temp_unit": temp_unit
    }

@app.route('/')
def wtr():
    args = request.args
    if "location" in args:
        wtr = get_wtr(args['location'])
        return Response(
            json.dumps(wtr),
            status=200,
            mimetype='application/json'
        )
    else:
        return Response(
            json.dumps({
                "error_message": "location not set"
            }),
            status=500,
            mimetype='application/json'
        )

if __name__ == '__main__':
    app.run(host = '0.0.0.0', port=int(environ.get('API_SERVER_PORT')))
    # wtr = get_wtr('New York, US')