function [ var_avg ] = depth_average(var, depths)
%DEPTH_AVERAGE Perform depth average of an array var
%    var should be masked to NaNs for land points
%    the index of the first NaN encountered will determine the depth of 
%    the water column
%    depth is the array of associated detphs
%    var can be of shape (depth, time)

  var_one = squeeze(var(:,1));
  if all(isnan(var_one))
      var_avg = NaN;
  else
      var(isnan(var)) = 0;
      
      var_avg = trapz(squeeze(depths), var, 1);
      dep_sub = depths(~isnan(var_one));
      max_depth = max(dep_sub);
      surf_depth = min(dep_sub);
      var_avg = var_avg/(max_depth-surf_depth);
  end
  

end

