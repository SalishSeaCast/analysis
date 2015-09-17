# Module to load Ocean Networks Canada csv files. Data is from moorings.

# Nancy Soontiens, 2015

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import netCDF4 as nc
from scipy import interpolate as interp


from salishsea_tools import tidetools, viz_tools
from salishsea_tools.nowcast import analyze


def load_mooring_csv(csvfilename):
    """Loads data contained in an ONC mooring csv file

    :arg csvfilename: path to the csv file
    :type csvfilename: string

    :returns: data, lat, lon, depth - a pandas data frame object and the
    latitude, longitude and depth of the morning
    """

    data_line, lat, lon, depth = find_metadata(csvfilename)
    # Look up headers
    headers = pd.read_csv(csvfilename, skiprows=data_line-2, nrows=1,
                          header=None, skipinitialspace=True, dtype=str)
    headers = np.array(headers)[0]
    headers[0] = headers[0].replace('#', '')
    headers[0] = headers[0].replace('"', '')

    # Load data
    data = pd.read_csv(csvfilename, header=None, skiprows=data_line,
                       names=headers, parse_dates=[0], low_memory=False)
    data = data.convert_objects(convert_numeric=True)
    data.rename(columns={'Time UTC (yyyy-mm-ddThh:mm:ss.fffZ)': 'time'},
                inplace=True)
    return data, lat, lon, depth


def find_metadata(csvfilename):
    """Look up the metadata, like latitude, longitude, depth for the data stored
    in csvfilename"

    :arg csvfilename: path of the csv file to open
    :type csvfilename: string

    :returns: data_line, lat, lon, depth - the first line of data, and the
    latitude, longitude and depth of the mooring.
    """

    l = open(csvfilename, 'r')

    # look up beginning of data, latitude, longitude, and depth
    for i, line in enumerate(l):
        if '#LATITUDE' in line:
            words = line.split()
            lat = float(words[1])
        if '#LONGITUDE' in line:
            words = line.split()
            lon = float(words[1])
        if '#DEPTH' in line:
            words = line.split()
            depth = float(words[1])
        if "#" not in line:
            data_line = i
            break
    l.close()

    return data_line, lat, lon, depth


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
    return data[(data['time'] >= sdt) & (data['time'] <= edt)]


def isolate_qc_data(data, qc_flag):
    """Return the data with QC flag 1 for the specified variable

    :arg data: the data
    :type data: pandas dataframe

    :arg qc_flag: the header for the desired qc flag,
    eg. 'Practical Salinity QC Flag  '
    :type qc_flag: string

    :returns: data_qc - the data subsetted with qc_flag=1
    """
    data_qc = data[data[qc_flag] == 1]

    return data_qc


def interpolate_depth(variable, depth_array, depth_new, depth_axis=1):
    """ interpolates a variable depth profile field to desire depth.
    The data in the variable will be masked at 0 values

    :arg variable: depth profile of the variable. 0 is interpreted as a
     masked value
    :type variable: numpy array

    :arg depth_array: the depth array associated with variable
    :type depth_array: numpy array

    :arg depth_new: the depth to interpolate to
    :type depth_new: float

    :arg depth_axis: the axis corresponding to depths in variable
    :type depth_axis: int

    :returns: var_new, the variable interpolated to depth_new
    """
    # mask
    mu = variable == 0
    var_mask = np.ma.array(variable, mask=mu)
    mu = depth_array == 0
    d_mask = np.ma.array(depth_array, mask=mu)
    f = interp.interp1d(d_mask, var_mask, axis=depth_axis)
    var_new = f(depth_new)

    return var_new


def load_model_data(sdt, edt, grid_B, results_home, period,
                    variable, lat, lon):
    """Load the model data in date range of interest and at the location.
    :arg sdt: the start date
    :type sdt: datetime object

    :arg edt: the end date
    :type edt: datetime object

    :arg grid_B: the model bathymetry
    :type grid_B: netCDF4 handle

    :arg results_home: directory for model results
    :type restuls_home: string

    :arg period: the model avergaing period eg '1h' or '1d'
    :time period: string

    :arg variable: the variable to be loaded, eg 'vosaline' or 'votemper'
    :type variable: string.

    :arg lat: the latitude
    :type lat: float

    :arg lon: the longitude
    :type lon: float

    :returns: var, times, mdepths - the array of data, the times associated
    and the model depth array
    """

    files = analyze.get_filenames(sdt, edt, period, 'grid_T', results_home)
    ftmp = nc.Dataset(files[0])
    mdepths = ftmp.variables['deptht'][:]
    # Model grid
    X = grid_B.variables['nav_lon'][:]
    Y = grid_B.variables['nav_lat'][:]
    bathy = grid_B.variables['Bathymetry'][:]
    # Look up grid coordinates
    j, i = tidetools.find_closest_model_point(lon, lat, X, Y, bathy)
    # Grab model data
    var, times = analyze.combine_files(files, variable,
                                       np.arange(mdepths.shape[0]), j, i)

    return var, times, mdepths


