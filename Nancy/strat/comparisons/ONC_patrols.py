# Module to load ONC CTD casts from patrols.
# Inlcudes functions to compare with model results

# NKS March 2016

import datetime
import numpy as np
import pandas as pd
import os
import netCDF4 as nc
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors

import comparisons

from salishsea_tools import tidetools, viz_tools


NOWCAST_PATH = '/results/SalishSea/nowcast/'


def find_data_line(csvfilename):
    """ Look up line number where data beings in csvfilename.
    Assumes first line without # in the front is the data

    :arg csvfilename: name of file
    :type csvfilename: string

    :returns: data_line, the line number of the data.
    """
    l = open(csvfilename, 'r')

    for i, line in enumerate(l):
        if "#" not in line:
            data_line = i
            break
    l.close()

    return data_line


def find_column_names(csvfilename, data_line):
    """Find the columns in an ONC csv file.
    Assumes column names are the line before two lines before data_line

    :arg csvfilename: name of file
    :type csvfilename: string

    :arg data_line: line number where the data begins
    :type data_lins: nonnegative integer

    :returns: columns
    line number of data start and list of column names
    """
    columns = pd.read_csv(csvfilename, skiprows=data_line-2, nrows=1,
                          header=None, skipinitialspace=True, dtype=str)
    columns = np.array(columns)[0]
    columns[0] = columns[0].replace('#', '')
    columns[0] = columns[0].replace('"', '')

    return columns


def load_patrol_csv(csvfilename):
    """Loads data contained in ONC patrol csv.

    :arg csvfilename: name of file
    :type csvfilename: string

    :returns: data, a pandas dataframe
    """

    data_line = find_data_line(csvfilename)
    columns = find_column_names(csvfilename, data_line)
    data = pd.read_csv(csvfilename, header=None, skiprows=data_line,
                       names=columns, parse_dates=[0], low_memory=False)
    data = data.convert_objects(convert_numeric=True)
    data.rename(columns={'Time UTC (yyyy-mm-ddThh:mm:ss.fffZ)': 'time'},
                inplace=True)
    data['day'] = [datetime.datetime(d.year, d.month, d.day)
                   for d in data.time]
    return data


def exclude_bad(data, columns, values):
    """Exclude rows of data with poor quality control flags.
    eg. data_new = exlcude_bad(data,
                               ['Practical Salinity Corrected QC Flag '],
                               [0,4,9])
    :arg data: the data set
    :type data: pandas DataFrame

    :arg columns: Column names with quality control information
    :type columns: list of strings

    :arg values: the quaility control values to be exlcuded
    :type values: lis tof integers

    :returns: data_return - new data frame with bad data excluded.
    """

    data_return = data
    for col in columns:
        for val in values:
            data_return = data_return[data_return[col] != val]
    return data_return


def list_days(data):
    """List the days in the database

    :arg data: the database. data is expected to have a column
    called day with datetimes Y-M-D
    :type data: pandas dataframe

    :returns: data_days, days
    data_days is a grouped dataframe, grouped by the day
    days is a list of the days in data
    """
    data_days = data.groupby(data.day)
    days = list(data_days.groups.keys())
    return data_days, days


def divide_into_casts(data):
    """Add a Cast column to an ONC data set.
    The result is that the dayta set is divided into casts.
    Assumes that a single cast is separated by monotonically increasing depths

    :arg data: the ONC dataset
    :type data: pandas DataFrame

    :returns: data_divivded, the data set divided into casts
    """

    cast_num = []
    data_divided = data

    depths = np.array(data['Depth Corrected (m)'])
    d1 = depths[0]
    cast = 1
    cast_num.append(cast)
    for d in depths[1:]:
        if d <= d1:
            cast = cast + 1
        d1 = d
        cast_num.append(cast)

    data_divided['Cast'] = cast_num
    return data_divided


def cast_position_and_time(cast):
    """Retrieve ONC cast average longitude, latitude and minimum time.

    :arg cast: the ONC cast
    :type cast: a single group of pandas grouby object

    :returns: lat, lon, date
    """

    lon = cast['Longitude Corrected (deg)'].mean()
    lat = cast['Latitude Corrected (deg)'].mean()
    date = cast['day'].min()

    return lat, lon, date


def results_dataset(period, grid, date):
    """Retrieve nowcast data set results

    :arg period: averaging period of results, e.g. '1h' or '1d'
    :type period: string

    :arg grid: grid type, e.g. 'grid_T' or 'grid_U'
    :type grid: string

    :arg date: date of results
    :type date: datetime

    :returns: netCDF4 handle
    """
    sub_dir = date.strftime('%d%b%y').lower()
    datestr = date.strftime('%Y%m%d')
    fname = 'SalishSea_{}_{}_{}_{}.nc'.format(period, datestr, datestr, grid)
    return nc.Dataset(os.path.join(NOWCAST_PATH, sub_dir, fname))


