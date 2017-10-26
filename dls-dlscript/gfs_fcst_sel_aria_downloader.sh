
#!/bin/bash
# The scripts assumes the script is being run at Singapore
# The time considered is corrected for singapore local time whenever necessary

#export dls_path=/home/megha/Synergy/SelRet/dls-prod
export dls_path=/syndata/dls-prod

didxurlsf=""
ddataurlsf=""

case "$1" in
	00) cdate=$(date +"%Y%m%d");;
	06) cdate=$(date +"%Y%m%d");;
	12) cdate=$(date +"%Y%m%d");;
	18) cdate=$(date +"%Y%m%d");;
esac

#cdate=$(date --date="-1 day" +"%Y%m%d")
cdate=$(date +"%Y%m%d")

urldirpath=$dls_path"/dls-urls/"$cdate

downloaddatapath=$dls_path"/dls-data/"$cdate/$1
touch $downloaddatapath/dls-prod.log
echo $downloaddatapath >> $downloaddatapath/dls-prod.log
mkdir -p $downloaddatapath >> $downloaddatapath/dls-prod.log
echo $urldirpath
if [ -d $urldirpath ]; then
	ddataurlsf="$cdate"_"$1"_"gfs_fcst_urls.csv"
	dataurlsfile="$urldirpath/$ddataurlsf"

#	dtime=$(time wget -d -t 1 --read-timeout=30 -o /dev/null --header="User-Agent: Mozilla/5.0 (Windows NT 6.0) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.97 Safari/537.11" --header="Referer: http://7msport.com/" --directory-prefix=$downloaddatapath --input-file $idxurlsfile)
#	echo $dtime

#	dtime=$(time wget -d -t 1 --read-timeout=30 -o /dev/null --header="User-Agent: Mozilla/5.0 (Windows NT 6.0) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.97 Safari/537.11" --header="Referer: http://7msport.com/" --directory-prefix=$downloaddatapath --input-file $dataurlsfile)
	aria2c -i $dataurlsfile  -d $downloaddatapath -x 10
	msg="$(date) : grib files for "$cdate" Downloaded in and stored at "$downloaddatapath
	echo $msg >> $dls_path/dls-prod.log

else
	msg="$(date) : URLs for "$cdate" could not found. Make sure urls are generated for "$cdate
	echo $msg >> $dls_path/dls-prod.log
fi

# Rename files to gfs.t00z.pgrb2.0p25. [f000, f001, ....., f384] 
#data_dir=$dls_path"/dls-data/"$cdate/$1
#traverse_dir=$data_dir"/*"

#echo "Traversing "$data_dir  >> $dls_path/dls-prod.log

#dlen=${#data_dir}

#sidx=$(($dlen + 1 + 24))
#echo $dlen, $sidx  >> $dls_path/dls-prod.log
#for f in $traverse_dir
#do
#  nf=${f:$sidx:24}
#  echo "Moving ", $f, " to ", $data_dir/$nf  >> $dls_path/dls-prod.log
#  sudo mv $f $data_dir/$nf
#  echo "Moved ", $f, " to ", $data_dir/$nf  >> $dls_path/dls-prod.log
#done
