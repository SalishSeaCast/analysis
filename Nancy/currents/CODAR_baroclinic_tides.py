import datetime
import netCDF4 as nc

from salishsea_tools import (tidetools, nc_tools, ellipse)

import baroclinic


def save_netcdf(tide, depths, const, lons, lats, to, tf):
    fname = '{}_CODAR_baroclinic_tides_{}_{}.nc'.format(const,
                                                        to.strftime('%Y%m%d'),
                                                        tf.strftime('%Y%m%d'))
    nc_file = nc.Dataset(fname, 'w', zlib=True)
    # dataset attributes
    nc_tools.init_dataset_attrs(
        nc_file,
        title='{} baroclinic tides'.format(const),
        notebook_name='N/A',
        nc_filepath='/data/nsoontie/MEOPAR/analysis/Nancy/tides/' + fname,
        comment='Baroclinic tidal analysis')
    # dimensions
    temp = tide['Phase']
    nc_file.createDimension('deptht', temp.shape[0])
    nc_file.createDimension('y', temp.shape[1])
    nc_file.createDimension('x', temp.shape[2])
    # variables
    # lat, lon
    lon = nc_file.createVariable('nav_lon', 'float32', ('y', 'x'), zlib=True)
    lon[:] = lons[:]
    lat = nc_file.createVariable('nav_lat', 'float32', ('y', 'x'), zlib=True)
    lat[:] = lats[:]
    # sema
    sema = nc_file.createVariable('Semi-Major', 'float32',
                                  ('deptht', 'y', 'x'), zlib=True)
    sema.units = 'm/s'
    sema.long_name = 'Semi-Major Axis (m/s)'
    # semi
    semi = nc_file.createVariable('Semi-Minor', 'float32',
                                  ('deptht', 'y', 'x'), zlib=True)
    semi.units = 'm/s'
    semi.long_name = 'Semi-Minor Axis (m/s)'
    # phase
    pha = nc_file.createVariable('Phase', 'float32',
                                 ('deptht', 'y', 'x'), zlib=True)
    pha.units = 'deg GMT'
    pha.long_name = 'Phase'
    # inclination
    inc = nc_file.createVariable('Inclination', 'float32',
                                 ('deptht', 'y', 'x'), zlib=True)
    inc.units = 'deg CCW E'
    inc.long_name = 'Inclincation'

    # depth
    depth = nc_file.createVariable('deptht', 'float32', ('deptht'), zlib=True)
    depth.units = 'm'
    depth.long_name = 'Depth'
    depth.coordinates = 'deptht'

    sema[:] = tide['Semi-Major Axis'][:]
    semi[:] = tide['Semi-Minor Axis'][:]
    depth[:] = depths[:]
    pha[:] = tide['Phase'][:]
    inc[:] = tide['Inclination'][:]
    nc_file.close()


# Main part of program
NodalCorr = tidetools.CorrTides

# Load Data
to = datetime.datetime(2014, 11, 26)
tf = datetime.datetime(2015, 4, 26)
fname = '{}_currents_{}_{}.nc'.format('CODAR', to.strftime('%Y%m%d'),
                                      tf.strftime('%Y%m%d'))
f = nc.Dataset(fname)
us = f.variables['vozocrtx'][:]
vs = f.variables['vomecrty'][:]
depths = f.variables['deptht'][:]
times = f.variables['time_counter'][:]
lons = f.variables['nav_lon'][:]
lats = f.variables['nav_lat'][:]
nconst = 2

dep = 0
u_rot, v_rot = ellipse.prepare_vel(us[:, dep, :, :], vs[:, dep, :, :])
#u_tide_bc, u_bc = baroclinic.baroclinic_tide(u_rot, times, depths, nconst)
#v_tide_bc, v_bc = baroclinic.baroclinic_tide(v_rot, times, depths, nconst)
#print 'Finished tide fitting'

# nodal corrections
#u_tide_bc = baroclinic.nodal_corrections(u_tide_bc, NodalCorr)
#v_tide_bc = baroclinic.nodal_corrections(v_tide_bc, NodalCorr)
#print 'Finished nodal corrections'
#baroclinic_ellipse = ellipse.get_params(u_bc, v_bc, times, nconst,
                                        #tidecorr=NodalCorr)
baroclinic_ellipse = ellipse.get_params(u_rot, v_rot, times, nconst,
                                        tidecorr=NodalCorr)
print 'Finished Ellipse calculations. Saving files next'

# Save things
for const in baroclinic_ellipse:
    save_netcdf(baroclinic_ellipse[const], depths, const,
                           lons, lats, to, tf)
    print 'Saved {}'.format(const)
