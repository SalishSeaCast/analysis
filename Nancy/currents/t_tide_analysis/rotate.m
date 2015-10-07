function [ urot, vrot ] = rotate( u, v, theta )
%Rotates orthogonal velocity vectors u,v by angle theta in deg 
%    Clockwise rotation

theta_rad = theta * pi / 180;

urot = u * cos(theta_rad) - v * (theta_rad);
vrot = u * sin(theta_rad) + v * cos(theta_rad);


end

