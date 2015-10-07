function [ mtime ] = time_to_mtime( times, ref_time )
%TIME_TO_MTIME convert time array in hours to matlab datenum
    %times is the array of times in hours measure relative to ref_time
    %ref_time is a vector with [yeay, month, day]
    
    ref = datenum(ref_time);
    
    mtime = ref +times/24;

end

