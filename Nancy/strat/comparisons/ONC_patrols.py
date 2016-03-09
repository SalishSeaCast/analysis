# Module to load ONC CTD casts from patrols.
# Inlcudes functions to compare with model results

#NKS March 2016

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import netCDF4 as nc
from scipy import interpolate as interp


from salishsea_tools import tidetools, viz_tools
from nowcast import analyze

