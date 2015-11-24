# Script to generate a netcdf file with the hourly time series of the TS, w,
# ssh in the CODAR region

import datetime
import netCDF4 as nc
import numpy as np

from salishsea_tools import (tidetools)
from salishsea_tools.nowcast import analyze

import baroclinic

NodalCorr = tidetools.CorrTides

to = datetime.datetime(2014, 11, 26)
tf = datetime.datetime(2015, 4, 26)
nowcast_path = '/data/dlatorne/MEOPAR/SalishSea/nowcast/'
grid = nc.Dataset('/data/nsoontie/MEOPAR/NEMO-forcing/grid/bathy_meter_SalishSea2.nc')
lon_grid = grid.variables['nav_lon']
lat_grid = grid.variables['nav_lat']
jmin = 379
jmax = 461
imin = 236
imax = 321
jss = np.arange(jmin, jmax)
iss = np.arange(imin, imax)
ks = np.arange(0, 40)

filest = analyze.get_filenames(to, tf, '1h', 'grid_T', nowcast_path)
filesw = analyze.get_filenames(to, tf, '1h', 'grid_W', nowcast_path)
Ts, times = analyze.combine_files(filest, 'votemper', ks, jss, iss)
Ss, times = analyze.combine_files(filest, 'vosaline', ks, jss, iss)
sshs, times = analyze.combine_files(filest, 'sossheig', 'None', jss, iss)
Ws, times = analyze.combine_files(filesw, 'vovecrtz', ks, jss, iss)
Ws = Ws.data

tmp = nc.Dataset(filest[0])
depthst = tmp.variables['deptht'][:]
tmp = nc.Dataset(filesw[0])
depthsw = tmp.variables['depthw'][:]

lons = lon_grid[jss, iss]
lats = lat_grid[jss, iss]

reftime = NodalCorr['reftime']
time = tidetools.convert_to_hours(times, reftime=reftime)

baroclinic.save_netcdf_TS(time, Ts, Ss, Ws, sshs, depthst, depthsw,
                          'CODAR', lons, lats, to, tf)
print('Finished')
