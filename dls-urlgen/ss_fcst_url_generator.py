# Script to generate WW3 URLs to be download 

import os
import sys
import datetime


def generate_url(cdate=None):
    # Base URL for the grib file containing forecast data
    #base_url = "ftp://ftpprd.ncep.noaa.gov/pub/data/nccf/com/omb/prod/fog.%s/fog.t%sz.fvnhg.grib2"
    base_ss_url = "ftp://ftpprd.ncep.noaa.gov/pub/data/nccf/com/rtofs/prod/rtofs.%s/rtofs_glo_2ds_f%03d_3hrly_prog.nc"

    if not cdate:
            cdate = datetime.datetime.now().strftime("%Y%m%d")
    print cdate
    runs = {0: range(3,75,3), 1: range(75,195,3)}
    urls = {}
    for run, hrs in runs.items():
        urls[run] = [base_ss_url % (cdate, hr) for hr in hrs]

    return urls

def generate_url_files(dpath,urls,cdate=None):
    # Date for which forecast data is being generated starting from forecast_at_start
    if not cdate:
            cdate = datetime.datetime.now().strftime("%Y%m%d")
    urlpath = os.path.join(dpath,cdate)
    if not os.path.isdir(urlpath):
            os.mkdir(urlpath)
    ss_urls = urls

    fcst_base_url_file = "%s_%s_ss_fcst_urls.csv"

    for ss_run,turls in ss_urls.items():
        ss_para_f = fcst_base_url_file % (cdate, ss_run)                        
        with open(os.path.join(urlpath,ss_para_f),"w") as fcst_file:
            for urli in turls:            
                fcst_file.write(urli+"\n")
            fcst_file.close()
                        

if __name__ ==  "__main__":
#       print len(sys.argv)
    if os.environ.has_key('dls_path'):
        dls_path = os.environ['dls_path']
        fname = 'visibility_fcst_url_gen_parameter.csv'
        fpath = os.path.join(dls_path,'dls-para',fname)
        if len(sys.argv) <= 1:
                cdate = datetime.datetime.now().strftime("%Y%m%d")
               # fpara = read_parameters(os.path.join(dls_path,'dls-para',fname))
        else:
                cdate = sys.argv[1]
                #fpara = read_parameters(os.path.join(dls_path,'dls-para',fname))
        #print cdate
        durls = generate_url(cdate=cdate)
        #print durls
        generate_url_files(os.path.join(dls_path,'dls-urls'),durls,cdate)
