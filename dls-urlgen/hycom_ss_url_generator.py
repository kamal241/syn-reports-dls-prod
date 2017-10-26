# Script to generate WW3 URLs to be download 

import os
import sys
import datetime


def read_parameters(fname):
        forecast_parameters = {}

        # Read file containing forecast parameters reqauired to generate URLs
        with open(fname) as ugpf:
                for line in ugpf:
                        linedata = line.split('=')
                        forecast_parameters[linedata[0]] = linedata[1]
        return forecast_parameters


def generate_url(cdate=None):
        

        # Base URL for the grib file containing forecast data
        #base_url = "ftp://ftpprd.ncep.noaa.gov/pub/data/nccf/com/omb/prod/fog.%s/fog.t%sz.fvnhg.grib2"
        base_sst_url = "ftp://ftp.mpc.ncep.noaa.gov/grids/operational/GLOBALHYCOM/grtofs_sst_%s.tar.gz"
        base_uv_url = "ftp://ftp.mpc.ncep.noaa.gov/grids/operational/GLOBALHYCOM/grtofs_uv_%s.tar.gz"
        base_sst45_url = "ftp://ftp.mpc.ncep.noaa.gov/grids/operational/GLOBALHYCOM/grtofs_sst_%s_day%d.nc.gz"
        base_uv45_url = "ftp://ftp.mpc.ncep.noaa.gov/grids/operational/GLOBALHYCOM/grtofs_uv_%s_day%d.nc.gz"
        
        if not cdate:
                cdate = datetime.datetime.now().strftime("%Y%m%d")
        print cdate
        days = [4,5]
        urls = {}
        sst_urls = { '%d' % day :[base_sst45_url % (cdate,day)] for day in days}
        sst_urls['123'] = [base_sst_url % cdate]
        #sst_urls['45'] = [base_sst45_url % (cdate,day) for day in days]        
        #uv_urls = {}
        uv_urls = { '%d' % day : [base_uv45_url % (cdate,day)] for day in days }
        #uv_urls['45'] = [base_uv45_url % (cdate,day) for day in days]
        uv_urls['123'] = [base_uv_url % cdate]
        #uv_urls['45'] = [base_uv45_url % (cdate,day) for day in days]
        urls['sst'] = sst_urls
        urls['uv'] = uv_urls


        return urls

def generate_url_files(dpath,urls,cdate=None):
        # Date for which forecast data is being generated starting from forecast_at_start
        if not cdate:
                cdate = datetime.datetime.now().strftime("%Y%m%d")
        urlpath = os.path.join(dpath,cdate)
        if not os.path.isdir(urlpath):
                os.mkdir(urlpath)
        hycom_urls = urls
        
        fcst_base_url_file = "%s_%s_%s_fcst_urls.csv"
        

        for hycom_para,hycom_url in hycom_urls.items():
                #hycom_para_fpath = os.path.join(urlpath,hyco)                
                for day,urls in hycom_url.items():                        
                        hycom_para_f = fcst_base_url_file % (cdate,day,hycom_para)                        
                        with open(os.path.join(urlpath,hycom_para_f),"w") as fcst_file:
                                for url in urls:
                                        fcst_file.write(url+"\n")
                        fcst_file.close()
                        

if __name__ ==  "__main__":
#       print len(sys.argv)
        if os.environ.has_key('dls_path'):
                dls_path = os.environ['dls_path']
#                fpath = os.path.join(dls_path,'dls-para',fname)
                if len(sys.argv) <= 1:
                        cdate = datetime.datetime.now().strftime("%Y%m%d")
                else:
                        cdate = sys.argv[1]
                durls = generate_url(cdate=cdate)
                generate_url_files(os.path.join(dls_path,'dls-urls'),durls,cdate)
