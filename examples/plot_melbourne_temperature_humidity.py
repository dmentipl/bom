#!/usr/bin/env python3
"""
This script reads in weather data from the Bureau of Meterology (BOM) in
JSON or AXF format from these URLs:

    http://reg.bom.gov.au/fwo/IDV60901/IDV60901.95936.json
    http://reg.bom.gov.au/fwo/IDV60901/IDV60901.95936.axf

which contains the latest observations from Melbourne (Olympic Park).
The script downloads this file. Currently it makes a plot of temperature
and humidity from all the most recent data.
"""

import bom
import matplotlib.pyplot as plt

MELBOURNE_OLYMPIC_PARK_JSON_URL = (
    'http://reg.bom.gov.au/fwo/IDV60901/IDV60901.95936.json'
)
MELBOURNE_OLYMPIC_PARK_AXF_URL = (
    'http://reg.bom.gov.au/fwo/IDV60901/IDV60901.95936.axf'
)

melb = bom.Observations(MELBOURNE_OLYMPIC_PARK_JSON_URL)
melb.plot_temperature_humidity(version=2)
plt.show()
