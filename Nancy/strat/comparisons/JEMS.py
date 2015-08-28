# Module to compare JEMS data with model output
# Reference: https://fortress.wa.gov/ecy/eap/marinewq/mwdataset.asp

# Nancy Soontiens, 2015

import numpy as np
import pandas as pd
import os
import glob
import matplotlib.pyplot as plt
import netCDF4 as nc

from salishsea_tools import tidetools, viz_tools

SITES = {
    'ADM001': {
        'lat': 48.0300,
        'lon': -122.6167,
        'depth': 153},
    'ADM002': {
        'lat': 48.1875,
        'lon': -122.8417,
        'depth': 97},
    'BLL009': {
        'lat': 48.6867,
        'lon': -122.5983,
        'depth': 31},
    'GRG002': {
        'lat': 48.8083,
        'lon': -122.9533,
        'depth': 201},
    'PSS019': {
        'lat': 48.0117,
        'lon': -122.3000,
        'depth': 107},
    'SEQ002': {
        'lat': 48.0767,
        'lon': -123.0167,
        'depth': 31.5},
    'SKG003': {
        'lat': 48.2967,
        'lon': -122.4883,
        'depth': 25}
}


def load_JEMS_csv(stn):
    """Loads data contained in a JEMS csv file

    :arg stn: the name of the JEMS station
    :type stn: string

    :returns: data, a pandas data frame object
    """
    path = '/ocean/nsoontie/MEOPAR/JEMS/'
    filename = os.path.join(path, '{}_0.csv'.format(stn))
    data = pd.read_csv(filename, error_bad_lines=False, parse_dates=[1],
                       skipinitialspace=True, warn_bad_lines=False)
    data['date'] = pd.to_datetime(data['date'])

    return data


def isolate_dates(data, sdt, edt):
    """ Isolate data in specified date range

    :arg data: the data to be subsetted. Has a column named 'date'
    :type data: pandas dataframe

    :arg sdt: the start date of the subset
    :type sdt: datetime object

    :arg edt: the end date of the subset
    :type edt: datetime object

    :returns: subsetted data frame
    """
    return data[(data['date'] >= sdt) & (data['date'] <= edt)]


def compare_JEMS_model(stn, sdt, edt, grid_B, results_home,
                       smin=5, smax=31, tmin=8, tmax=12):
    """Comparison between all JEMS T+S data in a date range and model nowcasts.

    :arg stn: The JEMS station name
    :type stn: string

    :arg sdt: the start date of the date range
    :type sdt: datetime object

    :arg edt: the end date of the date range
    :type edt: datetime object

    :arg grid_B: the model bathymetry
    :type grid_B: netCDF handle

    :arg results_home: the path to the model results
    :type results_home: string

    :arg smin: minimum salinity for axis
    :type smin: float

    :arg smax: maximum salinity for axis
    :type smax: float

    :arg tmin: minimum temperature for axis
    :type tmin: float

    :arg tmax: maximum salinity for axis
    :type tmax: float

    :returns: figmap, fig - figure objects for the map and comaprisons plots
    """

    # Observations
    lat = SITES[stn]['lat']
    lon = SITES[stn]['lon']
    data = load_JEMS_csv(stn)
    data = isolate_dates(data, sdt, edt)
    data = data.groupby('date')

    # Model grid
    X = grid_B.variables['nav_lon'][:]
    Y = grid_B.variables['nav_lat'][:]
    bathy = grid_B.variables['Bathymetry'][:]
    [j, i] = tidetools.find_closest_model_point(lon, lat, X, Y, bathy)

    # Set up loop and figure
    num = data.ngroups
    fig, axs = plt.subplots(num, 2, figsize=(10, 4*num))
    try:
        for day, axS, axT in zip(data.groups, axs[:, 0], axs[:, 1]):
            plot_comparisons(day, axS, axT, results_home, data, stn, j, i)
            axS.set_xlim([smin, smax])
            axS.set_ylim([SITES[stn]['depth'], 0])
            axT.set_xlim([tmin, tmax])
            axT.set_ylim([SITES[stn]['depth'], 0])
        axS.set_xlabel('Salinity (psu)')
        axT.set_xlabel('Temperature (deg C)')
    except IndexError:
        day = data.groups.keys()[0]
        axS = axs[0]
        axT = axs[1]
        plot_comparisons(day, axS, axT, results_home, data, stn, j, i)
        axS.set_xlim([smin, smax])
        axS.set_ylim([SITES[stn]['depth'], 0])
        axT.set_xlim([tmin, tmax])
        axT.set_ylim([SITES[stn]['depth'], 0])
        axS.set_xlabel('Salinity (psu)')
        axT.set_xlabel('Temperature (deg C)')

    # map
    figmap, ax = plt.subplots(1, 1)
    viz_tools.plot_coastline(ax, grid_B, coords='map')
    ax.plot(lon, lat, 'o')
    ax.set_title(stn)

    return figmap, fig


