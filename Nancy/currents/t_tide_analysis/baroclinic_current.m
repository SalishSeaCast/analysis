function [ ubc ] = baroclinic_current( u, depth )
%BAROCLINIC_CURRENT calculatet he baroclinic current over the full water
%column
% u should be shape (depth, time)
%   ubc = u - depthaverage(u)

uavg = depth_average(u, depth);
ubc = zeros(size(u));
for k =1:length(ubc(:,1))
    ubc(k,:) = u(k,:) - uavg;
end

