export dls_path=/syndata/dls-prod
export syn_report_path=/syndata/oreport

sct=$(date --date="8 hour" +"%H%M")
sct="0745"
rsfile="SGT"$sct".txt"
echo $rsfile
rsf=$syn_report_path/rfiles/SPTIME/$rsfile
echo $rsf
locations=()
while read line
do
	IFS=',' read -r -a myArray <<< $line	
	echo "${myArray[@]}"
	locations=("${locations[@]}" "${myArray[@]}")
done < $FILENAME

IFS=$oldIFS

if [ -f "${rsf}" ]; then
	OLDIFS=$IFS
	while read -r line
	do
#		IN="bla@some.com;john@home.com" 
#		IN="$line"
		echo $line
#		set -- "$IN" 
#		IFS=","; declare -a locs=($*) 
#		echo "${locs[@]}" 
#		echo "${locs[0]}" 
#		echo "${locs[1]}" 
	done < $rsf
	IFS=$OLDIFS
#	echo $rsf
	cldate=$(date +"%Y%m%d%H%M")
#	scemaillogpath=$dls_path
#	scemaillog=$scemaillogpath/$cldate".log"
#	touch $scemaillog

#	echo "Sending email for SGT${sct}" > $scemaillog
	echo "Sending email for SGT${sct}"

#	python /syndata/syn-reports/pisendscheduledemail.py $sct &
else
	echo "${rsf} does not exists"
fi
