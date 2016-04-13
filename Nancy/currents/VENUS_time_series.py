# Script to generate a netcdf file with the hourly time series of the currents
# at the three VENUS nodes - central, east, ddl

import datetime
import netCDF4 as nc

from salishsea_tools import (tidetools, ellipse)
from nowcast import (research_VENUS)

import baroclinic

NodalCorr = tidetools.CorrTides


to = datetime.datetime(2015, 10, 1)
tf = datetime.datetime(2016, 3, 30)
path = '/results/SalishSea/nowcast/'
grid = nc.Dataset('/data/nsoontie/MEOPAR/NEMO-forcing/grid/bathy_meter_SalishSea2.nc')
lon_grid = grid.variables['nav_lon']
lat_grid = grid.variables['nav_lat']

SITES = research_VENUS.SITES['VENUS']

for site in SITES:
    i = SITES[site]['i']
    j = SITES[site]['j']
    us, vs, times, depths = ellipse.ellipse_files_nowcast(to, tf, [i], [j],
                                                          path)
    lons = lon_grid[j-1:j+1, i-1:i+1]
    lats = lat_grid[j-1:j+1, i-1:i+1]

    baroclinic.save_netcdf(times, us, vs, depths, site, lons, lats, to, tf)
    print ('Saved {}'.format(site))
