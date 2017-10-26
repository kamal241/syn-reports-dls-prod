export dls_path=/syndata/dls-prod

didxurlsf=""
ddataurlsf=""

cdate=$(date +"%Y%m%d")
#cdate=$(date --date="-1 day" +"%Y%m%d")

urldirpath=$dls_path"/dls-urls/"$cdate

downloaddatapath=$dls_path"/dls-data/SST/"$cdate
echo $downloaddatapath >> $dls_path/dls-vis-prod.log
mkdir -p $downloaddatapath
echo $urldirpath
if [ -d $urldirpath ]; then
        ddataurlsf="$cdate"_"$2"_"$1"_"fcst_urls.csv"
        dataurlsfile="$urldirpath/$ddataurlsf"
        echo $ddataurlsf
        if [ -f $dataurlsfile ]; then
#		print $dataurlsfile
		aria2c -i $dataurlsfile  -d $downloaddatapath -x 10
	        msg="$(date) : nc files for "$cdate" Downloaded in and stored at "$downloaddatapath
        	echo $msg >> $dls_path/dls-ss-prod.log
	else
        	msg="$(date) : URLs for "$cdate" could not found. Make sure urls are generated for "$cdate
	        echo $msg >> $dls_path/dls-ss-prod.log
	fi
else
        msg="$(date) : URLs for "$cdate" could not found. Make sure urls are generated for "$cdate
        echo $msg >> $dls_path/dls-ss-prod.log
fi

