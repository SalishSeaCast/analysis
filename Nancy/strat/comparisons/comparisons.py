# Functions used to compare model and observation profiles

import netCDF4 as nc
from salishsea_tools import tidetools, viz_tools
import numpy as np
import matplotlib.pyplot as plt
import datetime
from salishsea_tools.nowcast import analyze
from wodpy import wod
import pandas as pd
import os
import glob


def read_file_to_dataframe(filename):
    """Reads a WOD file (filename) and returns data as a dataframe.
    data inlcudes columns Temperature, Salinity, Depth, Year, Month, Day,
    Longitude, Latitude, Datetime"""

    file = open(filename)

    # empty list for gatherting profiles.
    list_data = []

    # loop through profiles
    profile = wod.WodProfile(file)
    while not profile.is_last_profile_in_file(file):
        year = profile.year()
        lat = profile.latitude()
        lon = profile.longitude()
        s = profile.s()
        d = profile.z()
        t = profile.t()
        month = profile.month()
        day = profile.day()
        date = datetime.datetime(year, month, day)
        tmp = {'Year': year, 'Month': month, 'Day': day, 'Longitude': lon,
               'Latitude': lat,
               'Salinity': s, 'Temperature': t, 'Depth': d, 'Datetime': date}
        list_data.append(tmp)
        profile = wod.WodProfile(file)
    # again for last profile
    year = profile.year()
    lat = profile.latitude()
    lon = profile.longitude()
    s = profile.s()
    d = profile.z()
    t = profile.t()
    month = profile.month()
    day = profile.day()
    tmp = {'Year': year, 'Month': month, 'Day': day, 'Longitude': lon,
           'Latitude': lat,
           'Salinity': s, 'Temperature': t, 'Depth': d}
    list_data.append(tmp)

    # convert to data frame
    data = pd.DataFrame(list_data)

    return data


def isolate_region(data, lon_min, lon_max, lat_min, lat_max):
    """
    Isolates data in a rectangular region defined by lon_min, lon_max,
    lat_min, lat_max
    data is a pandas DataFrame
    """

    data_region = data[(data['Longitude'] > lon_min) &
                       (data['Longitude'] < lon_max) &
                       (data['Latitude'] > lat_min) &
                       (data['Latitude'] < lat_max)]
    return data_region


def isolate_time_period(data, start_date, end_date):
    """
    Isolates a time period in the data defined by start_date and end_date,
     both datetime objects.
     data is a pandas DataFrame.
    """

    data_time = data[(data['Datetime'] >= start_date) &
                     (data['Datetime'] <= end_date)]
    return data_time


def load_model(model_path, start_date, end_date, field, nowcast_flag=False):
    """Loads model grid_T data in date range defined by start_date and end_date
    Only considers daily averaged model fields.
    Returns model depths, variable defined by field, and dates associated with
    variable
    """

    files = analyze.get_filenames(start_date, end_date,
                                  '1d', 'grid_T', model_path)
    if nowcast_flag:
        var, dates = analyze.combine_files(files, field, np.arange(0, 40),
                                           np.arange(0, 898),
                                           np.arange(0, 398))
        tmp = nc.Dataset(files[0])
        depth = tmp.variables['deptht'][:]
    else:
        tracers = nc.MFDataset(files)
        time = tracers.variables['time_counter']
        # convert date
        dates = []
        start = datetime.datetime.strptime(time.time_origin,
                                           ' %Y-%b-%d %H:%M:%S')
        for t in time[:]:
            d = start + datetime.timedelta(seconds=t)
            dates.append(d)
        depth = tracers.variables['deptht'][:]
        var = tracers.variables[field][:]

    return depth, var, dates


