# Module to examine lighthouse data and compare with model

# Nancy Soontiens, 2015

import pandas as pd
from salishsea_tools.nowcast import analyze
from salishsea_tools import tidetools, viz_tools
import matplotlib.pyplot as plt
import numpy as np
from dateutil import tz
import datetime

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


def daytime_hightide(ssh, times):
    """Finds the index of the daytime high tides.
    Daytime is defined between 0530 and 1830 PST.

    :arg ssh: the sea surface height values
    :type ssh: numpy array (1D)

    :arg times: the times corresponding to the ssh values in UTC
    :type times: numpy array of datetime objects

    :returns: inds, a list of indices for the daytime high tides."""

    # Convert times to PST
    myPST = tz.tzoffset('myPST', -8*3600)
    times_pst = [d.astimezone(myPST) for d in times]
    times_pst = np.array(times_pst)

    # Loop through each day
    to = times[0]
    tf = times[-1]
    days = [to + datetime.timedelta(days=n) for n in np.arange((tf-to).days)]
    max_inds = []
    for day in days:
        # Define datetime to be between 0530 and 1830
        daytime1 = day.replace(hour=5, minute=30, tzinfo=myPST)
        daytime2 = day.replace(hour=18, minute=30, tzinfo=myPST)
        inds = np.where(
            np.logical_and(times_pst >= daytime1, times_pst <= daytime2)
        )

        # Isolate ssh in day time and calculate the difference netween sshs
        ssh_daytime = ssh[inds]
        ssh_diff = np.diff(ssh_daytime)

        # Look for index of maximun daytime high tide.
        # Defualt is maximim of the tide, but this might occur on boundary
        # Then, look for a local max by finding where differences switch
        # from pos to neg
        max_ind = np.argmax(ssh_daytime)
        for i in np.arange(1, len(ssh_diff)):
            if ssh_diff[i] < 0 and ssh_diff[i-1] > 0:
                max_ind = i

        # Find index of max tides and append to list
        max_time = times_pst[inds][max_ind].astimezone(tz=tz.tzutc())
        max_inds.append(np.where(times == max_time)[0][0])

    return max_inds


def compare_model(to, tf, lighthouse, mode, period, grid_B, smin=28, smax=33):
    # Load observations
    data, lat, lon = load_lighthouse(LIGHTHOUSES[lighthouse])
    # Look up modle grid point
    X = grid_B.variables['nav_lon'][:]
    Y = grid_B.variables['nav_lat'][:]
    bathy = grid_B.variables['Bathymetry'][:]
    j, i = tidetools.find_closest_model_point(lon, lat, X, Y, bathy)

    # load model
    files = analyze.get_filenames(to, tf, period, 'grid_T', MODEL_PATHS[mode])
    sal, time = analyze.combine_files(files, 'vosaline', 0, j, i)
    if period == '1h':
        # look up times of high tides
        ssh, times = analyze.combine_files(files, 'sossheig', 'None', j, i)
        print ssh.shape, sal.shape
        max_inds = daytime_hightide(ssh, times)
        sal = sal[max_inds]
        time = time[max_inds]
        title_str = 'max daytime tides'
    else:
        title_str = 'daily average'

    # plotting
    fig, ax = plt.subplots(1, 1, figsize=(8, 5))
    # plot time series
    ax.plot(time, sal, label=mode)
    ax.plot(data['date'], data['Salinity(psu)'], label='observations')
    ax.legend(loc=0)
    ax.set_title('{} Salinity - {}'.format(lighthouse, title_str))
    ax.set_xlim([to, tf])
    ax.set_ylim([smin, smax])
    ax.set_ylabel('Salinity [psu]')
    fig.autofmt_xdate()

    return fig


def monthly_means(lighthouse, grid_B, smin=28, smax=33):

    data, lat, lon = load_lighthouse(LIGHTHOUSES[lighthouse])
    fig, axs = plt.subplots(1, 2, figsize=(15, 5))
    grouped = data.groupby(['Month'])
    mean = grouped.apply(np.mean)
    ax = axs[0]
    mean.plot(y='Salinity(psu)', ax=ax)
    ax.set_ylim([smin, smax])
    ax.set_title('{} Monthly Mean Salinity'.format(lighthouse))
    # plot map
    axm = axs[1]
    axm.plot(lon, lat, 'o')
    viz_tools.plot_coastline(axm, grid_B, coords='map')

    return fig
