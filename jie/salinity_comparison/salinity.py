## The functions used to compare surface salinity
from __future__ import division, print_function
from salishsea_tools import (nc_tools,viz_tools,stormtools,tidetools)
from salishsea_tools.nowcast import figures
from datetime import datetime, timedelta
from pylab import *
from sklearn import linear_model
from glob import glob
from IPython.core.display import HTML
from salishsea_tools.nowcast import figures
import matplotlib.pyplot as plt
import scipy.io as sio
import netCDF4 as nc
import numpy as np
import math
#import glob
import os
import datetime

title_font = {
    'fontname': 'Bitstream Vera Sans', 'size': '15', 'color': 'black',
    'weight': 'medium'
}
axis_font = {'fontname': 'Bitstream Vera Sans', 'size': '13'}

ferry_stations = {'Tsawwassen': {'lat': 49.0084,'lon': -123.1281},
                  'Duke': {'lat': 49.1632,'lon': -123.8909},
                  'Vancouver': {'lat': 49.2827,'lon': -123.1207}}
paths = {'nowcast': '/data/dlatorne/MEOPAR/SalishSea/nowcast/',
        'longerresult': '/ocean/jieliu/research/meopar/river-treatment/14days_norefraserxml/',
        'widenresult': '/data/jieliu/MEOPAR/river-treatment/24nor_NW/' }

def results_dataset(period, grid, results_dir):
    """Return the results dataset for period (e.g. 1h or 1d)
    and grid (e.g. grid_T, grid_U) from results_dir.
    """
    filename_pattern = 'SalishSea_{period}_*_{grid}.nc'
    filepaths = glob(os.path.join(results_dir, filename_pattern.format(period=period, grid=grid)))
    return  nc.Dataset(filepaths[0])

def date(year, month, day, day_start, day_end, results_home,  period, grid):
    
    day_range = np.arange(day_start, day_end+1)
    day_len = len(day_range)
    files_all = [None] * day_len
    inds = np.arange(day_len)
    
    for i, day in zip(inds, day_range):
        run_date = datetime.datetime(year,month, day)
        #results_home = '/data/jieliu/MEOPAR/river-treatment/24nor_NW/'
        results_dir = os.path.join(results_home, run_date.strftime('%d%b%y').lower())
        filename = 'SalishSea_' + period + '_' + run_date.strftime('%Y%m%d').lower() + \
        '_' + run_date.strftime('%Y%m%d').lower() + '_' + grid + '.nc'
        file_single = os.path.join(results_dir, filename)
        files_all[i] = file_single

    return files_all

def find_dist (q, lon11, lat11, X, Y, bathy, longitude, latitude, saline_nemo_3rd, saline_nemo_4rd):
    k=0
    values =0
    valuess=0
    dist = np.zeros(9)
    weights = np.zeros(9)
    value_3rd=np.zeros(9)
    value_4rd=np.zeros(9)
    regr =linear_model.LinearRegression()
    regr.fit(lon11,lat11);
    regr.coef_

    [x1, j1] = tidetools.find_closest_model_point(lon11[q],regr.predict(lon11[q]),\
                                        X,Y,bathy,lon_tol=0.0052,lat_tol=0.00210,allow_land=False)
    for i in np.arange(x1-1,x1+2):
        for j in np.arange(j1-1,j1+2):
            dist[k]=tidetools.haversine(lon11[q],lat11[q],longitude[i,j],latitude[i,j])
            weights[k]=1.0/dist[k]
            value_3rd[k]=saline_nemo_3rd[i,j]*weights[k]
            value_4rd[k]=saline_nemo_4rd[i,j]*weights[k]
            values=values+value_3rd[k]
            valuess=valuess+value_4rd[k]
            k+=1
            
    return values, valuess, weights

def find_dist_ave (q, lon11, lat11, X, Y, bathy, longitude, latitude, saline_nemo_3rd, saline_nemo_4rd):
    k=0
    values_ave =0
    valuess_ave=0
    dist = np.zeros(9)
    weights = np.zeros(9)
    value_3rd=np.zeros(9)
    value_4rd=np.zeros(9)
    regr =linear_model.LinearRegression()
    regr.fit(lon11,lat11);
    regr.coef_

    [x1, j1] = tidetools.find_closest_model_point(lon11[q],regr.predict(lon11[q]),\
                                        X,Y,bathy,lon_tol=0.0052,lat_tol=0.00210,allow_land=False)
    for i in np.arange(x1-1,x1+2):
        for j in np.arange(j1-1,j1+2):
            dist[k]=tidetools.haversine(lon11[q],lat11[q],longitude[i,j],latitude[i,j])
            weights[k]=1.0/dist[k]
            value_3rd[k]=saline_nemo_3rd[i,j]*weights[k]
            value_4rd[k]=saline_nemo_4rd[i,j]*weights[k]
            values_ave=values_ave+value_3rd[k]
            valuess_ave=valuess_ave+value_4rd[k]
            k+=1
            
    return values_ave, valuess_ave, weights


