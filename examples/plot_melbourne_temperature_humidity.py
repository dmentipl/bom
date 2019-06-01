#!/usr/bin/env python3
"""
This script reads in weather data from the Bureau of Meterology (BOM) in JSON
format from this URL:

    http://reg.bom.gov.au/fwo/IDV60901/IDV60901.95936.json

which contains the latest observations from Melbourne (Olympic Park). The
script downloads this file.

Currently it makes a plot of temperature and humidity from all the most recent
data.
"""

import matplotlib.pyplot as plt
from bom.observations import MELBOURNE_OLYMPIC_PARK_URL, Observations

melb = Observations(MELBOURNE_OLYMPIC_PARK_URL)
melb.plot_temperature_humidity(version=2)
plt.show()
