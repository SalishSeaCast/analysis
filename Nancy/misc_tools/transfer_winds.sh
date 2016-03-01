# Script to transfer operational winds from /results to orcinus
# Uses scp to transfer the files

DEST=/home/sallen/MEOPAR/GEM2.5/ops/NEMO-atmos/
SOURCE=/results/forcing/atmospheric/GEM2.5/operational/

#start and end dates of the transfer period
start=2015-09-01
end=2015-10-02

d=$(date -I -d "$start") || exit -1
end_date=$(date -I -d "$end") || exit -1

while [ "$d" != "$end_date" ]; do
   fname=`date --date="$d" '+ops_y%Ym%md%d.nc'`
   echo $fname
   scp $SOURCE$fname orcinus:$DEST.
   d=$(date -I -d "$d + 1 day")
done