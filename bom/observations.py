'''
Observations puts Bureau of Meteorology station data into a pandas
DataFrame.
'''

import json
import pathlib
import urllib

import matplotlib.pyplot as plt
import pandas as pd

_TMP_FILE = pathlib.Path('~/Downloads').expanduser() / '.tmp'


class Observations:
    """
    Observations puts Bureau of Meteorology station data into a pandas
    DataFrame.

    Parameters
    ----------
    url : str
        The URL of the data. File format can be JSON or AXF.
    """

    def __init__(self, url):

        file_format = url.split('.')[-1].lower()

        with urllib.request.urlopen(url) as response, open(
            _TMP_FILE, 'wb'
        ) as out_file:
            data = response.read()
            out_file.write(data)

        if file_format == 'json':

            with open(_TMP_FILE) as data_file:
                data = json.load(data_file)

            obs_data = data['observations']['data']

            observations = {key: list() for key in obs_data[0].keys()}
            for obs in obs_data:
                for key, value in obs.items():
                    observations[key].append(value)

            for key in observations.keys():
                observations[key]

            self.notice = data['observations']['notice'][0]
            self.header = data['observations']['header'][0]
            self.data = pd.DataFrame(observations)

        elif file_format == 'axf':

            notice, header, data = _read_axf(_TMP_FILE)
            self.notice = notice
            self.header = header
            self.data = data

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
        self.data[::-1].plot(
            'local_date_time', 'air_temp', ax=axes[0], legend=False
        )
        self.data[::-1].plot(
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
            self.data['local_date_time'][::-1],
            self.data['air_temp'][::-1],
            color='tab:red',
            label='temperature',
        )
        ax1.set_ylabel('Temperature [°C]')
        ax1.set_title('Latest observations from Melbourne (Olympic Park)')

        ax2 = ax1.twinx()

        ln2 = ax2.plot(
            self.data['local_date_time'][::-1],
            self.data['rel_hum'][::-1],
            color='tab:blue',
            label='humidity',
        )
        ax2.set_ylabel('Relative humidity [%]')

        ax1.xaxis.set_major_locator(plt.MaxNLocator(20))
        ax1.grid(linestyle='--')

        lns = ln1 + ln2
        labs = [l.get_label() for l in lns]
        ax1.legend(lns, labs, loc=0)


def _read_axf(filename):

    non_csv_data = dict()
    line_number = -1
    get_columns = False
    with open(filename) as data_file:
        for line in data_file:
            line_number += 1
            line = line.strip()
            if line == '':
                continue
            if line.startswith('[data]'):
                csv_start = line_number + 2
                get_columns = True
                continue
            if get_columns:
                columns = [column.split('[')[0] for column in line.split(',')]
                break
            if line[0] == '[' and line[1] != '$':
                section = line[1:-1]
                non_csv_data[section] = dict()
                continue
            if line == '[$]':
                continue
            key = line[: line.find('[')]
            value = line.split('=')[-1].strip('"')
            non_csv_data[section][key] = value

    data = pd.read_csv(filename, names=columns, skiprows=csv_start, comment='[')
    header = non_csv_data['header']
    notice = non_csv_data['notice']

    return notice, header, data
