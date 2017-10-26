#!/bin/bash

export dls_path=/syndata/dls-prod/
export syn_report_path=/syndata/oreport
export tsyn_report_path=/syndata/treport
export WORKON_HOME=/syndata/
source /syndata/syn_reports/bin/activate

cdate=$(date +"%Y%m%d")

case "$1" in
        00) cdate=$(date +"%Y%m%d");;
        06) cdate=$(date +"%Y%m%d");;
        12) cdate=$(date +"%Y%m%d");;
        18) cdate=$(date --date="-1 day" +"%Y%m%d");;
esac

fld=$(date +"%Y%m%d%H%M%S")
fln="GRP_"$fld".txt"

echo "Generating report for "$cdate $1 >> $dls_path/$fln
#cdate=$(date --date="-1 day" +"%Y%m%d")

#python /syndata/syn-reports/tgenerate_reports.py $cdate $1
#python /syndata/syn-reports/generate_reports.py $cdate $1

#$dls_path/dls-dlscript/preparelatestrpt.sh $cdate $1
