fname ='/results/SalishSea/nowcast/17jun15/SalishSea_1h_20150617_20150617_grid_T.nc'
ncid = netcdf.open(fname);
x= netcdf.getVar(ncid, netcdf.inqVarID(ncid,'nav_lon'));
y= netcdf.getVar(ncid, netcdf.inqVarID(ncid,'nav_lat'));
dep= netcdf.getVar(ncid, netcdf.inqVarID(ncid,'deptht'));
sal= netcdf.getVar(ncid, netcdf.inqVarID(ncid,'vosaline'));
salt=sal(:,:,:,11);
x3d=x;
for i=1:39
x3d=cat(3,x3d,x);
end
y3d=y;
for i=1:39
y3d=cat(3,y3d,y);
end
dep2d=dep;
for i=1:397
dep2d=cat(2,dep2d,dep);
end
dep3d=dep2d;
for i=1:897
dep3d=cat(3,dep3d,dep2d);
end
dep3dT=permute(dep3d,[2,3,1]);

xsub=x3d(200:350,300:400,:);
ysub=y3d(200:350,300:400,:);
zsub=dep3dT(200:350,300:400,:);
sal_sub=salt(200:350,300:400,:);
xmax=max(xsub(:));
xmin=min(xsub(:));
ymin=min(ysub(:));
ymax=max(ysub(:));
zmin=min(zsub(:));
zmax=max(zsub(:));
[xg,yg,zg]=meshgrid(xmin:0.01:xmax, ymin:0.01:ymax, zmin:1:zmax);
sali = griddata(double(xsub),double(ysub),double(zsub),double(sal_sub),double(xg),double(yg),double(zg));
isosurface(xg,yg,zg,sali,25)
lighting gouraud
set(gca,'ZDir','Reverse')