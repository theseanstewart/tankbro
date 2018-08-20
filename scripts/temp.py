from w1thermsensor import W1ThermSensor
import datetime
import sys
import requests

# Gets the args passed without the file name
args = sys.argv[1:]

# If no argument is provided, raise an exception
if len(args) != 1:
    raise Exception('Must provide the URL to send temps to')

# The URL we are posting the data to
post_url = args[0]

# Set the current date time
date = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

# Convert Celsius to Fahrenheit
def c_to_f(c):
    f = c * 9.0 / 5.0 + 32.0
    return f

# Send the data to the webhook
# example: {"date": "2018-08-19 12:00:00", "sensor": "00xxxxxx", "c": 24.38, "f": 75.88 }
def send(sensor, c):
    f = c_to_f(c)
    json = {"date": date, "sensor": sensor, "c": c, "f": f }
    r = requests.post(post_url, json=json)
    r.status_code
    print("Sensor %s temperature, C=%.2f F=%.2f" % (sensor, c, f))

# Loop through the sensors and send the data
for sensor in W1ThermSensor.get_available_sensors():
    send(sensor.id, sensor.get_temperature())
