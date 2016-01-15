function n2 = calculate_n2(rho, e3w)
% Calculate the squared buoyancy frequency from desity rho and 
% w grid spacings e3w.
% assumes rho and e3w are shape (depth, time)

g = 9.80665; % acceleration due to gravity (m/s^2)
rho0 = 1035; % reference density (kg/m^3 - NEMO value)
drho = zeros(size(rho));
area=size(rho);
Nz=area(1);
for k =1:Nz-1
    drho(k+1, :) = 1/e3w(k+1, :)*(rho(k+1,:) - rho(k, :));
end
n2 = g*drho./rho0;
