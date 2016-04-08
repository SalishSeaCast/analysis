function area_wN2_analysis_kunze(filename, outfile, depthfile, t0, ref_time, time_units)

%%% Script to do a tidal analysis of baroclinic pressure using 
%%% Kunze 2002
%%% Full region
%%% depthfile is the mesh_mask file
%%% t0 is initial time index
%%% ref_time is the reference time (datevec)
%%% time_units is a string 's' or 'h' indicating if the time in the files
%%% is measure in seconds or hours.

g = 9.80665; % acceleration due to gravity (m/s^2)
% load data
[w, t, s, ssh, deptht, depthw, time, lons, lats] = load_netcdf_wts(filename);
[istart, jstart] = find_starting_index(lons(1,1) , lats(1,1));
% T grid can start on lons(1,1) and lats(1,1)
icount=istart;
jcount=jstart;
% load dept, scale factors and tmask
[dept_full, e3t_full, tmask_full] = load_depth_t(depthfile);
[depw_full, e3w_full, tmask_full] = load_depth_w(depthfile);
clear dept_full depw_full;

%prepare time
mtimes = time_to_mtime(time, ref_time, time_units); 
start = mtimes(t0);

%initialize strucuure for saving data array
area = squeeze(size(w(:,:,1,1)));
Nx=area(1); Ny=area(2);
Nz = length(w(1,1,:,1));
params = elev_parameters;

%mask value - no need to tidal analysis because land
mask_value=0; 

rho0 = 1035; %kg/m^3 - NEMO reference density

%Loop through everything
tide_count=0;
for i=1:Nx
    for j=1:Ny
        wsub = squeeze(w(i,j,:,t0:end));
        winterp = interp1(depthw, wsub, deptht,'pchip','extrap');
        rhosub = calculate_density(squeeze(t(i,j,:,t0:end)), squeeze(s(i,j,:,t0:end)));
        e3w = squeeze(e3w_full(icount,jcount,:));
        e3t = squeeze(e3t_full(icount,jcount,:));
        tmask = squeeze(tmask_full(icount,jcount,:));
        % calculate N2
        n2sub = calculate_n2(rhosub, e3w);
        n2sub = bsxfun(@times, n2sub, tmask);
        n2interp=interp1(depthw, n2sub, deptht,'pchip','extrap');
        %integrate n2*w
        n2_w_int = bsxfun(@times, vertical_integral(winterp.*n2interp,e3t), tmask);
        %depth average of integral(n2*w)
        n2_w_int_int = depth_average_mask(n2_w_int,e3t,tmask);
        n2_w_int_int_stack = repmat(n2_w_int_int, Nz,1);
        e3t_mask =  bsxfun(@times, e3t, tmask);
        H = sum(e3t_mask);
        pbc_t = bsxfun(@times,-rho0*(n2_w_int + 1/H*n2_w_int_int_stack),tmask);
        if ~all(tmask==0)
           % do t_tide analysis
           lat=lats(i,j);
           for k=1:Nz;
              %n2 first
              if ~all(pbc_t(k,:)==mask_value)
                  [tidestruc,~] = t_tide(squeeze(pbc_t(k,:)),'start time',start,'latitude',lat,'output','none');
                  if tide_count==0
                      pbc_t_struc = initialize_struc(tidestruc,[Nx,Ny,Nz],lats,lons);
                  end
                  const = tidestruc.name;
                  for n =1:length(const)
                      c = const(n,:);
                      cword=const2word(c);
                      ind = strmatch(c,tidestruc.name,'exact');
                      for p =1:length(params)
                          param = params(p, :);
                          pbc_t_struc.(cword).(param)(i,j,k) = tidestruc.tidecon(ind,p);
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

pbc_t_struc.('deptht') = deptht;

%save

save([outfile, '_pbc_t_try3',], 'pbc_t_struc')