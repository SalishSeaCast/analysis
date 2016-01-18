The IPython Notebooks in this directory are made by Jie for
quick sharing of results.

The links below are to static renderings of the notebooks via
[nbviewer.ipython.org](http://nbviewer.ipython.org/).
Descriptions below the links are from the first cell of the notebooks
(if that cell contains Markdown or raw text).

* ##[MeanCurrent.ipynb](http://nbviewer.ipython.org/urls/bitbucket.org/salishsea/analysis/raw/tip/jie/surface_current/MeanCurrent.ipynb)  
    
    * This notebook was made to evaluate mean current (only forced by river flow) during low river flow period by comparing with codar data.  

* ##[ImpactOfEachForcing.ipynb](http://nbviewer.ipython.org/urls/bitbucket.org/salishsea/analysis/raw/tip/jie/surface_current/ImpactOfEachForcing.ipynb)  
    
    * To investigate the impact of each forcing, i.e., river flow, tides, winds and Coriolis force on the plume properties and stratification.  

* ##[OnlyRiverMeanCurrent.ipynb](http://nbviewer.ipython.org/urls/bitbucket.org/salishsea/analysis/raw/tip/jie/surface_current/OnlyRiverMeanCurrent.ipynb)  
    
    * In addition to compare mean current of model results with codar by the same method, how about the idealized caseof mean current? That is, to run only with rivers, no tides, no weather. Two speculations of the potential results:  
      
    * 1 Only river mean flow is closer to codar, that indicates winds effects much of the mean currents in the previous way.  
    * 2 None of them is closer to codar, something else is still going on...  
    * 3 Analyze difference between only river and all conditions.  

* ##[NoCoriolisMeanCurrent.ipynb](http://nbviewer.ipython.org/urls/bitbucket.org/salishsea/analysis/raw/tip/jie/surface_current/NoCoriolisMeanCurrent.ipynb)  
    
    * To check my four days mean current without Coriolis force.  

* ##[HindcastSalCurrField.ipynb](http://nbviewer.ipython.org/urls/bitbucket.org/salishsea/analysis/raw/tip/jie/surface_current/HindcastSalCurrField.ipynb)  
    
    * This notebook was made to check the difference between short vs long river in the salinity and currents field in the hourly results. This work is motivated by the high value of min salinity in 3.6 with long river(TS4) vs TS2, which we speculate it may be either caused by intense vertical mixing or relatively low river flow at the mouth with long river (mass conservation). However, I don't quite believe that results and think if it is mainly caused by low river flow at the mouth, it seems to contradict with the baseline we have stronger currents field with long river even taken into account the tidal currents. What if that 3.6 daily results did not count in the tidal part as it resolves the tidal component. Here, in 3.4, with hourly results, I want to examine the same issue with short and long river and see if this makes diffrence.  

* ##[TSforMay2015.ipynb](http://nbviewer.ipython.org/urls/bitbucket.org/salishsea/analysis/raw/tip/jie/surface_current/TSforMay2015.ipynb)  
    
    * This notebook was made to create TS initial files based on 21apr15 to spinup for May2015.  


##License

These notebooks and files are copyright 2013-2016
by the Salish Sea MEOPAR Project Contributors
and The University of British Columbia.

They are licensed under the Apache License, Version 2.0.
http://www.apache.org/licenses/LICENSE-2.0
Please see the LICENSE file for details of the license.
