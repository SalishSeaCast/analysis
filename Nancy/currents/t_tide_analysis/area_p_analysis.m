function area_p_analysis(filename, outfile, depthfile, t0, ref_time, time_units)

%%% Script to do a tidal analysis of baroclinic pressure using 
%%% dp/dz = -rho*g. That is, MacKinnon ang Gregg 2002
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
clear dept_full

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
        rhosub = calculate_density(squeeze(t(i,j,:,t0:end)), squeeze(s(i,j,:,t0:end)));
        e3t = squeeze(e3t_full(icount,jcount,:));
        tmask = squeeze(tmask_full(icount,jcount,:));
        rhosub = bsxfun(@times, rhosub, tmask);
        rho_int = bsxfun(@times, vertical_integral(rhosub,e3t), tmask);
        rho_int_int = depth_average_mask(rho_int,e3t,tmask);
        rho_int_int_stack = repmat(rho_int_int, Nz,1);
        e3t_mask =  bsxfun(@times, e3t, tmask);
        H = sum(e3t_mask);
        pbc_t = bsxfun(@times,-g*(rho_int + 1/H*rho_int_int_stack),tmask);
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

save([outfile, '_pbc_t_try2',], 'pbc_t_struc')