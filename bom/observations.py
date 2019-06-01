'''
Observations puts Bureau of Meteorology station data into a pandas
DataFrame.
'''

import json
import pathlib
import urllib

import matplotlib.pyplot as plt
import pandas as pd

MELBOURNE_OLYMPIC_PARK_URL = (
    'http://reg.bom.gov.au/fwo/IDV60901/IDV60901.95936.json'
)
_TMP_FILE = pathlib.Path('~/Downloads').expanduser() / 'tmp.json'


class Observations:
    """
    Observations puts Bureau of Meteorology station data into a pandas
    DataFrame.

    Parameters
    ----------
    url : str
        The URL of the JSON data.
    """
    def __init__(self, url):

        with urllib.request.urlopen(url) as response, open(
            _TMP_FILE, 'wb'
        ) as out_file:
            data = response.read()
            out_file.write(data)

        with open(_TMP_FILE) as data_file:
            data = json.load(data_file)

        assert data, "Data wasn't read!"

        self._raw_data = data
        obs_data = data['observations']['data']

        observations = {key: list() for key in obs_data[0].keys()}
        for obs in obs_data:
            for key, value in obs.items():
                observations[key].append(value)

        for key in observations.keys():
            observations[key].reverse()

        self.observations = pd.DataFrame(observations)

    def plot_temperature_humidity(self, version=None):
        if version is None:
            version = 2
        if version == 1:
            self._plot_temperature_humidity1()
        elif version == 2:
            self._plot_temperature_humidity2()
        else:
            raise ValueError('version must be "1" or "2"')

    def _plot_temperature_humidity1(self):

        fig, axes = plt.subplots(ncols=1, nrows=2, sharex=True)
        self.observations.plot(
            'local_date_time', 'air_temp', ax=axes[0], legend=False
        )
        self.observations.plot(
            'local_date_time', 'rel_hum', ax=axes[1], legend=False
        )
        fig.autofmt_xdate()
        axes[1].set_xlabel('Date time')
        axes[0].set_ylabel('Temperature [°C]')
        axes[1].set_ylabel('Relative humidity [%]')
        [ax.grid(linestyle='--') for ax in axes]

    def _plot_temperature_humidity2(self):

        fig, ax1 = plt.subplots(figsize=(10, 5))
        fig.autofmt_xdate()

        ln1 = ax1.plot(
            self.observations['local_date_time'],
            self.observations['air_temp'],
            color='tab:red',
            label='temperature',
        )
        ax1.set_ylabel('Temperature [°C]')
        ax1.set_title('Latest observations from Melbourne (Olympic Park)')

        ax2 = ax1.twinx()

        ln2 = ax2.plot(
            self.observations['local_date_time'],
            self.observations['rel_hum'],
            color='tab:blue',
            label='humidity',
        )
        ax2.set_ylabel('Relative humidity [%]')

        ax1.xaxis.set_major_locator(plt.MaxNLocator(20))
        ax1.grid(linestyle='--')

        lns = ln1 + ln2
        labs = [l.get_label() for l in lns]
        ax1.legend(lns, labs, loc=0)
