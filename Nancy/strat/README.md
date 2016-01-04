The IPython Notebooks in this directory are made by Nancy for
quick sharing of results.

The links below are to static renderings of the notebooks via
[nbviewer.ipython.org](http://nbviewer.ipython.org/).
Descriptions below the links are from the first cell of the notebooks
(if that cell contains Markdown or raw text).

* ##[DWR_kw.ipynb](http://nbviewer.ipython.org/urls/bitbucket.org/salishsea/analysis/raw/tip/Nancy/strat/DWR_kw.ipynb)  
    
    This notebook looks at the vertical eddy viscosity/diffusivity during a deep water renewal event in late August 2003.  
      
    Compares a kw closure with k-eps closure  
      
    Both have no wind, rm_avm0 =1e-4, rn_avt0 = 1e-5, no bbl, isoneutral mixing  
      
    dwr_kw compared to dwr_isoneutral  

* ##[DWR_corrected_april.ipynb](http://nbviewer.ipython.org/urls/bitbucket.org/salishsea/analysis/raw/tip/Nancy/strat/DWR_corrected_april.ipynb)  
    
    This notebook looks at the vertical eddy viscosity/diffusivity during a deep water renewal event in late August 2003.  
      
    Compares dwr_new_bcs with dwr_base_bcs  
      
    Both have diff/visc 1e-6/1e-5, isoneutral, winds  
      
    dwr_corrected applies a correction to the origial bcs.  
      
    Simulations in late april. Restarted for May to July.  

* ##[Winds and Fresh Spurts at Race Rocks.ipynb](http://nbviewer.ipython.org/urls/bitbucket.org/salishsea/analysis/raw/tip/Nancy/strat/Winds and Fresh Spurts at Race Rocks.ipynb)  
    
    How do the spikes in freshness at Race Rocks relate to the local winds and spring/neap tides?  
      
    How is the salinity in Malaspina Strait connected to all of this?  

* ##[DWR_new_bcs.ipynb](http://nbviewer.ipython.org/urls/bitbucket.org/salishsea/analysis/raw/tip/Nancy/strat/DWR_new_bcs.ipynb)  
    
    This notebook looks at the vertical eddy viscosity/diffusivity during a deep water renewal event in late August 2003.  
      
    Compares dwr_new_bcs with dwr_base_bcs  
      
    Both have diff/visc 1e-6/1e-5, isoneutral, winds  
      
    dwr_new_bcs has salnity below 150m incrased by 0.3311  

* ##[DWR_notsmooth_kappa10_winds.ipynb](http://nbviewer.ipython.org/urls/bitbucket.org/salishsea/analysis/raw/tip/Nancy/strat/DWR_notsmooth_kappa10_winds.ipynb)  
    
    This notebook looks at the vertical eddy viscosity/diffusivity during a deep water renewal event in late August 2003.  
      
    Compares diff=1e-6 and visc=1e-5 with winds to base case with winds.   


* ##[Eddy values at VENUS nodes.ipynb](http://nbviewer.ipython.org/urls/bitbucket.org/salishsea/analysis/raw/tip/Nancy/strat/Eddy values at VENUS nodes.ipynb)  
    
    This notebook will compare the vertical eddy diffusivity and viscosity at the the VENUS nodes. Two simulations are compared -   
      
    1. dwr_notsmooth_kappa10_winds (rn_avt0=1e-5, rn_avt0 = 1e-4)  
    2. dwr_diff1e-6_visc1e-5_wind (rn_avt0= 1e-6, rn_avm0 = 1e-5)  
      
      
    Both used winds  

* ##[DWR_diff1e-6_visc1e-5_winds.ipynb](http://nbviewer.ipython.org/urls/bitbucket.org/salishsea/analysis/raw/tip/Nancy/strat/DWR_diff1e-6_visc1e-5_winds.ipynb)  
    
    This notebook looks at the vertical eddy viscosity/diffusivity during a deep water renewal event in late August 2003.  
      
    Compares diff=1e-6 and visc=1e-5 with winds to diff=1e-6, visc=1e-5 with no winds.   


* ##[DWR_new_bcs_surface.ipynb](http://nbviewer.ipython.org/urls/bitbucket.org/salishsea/analysis/raw/tip/Nancy/strat/DWR_new_bcs_surface.ipynb)  
    
    This notebook looks at the vertical eddy viscosity/diffusivity during a deep water renewal event in late August 2003.  
      
    Compares dwr_new_bcs_surface with dwr_new_bcs  
      
    Both have diff/visc 1e-6/1e-5, isoneutral, winds  
      
    dwr_new_bcs has salinity below 150m incrased by 0.3311  
      
    dwr_new_bcs_surface has salinity below 150m incrased by 0.3311 and salinity above 50m increased by 0.3311  

* ##[DWR_enst.ipynb](http://nbviewer.ipython.org/urls/bitbucket.org/salishsea/analysis/raw/tip/Nancy/strat/DWR_enst.ipynb)  
    
    This notebook looks stratification along thalweg in late April.  
      
    Compares dwr_base_enstr with dwr_enstr_eng  
      
    Both have diff/visc 1e-6/1e-5, isoneutral, winds  
      
    dwr_base_enstr has enstrophy conserving scheme.  
      
    dwr_enstr_eng has original choice - energy enstrophy conserving.  

* ##[DWR_bbl.ipynb](http://nbviewer.ipython.org/urls/bitbucket.org/salishsea/analysis/raw/tip/Nancy/strat/DWR_bbl.ipynb)  
    
    This notebook looks at the vertical eddy viscosity/diffusivity during a deep water renewal event in late August 2003.  
      
    Compares dwr_adv1 with dwr_base_bcs  
      
    Both have diff/visc 1e-6/1e-5, isoneutral, winds  
      
    dwr_bbl_adv1 has advecitve bbl, first option.  
      
    Similar results for dwr_bbl_diff  
      
    Almost no differences between the base case and dwr_bbl_adv2.  

* ##[Stratification and tides.ipynb](http://nbviewer.ipython.org/urls/bitbucket.org/salishsea/analysis/raw/tip/Nancy/strat/Stratification and tides.ipynb)  
    
    Check on a 40 day run with no stratification. This means no OBC temp/salinity, no weather and no rivers. Temp/salinity set to ocean values through whole domain.  

* ##[DWR_kappa10_smooth.ipynb](http://nbviewer.ipython.org/urls/bitbucket.org/salishsea/analysis/raw/tip/Nancy/strat/DWR_kappa10_smooth.ipynb)  
    
    This notebook looks at the vertical eddy viscosity/diffusivity during a deep water renewal event in late August 2003.  
      
    Compares kappa=10, smooth to kappa=20.5, not smooth  


* ##[DWR_diff1e-6_visc1e-5.ipynb](http://nbviewer.ipython.org/urls/bitbucket.org/salishsea/analysis/raw/tip/Nancy/strat/DWR_diff1e-6_visc1e-5.ipynb)  
    
    This notebook looks at the vertical eddy viscosity/diffusivity during a deep water renewal event in late August 2003.  
      
    Compares diff=1e-6 and visc=1e-5 to base case (diff=1e-5 and visc=1e-4).  
      
    In 2D, decreasing diff made the surface layer much fresher (less mixing across strong gradients). Decreasing visc made the surface layer slightly saltier (more mixing because stronger shear??).  
      
    My thought was that decreasing both in the 3D model would somehow cancel the effect on the surface layer.  
      
    2D model had no wind.  

* ##[Deep Water Renewal - East of Central.ipynb](http://nbviewer.ipython.org/urls/bitbucket.org/salishsea/analysis/raw/tip/Nancy/strat/Deep Water Renewal - East of Central.ipynb)  
    
* ##[Rich's IOS data.ipynb](http://nbviewer.ipython.org/urls/bitbucket.org/salishsea/analysis/raw/tip/Nancy/strat/Rich's IOS data.ipynb)  
    
    Notebook to determine the temporal and spatial coverage of IOS data that Rich has stored.  


* ##[DWR_diff1e-6.ipynb](http://nbviewer.ipython.org/urls/bitbucket.org/salishsea/analysis/raw/tip/Nancy/strat/DWR_diff1e-6.ipynb)  
    
    This notebook looks at the vertical eddy viscosity/diffusivity during a deep water renewal event in late August 2003.  
      
    Compares diff=1e-5 to 1e-6  


* ##[DWR_holls_36.ipynb](http://nbviewer.ipython.org/urls/bitbucket.org/salishsea/analysis/raw/tip/Nancy/strat/DWR_holls_36.ipynb)  
    
    This notebook looks at the vertical eddy viscosity/diffusivity during a deep water renewal event in late August 2003.  
      
    Compares dwr_base_36 to dwr_holl_36  
      
    Both have defualt 3.6 settings with winds, but the hol case has the hollingsworth corrections.  


* ##[DWR_isoneutral.ipynb](http://nbviewer.ipython.org/urls/bitbucket.org/salishsea/analysis/raw/tip/Nancy/strat/DWR_isoneutral.ipynb)  
    
    This notebook looks at the vertical eddy viscosity/diffusivity during a deep water renewal event in late August 2003.  
      
    Compares isoneutral mixing to default case  


* ##[DWR_corrected.ipynb](http://nbviewer.ipython.org/urls/bitbucket.org/salishsea/analysis/raw/tip/Nancy/strat/DWR_corrected.ipynb)  
    
    This notebook looks at the vertical eddy viscosity/diffusivity during a deep water renewal event in late August 2003.  
      
    Compares dwr_new_bcs with dwr_base_bcs  
      
    Both have diff/visc 1e-6/1e-5, isoneutral, winds  
      
    dwr_corrected applies a correction to the origial bcs.  

* ##[DWR_kappa10.ipynb](http://nbviewer.ipython.org/urls/bitbucket.org/salishsea/analysis/raw/tip/Nancy/strat/DWR_kappa10.ipynb)  
    
    This notebook looks at the vertical eddy viscosity/diffusivity during a deep water renewal event in late August 2003.  
      
    Compares kappa=10 to kappa=20.5  



##License

These notebooks and files are copyright 2013-2016
by the Salish Sea MEOPAR Project Contributors
and The University of British Columbia.

They are licensed under the Apache License, Version 2.0.
http://www.apache.org/licenses/LICENSE-2.0
Please see the LICENSE file for details of the license.
