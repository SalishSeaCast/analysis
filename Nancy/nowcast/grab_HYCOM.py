# Script to grab data from HYCOM model and save it.

from __future__ import division

import numpy as np
import pandas as pd
import netCDF4 as nc
import datetime
import os
import urllib

SAVE_PATH = '/ocean/nsoontie/MEOPAR/HYCOM/text/'


def main():
    """save yesterday's data from hycom"""
    date = datetime.date.today() - datetime.timedelta(days=1)
    iss = np.arange(1934, 1920, -1)
    jss = np.arange(1661, 1665)
    for i, j in zip(iss, jss):
        read_url(date, i, j)


def read_url(date, i, j):
    """Reads text from a url and save the output to a file
    Returns the filename of the output file

    :arg date: the data of the download
    :type date: datetime object

    :arg i: the i index of the hycom grid
    :type i: integer

    :arg j: the j index of the hycom grid
    :type j: integer

    :returns: filename, the name of the file where the data was saved"""

    url = ('http://nomads.ncep.noaa.gov:9090/dods/rtofs/rtofs_global{}/'
           'rtofs_glo_2ds_forecast_3hrly_diag.ascii'
           '?ssh[0:64][0][{}][{}]'.format(date.strftime('%Y%m%d'), j, i)
           )

    response = urllib.urlopen(url)
    html = response.read()

    # We might want to save output like we do for neah bay
    directory = os.path.join(SAVE_PATH, date.strftime('%Y-%m-%d'))
    if not os.path.exists(directory):
        os.makedirs(directory)
    f = 'hycom_{}_{}.txt'.format(i, j)
    filename = os.path.join(directory, f)
    text_file = open(filename, "w")
    text_file.write(html)
    text_file.close()

    return filename


def parse_hycom_text(filename):
    """Parses the text in a output file from the hycom model.

    :arg filename: file where the hycom model data is stored
    :type filename: string

    :returns: data, lon, lat
    data is a data frame with ssh and time columns
    lon is the longitude of the hycom model point
    lat is the latitude of the hycom grid point
    """
    ssh_read = False
    time_read = False
    lat_read = False
    lon_read = False
    # initialize variables
    sshs = []
    times = []
    lat = 0
    lon = 0

    # variable to define number of lines to skip
    skip_lines = 0
    with open(filename) as f:
        # loop through each line
        for line in f:
            # check if we should skip a line
            if skip_lines > 0:
                skip_lines = skip_lines - 1
                continue

            # read the line
            words = line.split()
            if words:  # there is data in the line, do stuff with it
                # if we should read a variable, read it
                # read ssh
                if ssh_read:
                    if words[0] == 'time,':  # check we are in the ssh part
                        time_read = True
                        ssh_read = False
                    else:
                        sshs.append(float(words[1]))  # append the ssh to list
                        skip_lines = 2
                # read time
                elif time_read:
                    if words[0] == 'lev,':  # check we are still in time part
                        time_read = False
                    else:
                        times = words
                # read lat
                elif lat_read:
                    lat = float(words[0])
                    lat_read = False
                # read lon
                elif lon_read:
                    lon = float(words[0]) - 360
                    # subtract 360 for conversion to model coordinates

                # if we aren't reading a variable, check that we can
                # determine which variable should be read next
                if words[0] == 'ssh,':
                    ssh_read = True
                elif words[0] == 'time,':
                    time_read = True
                    ssh_read = False
                elif words[0] == 'lat,':
                    lat_read = True
                    time_read = False
                elif words[0] == 'lon,':
                    lon_read = True
                    lat_read = False
    # finished reading the file

    # convert times to datetimes
    time_units = 'days since 1-1-1 00:00:0.0'
    for i, t in enumerate(times):
        t = float(t[:-1])
        times[i] = nc.num2date(t, time_units)
    # remove first ssh/times element because it is not real data
    sshs = sshs[1:]
    times = times[1:]

    # add the data to a data frame
    data = pd.DataFrame({'ssh': sshs, 'time': times})

    return data, lon, lat


if __name__ == '__main__':
    main()
