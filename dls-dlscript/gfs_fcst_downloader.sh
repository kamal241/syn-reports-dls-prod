
# The scripts assumes the script is being run at Singapore
# The time considered is corrected for singapore local time whenever necessary

export dls_path=/home/megha/Synergy/aws/dls-prod



didxurlsf=""
ddataurlsf=""

case "$1" in
	00) cdate=$(date +"%Y%m%d");;
	06) cdate=$(date +"%Y%m%d");;
	12) cdate=$(date +"%Y%m%d");;		
	18) cdate=$(date +"%Y%m%d");;
esac

cdate=$(date --date="-1 day" +"%Y%m%d")
urldirpath=$dls_path"/dls-urls/"$cdate

downloaddatapath=$dls_path"/dls-data/"$cdate/$1
echo $downloaddatapath
mkdir -p $downloaddatapath
#echo $urldirpath
if [ -d $urldirpath ]; then
	didxurlsf="$cdate"_"$1"_"gfs_fcst_idx_urls.csv"
	ddataurlsf="$cdate"_"$1"_"gfs_fcst_urls.csv"
	idxurlsfile="$urldirpath/$didxurlsf"
	dataurlsfile="$urldirpath/$ddataurlsf"

#	dtime=$(time wget -d -t 1 --read-timeout=30 -o /dev/null --header="User-Agent: Mozilla/5.0 (Windows NT 6.0) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.97 Safari/537.11" --header="Referer: http://7msport.com/" --directory-prefix=$downloaddatapath --input-file $idxurlsfile)
#	echo $dtime	
#	msg="$(date) : Index files for "$cdate" Downloaded in and stored at "$downloaddatapath
#	echo $msg >> dls-prod.log

	dtime=$(time wget -d -t 1 --read-timeout=30 -o /dev/null --header="User-Agent: Mozilla/5.0 (Windows NT 6.0) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.97 Safari/537.11" --header="Referer: http://7msport.com/" --directory-prefix=$downloaddatapath --input-file $dataurlsfile)
#	echo $dtime	
	msg="$(date) : grib files for "$cdate" Downloaded in and stored at "$downloaddatapath
	echo $msg >> dls-prod.log


#	echo "Downloading URLs from "$urldirpath
#	echo "IDX "$idxurlsfile
#	echo "DATA "$dataurlsfile
else
	msg="$(date) : URLs for "$cdate" could not found. Make sure urls are generated for "$cdate
	echo $msg >> dls-prod.log
fi

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