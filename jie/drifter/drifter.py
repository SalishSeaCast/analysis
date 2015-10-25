"""This drifter.py was made to load some 
   functions to plot drifter trajetories."""

from __future__ import division
import matplotlib.pyplot as plt
import netCDF4 as nc
import numpy as np
import datetime as dt
import pytz, datetime
import scipy.io
import os
from salishsea_tools import nc_tools, viz_tools, tidetools, stormtools, bathy_tools

grid = nc.Dataset('/ocean/jieliu/research/meopar/river-treatment/bathy_meter_SalishSea6.nc','r')

bathy, X, Y = tidetools.get_bathy_data(grid)

tracersT = nc.Dataset('/data/jieliu/MEOPAR/river-treatment/oct8_10RFdailySmoo/\
SalishSea_1h_20141008_20141010_grid_T.nc')
ssh = tracersT.variables['sossheig']
timesteps = tracersT.variables['time_counter']

def convert_time(matlab_time_array):
    "converts a matlab time array to python format"
    python_time_array=[]
    for t in matlab_time_array:
        python_datetime = dt.datetime.fromordinal(int(t)) + dt.timedelta(days=t%1) - dt.timedelta(days = 366)
        python_time_array.append(python_datetime)
    
    python_time_array = np.array(python_time_array)
    return python_time_array

def get_tracks(switch,lats,lons,ptime,in_water):
    """returns a list of tracks of each buoy, ie a trajectory for
    each time the buoy was released into the water"""
    all_tracks=[]
    for ind in switch:
        track_on = 1
        i = ind
        track ={'time':[], 'lat':[],'lon':[]}
        while(track_on):
            if in_water[i]!=1:
                track_on=0
            elif i==np.shape(in_water)[0]-1:    
                track['time'].append(ptime[i])
                track['lat'].append(lats[i])
                track['lon'].append(lons[i])
                track_on=0
            else:
                track['time'].append(ptime[i])
                track['lat'].append(lats[i])
                track['lon'].append(lons[i])
            i=i+1
        all_tracks.append(track)
        
    return all_tracks

def organize_info(buoy,btype):
    """ organizes the buoy info. Groups the buoy data into tracks for 
        when it was released into the water. """
    #creat arrays for easier access
    buoy_name = btype[buoy][0]
    lats = btype[buoy]['lat'].flatten()
    lons = btype[buoy]['lon'].flatten()
    mtime = btype[buoy]['mtime']
    in_water = btype[buoy]['isSub'].flatten()
    #convert mtime to python datetimes
    ptime = convert_time(mtime)
    
    #loop through in_water flag to find when buoy switched from being out of water to being in water. 
    switch = []; 
    for ind in np.arange(1,in_water.shape[0]):
        if int(in_water[ind]) != int(in_water[ind-1]):
            if int(in_water[ind])==1:
                switch.append(ind)
    
    all_tracks=get_tracks(switch,lats,lons,ptime.flatten(),in_water)
    
    return buoy_name, all_tracks

def print_info(buoy,btype):
    """ prints the release time, lat, lon, and duration of a buoy track"""
    name, tracks=organize_info(buoy,btype)
    print (name)
    print ('Release times, positions and duration in hours')
    for t in tracks:
        print (t['time'][0], t['lat'][0], t['lon'][0],\
        (t['time'][-1]-t['time'][0]).total_seconds()/3600)

def find_start(tracks, start_date):
    """returns the a list of indices for a track released on start date.
    Only checks the month and day of the start day"""
    i=0
    ind=[]
    starttimes=[]
    for t in tracks:   
        if int(t['time'][0].month) == start_date.month:
                if int(t['time'][0].day) == start_date.day:
                    ind.append(i)
        i=i+1
        
    return ind


def plot_buoy_random(tracks, startdate, day, hour,i=0, fancy=False):
    """ plots a buoy trajectory at the given startdate in an axis, ax.
    returns the trajectory that was plotted.
    The first track released on the startdate is plotted.
    For trajectories that were released mulitples times a day, i selects which release is plotted.
    """
    fig,(ax1,ax2) = plt.subplots(1,2,figsize=(10,5))
    
    ind =find_start(tracks,startdate)
    traj=tracks[ind[i]]
    duration = (traj['time'][-1]-traj['time'][0]).total_seconds()/3600
    random_time = dt.datetime(2014, 10, day, hour)
    lonn = []
    latt = []

    print ('Released', traj['time'][0], 'at', traj['lat'][0], ',' , traj['lon'][0], 'for' , duration, 'hours')
    ax1.plot(traj['lon'],traj['lat'],'ob')
    ax1.plot(traj['lon'][0],traj['lat'][0],'sr')
    ax1.set_xlim([-123.6,-123])
    ax1.set_ylim([48.8,49.4])
    ax1.set_xticks([-123.6, -123.4, -123.2,-123])
    ax1.set_xticklabels([-123.6, -123.4, -123.2,-123])
    ax1.set_title('Observed Drift Track')
    ax1.set_xlabel('Longitude')
    ax1.set_ylabel('Latitude')
    for ii in np.arange(len(traj['time'])):
        if dt.timedelta(hours=0)<(traj['time'][ii] - random_time) < dt.timedelta(hours = 1):
            ax1.plot(traj['lon'][ii], traj['lat'][ii], '*r')
            lonn.append(traj['lon'][ii])
            latt.append(traj['lat'][ii])
            if traj['time'][ii].minute ==30:
                print (traj['time'][ii], traj['lon'][ii], traj['lat'][ii])
                [jjj, iii] = tidetools.find_closest_model_point\
                (float(traj['lon'][ii]),float(traj['lat'][ii]),X,Y,bathy)
    
    [j,i]=tidetools.find_closest_model_point(float(traj['lon'][0]),float(traj['lat'][0]),X,Y,bathy)
    ax1.plot(-123-np.array([18.2, 13.7, 12])/60.,49+np.array([6.4, 8, 7.6])/60.,'-k',lw=2); 
    if fancy:
        cmap = plt.get_cmap('winter_r')
        cmap.set_bad('burlywood')
        ax1.pcolormesh(X, Y, bathy, cmap=cmap)
        ax1.text(-123.15,49.13, "Fraser River", fontsize=12)
    else:
        viz_tools.plot_coastline(ax1, grid, coords='map')
        viz_tools.plot_coastline(ax1, grid, coords='map',isobath=4)
        viz_tools.plot_coastline(ax1, grid, coords='map',isobath=20)
        print ('Random lat & lon in NEMO coords:', jjj, iii)
          
    ax2.plot(timesteps[0:48],ssh[0:48,466,329],'-k')
    
    ax2.set_xticklabels([])
    ax2.set_ylabel('Water level (m)')
    ax2.set_xlabel('Oct 8 - Oct 9 (hrs)')
    ax2.set_title('sossheig, ~Point Atkinson')
        
    t=hour
    ax2.plot([timesteps[t],timesteps[t]],[-2.0,1.5],'y-')
    
    return traj, jjj, iii, hour


