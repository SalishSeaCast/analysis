function [depw, e3w, tmask] = load_depth_w(depthfile)
% Load and return the w vertical grid points, scale factors and mask

% Load netcdf
ncid = netcdf.open(depthfile);
depw = netcdf.getVar(ncid, netcdf.inqVarID(ncid,'gdepw'));
depw = depw(:,:,:,1);
e3w = netcdf.getVar(ncid, netcdf.inqVarID(ncid,'e3w'));
e3w = e3w(:,:,:,1);
tmask = netcdf.getVar(ncid, netcdf.inqVarID(ncid,'tmask'));
tmask = double(tmask(:,:,:,1));

netcdf.close(ncid)

end