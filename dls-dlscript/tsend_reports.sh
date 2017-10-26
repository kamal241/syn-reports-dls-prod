export dls_path=/syndata/dls-prod
export tsyn_report_path=/syndata/treport


didxurlsf=""
ddataurlsf=""

#cdate=$(date --date="-1 day" +"%Y%m%d")
cdate=$(date +"%Y%m%d")

# if sendingat 0800 hrs
#case "$1" in
#        00) cdate=$(date +"%Y%m%d");;
#        12) cdate=$(date --date="-1 day" +"%Y%m%d") 
	#cdate=$(date +"%Y%m%d");;
#esac

python /syndata/syn-reports/tsendmail.py $cdate $1

