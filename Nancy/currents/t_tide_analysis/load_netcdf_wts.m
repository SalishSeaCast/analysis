function [w, t, s, ssh, deptht, depthw, time, lons, lats] = load_netcdf_wts(filename)
% Load and return vertical velocity (w), temperature(t), salinity (s) and
% sea surface height (ssh) time series stored in filename
% Sets elements equal to mask_value as NaNs (these are land points)

% Load netcdf
ncid = netcdf.open(filename);
w = netcdf.getVar(ncid, netcdf.inqVarID(ncid,'vovecrtz'));
t = netcdf.getVar(ncid, netcdf.inqVarID(ncid,'votemper'));
s = netcdf.getVar(ncid, netcdf.inqVarID(ncid,'vosaline'));
ssh = netcdf.getVar(ncid, netcdf.inqVarID(ncid,'sossheig'));
deptht = netcdf.getVar(ncid, netcdf.inqVarID(ncid,'deptht'));
depthw = netcdf.getVar(ncid, netcdf.inqVarID(ncid,'depthw'));
time = netcdf.getVar(ncid, netcdf.inqVarID(ncid,'time_counter'));

lats = netcdf.getVar(ncid, netcdf.inqVarID(ncid,'nav_lat'));
lons = netcdf.getVar(ncid, netcdf.inqVarID(ncid,'nav_lon'));

netcdf.close(ncid)

end