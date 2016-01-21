function area_w_N2_analysis(filename, outfile, depthfile, t0, ref_time, time_units)

%%% Script to do a BAROCLINIC tidal analysis with t_tide
%%% Full region
%%% depthfile is the mesh_mask file
%%% t0 is initial time index
%%% ref_time is the reference time (datevec)
%%% time_units is a string 's' or 'h' indicating if the time in the files
%%% is measure in seconds or hours.

% load data
[w, t, s, ssh, deptht, depthw, time, lons, lats] = load_netcdf_wts(filename);
[istart, jstart] = find_starting_index(lons , lats); %index for lons/lats(2,2)
icount=istart;
jcount=jstart;
% load dept, scale factors and tmask
[dept_full, e3t_full, tmask_full] = load_depth_t(depthfile);
[depw_full, e3w_full, tmask_full] = load_depth_w(depthfile);

%prepare time
mtimes = time_to_mtime(time, ref_time, time_units); 
start = mtimes(t0);

%initialize strucuure for saving data array
area = squeeze(size(w(:,:,1,1)));
Nx=area(1)-1; Ny=area(2)-1;
Nz = length(w(1,1,:,1)); %one less for Nz because exclude surface
params = elev_parameters;
%exclude first point in x/y to match with u/v analysis

%mask value - no need to tidal analysis because land
mask_value=0; 

rho0 = 1035; %kg/m^3 - NEMO reference density

%Loop through everything
tide_count=0;
for i=1:Nx
    for j=1:Ny
        wsub = squeeze(w(i+1,j+1,:,t0:end));
        winterp = interp1(depthw, wsub, deptht,'pchip','extrap');
        rhosub = calculate_density(squeeze(t(i+1,j+1,:,t0:end)), squeeze(s(i+1,j+1,:,t0:end)));
        sshsub =squeeze(ssh(i+1,j+1,t0:end));
        e3w = squeeze(e3w_full(icount,jcount,:));
        e3t = squeeze(e3t_full(icount,jcount,:));
        tmask = squeeze(tmask_full(icount,jcount,:));
        % calculate N2
        n2sub = calculate_n2(rhosub, e3w);
        n2sub = bsxfun(@times, n2sub, tmask);
        n2interp=interp1(depthw, n2sub, deptht,'pchip','extrap');
        pbc_t = -rho0*vertical_integral(winterp.*n2interp,e3t);
        if ~all(tmask==0)
           % do t_tide analysis
           lat=lats(i+1,j+1);
           % ssh
           [tidestruc,~] = t_tide(sshsub,'start time',start,'latitude',lat,'output','none');
           if tide_count==0
               sshstruc = initialize_struc(tidestruc,[Nx,Ny],lats,lons);
           end
           const = tidestruc.name;
           for n =1:length(const)
               c = const(n,:);
               cword=const2word(c);
               ind = strmatch(c,tidestruc.name,'exact');
               for p =1:length(params)
                   param = params(p, :);
                   sshstruc.(cword).(param)(i,j) = tidestruc.tidecon(ind,p);
               end
           end
           %%% Next is w and pbc_t/rho0 which both depend on z
           for k=1:Nz;
              %n2 first
              if ~all(pbc_t(k,:)==mask_value)
                  [tidestruc,~] = t_tide(squeeze(pbc_t(k,:)),'start time',start,'latitude',lat,'output','none');
                  if tide_count==0
                      pbc_t_struc = initialize_struc(tidestruc,[Nx,Ny,Nz],lats,lons);
                  end
                  for n =1:length(const)
                      c = const(n,:);
                      cword=const2word(c);
                      ind = strmatch(c,tidestruc.name,'exact');
                      for p =1:length(params)
                          param = params(p, :);
                          pbc_t_struc.(cword).(param)(i,j,k) = tidestruc.tidecon(ind,p);
                      end
                  end
              end
              %next w
              if ~all(winterp(k,:)==mask_value)
                  [tidestruc,~] = t_tide(squeeze(winterp(k,:)),'start time',start,'latitude',lat,'output','none');
                  if tide_count==0
                      wstruc = initialize_struc(tidestruc,[Nx,Ny,Nz],lats,lons);
                  end
                  for n =1:length(const)
                      c = const(n,:);
                      cword=const2word(c);
                      ind = strmatch(c,tidestruc.name,'exact');
                      for p =1:length(params)
                          param = params(p, :);
                          wstruc.(cword).(param)(i,j,k) = tidestruc.tidecon(ind,p);
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
wstruc.('deptht') = deptht;
pbc_t_struc.('deptht') = deptht;

%save

save([outfile, '_ssh'], 'sshstruc')
save([outfile, '_w',], 'wstruc')
save([outfile, '_pbc_t',], 'pbc_t_struc')