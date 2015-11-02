function [ ubc ] = baroclinic_current_masked( u, e3t, tmask )
%BAROCLINIC_CURRENT_MASKED calculatet he baroclinic current over the
%full water column using scale factors and tmask
% u should be shape (depth, time)
% e3t, tmask are shape (depth)
%   ubc = u - depthaverage(u)

uavg = depth_average_mask(u, e3t, tmask);
ubc = zeros(size(u));
for k =1:length(ubc(:,1))
    ubc(k,:) = u(k,:) - uavg;
end



end

