#!/usr/bin/env python
"""
This script reads in meteorological data from the Bureau of Meterology
in JSON or AXF format.

The default data contains the latest observations from Melbourne
(Olympic Park) from these URLs:

    http://reg.bom.gov.au/fwo/IDV60901/IDV60901.95936.json
    http://reg.bom.gov.au/fwo/IDV60901/IDV60901.95936.axf

The script downloads the data file, then makes a plot of temperature and
humidity.
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
