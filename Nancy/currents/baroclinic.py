# Module for doing baroclinic tidal calcuations

import netCDF4 as nc
import numpy as np
import os
import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse

from salishsea_tools import (tidetools, nc_tools, viz_tools)
from salishsea_tools.nowcast import (analyze)

NodalCorr = tidetools.CorrTides


def save_netcdf(times, us, vs, depths, station, lons, lats, to, tf):
    """Saves the u/v time series over volume into a netcdf file"""
    path = '/ocean/nsoontie/MEOPAR/TidalEllipseData/ModelTimeSeries/'
    fname = '{}_currents_{}_{}.nc'.format(station, to.strftime('%Y%m%d'),
                                          tf.strftime('%Y%m%d'))
    nc_file = nc.Dataset(os.path.join(path, fname), 'w', zlib=True)
    # dataset attributes
    nc_tools.init_dataset_attrs(
        nc_file,
        title='{} currents'.format(station),
        notebook_name='N/A',
        nc_filepath=os.path.join(path, fname),
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


def save_netcdf_TS(times, Ts, Ss, Ws, sshs, depthst, depthsw,
                   name, lons, lats, to, tf):
    """Saves the u/v time series over volume into a netcdf file"""
    path = '/ocean/nsoontie/MEOPAR/TidalEllipseData/ModelTimeSeries/'
    fname = '{}_TS_{}_{}.nc'.format(name, to.strftime('%Y%m%d'),
                                    tf.strftime('%Y%m%d'))
    nc_file = nc.Dataset(os.path.join(path, fname), 'w', zlib=True)
    # dataset attributes
    nc_tools.init_dataset_attrs(
        nc_file,
        title='{} TS, w, ssh'.format(name),
        notebook_name='N/A',
        nc_filepath=os.path.join(path, fname),
        comment='Generated for tidal and energy analysis')
    # dimensions
    nc_file.createDimension('time_counter', None)
    nc_file.createDimension('deptht', Ts.shape[1])
    nc_file.createDimension('y', Ts.shape[2])
    nc_file.createDimension('x', Ts.shape[3])
    nc_file.createDimension('depthw', Ws.shape[1])
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
    # T
    T = nc_file.createVariable('votemper', 'float32',
                               ('time_counter', 'deptht', 'y', 'x'), zlib=True)
    T.units = 'deg C'
    T.long_name = 'Temperature'
    T.coordinates = 'time_counter, deptht'
    # S
    S = nc_file.createVariable('vosaline', 'float32',
                               ('time_counter', 'deptht', 'y', 'x'), zlib=True)
    S.units = '[psu]'
    S.long_name = 'Practical Salinity'
    S.coordinates = 'time_counter, deptht'
    # W
    W = nc_file.createVariable('vovecrtz', 'float32',
                               ('time_counter', 'depthw', 'y', 'x'), zlib=True)
    W.units = 'm/s'
    W.long_name = 'Vertical Velocity'
    W.coordinates = 'time_counter, depthw'
    # SSH
    SSH = nc_file.createVariable('sossheig', 'float32',
                                 ('time_counter', 'y', 'x'), zlib=True)
    SSH.units = 'm'
    SSH.long_name = 'Sea Surface height'
    SSH.coordinates = 'time_counter'
    # deptht
    depth = nc_file.createVariable('deptht', 'float32', ('deptht'), zlib=True)
    depth.units = 'm'
    depth.long_name = 'Depth'
    depth.coordinates = 'deptht'
    # depthw
    depthw = nc_file.createVariable('depthw', 'float32', ('depthw'), zlib=True)
    depthw.units = 'm'
    depthw.long_name = 'Depth'
    depthw.coordinates = 'depthw'

    T[:] = Ts
    S[:] = Ss
    depth[:] = depthst
    depthw[:] = depthsw
    time_counter[:] = times
    SSH[:] = sshs

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


def get_constituent(const, datastruc):
    """returns major axis, minor axis, phase and inlincation for a
    tidal constituent in matlab datastruc
    Example get_constituent('M2', datastruc)"""

    var = datastruc[const]

    major = var[0, 0]['major'][0, 0][:]
    major = np.ma.masked_invalid(major)

    phase = var[0, 0]['phase'][0, 0][:]
    phase = np.ma.masked_invalid(phase)

    minor = var[0, 0]['minor'][0, 0][:]
    minor = np.ma.masked_invalid(minor)

    incli = var[0, 0]['incli'][0, 0][:]
    incli = np.ma.masked_invalid(incli)

    return major, minor, phase, incli


def get_constituent_errors(const, datastruc):
    """returns major axis, minor axis, phase and inclination errors for a
    tidal constituent in a matlab datastruc
    Example get_constituent_errors('M2', datastruc)"""

    var = datastruc[const]

    emajor = var[0, 0]['emajo'][0, 0][:]
    emajor = np.ma.masked_invalid(emajor)

    ephase = var[0, 0]['ephas'][0, 0][:]
    ephase = np.ma.masked_invalid(ephase)

    eminor = var[0, 0]['emino'][0, 0][:]
    eminor = np.ma.masked_invalid(eminor)

    eincli = var[0, 0]['eincl'][0, 0][:]
    eincli = np.ma.masked_invalid(eincli)

    return emajor, eminor, ephase, eincli


def plot_ellipse(lon, lat, inc, major, minor, ax, scale):
    """Plot a tidal ellipse at lon, lat given byt the inclination,
    major and minor axis. The ellipse is plotted in ax with scale"""
    if minor > 0:
        thecolor = 'firebrick'
    else:
        thecolor = 'dodgerblue'
    ellsc = Ellipse(xy=(lon, lat),
                    width=scale * major,
                    height=scale * minor,
                    angle=inc,
                    color=thecolor)
    ax.add_artist(ellsc)


def plot_CODAR_ellipse(ax, lons, lats, const, datastruc, depths, grid, step=3,
                       scale=0.08, baroclinic=False, depth_level=0,
                       barotropic=False, isobaths=[5, 20]):
    """Plot ellipses over the CODAR region"""
    major, minor, pha, inc = get_constituent(const, datastruc)
    if baroclinic:
        major = major[:, :, depth_level]
        minor = minor[:, :, depth_level]
        inc = inc[:, :, depth_level]
        title_str = 'baroclinic {0:.3g} m'.format(depths[depth_level][0])
    elif barotropic:
        title_str = 'barotropic'
    else:
        title_str = 'surface'
    for i in np.arange(0, lons.shape[-1], step):
        for j in np.arange(0, lats.shape[-1], step):
            if major[i, j]:
                plot_ellipse(lons[i, j], lats[i, j], inc[i, j],
                             major[i, j],
                             minor[i, j], ax, scale)

    ax.set_title('{} {} tidal ellipses'.format(const, title_str))

    ax.set_ylabel('Latitude (degrees N)')
    ax.set_xlabel('Longitude (degrees W)')

    viz_tools.plot_land_mask(ax, grid, coords='map')
    for isobath in isobaths:
        viz_tools.plot_coastline(ax, grid, coords='map', isobath=isobath)


def add_scale_ellipse(ax, lon, lat, dx=-.1, dy=.01, scale=0.08):
    """Add scale ellipse"""
    ell = Ellipse(xy=(lon, lat), width = scale*0.5, height = scale*0.5,
                  angle = 45, color='g')
    ax.add_artist(ell)
    ax.text(lon + dx, lat + dy, '0.5 m/s', color='g',
            fontsize=12, fontweight='heavy')


def rotate_ellipse_NS(time_deg, datastruc, const):
    """Rotate ellipse major/minor axis to north/south orientation."""
    # Construct major and minor
    major, minor, pha, inc = get_constituent(const, datastruc)
    # construct current at this time
    try:
        major_current = major*np.cos(np.deg2rad(time_deg - pha))
        minor_current = minor*np.cos(np.deg2rad(time_deg - pha) - np.pi/2)
    except ValueError:
        time_deg = np.expand_dims(time_deg, 2)
        major_current = major*np.cos(np.deg2rad(time_deg - pha))
        minor_current = minor*np.cos(np.deg2rad(time_deg - pha) - np.pi/2)
    # Rotate to u and v
    rotated_current = ((major_current + 1j*minor_current)
                       * np.exp(1j*np.deg2rad(inc)))
    u = np.real(rotated_current)
    v = np.imag(rotated_current)

    return u, v


def plot_ellipse_phase_arrow(ax, lons, lats, const, datastruc, time_deg,
                             step=3, scale=10, baroclinic=False,
                             depth_level=0):
    """Plot phase arrow relative to time_deg"""
    u, v = rotate_ellipse_NS(time_deg, datastruc, const)
    if baroclinic:
        u = u[:, :, depth_level]
        v = v[:, :, depth_level]
    ax.quiver(lons[::step, ::step], lats[::step, ::step],
              u[::step, ::step], v[::step, ::step], scale=scale,
              width=0.008, zorder=10, color='black', pivot='tail',
              headwidth=1, headlength=1)


def ellipse_to_uv(datastruc, const):
    """convert ellipse parameters to u/v amp and phase"""
    major, minor, pha, inc = get_constituent(const, datastruc)
    # positive and negative bits
    thetap = np.deg2rad(inc-pha)
    thetam = np.deg2rad(inc+pha)
    ecc = minor/major
    Wp = (1+ecc)/2.*major
    Wm = (1-ecc)/2.*major

    # complex positive and negative
    wp = Wp*np.exp(1j*thetap)
    wm = Wm*np.exp(1j*thetam)
    # Complex UV
    cU = wp+np.conjugate(wm)
    cV = (wp-np.conjugate(wm))/1j
    # u/v ampl and phase
    uamp = np.abs(cU)
    upha = -np.angle(cU)
    vamp = np.abs(cV)
    vpha = -np.angle(cV)

    return uamp, np.rad2deg(upha), vamp, np.rad2deg(vpha)


def rotate_baroclinc(bc_struc, bt_struc, const):
    """Rotate the baroclinic ellipse onto the barotropic major/minor axis"""

    major_bt, minor_bt, pha_bt, inc_bt = get_constituent(const, bt_struc)
    major_bc, minor_bc, pha_bc, inc_bc = get_constituent(const, bc_struc)

    # rotation angle is the difference between baroclinic and
    # barotropic inclinations
    # construct complex representation of rotated velocities
    inc_diff = np.deg2rad(inc_bc - np.expand_dims(inc_bt, 2))
    pha_bc = np.deg2rad(pha_bc)
    # Complex representation of the rotated major
    rotated_major_complex = (major_bc*np.cos(inc_diff)*np.exp(1j*pha_bc) -
                             (minor_bc*np.sin(inc_diff)
                              * np.exp(1j*(pha_bc+np.pi/2))))
    rotated_major_phase = np.angle(rotated_major_complex)
    rotated_major_amp = np.abs(rotated_major_complex)
    # Complex representation of the rotated minor
    rotated_minor_complex = (major_bc*np.sin(inc_diff)*np.exp(1j*pha_bc) +
                             (minor_bc*np.cos(inc_diff)
                             * np.exp(1j*(pha_bc+np.pi/2))))
    rotated_minor_phase = np.angle(rotated_minor_complex)
    rotated_minor_amp = np.abs(rotated_minor_complex)
    # Conversion to degrees
    rotated_minor_phase = np.rad2deg(rotated_minor_phase)
    rotated_major_phase = np.rad2deg(rotated_major_phase)
    # Force phase between 0 and 360
    rotated_minor_phase = rotated_minor_phase + 360*(rotated_minor_phase < 0)
    rotated_major_phase = rotated_major_phase + 360*(rotated_major_phase < 0)

    return rotated_major_phase, rotated_major_amp, rotated_minor_phase, rotated_minor_amp


