function [ var_avg ] = depth_average_mask(var, e3t, tmask)
%DEPTH_AVERAGE_MASK Perform depth average of an array var
% e3t is the array of scale factors (grid zpscing)
% tmask is an array of the model mask
% e3t and tmask can have only depth
% var has shape depth, time 
  
  
  var_one = squeeze(var(:,1));
  e3t_sub = e3t(~isnan(var_one));
  tmask_sub = tmask(~isnan(var_one));
  if all(isnan(var_one))
      var_avg =NaN(size(var(1,:)));
  else
      var(isnan(var)) = 0;
      integral = 0;
      for k=1:size(e3t_sub)
          integral = integral + var(k,:)*e3t_sub(k)*tmask_sub(k);
      end
      total_depth = sum(e3t_sub.*tmask_sub);
      if total_depth==0
          var_avg=NaN(size(var(1,:)));
      else
          var_avg = integral/total_depth;
      end
  end
end

