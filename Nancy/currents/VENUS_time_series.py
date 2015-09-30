# Script to generate a netcdf file with the hourly time series of the currents
# at the three VENUS nodes - central, east, ddl

import datetime
import netCDF4 as nc

from salishsea_tools import (tidetools, nc_tools, ellipse)
from salishsea_tools.nowcast import (research_VENUS)

NodalCorr = tidetools.CorrTides


def save_netcdf(times, us, vs, depths, station, lons, lats, to, tf):
    fname = '{}_currents_{}_{}.nc'.format(station, to.strftime('%Y%m%d'),
                                       tf.strftime('%Y%m%d'))
    nc_file = nc.Dataset(fname, 'w', zlib=True)
    # dataset attributes
    nc_tools.init_dataset_attrs(
        nc_file,
        title='{} currents'.format(station),
        notebook_name='N/A',
        nc_filepath='/data/nsoontie/MEOPAR/analysis/Nancy/tides/' + fname,
        comment='Generated for tidal analysis')
    # dimensions
    nc_file.createDimension('time_counter', None)
    nc_file.createDimension('deptht', depths.shape[0])
    nc_file.createDimension('y', us.shape[2])
    nc_file.createDimension('x', us.shape[3])
    # variables
    # time_counter
    time_counter = nc_file.createVariable(
        'time_counter', 'float32', ('time_counter'))
    time_counter.long_name = 'Time axis'
    time_counter.axis = 'T'
    time_counter.units = 'hour since 00:00:00 on {}'.format(NodalCorr['reftime'])
    # lat, lon
    lon = nc_file.createVariable('nav_lon', float, ('y', 'x'), zlib=True)
    lon[:] = lons[:]
    lat = nc_file.createVariable('nav_lat', float, ('y', 'x'), zlib=True)
    lat[:] = lats[:]
    # u, v
    u = nc_file.createVariable('vozocrtx', 'float32',
                               ('time_counter', 'deptht', 'y', 'x'), zlib=True)
    u.units = 'm/s'
    u.long_name = 'Zonal Velocity'
    u.coordinates = 'time_counter, depth'

    v = nc_file.createVariable('vomecrty', 'float32',
                               ('time_counter', 'deptht', 'y', 'x'), zlib=True)
    v.units = 'm/s'
    v.long_name = 'Meridional Velocity'
    v.coordinates = 'time_counter, deptht'
    # depth
    depth = nc_file.createVariable('deptht', 'float32', ('deptht'), zlib=True)
    depth.units = 'm'
    depth.long_name = 'Depth'
    depth.coordinates = 'deptht'

    u[:] = us[:]
    v[:] = vs[:]
    depth[:] = depths[:]
    time_counter[:] = times[:]

    nc_file.close()


to = datetime.datetime(2014, 11, 26)
tf = datetime.datetime(2015, 4, 26)
path = '/data/dlatorne/MEOPAR/SalishSea/nowcast/'
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

    save_netcdf(times, us, vs, depths, site, lons, lats, to, tf)
    print 'Saved {}'.format(site)
