cd /ocean/rich/home/metro/venus_adcp/matlab/
load('ADCPcentral.mat');

%Set the day we want to obseve the currents
to=datenum('14-May-2015');
tf=datenum('15-May-2015');

%Find the indices associated with these dates
ind=mtime > to & mtime < tf;

udate=utrue(:,ind);
vdate=vtrue(:,ind);

times=mtime(ind);
figure(1)
contourf(times,chartdepth,udate,[-30,-30:4:30])
set(gca,'ydir','reverse')
cbar = colorbar;
ylabel(cbar, '[cm/s]', 'FontName','Arial','FontSize',15)
axis('tight')
datetick('x')
xlabel('Time', 'FontName','Arial','FontSize',15)
ylabel('Depth (m)', 'FontName','Arial','FontSize',15)
title('E/W Current Profile (ADCP Obs) - May 14th 2015', 'FontName','Arial','FontSize',18)


figure(2)

contourf(times,chartdepth,vdate,[-40,-40:6:40])
cbar = colorbar;
set(gca,'ydir','reverse')
ylabel(cbar, '[cm/s]', 'FontName','Arial','FontSize',15)
axis('tight')
datetick('x')
xlabel('Time', 'FontName','Arial','FontSize',15)
ylabel('Depth (m)', 'FontName','Arial','FontSize',15)
title('N/S Current Profile (ADCP Obs) - May 14th 2015', 'FontName','Arial','FontSize',18)