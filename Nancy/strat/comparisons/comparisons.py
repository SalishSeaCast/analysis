# Functions used to compare model and observation profiles

import netCDF4 as nc
from salishsea_tools import tidetools, viz_tools
import numpy as np
import matplotlib.pyplot as plt
import datetime
from salishsea_tools.nowcast import analyze


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
        for count, date in enumerate(dates_mod):
            if date.day == day:
                t_ind = count
        var_plot = var_mod[t_ind, :, j, i]
        var_plot = np.ma.masked_values(var_plot, 0)

        ax.plot(var_obs, dep_obs, '-*r', label='obs', alpha=0.5)
        if j:
            ax.plot(var_plot, depth_mod, '-ob', label='model', alpha=0.5)
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
