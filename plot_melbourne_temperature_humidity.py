#!/usr/bin/env python3
'''
plot_melbourne_temperature_humidity.py
D. Mentiplay, 2018.

This script reads in weather data from the Bureau of Meterology (BOM) in JSON
format from this URL:

    http://reg.bom.gov.au/fwo/IDV60901/IDV60901.95936.json

which contains the latest observations from Melbourne (Olympic Park). The
script downloads this file.

Currently it makes a plot of temperature and humidity from all the most recent
data.

Module requirements:
    - matplotlib
'''

import json
import os
import urllib.request

import matplotlib as mpl
import matplotlib.pyplot as plt

mpl.rcParams['font.family'] = 'serif'

url = 'http://reg.bom.gov.au/fwo/IDV60901/IDV60901.95936.json'
file_name = os.path.expanduser('~/Downloads') + '/weather.json'

with urllib.request.urlopen(url) as response, open(file_name, 'wb') as out_file:
    data = response.read()
    out_file.write(data)

with open(file_name) as data_file:
    data = json.load(data_file)

assert(data), "Data wasn't read!"

notice = data['observations']['notice']
header = data['observations']['header']
observations = data['observations']['data']

date_time = [observation['local_date_time'] for observation in observations]
temperature = [observation['air_temp'] for observation in observations]
humidity = [observation['rel_hum'] for observation in observations]
date_time.reverse()
temperature.reverse()
humidity.reverse()

fig, ax1 = plt.subplots(figsize=(25,5))
fig.autofmt_xdate()

color = 'tab:red'
label = 'temperature'
ln1 = ax1.plot(date_time, temperature, color=color, label=label)
ax1.set_ylabel('Temperature [°C]')
ax1.set_title('Latest observations from Melbourne (Olympic Park)')

ax2 = ax1.twinx()

color = 'tab:blue'
label = 'humidity'
ln2 = ax2.plot(date_time, humidity, color=color, label=label)
ax2.set_ylabel('Relative humidity [%]')

ax1.xaxis.set_major_locator(plt.MaxNLocator(20))

lns = ln1 + ln2
labs = [l.get_label() for l in lns]
ax1.legend(lns, labs, loc=0)

plt.show()
