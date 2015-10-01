import datetime
import numpy as np
import netCDF4 as nc

from salishsea_tools import (tidetools, nc_tools, ellipse)
from salishsea_tools.nowcast import (analyze)


# Functions
def nodal_corrections(tide, tidecorr):
    """apply nodal corrections to tidal constituent amplude and phase

    tide is a nested dictionary with phase and ampliude for each constituent
    tidecorr is also a nested dictionary with nodal factors and phase shift
    for each constituent"""
    for const in tide:
        tide[const]['phase'] = (tide[const]['phase'] + tidecorr[const]['uvt'])
        tide[const]['amp'] = tide[const]['amp'] / tidecorr[const]['ft']

        shape = tide[const]['phase'].shape
        corr_amp = tide[const]['amp'].flatten()
        corr_phase = tide[const]['phase'].flatten()
        ind = 0
        for amp, phase in zip(corr_amp, corr_phase):
            corr_amp[ind], corr_phase[ind] = tidetools.convention_pha_amp(amp, phase)
            ind = ind + 1
        tide[const]['phase'] = np.reshape(corr_phase, shape)
        tide[const]['amp'] = np.reshape(corr_amp, shape)
    return tide


def baroclinic_tide(u, time, depth, nconst):
    """Perform a harmonic analysis on the baroclinic tide

    u is the full depth profile of a current
    If u is from NEMO output, it should be unstaggered before this funcion
    is applied.
    u should have at least a time and depth dimension but could also have
    y, x shape
    the depth dimensions must be in axis 1.
    time is the times associated with the current.
    depth is an array of depths associated with u
    nconsts is the number of constituents to analyze
    returns tide_bc - a nested dictionary with amp and phase for each
    constituent eg. tide_bc['M2']['phase']
    also returns the baroclinic currnt, u_bc"""

    # Calculate depth-averaged current
    u_depav = analyze.depth_average(u, depth, depth_axis=1)
    u_depav = np.expand_dims(u_depav, axis=1)
    # Calculate baroclinic current by removing depth averaged bit
    u_bc = u - u_depav

    # tidal analysis of baroclinic current
    tide_bc = tidetools.fittit(u_bc, time, nconst)

    return tide_bc, u_bc


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
nconst = 8

u_rot, v_rot = ellipse.prepare_vel(us, vs)
u_tide_bc, u_bc = baroclinic_tide(u_rot, times, depths, nconst)
v_tide_bc, v_bc = baroclinic_tide(v_rot, times, depths, nconst)
# nodal corrections
u_tide_bc = nodal_corrections(u_tide_bc, NodalCorr)
v_tide_bc = nodal_corrections(v_tide_bc, NodalCorr)
baroclinic_ellipse = ellipse.get_params(u_bc, v_bc, times, nconst,
                                        tidecorr=NodalCorr)

# Save things
for const in baroclinic_ellipse:
    save_netcdf(baroclinic_ellipse[const], depths, const, lons, lats, to, tf)
    print 'Saved {}'.format(const)
