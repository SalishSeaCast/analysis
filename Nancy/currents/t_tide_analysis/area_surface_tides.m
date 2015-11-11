function area_surface_tides(filename, outfile,t0, ref_time)

%%% Script to do a tidal analysis with t_tide
%%% A region at the surface
%%% t0 is initial time index

%depth index for tidal analysis
depav = 0; %depth average
dlevel = 1; % surface
trun = 0; %truncate water column
d1 = 0; d2 = 0; %depth range


% load data
[u, v, depth, time, lons, lats] = load_netcdf(filename);

%prepare time
mtimes = time_to_mtime(time, ref_time); 
start = mtimes(t0);

%initialize strucuure for saving data array
area = squeeze(size(u(:,:,1,1)));
Nx=area(1); Ny=area(2);
params = ellipse_parameters;
datastruc = struct('lats',lats(2:end,2:end), 'lons', lons(2:end,2:end));
   

%Loop through everything
tide_count=0;
for i=1:Nx-1
    for j=1:Ny-1
        urot = u(i:i+1,j:j+1,:,t0:end);
        vrot = v(i:i+1,j:j+1,:,t0:end);
        % prepare velocities for tidal analysis
        % That is, mask, unstagger and rotate
        [urot, vrot] = prepare_velocities(urot, vrot);
        [urot, vrot, depth] = subset_depth(urot, vrot, depth, depav, trun, d1, d2, dlevel);
        % to t_tide analysis
        lat=lats(i+1,j+1);
        complex_vel = urot + 1i*vrot;

        %Setting the values. Simplify somehow...
        if ~all(isnan(urot))
            [tidestruc,~] = t_tide(complex_vel,'start time',start,'latitude',lat,'output','none');
            if tide_count==0
                const = tidestruc.name;
            end
            for k =1:length(const)
                c = const(k,:);
                if ismember(c(1),'0123456789')
                    cword=['x', strtrim(c)];
                else
                    cword = strtrim(c);
                end
                ind = strmatch(c,tidestruc.name,'exact');
                if tide_count ==0
                    datastruc.(cword).('freq') = tidestruc.freq(ind);
                end
                for p =1:length(params)
                    param = params(p, :);
                    if tide_count ==0
                        datastruc.(cword).(params(p,:)) = NaN(Nx-1, Ny-1);
                    end
                    datastruc.(cword).(param)(i,j) = tidestruc.tidecon(ind,p);
                end
            end
            tide_count=tide_count+1;
        end
    end
end


%save
save(outfile, 'datastruc')

