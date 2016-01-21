function [ field_interp ] = vertical_integral( field, e3t )
%Vertically integrate field with grid spacings e3t.
%   Assumes field is depth by time

field_interp = zeros(size(field));

fdz = bsxfun(@times, field, e3t);
field_interp(1:end,:) = cumsum(fdz(1:end,:));
