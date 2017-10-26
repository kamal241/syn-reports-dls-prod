#!/bin/bash

#export dls_path=/syndata/dls-prod/
#export syn_report_path=/syndata/oreport
#export tsyn_report_path=/syndata/treport
export trpcl_adv_path=/syndata/trpcl_adv
export WORKON_HOME=/syndata/
source /syndata/syn_reports/bin/activate

cdate=$(date +"%Y%m%d")
logfdt=$(date +"%Y%m%d%H%M")
logdt=$(date +"%Y/%m/%d %H:%M")

trp_path=$trpcl_adv_path
ta_log=$trp_path/"TA_"$logfdt".log"
touch $ta_log

echo "${logdt} : Checking for Tropical Advisory on NHC" >> $ta_log
python /syndata/trpcl_adv/tropical_adv.py $cdate
echo "${logdt} : Completed Checking for Tropical Advisory on NHC" >> $ta_log
echo "${logdt} : Checking for Tropical Advisory on JTWC" >> $ta_log
python /syndata/trpcl_adv/jtwc_downloader.py $cdate
echo "${logdt} : Completed Checking for Tropical Advisory on JTWC" >> $ta_log
