function [ varout ] = unstagger( varin, unStagDim )
%Unstaggers a varin crosss a dimension unStagDim
%   Unstaggering performed by avergaing between adjacent elements 
%   in the given dimension


dims = size(varin);
numdims = length(dims);
varout = zeros(1);

if(strcmp(unStagDim, 'X') || strcmp(unStagDim, 'U'))
    dimU = dims(1);
    if (numdims == 5)
        varout = 0.5*(varin(1:dimU-1,:,:,:,:) + varin(2:dimU,:,:,:,:));
    elseif (numdims == 4)
        varout = 0.5*(varin(1:dimU-1,:,:,:) + varin(2:dimU,:,:,:));
    elseif (numdims == 3)
        varout = 0.5*(varin(1:dimU-1,:,:) + varin(2:dimU,:,:));
    elseif (numdims == 2)
        varout = 0.5*(varin(1:dimU-1,:) + varin(2:dimU,:));
    end
end

if(strcmp(unStagDim, 'Y') || strcmp(unStagDim, 'V'))
    dimV = dims(2);
    if (numdims == 5)
        varout = 0.5*(varin(:,1:dimV-1,:,:,:) + varin(:,2:dimV,:,:,:));
    elseif (numdims == 4)
        varout = 0.5*(varin(:,1:dimV-1,:,:) + varin(:,2:dimV,:,:));
    elseif (numdims == 3)
        varout = 0.5*(varin(:,1:dimV-1,:) + varin(:,2:dimV,:));
    elseif (numdims == 2)
        varout = 0.5*(varin(:,1:dimV-1) + varin(:,2:dimV));
    end
end

if(strcmp(unStagDim, 'Z'))
    dimW = dims(3);
    if (numdims == 5)
        varout = 0.5*(varin(:,:,1:dimW-1,:,:) + varin(:,:,2:dimW,:,:));
    elseif (numdims == 4)
        varout = 0.5*(varin(:,:,1:dimW-1,:) + varin(:,:,2:dimW,:));
    elseif (numdims == 3)
        varout = 0.5*(varin(:,:,1:dimW-1) + varin(:,:,2:dimW));
    end
end

if(unStagDim ~= ['X' 'U' 'V' 'Y' 'Z'])
    print('Warning: input field was not staggered');
end

varout = double(varout);

end