def get_SS2_bathy_data():
    """Get the original Salish Sea 2 bathymetry and grid data
    e.g. bathy, X, Y = get_SS2_bathy_data()

    .. note::

        This function is deprecated due to hard-coding of
        :file:`/ocean/klesouef/` path.
        Use :py:func:`tidetools.get_bathy_data` instead.

    :returns: bathy, X, Y
    """
    grid = nc.Dataset(
        '/ocean/jieliu/research/meopar/nemo-forcing/grid/bathy_meter_SalishSea2.nc', 'r')
    bathy = grid.variables['Bathymetry'][:, :]
    X = grid.variables['nav_lon'][:, :]
    Y = grid.variables['nav_lat'][:, :]
    return bathy, X, Y

def get_SS5_bathy_data():
    """Get the Salish Sea 5 bathymetry and grid data
    e.g. bathy, X, Y = get_SS5_bathy_data()

    .. note::

        This function is deprecated due to hard-coding of
        :file:`/ocean/klesouef/` path.
        Use :py:func:`tidetools.get_bathy_data` instead.

    :returns: bathy, X, Y
    """
    grid = nc.Dataset(
        '/ocean/jieliu/research/meopar/river-treatment/bathy_meter_SalishSea5.nc', 'r')
    bathy = grid.variables['Bathymetry'][:, :]
    X = grid.variables['nav_lon'][:, :]
    Y = grid.variables['nav_lat'][:, :]
    return bathy, X, Y


def get_SS6_bathy_data():
    """Get the Salish Sea 6 bathymetry and grid data
    e.g. bathy, X, Y = get_SS6_bathy_data()

    .. note::

        This function is deprecated due to hard-coding of
        :file:`/ocean/klesouef/` path.
        Use :py:func:`tidetools.get_bathy_data` instead.

    :returns: bathy, X, Y
    """
    grid = nc.Dataset(
        '/ocean/jieliu/research/meopar/river-treatment/bathy_meter_SalishSea6.nc', 'r')
    bathy = grid.variables['Bathymetry'][:, :]
    X = grid.variables['nav_lon'][:, :]
    Y = grid.variables['nav_lat'][:, :]
    return bathy, X, Y

