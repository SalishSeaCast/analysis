function cword = const2word(c)
%Convert a constituent to a string. Add x if constituents starts with num
if ismember(c(1),'0123456789')
   cword=['x', strtrim(c)];
else
   cword = strtrim(c);
end