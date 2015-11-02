function [i ,j] = find_starting_index(lons , lats)
%FIND_STARTING_INDEX - look up the starting index of this subdomain
%Assumes start of subdomin is sctually at lats(2,2) and lons(2,2)
%This is because of the way the unstaggering works and setting up my 
%subdomains

% load the model grid
filename = '/data/nsoontie/MEOPAR/NEMO-forcing/grid/bathy_meter_SalishSea2.nc';
ncid = netcdf.open(filename);
lat_grid = netcdf.getVar(ncid, netcdf.inqVarID(ncid,'nav_lat'));
lon_grid = netcdf.getVar(ncid, netcdf.inqVarID(ncid,'nav_lon'));
netcdf.close(ncid)

lat = lats(2,2);
lon = lons(2,2);

[i,j] = find(lon_grid==lon & lat_grid==lat);
