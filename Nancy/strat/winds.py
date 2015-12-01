# Module to explore wind data both forcing and observations.
# NKS 2015

import datetime
import glob
import os
import netCDF4 as nc
import numpy as np
import pandas as pd
from salishsea_tools import stormtools


def wind_file_names(start, end, path, base):
    """Grab model wind file names in a date range defined by start, end.
    path is directory where model winds are stored
    base is the filename base eg. 'ops'
    """
    files = glob.glob(os.path.join(path, '{}_*.nc'.format(base)))
    files_dates = []
    sstr = start.strftime('{}_y%Ym%md%d.nc'.format(base))
    estr = end.strftime('{}_y%Ym%md%d.nc'.format(base))
    for filename in files:
        if os.path.basename(filename) >= sstr:
            if os.path.basename(filename) <= estr:
                files_dates.append(filename)
    files_dates.sort(key=os.path.basename)
    return files_dates


def compile_operational_model(j, i, files):
    """Combine data from files into a single pandas dataframe."""

    data = []
    for f in files:
        G = nc.Dataset(f)
        tmp = {}
        variables = ['u_wind', 'v_wind', 'atmpres', 'solar', 'qair',
                     'therm_rad', 'precip', 'tair']
        for var in variables:
            tmp[var] = np.squeeze(G.variables[var][0:24, j, i])
        u = tmp['u_wind']
        v = tmp['v_wind']
        speed = np.sqrt(u**2 + v**2)
        d = np.arctan2(v, u)
        d = np.rad2deg(d + (d < 0)*2*np.pi)
        ts = np.squeeze(G.variables['time_counter'])
        torig = datetime.datetime(1970, 1, 1)
        dates = []
        # there is no time_origin attriubte in OP files, so I hard coded this
        for ind in np.arange(24):
            dates.append(torig + datetime.timedelta(seconds=ts[ind]))
        tmp['speed'] = speed
        tmp['direction'] = d
        tmp['time'] = dates
        # add to list
        data.append(pd.DataFrame(tmp))
    # Convert list of data frames to one big dataframe
    df = pd.concat(data)
    return df


