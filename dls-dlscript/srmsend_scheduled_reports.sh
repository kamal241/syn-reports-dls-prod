#!/bin/bash

export dls_path=/syndata/dls-prod
export syn_report_path=/syndata/oreport

sct=$(date --date="8 hour" +"%H%M")
#sct=$1
dayofweek=$(date --date="8 hour" +"%u")
weekofyear=$(date --date="8 hour" +"%Y_%V")

emd=$(date --date="8 hour" +"%Y_%V_%u")
cday=$(date --date="8 hour" +"%Y%m%d")
cdate=$(date --date="8 hour" +"%Y%m%d%H%M")

wkd=$syn_report_path/rfiles/REPORTDELIVERY/NOC/$weekofyear
#emdf=$wkd/$emd".txt"
emdf=$wkd/$cday".txt"

scemaillogpath=$dls_path
scemaillog=$scemaillogpath/"NOC"$cdate".log"
touch $scemaillog

if [ -d "${wkd}" ]; then
        echo $wkd " Directory already Exists" >> $scemaillog
else
        echo $wkd " Directory Does not Exists creating" >> $scemaillog
        #echo $wkd
        mkdir $wkd
        echo $wkd " Directory created successfully" >> $scemaillog
fi

if [ -f "${emdf}" ]; then
        echo $emdf" Exists" >> $scemaillog
else
        touch $emdf
        echo $emdf" Created Successfully" >> $scemaillog
fi

#cdate=ct=$(date --date="8 hour" +"%H%M")
rsfile="NOCSGT"$sct".txt"
rsf=$syn_report_path/rfiles/SPTIME/$rsfile
echo $rsf
##if [ -f "${rsf}" ]; then
#	echo $rsf
##	cldate=$(date +"%Y%m%d%H%M")
##	scemaillogpath=$dls_path
##	scemaillog=$scemaillogpath/$cldate".log"
##	touch $scemaillog

##	echo "Sending email for NOCSGT${sct}" > $scemaillog

##	#python /syndata/syn-reports/msendscheduledemail.py $sct
##else
##	echo "${rsf} does not exists"
##fi


OLDIFS=$IFS
if [ -f "${rsf}" ]; then
        while IFS='' read -r line || [[ -n "$line" ]]; do
		if [[ $line != "" ]]; then
                	echo $cdate","$line >> $emdf
		fi
        done < $rsf
        echo "Sending email for NOCSGT${sct}" >> $scemaillog
        echo "Sent email for NOCSGT${sct}" >> $scemaillog
else
        echo "Does not Exists" >> $scemaillog
fi
IFS=$OLDIFS
