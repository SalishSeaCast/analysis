The IPython Notebooks in this directory are evaluation of the
tide and storm surge results calculated by the Salish Sea NEMO model.

The links below are to static renderings of the notebooks via
[nbviewer.ipython.org](http://nbviewer.ipython.org/).
Descriptions below the links are from the first cell of the notebooks
(if that cell contains Markdown or raw text).

* ##[Many Tidal Constituents.ipynb](http://nbviewer.ipython.org/urls/bitbucket.org/salishsea/analysis/raw/tip/compare_tides/Many Tidal Constituents.ipynb)  
    
    Notebook that plots tides for different numbers of constituents at Cherry Point to show the importance of constituents beyond the top 8  

* ##[Analysis8Components.ipynb](http://nbviewer.ipython.org/urls/bitbucket.org/salishsea/analysis/raw/tip/compare_tides/Analysis8Components.ipynb)  
    
    This notebook will load data, perform a tidal analyis, compare with observations, plot the results, and save the analysis in a spreadsheet.  Eight Tidal Constituents: M2, K1, O1, S2, P1, N2, Q1 and K2 are considered.  

* ##[comp_wlev_harm-wNorth.ipynb](http://nbviewer.ipython.org/urls/bitbucket.org/salishsea/analysis/raw/tip/compare_tides/comp_wlev_harm-wNorth.ipynb)  
    
    **Model vs. Observed Harmonics with Open Northern Boundary**  
      
    Compare M2 and K1 tidal harmonics from NEMO model to observed harmonics with Northern boundary forcing included in the model.  

* ##[K1&M2 -- M2 variation due to EVD.ipynb](http://nbviewer.ipython.org/urls/bitbucket.org/salishsea/analysis/raw/tip/compare_tides/K1&M2 -- M2 variation due to EVD.ipynb)  
    
    Study M2 Tidal Variation using 5 Day Station SSH  

* ##[Partial Slip.ipynb](http://nbviewer.ipython.org/urls/bitbucket.org/salishsea/analysis/raw/tip/compare_tides/Partial Slip.ipynb)  
    
    A look at the effect of reducing the amount of slip on the tides.   
      
    - 5 day runs with all tidal constituents and flux corrected tides. (double corrected for M2).    
      
      
    1. control - rn_shlat = 0.5  
    2. partial1 - rn_shlat = 0.1  
      
    Note: free slip when rn_shlat = 0 and no slip when rn_shlat = 2.   
      
    Purpose: determine if modifying the amount of slip can affect the tidal amplitudes and phases.  
      


* ##[comp_wlev_harm_compositerun.ipynb](http://nbviewer.ipython.org/urls/bitbucket.org/salishsea/analysis/raw/tip/compare_tides/comp_wlev_harm_compositerun.ipynb)  
    
* ##[Comparison, Using new topography.ipynb](http://nbviewer.ipython.org/urls/bitbucket.org/salishsea/analysis/raw/tip/compare_tides/Comparison, Using new topography.ipynb)  
    
    Notebook to compare previous tides to tides over new topography  

* ##[comp_current_harm.ipynb](http://nbviewer.ipython.org/urls/bitbucket.org/salishsea/analysis/raw/tip/compare_tides/comp_current_harm.ipynb)  
    
    Compare harmonics from currents between measured and modelled. Measured harmonics are taken from Table 3 of Foreman et al (1995)  


* ##[find_wlev_stations.ipynb](http://nbviewer.ipython.org/urls/bitbucket.org/salishsea/analysis/raw/tip/compare_tides/find_wlev_stations.ipynb)  
    
    Where shall we evaluate the storm surge performance of the model? The station needs to have water level data for the period of 2002-2010 (this is when we have wind data).  
      
    * Point Atkinson (49.34,-123.25)  
      
    * Victoria Harbour (48.42,-123.37)  
      
    * Patricia Bay (48.65,-123.45)  
      
    * Campbell River (50.04,-125.25)  
      
    All other sites are not in our domain or do not have water level data for these points  

* ##[comp_wlev_ts.ipynb](http://nbviewer.ipython.org/urls/bitbucket.org/salishsea/analysis/raw/tip/compare_tides/comp_wlev_ts.ipynb)  
    
* ##[find_storms.ipynb](http://nbviewer.ipython.org/urls/bitbucket.org/salishsea/analysis/raw/tip/compare_tides/find_storms.ipynb)  
    
* ##[Check forcing.ipynb](http://nbviewer.ipython.org/urls/bitbucket.org/salishsea/analysis/raw/tip/compare_tides/Check forcing.ipynb)  
    
    A notebook to check that the phase and amplitude in the forcing files is what I expect.  

* ##[plot_foreman_thalweg.ipynb](http://nbviewer.ipython.org/urls/bitbucket.org/salishsea/analysis/raw/tip/compare_tides/plot_foreman_thalweg.ipynb)  
    
    Plot the Foreman et al (1995) model results against our model results, along a thalweg (the thalweg is defined and plotted by Nancy in computer_thalweg.ipynb)  

* ##[Single Tide 2 days.ipynb](http://nbviewer.ipython.org/urls/bitbucket.org/salishsea/analysis/raw/tip/compare_tides/Single Tide 2 days.ipynb)  
    
    Study Tides, over short periods, one Constituent at a Time  

* ##[Tidal Variations.ipynb](http://nbviewer.ipython.org/urls/bitbucket.org/salishsea/analysis/raw/tip/compare_tides/Tidal Variations.ipynb)  
    
    This notebook looks at the effect of changing different parameters on the tides.  
      
    Runs:   
    1. tide_flux_M2K1 - M2/K1 only over 5 days. No modifications to western tides. Northern tides flux decreased.  
    2. tide_flux_west - M2/K1 only with flux increased by 25% at west.   
    3. tide_bottom - bottom friction reduced to 3e-3 (from 5e-3). Note: I suspect we can reduce further, perhaps to 2e-3?  
    4. tide_nu15 - viscosity lowered to 15  
    5. tide_bottom1e-3 - bottom friction reduced to 1e-3  
    5. tide_K1phase2 - K1 phase decreased by 5 degrees.  
    7. tide_K1amp - K1 amp decreased 15 %, phase decreased 5 degrees, bottom friction 1e-3  
    8. tide_M2phase - tide_K1amp properties plus M2 phase decreased by 9 degrees for match at PA. Also bf=1e-3  
    9. tide_slip - above plus rn_shlat lowered to 0.1 from 0.5 (closer to freeslip).  
    10. tide_slipH - above plus rn_shlat increased to 1 from 0.5 (closer to noslip).  
    11. tide_bf0 - tide_M2phase plus rn_bfeb2=-0  
      
    Measured amplitude/phase from Foreman's Discovery Islands and 2004 paper are included.  
      
    Complex differences are from the Foreman inversion method in 2004 paper.   
      
    Uses the same curve fitting technique that Susan wrote.   

* ##[comp_wlev_harm.ipynb](http://nbviewer.ipython.org/urls/bitbucket.org/salishsea/analysis/raw/tip/compare_tides/comp_wlev_harm.ipynb)  
    
    **Model vs. Observed Harmonics**  
      
    Compare M2 and K1 tidal harmonics from NEMO model to observed harmonics. Model has Western boundary forcing and closed Northern boundary. These are early results; see the [Model vs. Observed Harmonics with Open Northern Boundary](http://nbviewer.ipython.org/urls/bitbucket.org/salishsea/analysis/raw/tip/compare_tides/comp_wlev_harm-wNorth.ipynb) notebook for analysis of more recent model results.  

* ##[Multi-tides w Fit.ipynb](http://nbviewer.ipython.org/urls/bitbucket.org/salishsea/analysis/raw/tip/compare_tides/Multi-tides w Fit.ipynb)  
    
    Study Tides: Multi-constituents : Fit to Tide Frequencies  

* ##[Compare Tidal Components.ipynb](http://nbviewer.ipython.org/urls/bitbucket.org/salishsea/analysis/raw/tip/compare_tides/Compare Tidal Components.ipynb)  
    
    Lets look at Mike's Data  

* ##[plot_foreman_thalweg-withNorth.ipynb](http://nbviewer.ipython.org/urls/bitbucket.org/salishsea/analysis/raw/tip/compare_tides/plot_foreman_thalweg-withNorth.ipynb)  
    
    For results including the Northern Boundary,  
    plot the Foreman et al (1995) model results against our model results, along a thalweg (the thalweg is defined and plotted by Nancy in computer_thalweg.ipynb)  

* ##[Ellipses.ipynb](http://nbviewer.ipython.org/urls/bitbucket.org/salishsea/analysis/raw/tip/compare_tides/Ellipses.ipynb)  
    
    Find Tidal Ellipses in CODAR region and VENUS ADCP vertical profiles  

* ##[tides-scatter.ipynb](http://nbviewer.ipython.org/urls/bitbucket.org/salishsea/analysis/raw/tip/compare_tides/tides-scatter.ipynb)  
    
    This notebook generates tidal comparisons for CMOS.   

* ##[plot_current_ellipses.ipynb](http://nbviewer.ipython.org/urls/bitbucket.org/salishsea/analysis/raw/tip/compare_tides/plot_current_ellipses.ipynb)  
    

##License

These notebooks and files are copyright 2013-2015
by the Salish Sea MEOPAR Project Contributors
and The University of British Columbia.

They are licensed under the Apache License, Version 2.0.
http://www.apache.org/licenses/LICENSE-2.0
Please see the LICENSE file for details of the license.
