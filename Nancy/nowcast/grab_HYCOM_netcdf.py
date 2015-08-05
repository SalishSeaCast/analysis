# Script to grab data from HYCOM model and save it.

from __future__ import division
import netCDF4 as nc
import datetime
import os
import numpy as np

SAVE_DIR = '/ocean/nsoontie/MEOPAR/HYCOM/'
HYCOM_URL = 'http://nomads.ncep.noaa.gov:9090/dods/rtofs/'
FILENAMES = ['rtofs_glo_2ds_{}_3hrly_diag',  # ssh files
             'rtofs_glo_3dz_{}_6hrly_reg2',   # temp/salinity
             ]
# sub domain
LON_MIN = -126
LON_MAX = -124
LAT_MIN = 48
LAT_MAX = 49


def main():
    """save yesterday's data from hycom"""
    date = datetime.date.today() - datetime.timedelta(days=1)
    modes = ['forecast', 'nowcast']
    for name in FILENAMES:
        for mode in modes:
            save_netcdf_file(date, mode, name)


def save_netcdf_file(date, mode, name):
    """Saves hycom netcdf file in a subdomain

    :arg date: the hycom simulation date
    :type date: datetime object

    :arg mode: forecast or nowcast
    :type mode: string, either 'forecast' or 'nowcast'

    :arg name: basename of the HYCOM model. Determines which variables
    are downloaded.
    :type name: string
    """
    # setting up to read file
    datestr = 'rtofs_global{}'.format(date.strftime('%Y%m%d'))
    filename = name.format(mode)
    url = os.path.join(HYCOM_URL, datestr, filename)

    # look up subdomain indices
    iss, jss = determine_subdomain(url, LON_MIN, LON_MAX, LAT_MIN, LAT_MAX)

    # setting up to save file
    directory = os.path.join(SAVE_DIR, mode, date.strftime('%Y-%m-%d'))
    if not os.path.exists(directory):
        os.makedirs(directory)
    save_path = os.path.join(directory, filename+'.nc')

    # copy netcdf to save file
    cmd = 'ncks -d lat,{j1},{j2} -d lon,{i1},{i2} {hycom} {newfile}'.format(
          j1=jss[0][0], j2=jss[0][-1], i1=iss[0][0], i2=iss[0][-1],
          hycom=url, newfile=save_path)
    os.system(cmd)


def determine_subdomain(url, lon_min, lon_max, lat_min, lat_max):
    """Return indices for latitude and longitude in a subdomain.
       The subdomain is defined by lon_min, lon_max, lat_min, lat_max.

    :arg url: opendap URL
    :type url: string

    :arg lon_min: minimum longitude of subdomain
    :type lon_min: float

    :arg lon_max: maxmium longitude of subdomain
    :type lon_max: float

    :arg lat_min: minimum latitude of subdomain
    :type lat_min: float

    :arg lat_max: maximum latitude of subdomain
    :type lat_max: float

    :returns: iss, jss - numpy arrays with the indices corresponding to
    subdomina. iss for longitude, jss for latitude.  """

    f = nc.Dataset(url)
    lons = f.variables['lon'][:]
    lats = f.variables['lat'][:]
    if lons.max() > 180:
        lons = lons - 360
    iss = np.where(np.logical_and(lons <= lon_max, lons >= lon_min))
    jss = np.where(np.logical_and(lats <= lat_max, lats >= lat_min))

    return iss, jss


if __name__ == '__main__':
    main()
