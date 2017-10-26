
# The scripts assumes the script is being run at Singapore
# The time considered is corrected for singapore local time whenever necessary

#export dls_path=/home/megha/Synergy/SelRet/dls-prod
export dls_path=/syndata/dls-prod

didxurlsf=""
ddataurlsf=""

cdate=$(date +"%Y%m%d")

case "$1" in
        00) cdate=$(date +"%Y%m%d");;
        06) cdate=$(date +"%Y%m%d");;
        12) cdate=$(date +"%Y%m%d");;
        18) cdate=$(date +"%Y%m%d");;
esac
#cdate=$(date --date="-1 day" +"%Y%m%d")

urldirpath=$dls_path"/dls-urls/"$cdate

downloaddatapath=$dls_path"/dls-data/VIS/"$cdate/$1
echo $downloaddatapath >> $dls_path/dls-vis-prod.log
mkdir -p $downloaddatapath 
echo $urldirpath
if [ -d $urldirpath ]; then
	ddataurlsf="$cdate"_"$1"_"vis_fcst_urls.csv"
	didxurlsf="$cdate"_"$1"_"vis_fcst_idx_urls.csv"
	dataurlsfile="$urldirpath/$ddataurlsf"
	idxurlsfile="$urldirpath/$didxurlsf"
#	dtime=$(time wget -d -t 1 --read-timeout=30 -o /dev/null --header="User-Agent: Mozilla/5.0 (Windows NT 6.0) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.97 Safari/537.11" --header="Referer: http://7msport.com/" --directory-prefix=$downloaddatapath --input-file $idxurlsfile)
#	echo $dtime	

#	dtime=$(time wget -d -t 1 --read-timeout=30 -o /dev/null --header="User-Agent: Mozilla/5.0 (Windows NT 6.0) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.97 Safari/537.11" --header="Referer: http://7msport.com/" --directory-prefix=$downloaddatapath --input-file $dataurlsfile)
	aria2c -i $idxurlsfile  -d $downloaddatapath -x 10
	aria2c -i $dataurlsfile  -d $downloaddatapath -x 10
	msg="$(date) : grib files for "$cdate" Downloaded in and stored at "$downloaddatapath
	echo $msg >> $dls_path/dls-vis-prod.log

else
	msg="$(date) : URLs for "$cdate" could not found. Make sure urls are generated for "$cdate
	echo $msg >> $dls_path/dls-vis-prod.log
fi

# Rename files to gfs.t00z.pgrb2.0p25. [f000, f001, ....., f384] 


