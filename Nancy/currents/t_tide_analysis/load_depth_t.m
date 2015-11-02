function [dept, e3t, tmask] = load_depth_t()
% Load and return the t vertical grid points, scale factors and mask

filename = '/ocean/nsoontie/MEOPAR/Ariane/mesh_mask.nc';
% Load netcdf
ncid = netcdf.open(filename);
dept = netcdf.getVar(ncid, netcdf.inqVarID(ncid,'gdept'));
dept = dept(:,:,:,1);
e3t = netcdf.getVar(ncid, netcdf.inqVarID(ncid,'e3t'));
e3t = e3t(:,:,:,1);
tmask = netcdf.getVar(ncid, netcdf.inqVarID(ncid,'tmask'));
tmask = double(tmask(:,:,:,1));

netcdf.close(ncid)

end