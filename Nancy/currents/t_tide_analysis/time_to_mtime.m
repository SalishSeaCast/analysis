function [ mtime ] = time_to_mtime( times, ref_time, time_units )
%TIME_TO_MTIME convert time array in hours to matlab datenum
    %times is the array of times in hours measure relative to ref_time
    %ref_time is a vector with [yeay, month, day]
%%% time_uinits is a string 's' or 'h' indicating if the time in the files
%%% is measure in seconds or hours.
    
    ref = datenum(ref_time);
    
    if time_units == 's'
        factor = 1/24/3600;
    elseif time_units == 'h'
        factor = 1/24;
    end
    mtime = ref +times*factor;

end

