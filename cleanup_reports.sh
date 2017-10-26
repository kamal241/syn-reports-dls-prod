export dls_path=/syndata/dls-prod
export syn_report_path=/syndata/oreport

cdate=$(date --date="-2 day" +"%Y%m%d")

rmiwpath=$syn_report_path"/rimages/WSPRMSL/"$cdate
rmispath=$syn_report_path"/rimages/SWHGT/"$cdate
rmistpath=$syn_report_path"/rimages/SST/"$cdate
rmrpath=$syn_report_path"/rreports/"$cdate
rmofs=$syn_report_path"/rfiles/"$cdate
#"/"$cdate*".txt"
#echo $rmofs
cleanuplogf="cleanup_reports"_"$cdate".log
touch $dls_path/$cleanuplogf
#echo $rmpath
#echo $cleanuplogf
if [ -d $rmiwpath ]; then
	echo "Removing "$rmiwpath" for GFS Data" >> $dls_path/$cleanuplogf
	rm -R $rmiwpath
	echo $rmiwpath" WSPRMSL images removed successfully" >> $dls_path/$cleanuplogf
else
	echo $rmiwpath" does not exists" >> $dls_path/$cleanuplogf
fi
if [ -d $rmispath ]; then
	echo "Removing "$rmispath" for GFS Data" >> $dls_path/$cleanuplogf
	rm -R $rmispath
	echo $rmispath" WSPRMSL images removed successfully" >> $dls_path/$cleanuplogf
else
	echo $rmispath" does not exists" >> $dls_path/$cleanuplogf
fi
if [ -d $rmistpath ]; then
	echo "Removing "$rmistpath" for GFS Data" >> $dls_path/$cleanuplogf
	rm -R $rmistpath
	echo $rmistpath" WSPRMSL images removed successfully" >> $dls_path/$cleanuplogf
else
	echo $rmistpath" does not exists" >> $dls_path/$cleanuplogf
fi
if [ -d $rmrpath ]; then
	echo "Removing "$rmrpath" for GFS Data" >> $dls_path/$cleanuplogf
	rm -R $rmrpath
	echo $rmrpath" WSPRMSL images removed successfully" >> $dls_path/$cleanuplogf
else
	echo $rmrpath" does not exists" >> $dls_path/$cleanuplogf
fi
if [ -d $rmofs ]; then
	echo "Removing "$rmofs" for ofiles" >> $dls_path/$cleanuplogf
	rm -R $rmofs
	echo $rmofs" Output report file removed successfully" >> $dls_path/$cleanuplogf
else
	echo $rmofs" does not exists" >> $dls_path/$cleanuplogf
fi

