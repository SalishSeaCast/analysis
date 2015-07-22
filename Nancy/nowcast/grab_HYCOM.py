# Script to grab data from HYCOM model and save it.

from __future__ import division

import numpy as np

import datetime
import os
import urllib2

SAVE_PATH = '/data/nsoontie/MEOPAR/analysis/Nancy/nowcast/'


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

    response = urllib2.urlopen(url)
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

if __name__ == '__main__':
    main()
