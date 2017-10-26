#!/bin/bash
export syn_report_path=/syndata/oreport

dt=$1
tm=$2

#echo $dt, $tm
pattern=$dt"__"$tm"__*.txt"
#echo $pattern
search_dir=$syn_report_path/"rfiles"/$dt
#echo $search_dir
lrfiles=($(find $search_dir -name $pattern))
#lrfiles=(1 2 3)
#echo $lrfiles
for csf in "${lrfiles[@]}"
do
#        echo "Checking ${csf}"
        if [ -f "${csf}" ]; then
                {
                read;
                while IFS=',' read client lname rf lcid
                do
#                        echo $client, $lname, $rf, $lcid
                        if [ -f $rf ]; then
#				echo ""
#				echo $rf
				rm $rf
                        fi
                done
                } < "$csf"
        else
                echo "$csf does not exists"
        fi
#echo $csf
rm $csf
done


