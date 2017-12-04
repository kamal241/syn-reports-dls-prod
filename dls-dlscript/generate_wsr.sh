#!/bin/bash

export dls_path=/syndata/dls-prod/
export syn_report_path=/syndata/oreport
export WORKON_HOME=/syndata/
source /syndata/syn_reports/bin/activate

sct=$(date --date="8 hour" +"%H%M")
#sct=$1

year=$(date --date="-16 hour" +"%Y")
weekofyear=$(date --date="-16 hour" +"%V")
#weekofyear=$(date --date="-1 day" +"%V")
cdate=$(date --date="8 hour" +"%d-%m-%Y")
echo $cdate
echo $year $weekofyear $cdate
python /syndata/syn-reports/service_report.py $year $weekofyear $cdate
wsrf=$syn_report_path/rreports/WSR/"GMO_WSR_"$cdate".pdf"
if [ -f "${wsrf}" ]; then
	rm $syn_report_path/rreports/LATEST/WSR/GMO/*.pdf
	cp $wsrf $syn_report_path/rreports/LATEST/WSR/GMO/
else
	echo $wsrf" does not exist"
fi

nocwsrf=$syn_report_path/rreports/WSR/"NOC_WSR_"$cdate".pdf"
if [ -f "${nocwsrf}" ]; then
	rm $syn_report_path/rreports/LATEST/WSR/NOC/*.pdf
	cp $nocwsrf $syn_report_path/rreports/LATEST/WSR/NOC/
else
	echo $nocwsrf" does not exist"
fi
