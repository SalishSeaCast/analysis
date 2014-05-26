function [pred_all,pred_8,wlev,tim] = get_ttide_8(csvfilename,location)
%returns the tidal predictions if only 8 constituents were used.
%the 8 constituents are: M2,K1,O1,P1,Q1,N2,S2,K2
%csvfilename contains DFO produced water level observations.
%pred_all is the t_tide prediction with all constituents
%pred_8 is the t_tide prediction with only 8 constituents
%saves a spreadsheet with tim, pred_all, pred_8

% NKS May 2014

%Read in the measured water level data the location
fid = fopen(csvfilename);
meas = textscan(fid,'%f/%f/%f %f:%f,%f,','HeaderLines',8);
lat = csvread(csvfilename,2,1,[2,1,2,1]);
fclose(fid);

%Calculate dates from columns of data
time = datenum(meas{1},meas{2},meas{3},meas{4},meas{5},0);
wlev = meas{6};

%Start date of measured water level record
start_date = time(1);
end_date = time(end);

%measured data may not have entry for every date in the range
tim = start_date:1/24:end_date;
newmeas = zeros(length(tim),2);

%counter in measured time
counter = 1;
%tt is counter in created time
for tt = 1:length(tim)
    if time(counter) == tim(tt)
        newmeas(tt,1:2) = [time(counter), wlev(counter)];
        counter = counter + 1;
    else
        newmeas(tt,1:2) = [tim(tt), NaN];
    end
end

wlev = newmeas(:,2);

clear time newmeas meas

%Use t_tide to determine harmonic constituents. Needs to be at least one
%year time series (366 days)
[tidestruc,~] = t_tide(wlev,'start time',start_date(1,1),'latitude',lat);
    
%Get predicted tide for same period
pred = t_predic(tim,tidestruc,'latitude',lat);


%Create a new struct object with onle 8 consts.
names_8=['M2'; 'K1'; 'O1';'P1';'Q1';'N2';'S2';'K2'];
freqs_8 = zeros(8,1);
pha_8 = zeros(8,1);
pha_err8 = zeros(8,1);
amp_8 = zeros(8,1);
amp_err8 = zeros(8,1);
 for i=1:8
n=names_8(i,:);
ind = strmatch(n,tidestruc.name,'exact');
freqs_8(i) = tidestruc.freq(ind);
amp_8(i) = tidestruc.tidecon(ind,1);
amp_err8(i) = tidestruc.tidecon(ind,2);
pha_8(i) = tidestruc.tidecon(ind,3);
pha_err8(i) = tidestruc.tidecon(ind,4);
 end
 
tidecon_8=[amp_8'; amp_err8'; pha_8'; pha_err8']';

tidestruc_8.name=names_8;
tidestruc_8.tidecon=tidecon_8;
tidestruc_8.freq=freqs_8;

pred_8 = t_predic(tim,tidestruc_8,'latitude',lat);

%Plot it
figure
plot(tim,pred_8,'b',tim,pred,'m')
legend('predictions 8 const.', 'predictions all','Location','EastOutside')
xlabel('time')
ylabel('water level elevation (m CD)')
datetick('x','mm/yyyy')

%second save predictions
M = datestr(tim);
n = length(tim);
filename = [location  '_t_tide_compare8_' datestr(start_date) '_' datestr(end_date) '.csv'];
fid = fopen(filename, 'w');
%add some headers
fprintf(fid, 'Time_Local \t pred_8 \t pred_all \n');
for row=1:n
    fprintf(fid, '%s \t', M(row,:));
    fprintf(fid,' %f\t', pred_8(row));
    fprintf(fid,' %f\n', pred(row));
end
fclose(fid);
