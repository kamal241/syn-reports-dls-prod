export dls_path=/home/megha/Synergy/aws/dls-prod
echo $dls_path
python $dls_path/dls-urlgen/gfs_fcst_url_generator.py
echo "URLs Generated"