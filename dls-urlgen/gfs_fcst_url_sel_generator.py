# Script to generate URLs to be download 

import os
import sys
import datetime

def read_parameters(fname):
	forecast_parameters = {}

	# Read file containing forecast parameters reqauired to generate URLs
	with open(fname) as ugpf:
		for line in ugpf:
			linedata = line.split('=')
			forecast_parameters[linedata[0]] = linedata[1][:-1]

	return forecast_parameters

def generate_url(parad,cdate=None):
	forecast_parameters = parad

	# Base URL for the grib file containing forecast data
	base_url = "http://www.ftp.ncep.noaa.gov/data/nccf/com/gfs/prod/gfs.%s/gfs.t%sz.pgrb2.0p25"
	base_url = "http://nomads.ncep.noaa.gov/cgi-bin/filter_gfs_0p25.pl?file=gfs.t%sz.pgrb2.0p25."
	o_para = "f%03d&%s&dir=%%2Fgfs.%s"
	sel_parameters = "lev_10_m_above_ground=on&lev_2_m_above_ground=on&lev_925_mb=on&lev_975_mb=on&lev_convective_cloud_bottom_level=on&"
	sel_parameters = sel_parameters + "lev_convective_cloud_layer=on&lev_low_cloud_bottom_level=on&lev_low_cloud_layer=on&lev_mean_sea_level=on&"
	sel_parameters = sel_parameters + "lev_middle_cloud_bottom_level=on&lev_middle_cloud_layer=on&lev_surface=on&var_APCP=on&var_GUST=on&"
	sel_parameters = sel_parameters + "lev_0-0.1_m_below_ground=on&lev_entire_atmosphere=on&"
	sel_parameters = sel_parameters + "var_PRES=on&var_PRMSL=on&var_RH=on&var_TCDC=on&var_TMP=on&var_UGRD=on&var_VGRD=on&"
	sel_parameters = sel_parameters + "var_CICEP=on&var_SOILW=on&var_SUNSD=on&var_TCDC=on&var_TSOIL=on&var_WATR=on&"
	sel_parameters = sel_parameters + "leftlon=0&rightlon=360&toplat=90&bottomlat=-90"

	# Base URL for the grib file index containing forecast data
	idx_base_url = "http://www.ftp.ncep.noaa.gov/data/nccf/com/gfs/prod/gfs.%s/gfs.t%sz.pgrb2.0p25"

	# Forecast starting hours e.g 00 hours
	forecast_at_start = int(forecast_parameters['forecast_at_start'])

	# After each forecast_at_step new forecast will be generated
	forecast_at_step = int(forecast_parameters['forecast_at_step'])

	# Forecast upper limit hours for which  
	# e.g for 18 hours limit value it will be 18 + forecast_at_step(6) = 24
	forecast_at_limit = int(forecast_parameters['forecast_at_limit'])

	# Individual forecast valid till hour
	forecast_valid_start = int(forecast_parameters['forecast_valid_start'])

	# Individual forecast valid till hour
	forecast_valid_limit = int(forecast_parameters['forecast_valid_limit'])

	# Forecast valid step f006, f012, f018, ..... for forecast_valid_step=6
	forecast_valid_step	= int(forecast_parameters['forecast_valid_step'])

	forecast_at = [ "%02d" % di for di in range(forecast_at_start,forecast_at_limit,forecast_at_step)]

	# Date for which forecast data is being generated starting from forecast_at_start
	if not cdate:
		cdate = datetime.datetime.now().strftime("%Y%m%d")


	# Generate Base URLs to download forecast_at hours files
	# e.g {	'00': 'http://www.ftp.ncep.noaa.gov/data/nccf/com/gfs/prod/gfs.2016083000/gfs.t00z.pgrb2.0p25', 
	#		'06': 'http://www.ftp.ncep.noaa.gov/data/nccf/com/gfs/prod/gfs.2016083006/gfs.t06z.pgrb2.0p25',
	#		........... }
	urls = {fat:base_url % (fat) for fat in forecast_at}
#	print urls
	# Generate Base URLs to download forecast_at hours index files
	# e.g {	'00': 'http://www.ftp.ncep.noaa.gov/data/nccf/com/gfs/prod/gfs.2016083000/gfs.t00z.pgrb2.0p25', 
	#		'06': 'http://www.ftp.ncep.noaa.gov/data/nccf/com/gfs/prod/gfs.2016083006/gfs.t06z.pgrb2.0p25',
	#		........... }

	idx_urls = [idx_base_url % (cdate+fat,fat) for fat in forecast_at]

	fv1 = range(forecast_valid_start,121,1)
	fv2 = range(123,241,3)
	fv3 = range(252,forecast_valid_limit+1,12)
	fv = fv1 + fv2 + fv3

	all_url = {k:[v+ o_para % (fvhr,sel_parameters,cdate+k) for fvhr in fv] for k,v in urls.items()}
#	print all_url['00'][0]
#	print all_url['06'][0]
#	print all_url['12'][0]
#	print all_url['18'][0]

#	all_url = {k:[v+".f%03d" % fvhr for fvhr in range(forecast_valid_start,forecast_valid_limit+1,forecast_valid_step)] for k,v in urls.items()}
	all_idx_url = {k:[v+".f%03d.idx" % fvhr for fvhr in range(forecast_valid_start,forecast_valid_limit+1,forecast_valid_step)] for k,v in urls.items()}

	return all_url,all_idx_url

def generate_url_files(dpath,urls,cdate=None):
	# Date for which forecast data is being generated starting from forecast_at_start
	if not cdate:
		cdate = datetime.datetime.now().strftime("%Y%m%d")
	urlpath = os.path.join(dpath,cdate)
	if not os.path.exists(urlpath):
		os.mkdir(urlpath)
	grib_urls = urls[0]
	grib_idx_urls = urls[1]
	fcst_base_url_file = "%s_%s_gfs_fcst_urls.csv"
	fcst_base_url_idx_file = "%s_%s_gfs_fcst_idx_urls.csv"


	for fcst_at,grib_url in grib_urls.items():
		fcst_at_fpath = os.path.join(urlpath,fcst_at)
		fcst_at_f = fcst_base_url_file % (cdate,fcst_at)
		with open(os.path.join(urlpath,fcst_at_f),"w") as fcst_file:
			for gurl in grib_url:
				fcst_file.write(gurl+"\n")
		fcst_file.close()

if __name__ ==  "__main__":
	print len(sys.argv)
	if os.environ.has_key('dls_path'):
		dls_path = os.environ['dls_path']
		fname = 'gfs_fcst_url_gen_parameter.csv'
		fpath = os.path.join(dls_path,'dls-para',fname)
		if len(sys.argv) <= 1:
			cdate = datetime.datetime.now().strftime("%Y%m%d")
			fpara = read_parameters(os.path.join(dls_path,'dls-para',fname))
		else:
			cdate = sys.argv[1]
			fpara = read_parameters(os.path.join(dls_path,'dls-para',fname))
		print cdate
		durls = generate_url(fpara,cdate)
		generate_url_files(os.path.join(dls_path,'dls-urls'),durls,cdate)

