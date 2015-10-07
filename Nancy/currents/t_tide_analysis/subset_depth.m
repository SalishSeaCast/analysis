function [ uout, vout, dout ] = subset_depth( uin, vin, din, depav, trun, d1, d2, dlevel )
%SUBSET_DEPTH Subsample the velocities over depth in prepration for tidal
%analysis. Options for depth averaging, truncating a depth range or
%sampling a single model level
%   uin, vin, din - the u/v velocities and depth arrays for subsampling
%   depav = 1  for depth averaged velocities, 0 for not
%   trun = 1 for truncate depths/velocties in a certain depth range given 
%   by d1 < dind < d2. d1, d2 in meters. 0 for no truncation
%   dlevel - in the case of no truncation or depth levels, a single model
%   level can be chosen with delvel. 1<=delvel <=40.
%
%   returns uout, vout, dout - the subsetted and possibily depth averaged
%   velocities fields.
% Examples 
% depav = 1, trun = 1, d1=10, d2 = 100, dlevel=1 will depth average over 
% 10m-100m using the model cells closest to 10m and 100m
% 
% depav=0, trun=0, d1=10, d2=100, dlevel = 1 will return the model surface
% level. 
%
% depav = 1, trun = 0, d1=10, d2 = 100, dlevel =1 will depth average over
% the whole water column.

% depav = 0, trun = 1, d1=10, d2 = 100, dlevel =1 will return model
% velocities at all levels bewteen 10m and 100m.

utmp = uin;
vtmp = vin;
dtmp = din;
if trun
    utmp = uin((din >d1) & (din <d2),:);
    vtmp=  vin((din >d1) & (din <d2),:);
    dtmp = din((din >d1) & (din <d2),:);
end
if depav
    utmp = depth_average(utmp, dtmp);
    vtmp = depth_average(vtmp, dtmp);
else
    utmp = squeeze(utmp(dlevel,:));
    vtmp = squeeze(vtmp(dlevel,:));
    dtmp = din(dlevel);
end
uout=utmp;
vout=vtmp;
dout=dtmp;
end

