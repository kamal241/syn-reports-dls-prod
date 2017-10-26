export dls_path=/syndata/dls-prod

cdate=$(date --date="-1 day" +"%Y%m%d")

rmpath=$dls_path"/dls-data/SST/"$cdate
cleanuplogf="cleanup_sst"_"$cdate".log
touch $dls_path/$cleanuplogf
#echo $rmpath
#echo $cleanuplogf
if [ -d $rmpath ]; then
	echo "Removing "$rmpath" for SST Data" >> $dls_path/$cleanuplogf
	rm -R $rmpath
	echo $rmpath" SST Data removed successfully" >> $dls_path/$cleanuplogf
else
	echo $rmpath" does not exists" >> $dls_path/$cleanuplogf
fi
