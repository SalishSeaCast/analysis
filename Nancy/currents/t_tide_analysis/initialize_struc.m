function datastruc = initialize_struc(tidestruc,size,lats,lons)
datastruc = struct('lats',lats, 'lons', lons);
params = elev_parameters;
const = tidestruc.name;
for n =1:length(const)
  c = const(n,:);
  if ismember(c(1),'0123456789')
      cword=['x', strtrim(c)];
  else
      cword = strtrim(c);
  end
  ind = strmatch(c,tidestruc.name,'exact');
  datastruc.(cword).('freq') = tidestruc.freq(ind);
  for p =1:length(params)
     param = params(p, :);
     datastruc.(cword).(param) = NaN(size);
  end
end