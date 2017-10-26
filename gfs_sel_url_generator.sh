#export dls_path=/home/megha/Synergy/SelRet/dls-prod
export dls_path=/syndata/dls-prod
export syn_report_path=/syndata/oreport
cdate=$(date +"%Y%m%d")
mkdir $syn_report_path/rimages/WSPRMSL/$cdate
chmod 777 $syn_report_path/rimages/WSPRMSL/$cdate
mkdir $syn_report_path/rimages/SWHGT/$cdate
chmod 777 $syn_report_path/rimages/SWHGT/$cdate
mkdir $syn_report_path/rimages/SST/$cdate
chmod 777 $syn_report_path/rimages/SST/$cdate
mkdir $syn_report_path/rreports/$cdate
chmod 777 $syn_report_path/rreports/$cdate
mkdir $syn_report_path/rfiles/$cdate
chmod 777 $syn_report_path/rfiles/$cdate
echo $dls_path
python $dls_path/dls-urlgen/gfs_fcst_url_sel_generator.py $1
python $dls_path/dls-urlgen/gfs_ww3_url_generator.py $1
python $dls_path/dls-urlgen/gfs_visibility_url_generator.py $1
python $dls_path/dls-urlgen/ss_fcst_url_generator.py $1
echo "URLs Generated"

export tsyn_report_path=/syndata/treport
cdate=$(date +"%Y%m%d")
mkdir $tsyn_report_path/rimages/WSPRMSL/$cdate
chmod 777 $tsyn_report_path/rimages/WSPRMSL/$cdate
mkdir $tsyn_report_path/rimages/SWHGT/$cdate
chmod 777 $tsyn_report_path/rimages/SWHGT/$cdate
mkdir $tsyn_report_path/rimages/SST/$cdate
chmod 777 $tsyn_report_path/rimages/SST/$cdate
mkdir $tsyn_report_path/rreports/$cdate
chmod 777 $tsyn_report_path/rreports/$cdate
mkdir $tsyn_report_path/rfiles/$cdate
chmod 777 $tsyn_report_path/rfiles/$cdate

export trpcl_adv_path=/syndata/trpcl_adv
mkdir $trpcl_adv_path/data/$cdate
chmod 777 $trpcl_adv_path/data/$cdate
