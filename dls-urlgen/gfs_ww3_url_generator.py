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

def generate_url(parad,cdate=None):
	forecast_parameters = parad

	# Base URL for the grib file containing forecast data
	base_url = "http://www.ftp.ncep.noaa.gov/data/nccf/com/wave/prod/gwes.%s/gwes00.glo_30m.t%sz.grib2"

	# Base URL for the grib file index containing forecast data
	idx_base_url = "http://www.ftp.ncep.noaa.gov/data/nccf/com/wave/prod/gwes.%s/gwes00.glo_30m.t%sz.grib2.idx"

	# Forecast starting hours e.g 00 hours
	forecast_at_start = int(forecast_parameters['forecast_at_start'])

	# After each forecast_at_step new forecast will be generated
	forecast_at_step = int(forecast_parameters['forecast_at_step'])

	# Forecast upper limit hours for which  
	# e.g for 18 hours limit value it will be 18 + forecast_at_step(6) = 24
	forecast_at_limit = int(forecast_parameters['forecast_at_limit'])
	forecast_at = [ "%02d" % di for di in range(forecast_at_start,forecast_at_limit,forecast_at_step)]
	# Date for which forecast data is being generated starting from forecast_at_start
	if not cdate:
		cdate = datetime.datetime.now().strftime("%Y%m%d")


	# Generate Base URLs to download forecast_at hours files
	# e.g {	'00': 'http://www.ftp.ncep.noaa.gov/data/nccf/com/gfs/prod/gfs.2016083000/gfs.t00z.pgrb2.0p25', 
	#		'06': 'http://www.ftp.ncep.noaa.gov/data/nccf/com/gfs/prod/gfs.2016083006/gfs.t06z.pgrb2.0p25',
	#		........... }
	urls = {fat:base_url % (cdate,fat) for fat in forecast_at}

	# Generate Base URLs to download forecast_at hours index files
	# e.g {	'00': 'http://www.ftp.ncep.noaa.gov/data/nccf/com/gfs/prod/gfs.2016083000/gfs.t00z.pgrb2.0p25', 
	#		'06': 'http://www.ftp.ncep.noaa.gov/data/nccf/com/gfs/prod/gfs.2016083006/gfs.t06z.pgrb2.0p25',
	#		........... }

	idx_urls = {fat:idx_base_url % (cdate,fat) for fat in forecast_at}


#	all_url = {k:[v+".f%03d" % fvhr for fvhr in range(forecast_valid_start,forecast_valid_limit+1,forecast_valid_step)] for k,v in urls.items()}
#	all_idx_url = {k:[v+".f%03d.idx" % fvhr for fvhr in range(forecast_valid_start,forecast_valid_limit+1,forecast_valid_step)] for k,v in urls.items()}

	return urls,idx_urls

def generate_url_files(dpath,urls,cdate=None):
	# Date for which forecast data is being generated starting from forecast_at_start
	if not cdate:
		cdate = datetime.datetime.now().strftime("%Y%m%d")
	urlpath = os.path.join(dpath,cdate)
	if not os.path.isdir(urlpath):
		os.mkdir(urlpath)
	grib_urls = urls[0]
	grib_idx_urls = urls[1]
	fcst_base_url_file = "%s_%s_ww3_fcst_urls.csv"
	fcst_base_url_idx_file = "%s_%s_ww3_fcst_idx_urls.csv"
	
	for fcst_at,grib_url in grib_urls.items():
		fcst_at_fpath = os.path.join(urlpath,fcst_at)
		fcst_at_f = fcst_base_url_file % (cdate,fcst_at)
		with open(os.path.join(urlpath,fcst_at_f),"w") as fcst_file:
#		for gurl in grib_url:
			fcst_file.write(grib_url+"\n")
	fcst_file.close()
	
	for fcst_at,grib_idx_url in grib_idx_urls.items():
		fcst_at_fpath = os.path.join(urlpath,fcst_at)
		fcst_at_idx_f = fcst_base_url_idx_file % (cdate,fcst_at)
		with open(os.path.join(urlpath,fcst_at_idx_f),"w") as fcst_idx_file:
#		for gurl in grib_idx_url:
			fcst_idx_file.write(grib_idx_url+"\n")
		fcst_idx_file.close()			

if __name__ ==  "__main__":
#	print len(sys.argv)
	if os.environ.has_key('dls_path'):
		dls_path = os.environ['dls_path']
		fname = 'ww3_fcst_url_gen_parameter.csv'
		fpath = os.path.join(dls_path,'dls-para',fname)
		if len(sys.argv) <= 1:
			cdate = datetime.datetime.now().strftime("%Y%m%d")
			fpara = read_parameters(os.path.join(dls_path,'dls-para',fname))
		else:
			cdate = sys.argv[1]
			fpara = read_parameters(os.path.join(dls_path,'dls-para',fname))
		durls = generate_url(fpara,cdate)
		generate_url_files(os.path.join(dls_path,'dls-urls'),durls,cdate)

