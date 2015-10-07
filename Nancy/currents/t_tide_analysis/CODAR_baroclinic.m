%%% Script to do a BAROCLINIC tidal analysis with t_tide

filename = '/ocean/nsoontie/MEOPAR/TidalEllipseData/ModelTimeSeries/CODAR_currents_20141126_20150426.nc';
%depth index for tidal analysis
depav = 0; %depth average
dlevel = 1; % surface
trun = 0; %truncate water column
d1 = 0; d2 = 0; %depth range
outfile = '/ocean/nsoontie/MEOPAR/TidalEllipseData/CODAR/CODAR_region_baroclinic_20141126_20150426';

% load data
[u, v, depth, time, lons, lats] = load_netcdf(filename);

%prepare time
ref_time = [2014, 09, 10];
mtimes = time_to_mtime(time, ref_time); 
start = mtimes(1);

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
        urot = u(i:i+1,j:j+1,:,:);
        vrot = v(i:i+1,j:j+1,:,:);
        % prepare velocities for tidal analysis
        % That is, mask, unstagger and rotate
        [urot, vrot] = prepare_velocities(urot, vrot);
        ubc = baroclinic_current(urot, depth);
        vbc = baroclinic_current(vrot, depth);
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
end
datastruc.('depth') = depth;

%save
save(outfile, 'datastruc')

