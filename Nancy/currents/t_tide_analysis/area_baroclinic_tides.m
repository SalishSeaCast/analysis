function area_baroclinic_tides(filename, outfile, t0, ref_time)

%%% Script to do a BAROCLINIC tidal analysis with t_tide
%%% Full region
%%% t0 is initial time index

% load data
[u, v, depth, time, lons, lats] = load_netcdf(filename);
[istart, jstart] = find_starting_index(lons , lats);
icount=istart;
jcount=jstart;
% load dept, scale factors and tmask
[dept_full, e3t_full, tmask_full] = load_depth_t();

%prepare time
mtimes = time_to_mtime(time, ref_time); 
start = mtimes(t0);

%initialize strucuure for saving data array
area = squeeze(size(u(:,:,1,1)));
Nx=area(1); Ny=area(2);
Nz = length(u(1,1,:,1));
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
        e3t = squeeze(e3t_full(icount,jcount,:));
        tmask = squeeze(tmask_full(icount,jcount,:));
        if ~all(tmask==0)
           ubc = baroclinic_current_masked(urot, e3t, tmask);
           vbc = baroclinic_current_masked(vrot, e3t, tmask);
           % do t_tide analysis
           lat=lats(i+1,j+1);
           for k=1:Nz;
              complex_vel = squeeze(ubc(k,:)) + 1i*squeeze(vbc(k,:));
              %Setting the values. Simplify somehow...
              if ~all(isnan(ubc(k,:)))
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
                               datastruc.(cword).(params(p,:)) = NaN(Nx-1, Ny-1, Nz);
                           end
                           datastruc.(cword).(param)(i,j,k) = tidestruc.tidecon(ind,p);
                       end
                   end
                   tide_count=tide_count+1;
              end
            end
        end
        jcount=jcount+1;
    end
    jcount=jstart;
    icount=icount+1;
end
datastruc.('depth') = depth;

%save
save(outfile, 'datastruc')

