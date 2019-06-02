Bureau of Meteorology data
==========================

Use Bureau of Meteorology data to do something.

Install
-------

I use Conda to install this repository locally. From the main repository
directory, type

```
conda develop .
```

Then you should be able to `import bom`.

Use
---

The main use is to get 72 hour station forecast data. For example, to plot
Melbourne (Olympic Park) temperature and humidity from the last 72 hours:

```python
>>> melb = bom.Observations(
        'http://reg.bom.gov.au/fwo/IDV60901/IDV60901.95936.json'
    )

>>> melb.plot_temperature_humidity()
```

To find the URL, for example, Google "Latest Weather Observations for Melbourne
(Olympic Park)", follow the first link (probably), and then go to the bottom of
the page looking for a section "Other formats". There should be links to both
.axf and .json files. You need to replace the "www" in the URL with "reg".

See the examples directory for more examples.
