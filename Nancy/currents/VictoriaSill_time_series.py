# Script to generate a netcdf file with the hourly time series of the currents
# at the three VENUS nodes - central, east, ddl

import datetime
import netCDF4 as nc
import numpy as np

from salishsea_tools import (tidetools, ellipse)

import baroclinic

NodalCorr = tidetools.CorrTides

to = datetime.datetime(2014, 11, 26)
tf = datetime.datetime(2015, 4, 26)
path = '/data/dlatorne/MEOPAR/SalishSea/nowcast/'
grid = nc.Dataset('/data/nsoontie/MEOPAR/NEMO-forcing/grid/bathy_meter_SalishSea2.nc')
lon_grid = grid.variables['nav_lon']
lat_grid = grid.variables['nav_lat']
jmin = 200
jmax = 380
imin = 171
imax = 251
jss = np.arange(jmin, jmax)
iss = np.arange(imin, imax)

us, vs, times, depths = ellipse.ellipse_files_nowcast(to, tf, iss, jss, path)
jss = np.append(jss[0]-1, jss)
iss = np.append(iss[0]-1, iss)
lons = lon_grid[jss, iss]
lats = lat_grid[jss, iss]

baroclinic.save_netcdf(times, us, vs, depths,'VictoriaSill', lons, lats, to, tf)
print('Finished')
