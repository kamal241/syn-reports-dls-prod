export dls_path=/syndata/dls-prod

cdate=$(date --date="-2 day" +"%Y%m%d")

rmpath=$dls_path"/dls-data/WW3/"$cdate
cleanuplogf="cleanup_ww3"_"$cdate".log
touch $dls_path/$cleanuplogf
#echo $rmpath
#echo $cleanuplogf
if [ -d $rmpath ]; then
	echo "Removing "$rmpath" for WW3 Data" >> $dls_path/$cleanuplogf
	rm -R $rmpath
	echo $rmpath" WW3 Data removed successfully" >> $dls_path/$cleanuplogf
else
	echo $rmpath" does not exists" >> $dls_path/$cleanuplogf
fi
