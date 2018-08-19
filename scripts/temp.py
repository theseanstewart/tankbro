# Temp reading code taken from https://learn.adafruit.com/adafruits-raspberry-pi-lesson-11-ds18b20-temperature-sensing/software
#
# Reads the C and F values from the temperature probe and posts the values
# along with the current date to a given URL.
#
# Example: python temp.py https://webhook.site/#/asdfasdf 10

import os
import glob
import time
import datetime
import subprocess
import requests
import sys

# Get the args passed to the script
# Gets the args passed without the file name
args = sys.argv[1:]

if len(args) != 2:
    raise Exception('Must provide two arguments')

# The URL we are posting the data to
post_url = args[0]

# The number of temperature samples to take and average
samples = int(args[1])

# Number of seconds to wait between samples
wait_for = 1

os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')

base_dir = '/sys/bus/w1/devices/'
device_folder = glob.glob(base_dir + '28*')[0]
device_file = device_folder + '/w1_slave'

def read_temp_raw():
        catdata = subprocess.Popen(['cat',device_file], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out,err = catdata.communicate()
        out_decode = out.decode('utf-8')
        lines = out_decode.split('\n')
        return lines

def read_temp():
    lines = read_temp_raw()
    while lines[0].strip()[-3:] != 'YES':
        time.sleep(0.2)
        lines = read_temp_raw()
    equals_pos = lines[1].find('t=')
    if equals_pos != -1:
        temp_string = lines[1][equals_pos+2:]
        temp_c = float(temp_string) / 1000.0
        temp_f = temp_c * 9.0 / 5.0 + 32.0
        return temp_c, temp_f

def average_samples(samples):
    average = 0
    sum = 0
    for n in samples:
        sum = sum + n
    return format(sum / len(samples), '.2f')

def send(c, f):
    date = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    json = {"date": date, "C": c, "F": f }
    r = requests.post(post_url, json=json)
    r.status_code

i = 0
temp_f = []
temp_c = []
while i < samples:
        c, f = read_temp()
        temp_c.append(c)
        temp_f.append(f)
        time.sleep(wait_for)
        i += 1

c = average_samples(temp_c)
f = average_samples(temp_f)

print(c, f)
send(c, f)
