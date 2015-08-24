function [tidestruc,lat,msl]=read_CHS_harmonics(tidefile)
%reads a tidefile and constructs a tidestruc object for use in ttide

fid = fopen(tidefile,'r');
tmp = textscan(fid,'%s','Delimiter','\n');

%load data
result = regexp(tmp{1},' ','split');

%get station latitude
l1 = result{2}(5); l2 = result{2}(6);
lat=str2num(l1{1})+str2num(l2{1})/60;

%get msl
tide=strsplit(tmp{1}{25});
a=tide(3); msl=str2num(a{1});

%building tide struc - first read data line by line
%Assuming all tide files begin constituents on line 25.
%numer of constituents (n) is #rows in file - 25

%allocate arrays
nrows = numel(textread(tidefile,'%1c%*[^\n]')) ;
n=nrows - 25;
names=cell(n,1);
freqs = zeros(n,1);
phas = zeros(n,1);
phas_err = ones(n,1);
amps= zeros(n,1);
amps_err = ones(n,1);

c=1;
for i=26:nrows
    tide=strsplit(tmp{1}{i});
    names(c)=tide(1);
    period=tide(2);
    freqs(c)=1/str2num(period{1});
    a=tide(3); amps(c)=str2num(a{1});
    p=tide(4); phas(c)=str2num(p{1});
    c=c+1;
end

%builing the tidet struc objuect
tidecon=[amps'; amps_err'; phas'; phas_err']';
tidestruc.name=char(cellstr(names));
tidestruc.tidecon=tidecon;
tidestruc.freq=freqs;
