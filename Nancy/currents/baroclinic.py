# Module for doing baroclinic tidal calcuations

import netCDF4 as nc
import numpy as np

from salishsea_tools import (tidetools, nc_tools)
from salishsea_tools.nowcast import (analyze)

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
    nc_file.createDimension('deptht', us.shape[1])
    nc_file.createDimension('y', us.shape[2])
    nc_file.createDimension('x', us.shape[3])
    # variables
    # time_counter
    time_counter = nc_file.createVariable(
        'time_counter', 'float64', ('time_counter'))
    time_counter.long_name = 'Time axis'
    time_counter.axis = 'T'
    time_counter.units = 'hour since {}'.format(NodalCorr['reftime'])
    # lat, lon
    lon = nc_file.createVariable('nav_lon', 'float32', ('y', 'x'), zlib=True)
    lon[:] = lons[:]
    lat = nc_file.createVariable('nav_lat', 'float32', ('y', 'x'), zlib=True)
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

    u[:] = us
    v[:] = vs
    depth[:] = depths
    time_counter[:] = times

    nc_file.close()


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