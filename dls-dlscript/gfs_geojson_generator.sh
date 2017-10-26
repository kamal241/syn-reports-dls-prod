export dls_path=/syndata/dls-prod
echo $dls_path
python $dls_path/dls-dlscript/gfs_fcst_url_sel_generator.py $1
python $dls_path/dls-urlgen/gfs_ww3_url_generator.py $1
echo "URLs Generated"
