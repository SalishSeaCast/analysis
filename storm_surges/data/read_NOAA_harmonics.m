function [tidestruc,lat,msl]=read_NOAA_harmonics(tidefile)
%reads a tidefile and constructs a tidestruc object for use in ttide

fid = fopen(tidefile,'r');
tmp = textscan(fid,'%s','Delimiter','\n');

%load data
result = regexp(tmp{1},',','split');

%get msl
msl=str2num(result{1}{2});

%get station latitude
lat=str2num(result{2}{2});


%building tide struc - first read data line by line
%Assuming all tide files begin constituents on line 25.
%numer of constituents (n) is #rows in file - 25

%allocate arrays
nrows = numel(textread(tidefile,'%1c%*[^\n]')) ;
n=nrows - 4;
names=cell(n,1);
freqs = zeros(n,1);
phas = zeros(n,1);
phas_err = ones(n,1);
amps= zeros(n,1);
amps_err = ones(n,1);

c=1;
for i=5:nrows
    tide=result{i};
    name = tide{2};
    if strmatch(name,'RHO','exact')
        name='RHO1';
    elseif strmatch(name,'LAM2','exact') 
        name='LDA2';
    elseif strmatch(name,'2MK3','exact') 
        name='MO3 ';
    elseif strmatch(name,'M1  ','exact') 
        name='NO1 ';
    end
    names(c)=cellstr(name);
    amps(c)=str2num(tide{3});
    phas(c)=str2num(tide{4});
    speed=tide{5};
    freqs(c)=pi*str2num(speed)/180/(2*pi);
    c=c+1;
end

%builing the tidet struc objuect
tidecon=[amps'; amps_err'; phas'; phas_err']';
tidestruc.name=char(cellstr(names));
tidestruc.tidecon=tidecon;
tidestruc.freq=freqs;