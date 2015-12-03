function [dept, e3t, tmask] = load_depth_t(depthfile)
% Load and return the t vertical grid points, scale factors and mask

% Load netcdf
ncid = netcdf.open(depthfile);
dept = netcdf.getVar(ncid, netcdf.inqVarID(ncid,'gdept'));
dept = dept(:,:,:,1);
e3t = netcdf.getVar(ncid, netcdf.inqVarID(ncid,'e3t'));
e3t = e3t(:,:,:,1);
tmask = netcdf.getVar(ncid, netcdf.inqVarID(ncid,'tmask'));
tmask = double(tmask(:,:,:,1));

netcdf.close(ncid)

end