def compare_model_obs(month, model_year, field, data_obs, model_path,
                      xmin=-124, xmax=-122, ymin=48, ymax=50,
                      zmin=0, zmax=300, vmin=10, vmax=32):
    """Compares the observations from WOD with model output on the same day
    and at a close grid point.
    Comparisons are during single month.
    field is compared ('Temperature' or 'Salinity' )
    Observations stored in data_obs (DataFrame)
    Model_path defines where the model data is stored(can be nowcast or spinup)
    """
    # Load model grid
    grid = '/data/nsoontie/MEOPAR/NEMO-forcing/grid/bathy_meter_SalishSea2.nc'
    f = nc.Dataset(grid)
    bathy = f.variables['Bathymetry'][:]
    X = f.variables['nav_lon'][:]
    Y = f.variables['nav_lat'][:]

    fig, [ax, axm] = plt.subplots(1, 2, figsize=(10, 3))

    # date ranges based on month and model_year
    sdt = datetime.datetime(model_year, month, 1)
    edt = sdt + datetime.timedelta(days=31)

    # Model variables and nowcast/spinup?
    if field == 'Salinity':
        model_field = 'vosaline'
    elif field == 'Temperatute':
        model_field = 'votemper'
    # Is this a nowcast?
    if model_year == 2014 or model_year == 2015:
        nowcast_flag = True
        title = 'Nowcast'
    else:
        nowcast_flag = False
        title = 'Spinup'

    # load model variables
    depth_mod, var_mod, dates_mod = load_model(model_path, sdt, edt,
                                               model_field,
                                               nowcast_flag=nowcast_flag)

    # plot obs and model
    data_m = data_obs[data_obs['Month'] == month]
    for dep_obs, var_obs, lon, lat, day in zip(data_m['Depth'],
                                               data_m[field],
                                               data_m['Longitude'],
                                               data_m['Latitude'],
                                               data_m['Day']):
        # model grid points
        [j, i] = tidetools.find_closest_model_point(lon, lat, X, Y, bathy)
        # model time index
        t_ind = []
        for count, date in enumerate(dates_mod):
            if date.month == month:
                if date.day == day:
                    t_ind = count
        var_plot = var_mod[t_ind, :, j, i]
        var_plot = np.ma.masked_values(var_plot, 0)

        ax.plot(var_obs, dep_obs, '-*r', label='obs', alpha=0.5)
        if j:
            try:
                ax.plot(var_plot, depth_mod, '-ob', label='model', alpha=0.5)
            except ValueError:
                print ('No model data for {}/{}'.format(day, month))
        # plot location on map
        axm.plot(lon, lat, '*r')

    # Set plot axis and labels
    ax.set_ylim([zmax, zmin])
    ax.set_xlim([vmin, vmax])
    ax.set_title(title)
    ax.set_ylabel('Depth [m]')
    ax.set_xlabel(field)

    # plot mode coastline
    viz_tools.plot_coastline(axm, f, coords='map')
    axm.set_ylim([ymin, ymax])
    axm.set_xlim([xmin, xmax])
    axm.set_title('Month {}'.format(month))

    # fake the legend
    simObs, = ax.plot(-1, 0, 'r*')
    simMod, = ax.plot(-1, 0, 'bo')
    ax.legend([simObs, simMod], ['obs', 'model'], loc=0)

    return fig


def compare_cast_model(month, model_year, field, data_obs, model_path,
                       xmin=-124, xmax=-122, ymin=48, ymax=50, zmin=0,
                       zmax=300, vmin=10, vmax=32, x=7):
    """Comparison between model and observations at every cast in a given month
    Model is compared x days before and after cast date
    """
    # Load model grid
    grid = '/data/nsoontie/MEOPAR/NEMO-forcing/grid/bathy_meter_SalishSea2.nc'
    f = nc.Dataset(grid)
    bathy = f.variables['Bathymetry'][:]
    X = f.variables['nav_lon'][:]
    Y = f.variables['nav_lat'][:]

    # date ranges based on month and model_year
    date = datetime.datetime(model_year, month, 1)
    sdt = date - datetime.timedelta(days=31)
    edt = date + datetime.timedelta(days=60)

    # Model variables and nowcast/spinup?
    if field == 'Salinity':
        model_field = 'vosaline'
    elif field == 'Temperatute':
        model_field = 'votemper'
    # Is this a nowcast?
    if model_year == 2014 or model_year == 2015:
        nowcast_flag = True
    else:
        nowcast_flag = False

    # load model variables
    depth_mod, var_mod, dates_mod = load_model(model_path, sdt, edt,
                                               model_field,
                                               nowcast_flag=nowcast_flag)
    # plot obs and model
    data_m = data_obs[data_obs['Month'] == month]
    num_casts = len(data_m.index)
    fig, axs = plt.subplots(num_casts, 2, figsize=(10, 3.5*num_casts))
    cast = 0
    for dep_obs, var_obs, lon, lat, day, year in zip(data_m['Depth'],
                                                     data_m[field],
                                                     data_m['Longitude'],
                                                     data_m['Latitude'],
                                                     data_m['Day'],
                                                     data_m['Year']):
        # model grid points
        try:
            ax = axs[cast, 0]
            axm = axs[cast, 1]
        except IndexError:
            ax = axs[0]
            axm = axs[1]
        [j, i] = tidetools.find_closest_model_point(lon, lat, X, Y, bathy)
        # model time index
        t_ind = []
        for count, date in enumerate(dates_mod):
            if date.day == day:
                if date.month == month:
                    t_ind.append(count)
                    t_ind.append(count - x)  # x days earlier
                    t_ind.append(count + x)  # x days later
        labels = ['same day', '{} days earlier'.format(x),
                  '{} days later'.format(x)]
        colors = ['b', 'g', 'k']
        for ii, t in enumerate(t_ind):
            try:
                var_plot = var_mod[t, :, j, i]
                var_plot = np.ma.masked_values(var_plot, 0)
                if j:
                    ax.plot(var_plot, depth_mod, '-b',
                            color=colors[ii], label=labels[ii],
                            alpha=0.5)
            except IndexError:
                    print ('No model data for {}/{}, '
                           '{}'.format(day, month, labels[ii])
                           )
        # plot observations and location on map
        ax.plot(var_obs, dep_obs, '-*r', label='obs')
        axm.plot(lon, lat, '*r')
        # Set plot axis and labels
        ax.set_ylim([zmax, zmin])
        ax.set_xlim([vmin, vmax])
        ax.set_ylabel('Depth [m]')
        ax.set_xlabel(field)

        # plot mode coastline
        viz_tools.plot_coastline(axm, f, coords='map')
        axm.set_ylim([ymin, ymax])
        axm.set_xlim([xmin, xmax])
        axm.set_title('{}-{}-{}'.format(year, month, day))

        # legend
        ax.legend(loc=0)
        cast = cast+1

    return fig