def salinity_fxn(saline, run_date, results_home):
    """The significance of this function was to return longitude,
       latitude, salinity values for observations, 1.5m of 3rd & 4rd, 
       3m average of 3rd & 4rd model result """

    a=saline['ferryData']
    b=a['data']
    dataa = b[0,0]
    time=dataa['matlabtime'][0,0]
    lonn=dataa['Longitude'][0,0]
    latt=dataa['Latitude'][0,0]
    salinity=dataa['Practical_Salinity'][0,0]
    
    
    a=len(time)
    lon1=np.zeros([a,1])
    lat1=np.zeros([a,1])
    salinity1=np.zeros([a,1])
    for i in np.arange(0,a):
        matlab_datenum = np.float(time[i])
        python_datetime = datetime.datetime.fromordinal(int(matlab_datenum))\
        + timedelta(days=matlab_datenum%1) - timedelta(days = 366)
        
        if((python_datetime.year == run_date.year) & (python_datetime.month == run_date.month)\
           & (python_datetime.day == run_date.day)
           & (python_datetime.hour >= 3))&(python_datetime.hour < 5):
            lon1[i]=lonn[i]
            lat1[i]=latt[i]
            salinity1[i]=salinity[i]
            
    mask=lon1[:,0]!=0
    lon1_2_4=lon1[mask]
    lat1_2_4=lat1[mask]
    salinity1_2_4=salinity1[mask]
    lon11=lon1_2_4[0:-1:20]
    lat11=lat1_2_4[0:-1:20]
    salinity11=salinity1_2_4[0:-1:20]
    if results_home == paths['longerresult']: 
        bathynew, X, Y = get_SS5_bathy_data()
    elif results_home == paths['nowcast']: 
        bathyold, X, Y = get_SS2_bathy_data()
    
    #bathy, X, Y = tidetools.get_SS2_bathy_data()
    
    #aa=date(run_date.year,run_date.month,run_date.day,run_date.day,'1h','grid_T') 
    #sim_date = datetime.datetime(2015,3,19)####need to change for \
    #different daily model results, construct a datetime object
    #run_date = datetime.datetime(2015,3,19)
    
    date_str = run_date.strftime('%d-%b-%Y') ##create a string based on this date
    filepath_name = date(run_date.year,run_date.month, run_date.day,\
    run_date.day,run_date.day, results_home,'1h','grid_T') 
    tracers=nc.Dataset(filepath_name[0])
    #j=int(aa[0][65:67])
    #jj=int(aa[0][67:69])
    latitude=tracers.variables['nav_lat'][:] 
    longitude=tracers.variables['nav_lon'][:] 
    saline_nemo = tracers.variables['vosaline']
    saline_nemo_3rd = saline_nemo[3,1, 0:898, 0:398] 
    saline_nemo_4rd = saline_nemo[4,1, 0:898, 0:398]
    saline_nemo_ave3rd = np.mean(saline_nemo[3, 0:3, 0:898, 0:398], axis = 0)
    saline_nemo_ave4rd = np.mean(saline_nemo[4, 0:3, 0:898, 0:398], axis = 0)
    
    matrix=np.zeros([36,9])
    matrix_ave=np.zeros([36,9])
    values=np.zeros([36,1])
    valuess=np.zeros([36,1])
    values_ave=np.zeros([36,1])
    valuess_ave=np.zeros([36,1])
    value_mean_3rd_hour=np.zeros([36,1])
    value_mean_ave3rd=np.zeros([36,1])
    value_mean_ave4rd=np.zeros([36,1]) 
    value_mean_4rd_hour=np.zeros([36,1])
    for q in np.arange(0,36):
        if results_home == paths['longerresult']:
            values[q], valuess[q], matrix[q,:]=find_dist(q, lon11, lat11, X, Y,\
                                     bathynew, longitude, latitude, saline_nemo_3rd, saline_nemo_4rd)
            value_mean_3rd_hour[q]=values[q]/sum(matrix[q])
            value_mean_4rd_hour[q]=valuess[q]/sum(matrix[q])
            
            values_ave[q], valuess_ave[q], matrix_ave[q,:]=find_dist_ave(q, lon11, lat11, X, Y,\
                                     bathynew, longitude, latitude, saline_nemo_ave3rd, saline_nemo_ave4rd)
            value_mean_ave3rd[q]=values_ave[q]/sum(matrix_ave[q])
            value_mean_ave4rd[q]=valuess_ave[q]/sum(matrix_ave[q])
        elif results_home == paths['nowcast']:
            values[q], valuess[q], matrix[q,:]=find_dist(q, lon11, lat11, X, Y,\
                                     bathyold, longitude, latitude, saline_nemo_3rd, saline_nemo_4rd)
            value_mean_3rd_hour[q]=values[q]/sum(matrix[q])
            value_mean_4rd_hour[q]=valuess[q]/sum(matrix[q])

            values_ave[q], valuess_ave[q], matrix_ave[q,:]=find_dist_ave(q, lon11, lat11, X, Y,\
                                     bathynew, longitude, latitude, saline_nemo_ave3rd, saline_nemo_ave4rd)
            value_mean_ave3rd[q]=values_ave[q]/sum(matrix_ave[q])
            value_mean_ave4rd[q]=valuess_ave[q]/sum(matrix_ave[q])

    return lon11, lat11, lon1_2_4, lat1_2_4,\
    value_mean_3rd_hour, value_mean_4rd_hour, \
    value_mean_ave3rd, value_mean_ave4rd,\
    salinity11, salinity1_2_4, date_str

