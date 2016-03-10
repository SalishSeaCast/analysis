# Script to transfer operational winds from /results to orcinus
# Uses scp to transfer the files

DEST=/home/nksoonti/MEOPAR/rivers/
SOURCE=/results/forcing/rivers/

#start and end dates of the transfer period
start=2015-07-01
end=2015-10-02

d=$(date -I -d "$start") || exit -1
end_date=$(date -I -d "$end") || exit -1

while [ "$d" != "$end_date" ]; do
   fname=`date --date="$d" '+RFraserCElse_y%Ym%md%d.nc'`
   echo $fname
   scp $SOURCE$fname orcinus:$DEST.
   ssh orcinus "chgrp wg-moad $DEST$fname"
   ssh orcinus "chmod 664 $DEST$fname"
   d=$(date -I -d "$d + 1 day")
done