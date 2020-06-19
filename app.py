import pyowm
import time
from flask import Flask, request, json, Response
from os import environ
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)
def get_wtr(location: str, temp_unit: str = 'fahrenheit'):
    owm = pyowm.OWM(environ.get('OWM_API_KEY'))
    wtr = owm.weather_at_place(location).get_weather()
    return {
        "status": wtr.get_detailed_status(),
        "wind": wtr.get_wind(),
        "temp": wtr.get_temperature(temp_unit),
        "reference_time": time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(wtr.get_reference_time())),
        "sunset": time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(wtr.get_sunset_time())),
        "sunrise": time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(wtr.get_sunrise_time()))

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