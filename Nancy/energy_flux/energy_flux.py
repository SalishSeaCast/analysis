# functions used to calculate energy fluxes

# NKS 2015

import numpy as np
import scipy.io as sio
import netCDF4 as nc

import os

g = 9.81  # acceleration due to gravity m/s^2
rho0 = 1035  # reference density (kg/m^3)


def barotropic_pressure(pstruc, const):
    """Calculates the amplitude and phase of the barotropic
     pressure signal for a constituent"""

    var = pstruc[const]

    amp = var[0, 0]['ampl'][0, 0][:]
    amp = np.ma.masked_invalid(amp)

    phase = var[0, 0]['phas'][0, 0][:]
    phase = np.ma.masked_invalid(phase)

    amp = amp * g * rho0

    return amp, phase


def ellipse_constituent(cstruc, const):
    var = cstruc[const]

    major = var[0, 0]['major'][0, 0][:]
    major = np.ma.masked_invalid(major)

    phase = var[0, 0]['phase'][0, 0][:]
    phase = np.ma.masked_invalid(phase)

    minor = var[0, 0]['minor'][0, 0][:]
    minor = np.ma.masked_invalid(minor)

    incli = var[0, 0]['incli'][0, 0][:]
    incli = np.ma.masked_invalid(incli)

    return major, minor, phase, incli


def cph2rps(freq):
    """Convert frequency in cycles per hours to radians per second"""
    return freq*2*np.pi/3600


def baroclinic_pressure(pstruc, const):

    var = pstruc[const]
    # t_tide records frequency in cylces/hour
    # convert to
    freq = cph2rps(var[0, 0]['freq'][0, 0])

    amp = var[0, 0]['ampl'][0, 0][:]
    amp = np.ma.masked_invalid(amp)

    phase = var[0, 0]['phas'][0, 0][:]
    phase = np.ma.masked_invalid(phase)

    p_amp = amp/freq
    p_phase = phase+90

    return p_amp, p_phase


def flux_vectors(major, minor, phase, incl, p_amp, p_phase):
    """ Calculate flux vectors in north-south coordinates"""
    Fmaj = 0.5*major*p_amp*np.cos(np.deg2rad(phase) - np.deg2rad(p_phase))
    Fmin = 0.5*minor*p_amp*np.sin(np.deg2rad(phase) - np.deg2rad(p_phase))
    # Rotate to north/south
    Fx = Fmaj*np.cos(np.deg2rad(incl)) - Fmin*np.sin(np.deg2rad(incl))
    Fy = Fmaj*np.sin(np.deg2rad(incl)) + Fmin*np.cos(np.deg2rad(incl))

    return Fx, Fy


def barotropic_flux(pstruc, cstruc, const):
    major, minor, phase, incl = ellipse_constituent(cstruc, const)
    p_amp, p_phase = barotropic_pressure(pstruc, const)

    Fx, Fy  = flux_vectors(major, minor, phase, incl, p_amp, p_phase)

    return Fx, Fy


def baroclinic_flux(pstruc, cstruc, const):
    major, minor, phase, incl = ellipse_constituent(cstruc, const)
    p_amp, p_phase = baroclinic_pressure(pstruc, const)

    Fx, Fy = flux_vectors(major, minor, phase, incl, p_amp, p_phase)

    return Fx, Fy


def find_starting_index(NEMO_lons, NEMO_lats, lon, lat):
    """Find grid index of lon, lat"""
    j,i = np.where(np.logical_and(NEMO_lons==lon, NEMO_lats==lat))

    return j,i


def water_depth(tmask,e3t):
    """Cacluate the total water depth"""
    water_depth = np.sum(e3t*tmask, axis=0)
    water_depth = np.ma.masked_values(water_depth, 0)
    return water_depth


def depth_integrate(var, tmask, e3t):
    """Integrate over depth"""
    var_int = np.sum(var*tmask*e3t, axis=2)
    return var_int
