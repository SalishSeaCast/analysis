The IPython Notebooks in this directory are made by Nancy for
quick sharing of results. Thse notebooks are about drifters and Ariane particles. 

The links below are to static renderings of the notebooks via
[nbviewer.ipython.org](http://nbviewer.ipython.org/).
Descriptions below the links are from the first cell of the notebooks
(if that cell contains Markdown or raw text).

* ##[Drifters_Ariane_Comparison_Nancy.ipynb](http://nbviewer.ipython.org/urls/bitbucket.org/salishsea/analysis/raw/tip/Nancy/drifters/Drifters_Ariane_Comparison_Nancy.ipynb)  
    
    **This notebook compares the trajectories of drifters versus the particle trajectories produced by Ariane using our model data.**  
      
    Nancy redid Idalia's computations because for Fortran/Python indexing. Originally, we used python to look up the grid index of the drifter release points. But since Ariane is written in Fortran, we should have added one to these indices. Nancy redid the calculation with +1. This notebook compares those trajectories.   

* ##[Drifters.ipynb](http://nbviewer.ipython.org/urls/bitbucket.org/salishsea/analysis/raw/tip/Nancy/drifters/Drifters.ipynb)  
    
    Looking at the drifter data from Mark. Trying to determine dates and locations of releases.  


##License

These notebooks and files are copyright 2013-2015
by the Salish Sea MEOPAR Project Contributors
and The University of British Columbia.

They are licensed under the Apache License, Version 2.0.
http://www.apache.org/licenses/LICENSE-2.0
Please see the LICENSE file for details of the license.