def retrieve_nowcast_data(lon, lat, date, obs_depth, field, grid_B, mesh_mask):
    """Gather nowcast field daily mean, min and max at lat, lon on date,
    interpolated to obs_depth.

    :arg lon: longitude point
    :type lon: real number

    :arg lat: latitude point
    :type lat: real number

    :arg date: simulation date
    :type date: datetime

    :arg obs_depth: array of depths to be interpolated to
    :type obs_depth: numpy array

    :arg field: name of variable to load, e.g 'vosaline' or 'votemper'
    :type field: string

    :arg grid_B: model bathymetry
    :type grid_B: netCDF4 object

    :arg mesh_mask: model mesh mask
    :type mesh_mask: netCDF4 object

    :returns: model_d_interp, model_max, model_min - numpy arrays
    """
    # look up model grid point
    bathy, lons, lats = tidetools.get_bathy_data(grid_B)
    j, i = tidetools.find_closest_model_point(lon, lat, lons, lats, bathy)
    # loading
    grid_d = results_dataset('1d', 'grid_T', date)
    grid_h = results_dataset('1h', 'grid_T', date)
    model_d = grid_d.variables[field][0, :, j, i]
    model_h = grid_h.variables[field][:, :, j, i]
    gdep = mesh_mask.variables['gdept'][0, :, j, i]
    # masking
    tmask = mesh_mask.variables['tmask'][:, :, j, i]
    tmask = 1 - tmask + np.zeros(model_h.shape)
    model_d = np.ma.array(model_d, mask=tmask[0, :])
    gdep_mask = np.ma.array(gdep, mask=tmask[0, :])
    model_h = np.ma.array(model_h, mask=tmask)
    # interpolate to observed depth
    model_d_interp = comparisons.interpolate_depth(model_d, gdep_mask,
                                                   obs_depth)
    model_h_interp = np.zeros((model_h.shape[0], len(obs_depth)))
    for t in np.arange(model_h.shape[0]):
        model_h_interp[t, :] = comparisons.interpolate_depth(model_h[t, :],
                                                             gdep_mask,
                                                             obs_depth)
    # daily max and min
    model_max = np.max(model_h_interp, axis=0)
    model_min = np.min(model_h_interp, axis=0)

    return model_d_interp, model_max, model_min


def plot_profile_comparison(ax, cast, model_d_interp, var_name,
                            var_lims, depth_lims):
    """Plot cast depth profile comparison between model and observations

    :arg ax: axis for plotting
    :type ax: axis object

    :arg cast: the observed cast for comaprison
    :type cast: pandas DataFrame-like object

    :arg model_d_interp: model values interpolated to observed depths
    :type model_d_interp: numpy array

    :arg var_name: observed variable name,
    eg 'Practical Salinity Corrected (psu)'
    :type var_name: string

    :arg var_lims: min/max variable values, eg [29,34]
    :type var_lims: 2-tuple

    :arg depth_lims: min/max depth values, eg [0,150]
    :type depth_lims: 2-tuple

    :returns: lo, lm - scatter plot handles for observations and model.
    Can be used for adding a legend later.
    """

    lo = ax.scatter(cast[var_name], cast['Depth Corrected (m)'],
                    c='g', label='Observed')
    lm = ax.scatter(model_d_interp, cast['Depth Corrected (m)'],
                    c='b', label='Modelled')

    ax.set_ylim([depth_lims[-1], depth_lims[0]])
    ax.set_ylabel('Depth [m]')

    ax.set_xlim(var_lims)
    ax.set_xlabel(var_name)

    ax.set_title(cast.day.min().strftime('%Y-%m-%d'))

    return lo, lm


def plot_map(ax, cast, grid_B, xlims, ylims):
    """ Plot the location of cast lon/lat on a map.

    :arg ax: axis for plotting
    :type ax: axis object

    :arg cast: the observed cast
    :type cast: pandas DataFrame-like object

    :arg grid_B: model bathymetry
    :type grid_B: netCDF4 object

    :arg xlims: min/max longitudes, eg [-124,-123]
    :type xlims: 2-tuple

    :arg ylims: min/max latitudes, eg [48,49]
    :type ylims: 2-tuple

    """
    cast.plot(x='Longitude Corrected (deg)', y='Latitude Corrected (deg)',
              kind='scatter', ax=ax)
    viz_tools.plot_coastline(ax, grid_B, coords='map')
    ax.set_xlim(xlims)
    ax.set_ylim(ylims)
    ax.set_title(cast.day.min().strftime('%Y-%m-%d'))


