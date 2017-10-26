export dls_path=/syndata/dls-prod
export syn_report_path=/syndata/oreport


didxurlsf=""
ddataurlsf=""

#cdate=$(date --date="-1 day" +"%Y%m%d")
cdate=$(date +"%Y%m%d")

case "$1" in
        00) cdate=$(date +"%Y%m%d");;
        06) cdate=$(date +"%Y%m%d");;
        12) cdate=$(date +"%Y%m%d");;
        18) cdate=$(date --date="-1 day" +"%Y%m%d");;
esac

python /syndata/syn-reports/sendemail.py $cdate $1