def salinity_ferry_route(grid_T, grid_B, PNW_coastline, sal_hr, saline, run_date,results_home):
    """ plot daily salinity comparisons between ferry observations 
    and model results as well as ferry route with model salinity 
    distribution.
    
    :arg grid_B: Bathymetry dataset for the Salish Sea NEMO model.
    :type grid_B: :class:`netCDF4.Dataset`
    
    :arg PNW_coastline: Coastline dataset.
    :type PNW_coastline: :class:`mat.Dataset`
    
    :arg ferry_sal: saline
    :type ferry_sal: numpy
    
    :returns: fig
    """

    latitude=grid_T.variables['nav_lat'] 
    longitude=grid_T.variables['nav_lon']
    fig, axs = plt.subplots(1, 2, figsize=(15, 8))

    figures.plot_map(axs[1], grid_B, PNW_coastline)
    axs[1].set_xlim(-124.5, -122.5)
    axs[1].set_ylim(48.2, 49.5)
    viz_tools.set_aspect(axs[1],coords='map',lats=latitude)
    cmap=plt.get_cmap('spectral')
    cmap.set_bad('burlywood')
    mesh=axs[1].pcolormesh(longitude[:],latitude[:],sal_hr[:],cmap=cmap)
    cbar=fig.colorbar(mesh)
    plt.setp(plt.getp(cbar.ax.axes, 'yticklabels'), color='w')
    cbar.set_label('Pratical Salinity', color='white')
    
    axs[1].set_title('Ferry Route: 3am[UTC] 1.5m model result ', **title_font)
 
    bbox_args = dict(boxstyle='square', facecolor='white', alpha=0.7)
    stations=['Tsawwassen','Duke','Vancouver']
    for stn in stations:
        axs[1].plot(ferry_stations[stn]['lon'], ferry_stations[stn]['lat'], marker='D', \
                    color='white',\
                 markersize=10, markeredgewidth=2)
    axs[1].annotate ('Tsawwassen',(ferry_stations['Tsawwassen']['lon'] + 0.02,\
    ferry_stations['Tsawwassen']['lat'] + 0.12), fontsize=15, color='black', bbox=bbox_args )
    axs[1].annotate ('Duke',(ferry_stations['Duke']['lon'] - 0.35,\
    ferry_stations['Duke']['lat'] ),fontsize=15, color='black', bbox=bbox_args )
    axs[1].annotate ('Vancouver',(ferry_stations['Vancouver']['lon'] - 0.1,\
    ferry_stations['Vancouver']['lat']+ 0.09 ),fontsize=15, color='black', bbox=bbox_args )
    figures.axis_colors(axs[1], 'white')
    
    #filepath_name = date(run_date.year,run_date.month, run_date.day,\
     #run_date.day,run_date.day, results_home,'1h','grid_T')     
    lon11, lat11, lon1_2_4, lat1_2_4,\
    value_mean_3rd_hour, value_mean_4rd_hour, \
    value_mean_ave3rd, value_mean_ave4rd,\
    salinity11, salinity1_2_4,date_str = salinity_fxn(saline, run_date, results_home )
    axs[1].plot(lon11,lat11,'black', linewidth = 4)
    model_salinity_3rd_hour=axs[0].plot(lon11,value_mean_3rd_hour,'DodgerBlue',\
                                    linewidth=2, label='3 am [UTC]')
    model_salinity_4rd_hour=axs[0].plot(lon11,value_mean_4rd_hour,'MediumBlue',\
                                        linewidth=2, label="4 am [UTC]" )
    observation_salinity=axs[0].plot(lon1_2_4,salinity1_2_4,'DarkGreen', \
                                     linewidth=2, label="Observed")
    axs[0].text(0.25, -0.1,'Observations from Ocean Networks Canada', \
                transform=axs[0].transAxes, color='white')

    axs[0].set_xlim(-124, -123)
    axs[0].set_ylim(0, 30)
    axs[0].set_title('Surface Salinity: ' + date_str, **title_font)
    axs[0].set_xlabel('Longitude', **axis_font)
    axs[0].set_ylabel('Practical Salinity', **axis_font)
    axs[0].legend()
    axs[0].grid()
   

    fig.patch.set_facecolor('#2B3E50')
    figures.axis_colors(axs[0], 'gray')
    
    return fig

