#!/bin/bash
export dls_path=/home/megha/Synergy/aws/dls-prod
cdate=$(date --date="-1 day" +"%Y%m%d")
data_dir=$dls_path"/dls-data/"$cdate/$1
traverse_dir=$data_dir"/*"
#cdate=$(date --date="-1 day" +"%Y%m%d")

echo "Traversing "$data_dir
dlen=${#data_dir}
echo $dlen
sidx=$(($dlen + 1 + 24))

echo $sidx, $eidx
for f in $traverse_dir
do
  nf=${f:$sidx:24}
  mv $f $data_dir/$nf
done