def plot_scatter_comparison(ax, cast, model_d_interp, model_max,
                            model_min, var_name, var_lims, depth_lims):
    """Scatter plot to compare observed and model daily average values.
    Plots model error bars based on model daily max/min.
    Points are coloured by depth

    :arg ax: axis for plotting
    :type ax: axis object

    :arg cast: the observed cast for comaprison
    :type cast: pandas DataFrame-like object

    :arg model_d_interp: model values interpolated to observed depths
    :type model_d_interp: numpy array

    :arg model_max: model daily maximum interpolated to observed depths
    :type model_max: numpy array

    :arg model_min: model daily minimum interpolated to observed depths
    :type model_min: numpy array

    :arg var_name: observed variable name,
    eg 'Practical Salinity Corrected (psu)'
    :type var_name: string

    :arg var_lims: min/max variable values, eg [29,34]
    :type var_lims: 2-tuple

    :arg depth_lims: min/max depth values, eg [0,150]
    :type depth_lims: 2-tuple

    :returns: mesh - scatter plot depth colors.
    Can be used for adding a colorbar.
    """
    yerr = [model_d_interp-model_min, model_max-model_d_interp]
    ax.errorbar(cast[var_name], model_d_interp, yerr=yerr, fmt='k:',
                ecolor='gray', marker='', zorder=0)
    mesh = ax.scatter(cast[var_name], model_d_interp,
                      c=cast['Depth Corrected (m)'], cmap='Spectral',
                      norm=mcolors.LogNorm(),
                      vmin=depth_lims[0]+.5, vmax=depth_lims[1])
    ax.plot(var_lims, var_lims, 'r')
    ax.set_ylim(var_lims)
    ax.set_xlim(var_lims)
    ax.set_xlabel('Observed {}'.format(var_name))
    ax.set_ylabel('Modelled {}'.format(var_name))
    ax.set_title(cast.day.min().strftime('%Y-%m-%d'))
    return mesh


def compare_patrol_model_obs(data, names, grid_B, mesh_mask,
                             var_lims=[29, 34], depth_lims=[0, 160],
                             xlims=[-124, -123], ylims=[48, 49]):
    """ Compare model and observations for all ctd casts in data.
    For each day in data this code produces
    a. A scatter plot of obs vs data
    b. A obs vs data depth profile comparison
    c. A map with observed lon/lats in the comaparison

    :arg data: observed data from an ONC patrols
    It is a good idea to exclude data points with low QC
    :type data: pandas DataFrame

    :arg names: dictionary with observed, model variable name mapping
    e.g names = {'obs': 'Practical Salinity Corrected (psu)',
                 'model': 'vosaline' }
    :type names: dictionary

    :arg grid_B: model bathymetry
    :type grid_B: netCDF4 object

    :arg mesh_mask: model mesh mask
    :type mesh_mask: netCDF4 object

    :arg var_lims: min/max variable values, eg [29,34]
    :type var_lims: 2-tuple

    :arg depth_lims: min/max depth values, eg [0,150]
    :type depth_lims: 2-tuple

    :arg xlims: min/max longitudes, eg [-124,-123]
    :type xlims: 2-tuple

    :arg ylims: min/max latitudes, eg [48,49]
    :type ylims: 2-tuple
    """

    # Observed and model field names
    var_name = names['obs']
    field = names['model']
    # Loop through days
    data_days, days = list_days(data)
    for d in days:
        daily = data_days.get_group(d).dropna()
        daily_casts = daily.groupby('Cast')
        fig, axs = plt.subplots(1, 3, figsize=(15, 3))
        # Loop through casts in a day
        for c in daily_casts.groups:
            cast = daily_casts.get_group(c)
            lat, lon, date = cast_position_and_time(cast)
            obs_depth = np.array(cast['Depth Corrected (m)'][:])
            try:
                model_d_interp, model_max, model_min = retrieve_nowcast_data(
                    lon, lat, date, obs_depth, field, grid_B, mesh_mask)
                mesh = plot_scatter_comparison(axs[0], cast, model_d_interp,
                                               model_max, model_min,
                                               var_name, var_lims, depth_lims)
                lo, lm = plot_profile_comparison(axs[1], cast,
                                                 model_d_interp, var_name,
                                                 var_lims, depth_lims)
                plot_map(axs[2], cast, grid_B, xlims, ylims)
            except IndexError:
                print(
                    'No Model Point for {} {}'.format(
                        cast['Longitude Corrected (deg)'].mean(),
                        cast['Latitude Corrected (deg)'].mean()))
        # Label colorbar, etc
        try:
            cbar = plt.colorbar(mesh, ax=axs[0])
            cbar.set_label('Depth (m)')
            ticks = [1, 10, 25, 50, 100, 200, 400]
            cbar.set_ticks(ticks)
            cbar.set_ticklabels(ticks)
            axs[1].legend([lo, lm], ['Observed', 'Modelled'])
        except UnboundLocalError:
            print('No plot for {}'.format(d))
