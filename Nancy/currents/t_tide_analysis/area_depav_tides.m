function area_depav_tides(filename, outfile, t0)

%%% Script to do a tidal analysis with t_tide
%%% full region, depth averaged. Note - does not account for boundary
%%% layer effects
%%% t0 is initial time index


% load data
[u, v, depth, time, lons, lats] = load_netcdf(filename);
[istart, jstart] = find_starting_index(lons , lats);
% load dept, scale factors and tmask
[dept_full, e3t_full, tmask_full] = load_depth_t();

%prepare time
ref_time = [2014, 09, 10];
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
        
        % do t_tide analysis
        lat=lats(i+1,j+1);

        if ~all(isnan(urot))
            e3t = squeeze(e3t_full(istart,jstart,:));
            tmask = squeeze(tmask_full(istart,jstart,:));
            uavg = depth_average_masked(squeeze(urot), e3t, tmask);
            vavg = depth_average_masked(squeeze(vrot), e3t, tmask);
            complex_vel = uavg + 1i*vavg;
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
        jstart=jstart+1;
    end
    istart=istart+1;
end
datastruc.('depth') = depth;

%save
save(outfile, 'datastruc')

