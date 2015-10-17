%%% Script to do a tidal analysis with t_tide
%%% Full depth profile and depth averaged values at VENUS Central or East

filename = '/ocean/nsoontie/MEOPAR/TidalEllipseData/ModelTimeSeries/Central_currents_20141126_20150426.nc';
%depth index for tidal analysis
depav = 1; %depth average
dlevel = 1; % surface
trun = 1; %truncate water column
d1 = 35; d2 = 290; %depth range
output_file = '/ocean/nsoontie/MEOPAR/TidalEllipseData/Nodes/Central_20141126_20150426';

% load data
[u, v, depth, time, lons, lats] = load_netcdf(filename);
lat=lats(end,end);
params = ellipse_parameters;

%prepare time
ref_time = [2014, 09, 10];
mtimes = time_to_mtime(time, ref_time); 
start = mtimes(1);

% prepare velocities for tidal analysis
% That is, mask, unstagger and rotate, truncate
[urot, vrot] = prepare_velocities(u, v);
Nz = length(urot(:,1));

%Tidal analysis over each model level first
tide_count=0;
for k =1:Nz
    us = squeeze(urot(k,:));
    vs = squeeze(vrot(k,:));
    % prepare velocities for tidal analysis
    % That is, mask, unstagger and rotate
    complex_vel = us + 1i*vs;
    %Setting the values. Simplify somehow...
    if ~all(isnan(us))
        [tidestruc,~] = t_tide(complex_vel,'start time',start,'latitude',lat,'output','none');
        if tide_count==0
            const = tidestruc.name;
        end
        for n =1:length(const)
            c = const(n,:);
            if ismember(c(1),'0123456789')
                cword=['x', strtrim(c)];
            else
                cword = strtrim(c);
            end
            ind = strmatch(c,tidestruc.name,'exact');
            if tide_count ==0
                datastruc.('fullprofile').(cword).('freq') = tidestruc.freq(ind);
            end
            for p =1:length(params)
                param = params(p, :);
                if tide_count ==0
                    datastruc.('fullprofile').(cword).(params(p,:)) = NaN(Nz,1);
                end
                datastruc.('fullprofile').(cword).(param)(k) = tidestruc.tidecon(ind,p);
            end
        end
        tide_count=tide_count+1;
    end
end
datastruc.('fullprofile').('drange') = depth;

%Depth averaging
[uavg, vavg, davg] = subset_depth(urot, vrot, depth, depav, trun, d1, d2, dlevel);
%do depth averaged t_tide analysis
complex_vel = uavg + 1i*vavg;
[tidestruc,~] = t_tide(complex_vel,'start time',start,'latitude',lat, 'output','none');
for n =1:length(const)
    c = const(n,:);
    if ismember(c(1),'0123456789')
        cword=['x', strtrim(c)];
    else
        cword = strtrim(c);
    end
    ind = strmatch(c,tidestruc.name,'exact');
    datastruc.('depav').(cword).('freq') = tidestruc.freq(ind);
    for p =1:length(params)
        param = params(p, :);
        datastruc.('depav').(cword).(param) = tidestruc.tidecon(ind,p);
    end
end       
datastruc.('depav').('drange') = davg;

%Saving
save(output_file, 'datastruc')