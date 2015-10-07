function [u, v, depth, time, lons, lats] = load_netcdf(filename)
% Load and return velocity time series (u/v) stored in filename
% Sets elements of u/v equale to mask_value as NaNs (these are land points)

% Load netcdf
ncid = netcdf.open(filename);
u = netcdf.getVar(ncid, netcdf.inqVarID(ncid,'vozocrtx'));
v = netcdf.getVar(ncid, netcdf.inqVarID(ncid,'vomecrty'));
depth = netcdf.getVar(ncid, netcdf.inqVarID(ncid,'deptht'));
time = netcdf.getVar(ncid, netcdf.inqVarID(ncid,'time_counter'));

lats = netcdf.getVar(ncid, netcdf.inqVarID(ncid,'nav_lat'));
lons = netcdf.getVar(ncid, netcdf.inqVarID(ncid,'nav_lon'));

netcdf.close(ncid)

end