def resample_obs(data, period):
    """Resample observations based on period

    :arg data: the data to be resampled
    :type data: pandas data frame with time column

    :arg period: the resampling period, eg. '1h' or '1d'
    :type period: string

    :returns: data_r, the resampled data frame
    """
    # Add time to index
    date_index = pd.DatetimeIndex(data['time'])
    data['date_index'] = date_index
    data.set_index('date_index', inplace=True)
    if period == '1h':
        r = 'H'
    elif period == '1d':
        r = 'D'
    data_r = data.resample(r, how='mean', base=0.5)
    # Re add time column and remove index
    data_r['time'] = data_r.index
    data_r = data_r.reset_index(drop=True)

    return data_r


def model_vertical_postion(sal, temp, mdepths, depth, interp):
    """Align the model output with the correct vertical position.
    Either interpolate or closest model level

    :arg sal: model salinty
    :type sal: numpy array

    :arg temp: model temperature
    :type temp: numpy array

    :arg mdepths: model depths
    :type mdepths: numpy array

    :arg depth: observations depth - used to look up model grid point or
    interpolate
    :type depth: float

    :arg interp: if True - interpolate model to depth otherwise look up
    closest model level
    :type interp: boolean

    :returns: sal_level, temp_level, text - the salinity and temperature at the
    desired depth level and text to be added to the figure
    """
    if interp:
        sal_level = interpolate_depth(sal, mdepths, depth, depth_axis=1)
        temp_level = interpolate_depth(temp, mdepths, depth, depth_axis=1)
        text = 'Depth: {} m'.format(depth)
    else:
        k = tidetools.find_model_level(depth, mdepths)
        # Use one grid point higher if masked
        if sal[:, k].any() == 0:
            k = k - 1
        sal_level = sal[:, k]
        temp_level = temp[:, k]
        text = 'Observed depth: {} m, Model depth: {} m'.format(depth,
                                                                mdepths[k])
    return sal_level, temp_level, text


def compare_ONC_model(csvfilename, sdt, edt, grid_B, results_home, period='1h',
                      interp=False, smin=30, smax=35, tmin=8, tmax=12):
    """Comparison between ONC mooring data in a date range and model results.

    :arg csvfilename: The file with the ONC data
    :type csvfilename: string

    :arg sdt: the start date of the date range
    :type sdt: datetime object

    :arg edt: the end date of the date range
    :type edt: datetime object

    :arg grid_B: the model bathymetry
    :type grid_B: netCDF handle

    :arg results_home: the path to the model results
    :type results_home: string

    :arg interp: a flag to specify if model should be interpolated to depth
     or just use closest model grid point
    :type interp: boolean

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
    data, lat, lon, depth = load_mooring_csv(csvfilename)
    # resample observations and isolate date range
    data = isolate_dates(data, sdt, edt)
    data = resample_obs(data, period)
    # Model files
    sal, times, mdepths = load_model_data(sdt, edt, grid_B, results_home,
                                          period, 'vosaline', lat, lon)
    temp, times, mdepths = load_model_data(sdt, edt, grid_B, results_home,
                                           period, 'votemper', lat, lon)
    # Align model vertically
    sal, temp, text = model_vertical_postion(sal, temp, mdepths, depth, interp)

    # Plotting
    fig, axs = plt.subplots(2, 1, figsize=(10, 7))
    # Salinity
    ax = axs[0]
    ax.plot(times, sal, label='model')
    qc_data = isolate_qc_data(data, 'Practical Salinity QC Flag  ')
    ax.plot(qc_data['time'], qc_data['Practical Salinity (psu)'],
            label='observations')
    ax.set_ylabel('Practical Salinity [psu]')
    # Temperature
    ax = axs[1]
    ax.plot(times, temp, label='model')
    qc_data = isolate_qc_data(data, 'Temperature QC Flag  ')
    ax.plot(qc_data['time'], qc_data['Temperature (C)'], label='observations')
    ax.set_ylabel('Temperature [C]')

    # Format figure
    title = '{} average - '.format(period) + text
    for ax, lims in zip(axs, [[smin, smax], [tmin, tmax]]):
        ax.set_xlim([sdt, edt])
        ax.set_ylim(lims)
        ax.legend(loc=0)
        ax.grid()
        ax.set_title(title)
    # Plot map
    figmap, ax = plt.subplots(1, 1)
    viz_tools.plot_coastline(ax, grid_B, coords='map')
    ax.plot(lon, lat, 'o')

    return figmap, fig