def compare_cast_hourly(month, model_year, field, data_obs, model_path,
                        xmin=-124, xmax=-122, ymin=48, ymax=50, zmin=0,
                        zmax=300, vmin=10, vmax=32):
    """Comparison between model and observations at every cast in a given month
    Model daily average is compared witth houlry std errors
    """
    # Load model grid
    grid = '/data/nsoontie/MEOPAR/NEMO-forcing/grid/bathy_meter_SalishSea2.nc'
    f = nc.Dataset(grid)
    bathy = f.variables['Bathymetry'][:]
    X = f.variables['nav_lon'][:]
    Y = f.variables['nav_lat'][:]

    # date ranges based on month and model_year
    date = datetime.datetime(model_year, month, 1)
    sdt = date - datetime.timedelta(days=31)
    edt = date + datetime.timedelta(days=60)

    # Model variables and nowcast/spinup?
    if field == 'Salinity':
        model_field = 'vosaline'
    elif field == 'Temperatute':
        model_field = 'votemper'
    # Is this a nowcast?
    nowcast_flag = True

    # load model variables
    depth_mod, var_mod, dates_mod = load_model(model_path, sdt, edt,
                                               model_field,
                                               nowcast_flag=nowcast_flag)
    # plot obs and model
    data_m = data_obs[data_obs['Month'] == month]
    num_casts = len(data_m.index)
    fig, axs = plt.subplots(num_casts, 2, figsize=(10, 3.5*num_casts))
    cast = 0
    for dep_obs, var_obs, lon, lat, day, year in zip(data_m['Depth'],
                                                     data_m[field],
                                                     data_m['Longitude'],
                                                     data_m['Latitude'],
                                                     data_m['Day'],
                                                     data_m['Year']):
        # model grid points
        try:
            ax = axs[cast, 0]
            axm = axs[cast, 1]
        except IndexError:
            ax = axs[0]
            axm = axs[1]
        [j, i] = tidetools.find_closest_model_point(lon, lat, X, Y, bathy)
        # model time index
        t_ind = []
        for count, date in enumerate(dates_mod):
            if date.day == day:
                if date.month == month:
                    t_ind = count
                    date = datetime.datetime(model_year, date.month, date.day)
                    hourly_grid = get_hourly_grid(date, model_path)
                    var_plot = var_mod[t_ind, :, j, i]
                    var_plot = np.ma.masked_values(var_plot, 0)
                    max_h, min_h = calculate_hourly_ext(model_field,
                                                        hourly_grid, j, i)
                    if j:
                        try:
                            ax.plot(var_plot, depth_mod, '-b',
                                    label='daily mean', alpha=0.5)
                            ax.plot(max_h, depth_mod, 'k--', label='daily max')
                            ax.plot(min_h, depth_mod, 'k:', label='daily min')
                        except ValueError:
                            print ('No model data for'
                                   ' {}/{}'.format(day, month))
        # plot observations and location on map
        ax.plot(var_obs, dep_obs, '-*r', label='obs')
        axm.plot(lon, lat, '*r')
        # Set plot axis and labels
        ax.set_ylim([zmax, zmin])
        ax.set_xlim([vmin, vmax])
        ax.set_ylabel('Depth [m]')
        ax.set_xlabel(field)

        # plot mode coastline
        viz_tools.plot_coastline(axm, f, coords='map')
        axm.set_ylim([ymin, ymax])
        axm.set_xlim([xmin, xmax])
        axm.set_title('{}-{}-{}'.format(year, month, day))

        # legend
        ax.legend(loc=0)
        cast = cast+1

    return fig


def get_hourly_grid(date, model_path):
    results_dir = os.path.join(model_path, date.strftime('%d%b%y').lower())
    grid_T = results_dataset('1h', 'grid_T', results_dir)
    return grid_T


def results_dataset(period, grid, results_dir):
    """Return the results dataset for period (e.g. 1h or 1d)
    and grid (e.g. grid_T, grid_U) from results_dir.
    """
    filename_pattern = 'SalishSea_{period}_*_{grid}.nc'
    filepaths = glob.glob(
        os.path.join(
            results_dir, filename_pattern.format(period=period, grid=grid)))
    return nc.Dataset(filepaths[0])


def calculate_hourly_ext(varname, grid_T, j, i):
    var = grid_T.variables[varname][:, :, j, i]
    var = np.ma.masked_values(var, 0)
    min_h = np.min(var, axis=0)
    max_h = np.max(var, axis=0)
    return max_h, min_h
