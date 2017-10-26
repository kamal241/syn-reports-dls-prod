#!/bin/bash

export dls_path=/syndata/dls-prod/
export syn_report_path=/syndata/oreport
export tsyn_report_path=/syndata/treport
export trpcl_adv_path=/syndata/trpcl_adv
export WORKON_HOME=/syndata/
source /syndata/syn_reports/bin/activate

cdate=$(date +"%Y%m%d")

case "$1" in
        00) cdate=$(date +"%Y%m%d");;
        06) cdate=$(date +"%Y%m%d");;
        12) cdate=$(date +"%Y%m%d");;
        18) cdate=$(date --date="-1 day" +"%Y%m%d");;
esac

#cdate=$(date --date="-1 day" +"%Y%m%d")
echo "Generating TEST"
python /syndata/syn-reports/test_generate_gmo_reports.py $cdate $1
#python /syndata/syn-reports/test_generate_reports.py $cdate $1
echo "Completed TEST"
