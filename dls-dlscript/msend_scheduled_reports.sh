export dls_path=/syndata/dls-prod
export syn_report_path=/syndata/oreport

#cdate=ct=$(date --date="8 hour" +"%H%M")
sct=$(date --date="8 hour" +"%H%M")
rsfile="NOCSGT"$sct".txt"
#echo $rsfile
rsf=$syn_report_path/rfiles/SPTIME/$rsfile
echo $rsf
if [ -f "${rsf}" ]; then
#	echo $rsf
	cldate=$(date +"%Y%m%d%H%M")
	scemaillogpath=$dls_path
	scemaillog=$scemaillogpath/$cldate".log"
	touch $scemaillog

	echo "Sending email for NOCSGT${sct}" > $scemaillog

	python /syndata/syn-reports/msendscheduledemail.py $sct
else
	echo "${rsf} does not exists"
fi
