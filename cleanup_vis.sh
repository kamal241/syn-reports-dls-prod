export dls_path=/syndata/dls-prod

cdate=$(date --date="-2 day" +"%Y%m%d")

rmpath=$dls_path"/dls-data/VIS/"$cdate
cleanuplogf="cleanup_VIS"_"$cdate".log
touch $dls_path/$cleanuplogf
#echo $rmpath
#echo $cleanuplogf
if [ -d $rmpath ]; then
	echo "Removing "$rmpath" for VIS Data" >> $dls_path/$cleanuplogf
	rm -R $rmpath
	echo $rmpath" VIS Data removed successfully" >> $dls_path/$cleanuplogf
else
	echo $rmpath" does not exists" >> $dls_path/$cleanuplogf
fi
