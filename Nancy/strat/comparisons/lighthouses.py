# Module to examine lighthouse data and compare with model

# Nancy Soontiens, 2015

import pandas as pd
from salishsea_tools.nowcast import analyze
from salishsea_tools import tidetools, viz_tools
import matplotlib.pyplot as plt
import numpy as np

LIGHTHOUSES = {'Race Rocks':
               'http://www.pac.dfo-mpo.gc.ca/science/oceans/data-donnees/lighthouses-phares/data/racerockday.txt',
               'Entrance Island':
               'http://www.pac.dfo-mpo.gc.ca/science/oceans/data-donnees/lighthouses-phares/data/entranceday.txt',
               'Chrome Island':
               'http://www.pac.dfo-mpo.gc.ca/science/oceans/data-donnees/lighthouses-phares/data/chromeday.txt',
               'Departure Bay':
               'http://www.pac.dfo-mpo.gc.ca/science/oceans/data-donnees/lighthouses-phares/data/departurday.txt'}

MODEL_PATHS = {'nowcast': '/data/dlatorne/MEOPAR/SalishSea/nowcast/',
               'spinup': '/ocean//dlatorne/MEOPAR/SalishSea/results/spin-up/'
               }


def load_lighthouse(url):
    """ Loads lighthouse data at the specified url

    returns data, lat, lon
    data is the lighthouse dataframe with data, Year, Month, Day,
    Salinity(psu) and Temperature(C) columns
    lat is the lighthouse latitude (float)
    lon is the lighthouse longitude (float) """

    data = pd.read_table(url, delim_whitespace=True, skiprows=2,
                         na_values=99.9, parse_dates={'date': [0, 1, 2]},
                         keep_date_col=True)
    data['date'] = pd.to_datetime(data['date'])
    data[['Month', 'Day']] = data[['Month', 'Day']].astype(int)

    # grab lat and lon
    tmp = pd.read_csv(url, nrows=1, delim_whitespace=True,
                      header=None, skiprows=1)
    lat = divmod(float(tmp[2]), 1)[0] + divmod(float(tmp[2]), 1)[1]*100/60.
    lon = -(divmod(float(tmp[3]), 1)[0] + divmod(float(tmp[3]), 1)[1]*100/60.)

    return data, lat, lon


def compare_model(to, tf, lighthouse, mode, grid_B, smin=28, smax=33):
    # Load observations
    data, lat, lon = load_lighthouse(LIGHTHOUSES[lighthouse])
    # Look up modle grid point
    X = grid_B.variables['nav_lon'][:]
    Y = grid_B.variables['nav_lat'][:]
    bathy = grid_B.variables['Bathymetry'][:]
    j, i = tidetools.find_closest_model_point(lon, lat, X, Y, bathy)

    # load model
    files = analyze.get_filenames(to, tf, '1d', 'grid_T', MODEL_PATHS[mode])
    sal_daily, time_daily = analyze.combine_files(files, 'vosaline', 0, j, i)

    # plotting
    fig, axs = plt.subplots(1, 2, figsize=(15, 5))

    # plot time series
    ax = axs[0]
    ax.plot(time_daily, sal_daily, label=mode)
    ax.plot(data['date'], data['Salinity(psu)'], label='observations')
    ax.legend(loc=0)
    ax.set_title('{} Salinity'.format(lighthouse))
    ax.set_xlim([to, tf])
    ax.set_ylim([smin, smax])
    fig.autofmt_xdate()
    # plot map
    axm = axs[1]
    axm.plot(lon, lat, 'o')
    viz_tools.plot_coastline(axm, grid_B, coords='map')

    return fig


def monthly_means(lighthouse, smin=28, smax=33):

    data, lat, lon = load_lighthouse(LIGHTHOUSES[lighthouse])
    fig, ax = plt.subplots(1, 1)
    grouped = data.groupby(['Month'])
    mean = grouped.apply(np.mean)
    mean.plot(y='Salinity(psu)', ax=ax)
    ax.set_ylim([smin, smax])
    ax.set_title('{} Monthly Mean Salinity'.format(lighthouse))

    return fig