def salinity_ferry_route_more(grid_T, grid_B, PNW_coastline, ave, sal_hr_1, sal_hr_ave, saline, run_date,results_home):
    """ plot daily salinity comparisons between ferry observations 
    and model results as well as ferry route with model salinity 
    distribution.
    
    :arg grid_B: Bathymetry dataset for the Salish Sea NEMO model.
    :type grid_B: :class:`netCDF4.Dataset`
    
    :arg PNW_coastline: Coastline dataset.
    :type PNW_coastline: :class:`mat.Dataset`
    
    :arg ferry_sal: saline
    :type ferry_sal: numpy
    
    :returns: fig
    """

    latitude=grid_T.variables['nav_lat'] 
    longitude=grid_T.variables['nav_lon']
    fig, axs = plt.subplots(1, 2, figsize=(15, 8))

    figures.plot_map(axs[1], grid_B, PNW_coastline)
    axs[1].set_xlim(-124.5, -122.5)
    axs[1].set_ylim(48.2, 49.5)
    viz_tools.set_aspect(axs[0],coords='map',lats=latitude)
    cmap=plt.get_cmap('spectral')
    cmap.set_bad('burlywood')
    if ave ==0:
        mesh=axs[1].pcolormesh(longitude[:],latitude[:],sal_hr_1[:],cmap=cmap)
        axs[1].set_title('Ferry Route: 3am[UTC] 1.5m model result ', **title_font)
    elif ave ==1:
        mesh=axs[1].pcolormesh(longitude[:],latitude[:],sal_hr_ave[:],cmap=cmap)
        axs[1].set_title('Ferry Route: 3am[UTC] 3m average model result ', **title_font)
    cbar=fig.colorbar(mesh)
    plt.setp(plt.getp(cbar.ax.axes, 'yticklabels'), color='w')
    cbar.set_label('Pratical Salinity', color='white') 
    
    bbox_args = dict(boxstyle='square', facecolor='white', alpha=0.7)
    stations=['Tsawwassen','Duke','Vancouver']
    for stn in stations:
        axs[1].plot(ferry_stations[stn]['lon'], ferry_stations[stn]['lat'], marker='D', \
                    color='white',\
                 markersize=10, markeredgewidth=2)
    axs[1].annotate ('Tsawwassen',(ferry_stations['Tsawwassen']['lon'] + 0.02,\
    ferry_stations['Tsawwassen']['lat'] + 0.12), fontsize=15, color='black', bbox=bbox_args )
    axs[1].annotate ('Duke',(ferry_stations['Duke']['lon'] - 0.35,\
    ferry_stations['Duke']['lat'] ),fontsize=15, color='black', bbox=bbox_args )
    axs[1].annotate ('Vancouver',(ferry_stations['Vancouver']['lon'] - 0.1,\
    ferry_stations['Vancouver']['lat']+ 0.09 ),fontsize=15, color='black', bbox=bbox_args )
    figures.axis_colors(axs[1], 'white')

 
    #filepath_name = date(run_date.year,run_date.month, run_date.day,\
     #run_date.day,run_date.day, results_home,'1h','grid_T')     
    lon11, lat11, lon1_2_4, lat1_2_4,\
    value_mean_3rd_hour, value_mean_4rd_hour, \
    value_mean_ave3rd, value_mean_ave4rd,\
    salinity11, salinity1_2_4,date_str = salinity_fxn(saline, run_date, results_home)
    axs[1].plot(lon11,lat11,'black', linewidth = 4)
    if ave ==0:
        model_salinity_3rd_hour=axs[0].plot(lon11,value_mean_3rd_hour,'DodgerBlue',\
                                    linewidth=2, label='3 am [UTC]')
        model_salinity_4rd_hour=axs[0].plot(lon11,value_mean_4rd_hour,'MediumBlue',\
                                        linewidth=2, label="4 am [UTC]" )
        observation_salinity=axs[0].plot(lon1_2_4,salinity1_2_4,'DarkGreen', \
                                     linewidth=2, label="Observed")
    elif ave ==1:
        model_salinity_3rd_hour=axs[0].plot(lon11,value_mean_ave3rd,'DodgerBlue',\
                                    linewidth=2, label='3 am [UTC]')
        model_salinity_4rd_hour=axs[0].plot(lon11,value_mean_ave4rd,'MediumBlue',\
                                        linewidth=2, label="4 am [UTC]" )
        observation_salinity=axs[0].plot(lon1_2_4,salinity1_2_4,'DarkGreen', \
                                     linewidth=2, label="Observed")
    axs[0].text(0.25, -0.1,'Observations from Ocean Networks Canada', \
                transform=axs[0].transAxes, color='white')

    axs[0].set_xlim(-124, -123)
    axs[0].set_ylim(0, 30)
    axs[0].set_title('Surface Salinity: ' + date_str, **title_font)
    axs[0].set_xlabel('Longitude', **axis_font)
    axs[0].set_ylabel('Practical Salinity', **axis_font)
    axs[0].legend()
    axs[0].grid()
    fig.patch.set_facecolor('#2B3E50')
    figures.axis_colors(axs[0], 'gray')
      

    return fig


def find_min_salinity_value(run_date, results_home, saline)
    """This function was made to find out the minimum salinity value
       for observation, 1.5m model result and average 3m depth model 
       result."""
     
     #filepath_name = date(run_date.year,run_date.month, run_date.day,\
     #run_date.day,run_date.day, results_home,'1h','grid_T')  
    lon11, lat11, lon1_2_4, lat1_2_4,\
    value_mean_3rd_hour, value_mean_4rd_hour, \
    value_mean_ave3rd, value_mean_ave4rd,\
    salinity11, salinity1_2_4,date_str = salinity_fxn(saline, run_date, results_home)







