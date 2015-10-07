function [ uout, vout  ] = prepare_velocities( uin, vin )
%Masks, unstaggers, and rotates NEMO velocities vectors
%   Masking - zero values set to NaNs because those are land points
%   Unstaggering - u and v set to a T grid point
%   rotate - u/v rortated to east/west and north/south

%Masking
mask_value = 0;
uin(uin==mask_value)=NaN;
vin(vin==mask_value)=NaN;

%Unstaggering
uout = unstagger(uin, 'U');
uout = squeeze(uout(1,end,:,:));
vout = unstagger(vin, 'V');
vout = squeeze(vout(end,1,:,:));

%Rotating
theta = 29;
[uout, vout] = rotate(uout, vout, theta);
end

