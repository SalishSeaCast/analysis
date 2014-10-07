The IPython Notebooks in this directory are related to preparing
for storm surge simulations.

The links below are to static renderings of the notebooks via
[nbviewer.ipython.org](http://nbviewer.ipython.org/).
Descriptions below the links are from the first cell of the notebooks
(if that cell contains Markdown or raw text).

* ##[Pressure to sea level.ipynb](http://nbviewer.ipython.org/urls/bitbucket.org/salishsea/analysis/raw/tip/storm_surges/Pressure to sea level.ipynb)  
    
    This notebook experiments with bring the surface pressure from CGRF down to sea level.   

* ##[Compare Neah Bay and Tofino.ipynb](http://nbviewer.ipython.org/urls/bitbucket.org/salishsea/analysis/raw/tip/storm_surges/Compare Neah Bay and Tofino.ipynb)  
    
    This notebook compares the surges at Neah Bay and Tofino to determine if the timing of the surge event at these two location is in sync. Also look at Toke Point.  
      
    Also does a quick check of the contribution to SSH due to the inverse barometer effect.  

* ##[final-nov2006.ipynb](http://nbviewer.ipython.org/urls/bitbucket.org/salishsea/analysis/raw/tip/storm_surges/final-nov2006.ipynb)  
    
    This notebook will compare sea surface height between new and old configurations for dec 2006.  
      
    new config: sea level pressure adjusted to sea level + corr15 tides. So bottom friction is 5 e-3  
      
    old config: no pressure correction and old tides. Bottom friction is 1 e-3, M2/K1 adjusted for good match in SoG.   
      


* ##[2005 harmonics at Tofino.ipynb](http://nbviewer.ipython.org/urls/bitbucket.org/salishsea/analysis/raw/tip/storm_surges/2005 harmonics at Tofino.ipynb)  
    
    This notebook compares anomalies at Tofino. Two choices are presented  
      
    1. Tidal predictions calculated with 2005 harmonics  
    2. Tidal predictions calulated with 2006 harmonics  
      
    In our analysis of storm surges, we are calculating observed anomlaies calculated with 2005 harmonics. So shouldn't we do the same when setting up forcing conditions in our model? Will it make a difference?  
      
    We'll compare with anomalies at Neah Bay as well since that is close by to Tofino.  

* ##[SandHeadsWinds.ipynb](http://nbviewer.ipython.org/urls/bitbucket.org/salishsea/analysis/raw/tip/storm_surges/SandHeadsWinds.ipynb)  
    
    **Sand Heads Winds**  
      
    This notebook demonstrates how to read the file of historical wind data  
    from the Sand Heads weather station that is maintained in the SOG-forcing  
    repo into a data structure of NumPy arrays.  
      
    The code is based on code in the `bloomcast.wind` module in the [SoG-bloomcast project](https://bitbucket.org/douglatornell/sog-bloomcast).  

* ##[final.ipynb](http://nbviewer.ipython.org/urls/bitbucket.org/salishsea/analysis/raw/tip/storm_surges/final.ipynb)  
    
    This notebook will compare sea surface height between new and old configurations.  
      
    new config: sea level pressure adjusted to sea level + corr15 tides. So bottom friction is 5 e-3  
      
    old config: no pressure correction and old tides. Bottom friction is 1 e-3, M2/K1 adjusted for good match in SoG.   
      


* ##[spinups.ipynb](http://nbviewer.ipython.org/urls/bitbucket.org/salishsea/analysis/raw/tip/storm_surges/spinups.ipynb)  
    
    A notebook for determining how long it takes for velocities to spinup after initializing with a restart files. This is useful for determing storm surge simulation start dates.   
      
    Note this probably depends on viscosity. This simulations use nu =50.  

* ##[FindWindEvents.ipynb](http://nbviewer.ipython.org/urls/bitbucket.org/salishsea/analysis/raw/tip/storm_surges/FindWindEvents.ipynb)  
    
    This notebook looks for large wind events in Sandheads historical wind data. We are looking for a wind storm that did not result in a surge. We would like to ensure that the model does not make a surge if one did not actually occur.   
      
    This codes uses a combination of Doug's class for reading Sandheads data and Kate's methodology for finding ssh anamolies.  

* ##[final-dec2006.ipynb](http://nbviewer.ipython.org/urls/bitbucket.org/salishsea/analysis/raw/tip/storm_surges/final-dec2006.ipynb)  
    
    This notebook will compare sea surface height between new and old configurations for dec 2006.  
      
    new config: sea level pressure adjusted to sea level + corr15 tides. So bottom friction is 5 e-3  
      
    old config: no pressure correction and old tides. Bottom friction is 1 e-3, M2/K1 adjusted for good match in SoG.   
      


* ##[Surge Spatial Extent.ipynb](http://nbviewer.ipython.org/urls/bitbucket.org/salishsea/analysis/raw/tip/storm_surges/Surge Spatial Extent.ipynb)  
    
    This notebook will plot the spatial extent of the surge on Feb. 4 2006  


* ##[weather_Nov-15-2006.ipynb](http://nbviewer.ipython.org/urls/bitbucket.org/salishsea/analysis/raw/tip/storm_surges/weather_Nov-15-2006.ipynb)  
    
    This notebook plots the weather at Point Atkinson on Nov. 15, 2006 from the Environment Canada website.   
      
    Additionally, we will look at the weather at YVR and Sandheads since it will be easy to compare with CGRF.   

* ##[Reading Neah Bay Surge website.ipynb](http://nbviewer.ipython.org/urls/bitbucket.org/salishsea/analysis/raw/tip/storm_surges/Reading Neah Bay Surge website.ipynb)  
    
    This notebook will experiment with reading data from the Neah Bay storm surge website. Eventually, we will run a script that will extract surge predictions from the site daily and generate forcing files for our storm surge forecasts.  
      
    http://www.nws.noaa.gov/mdl/etsurge/index.php?page=stn&region=wc&datum=mllw&list=&map=0-48&type=both&stn=waneah  

* ##[Tofino and Port Hardy Comparison.ipynb](http://nbviewer.ipython.org/urls/bitbucket.org/salishsea/analysis/raw/tip/storm_surges/Tofino and Port Hardy Comparison.ipynb)  
    
    This notebook compares the hourly sea surface height anomaly at Tofino and Port Hardy. We do not have a surge prediction tool at Port Hardy so this comparison will guide our decisions regarding the northern boundary condition on sea surface height.   


##License

These notebooks and files are copyright 2013-2014
by the Salish Sea MEOPAR Project Contributors
and The University of British Columbia.

They are licensed under the Apache License, Version 2.0.
http://www.apache.org/licenses/LICENSE-2.0
Please see the LICENSE file for details of the license.