def plot_comparisons(day, axS, axT, results_home, data, stn, j, i):
    """Plots the observed and modelled temperature and salinity profiles
     Modelled profiles are of the daily mean with +-2 daily standard deviation.

    :arg day: the day for comparison. This is a key from the data pandas
     grouped object.
    :type day: numpy datetime64

    :arg axS: axis for plotting salinity
    :type axS: axis object

    :arg axT: axis for plotting temperature
    :type axT: axis object

    :arg results_home: directory path to model results
    :type results_home: string

    :arg data: Dataframe that contains observations, grouped by day
    :type data: grouped pandas DataFrame

    :arg stn: the JEMS station name
    :type stn: string

    :arg j: the NEMO y-index
    :type j: integer

    :arg i: the NEMO x-index
    :type i: integer
    """

    dt = pd.to_datetime(day)
    obs = data.get_group(day)
    # Model files
    results_dir = os.path.join(results_home, dt.strftime('%d%b%y').lower())
    grid_T = results_dataset('1d', 'grid_T', results_dir)
    sal = grid_T.variables['vosaline'][0, :, j, i]
    sal = np.ma.masked_values(sal, 0)
    temp = grid_T.variables['votemper'][0, :, j, i]
    temp = np.ma.masked_values(temp, 0)
    deptht = grid_T.variables['deptht'][:]
    # Hourly data
    grid_T = results_dataset('1h', 'grid_T', results_dir)
    sal_hr = grid_T.variables['vosaline'][:, :, j, i]
    sal_hr = np.ma.masked_values(sal_hr, 0)
    temp_hr = grid_T.variables['votemper'][:, :, j, i]
    temp_hr = np.ma.masked_values(temp_hr, 0)
    # Standard deviations
    sal_std = np.std(sal_hr, axis=0)
    temp_std = np.std(temp_hr, axis=0)

    # plotting Salinty
    axS.plot(sal, deptht, label='model daily average')
    axS.plot(obs['salinity (psu)'], obs['depth (meters)'], label='obs')
    # labels, legends, etc
    axS.set_title(dt.strftime('%Y-%m-%d'))
    axS.set_ylabel('Depth (m)')
    axS.legend(loc=0)
    # plotting temperature
    axT.plot(temp, deptht, label='model')
    axT.plot(obs['temperature (centigrade)'], obs['depth (meters)'],
             label='obs')
    # labels, legends, etc
    axT.set_title(dt.strftime('%Y-%m-%d'))
    axT.legend(loc=0)
    # plot mean+-2*std
    axS.plot(sal+2*sal_std, deptht, alpha=0.5, color='b', ls=':')
    axS.plot(sal-2*sal_std, deptht, alpha=0.5, color='b', ls=':')
    axT.plot(temp+2*temp_std, deptht, alpha=0.5, color='b', ls=':')
    axT.plot(temp-2*temp_std, deptht, alpha=0.5, color='b', ls=':')


def results_dataset(period, grid, results_dir):
    """Return the results dataset for period (e.g. 1h or 1d)
    and grid (e.g. grid_T, grid_U) from results_dir.
    """
    filename_pattern = 'SalishSea_{period}_*_{grid}.nc'
    filepaths = glob.glob(
        os.path.join(
            results_dir, filename_pattern.format(period=period, grid=grid)))
    return nc.Dataset(filepaths[0])
