import pygrib
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib. path import Path
from matplotlib.colors import rgb2hex
from mpl_toolkits.basemap import Basemap, shiftgrid
from mpl_toolkits.basemap import interp
import numpy as np
import math
from uvunify import uvect, vvect, uvdir
import geojson
from geojson import Feature, LineString, Polygon, MultiPolygon,FeatureCollection
import os
import pyproj

def get_pres_msl_contour(left,bottom,top,right,t,fv):

	if os.environ.has_key('dls_path'):
		dls_path = os.environ['dls_path']

	w,h,dpi,fs=800,600,40,6
	fig = figure(figsize=(w/dpi,h/dpi))
	plt.figure(figsize=(w/dpi,h/dpi))
	
#	grib = '/home/megha/Synergy/gis_project/development/experiments/netcdf/SynergyTestData/GRIB/GFS/20161010/06/gfs.t06z.pgrb2.0p25.f006' 
	grib = os.path.join(dls_path,'dls-data','%s/%s/gfs.t%02dz.pgrb2.0p25.f%03d' % (t[:8],t[8:11],int(t[8:11]),fv))

#	grbs = pygrib.open(grib)
	grbs = pygrib.index(grbf,'shortName','typeOfLevel','level')
#	grbs.seek(0)

#	prmsl = grbs.message(414)	

#	prmsl = grbs.select(name='Pressure reduced to MSL',typeOfLevel="meanSea",level=0)
	uin = grbs.select(shortName='10u',typeOfLevel="heightAboveGround",level=10)[0]
	vin = grbs.select(shortName='10v',typeOfLevel="heightAboveGround",level=10)[0]
#	uin = grbs.select(name='10 metre U wind component')[0]
#	vin = grbs.select(name='10 metre V wind component')[0]

	presdata = grbs.select(shortName="prmsl",typeOfLevel="meanSea",level=0)

	tgrb = presdata[0]

	lt1, lt2, ln1, ln2 = bottom,top,left,right 		#	18.0, 28.0, 53.0, 63.0
#	lt1, lt2, ln1, ln2 = math.floor(bottom),math.ceil(top),math.floor(left),math.ceil(right) 		#	18.0, 28.0, 53.0, 63.0
#	lt1, lt2, ln1, ln2 = 22.50, 28.70, 68.6, 72.9 # 18.0, 28.0, 53.0, 63.0
#	print lt1, lt2, ln1, ln2
	udata, lats, lons = uin.data(lat1=lt1,lat2=lt2,lon1=ln1,lon2=ln2)
	vdata, lats, lons = vin.data(lat1=lt1,lat2=lt2,lon1=ln1,lon2=ln2)

	wspeed = np.sqrt(udata*udata + vdata*vdata) * 1.94384

	mwdir = np.arctan2(udata,vdata) * 180/np.pi

	mudata = uvect(mwdir)
	mvdata = vvect(mwdir)

	presdata, lats, lons = tgrb.data(lat1=lt1,lat2=lt2,lon1=ln1,lon2=ln2)
	presdata = presdata * 0.01

	map = Basemap(projection='merc', llcrnrlat=lt1, urcrnrlat=lt2,llcrnrlon=ln1, urcrnrlon=ln2, resolution='h')

	x, y = map(lons, lats)
	ccx, ccy= map(lons, lats, inverse=True)

	# 1 degree resolution data
	yy = np.arange(0,y.shape[0], 1)
	xx = np.arange(0,x.shape[0], 1)

	points = np.meshgrid(yy,xx)

	parallels = np.arange(-90.,91.,1.)

	# Label the meridians and parallels
	map.drawparallels(parallels,labels=[False,True,True,False],fontsize=fs)

	# Draw Meridians and Labels
	meridians = np.arange(-180.,181.,1.)
	map.drawmeridians(meridians,labels=[False,False,False,True],fontsize=fs)

	map.drawcoastlines(color = 'k')

	pres_min = np.min(presdata)
	pres_max = np.max(presdata)
	pres_diff = (pres_max - pres_min) / 10.0

	pdn = np.arange(pres_min,pres_max+pres_diff,pres_diff)


	pres_min = int(math.floor(np.min(presdata)))
	pres_max = int(math.ceil(np.max(presdata)))
	pres_diff = int(math.ceil((pres_max - pres_min) / 10.0))

	levs = range(pres_min,pres_max+pres_diff,pres_diff)

	cswf = map.contourf(x,y,wspeed,cmap=plt.cm.jet, alpha=.5)
#	cswf = map.contourf(x[points],y[points],wspeed[points],cmap=plt.cm.jet, alpha=.5)
	cb = map.colorbar(location='right', pad="12%")
	cb.ax.tick_params(labelsize=8)

	epsg_3395 = pyproj.Proj(init='epsg:3395')
	epsg_3857 = pyproj.Proj(init='epsg:3857')
	epsg_4326 = pyproj.Proj(init='epsg:4326')
	tp = pyproj.Proj(proj='utm', zone=40, ellps='WGS84')

	
	poly_features = []
	for cidx,collection in enumerate(cswf.collections):	
		paths = collection.get_paths()
		color = collection.get_facecolor()
		for pidx,path in enumerate(paths):			
			coordinates = []
			polyscoords = []
			codes = path.codes
			for code,segment in zip(codes,path.iter_segments()):
				tlon, tlat = segment[0][0], segment[0][1]
				coordinates.append((tlon, tlat))
				if code == Path.CLOSEPOLY:
					polyscoords.append(coordinates)
					coordinates = []		
			polyhs= Polygon(polyscoords)
			properties = { "stroke-width": 1,"stroke":rgb2hex(color[0]),"stroke-opacity": 0.5,"fill":rgb2hex(color[0]),"fill-opacity": 0.5,"label":cidx}
			poly_features.append(Feature(geometry=polyhs, properties=properties))

	poly_feature_properties = {"name":"WS", "level":10, "unit": "m", "levelName":"10 m"}
	poly_feature_collection = FeatureCollection(poly_features,properties=poly_feature_properties)

#	poly_geojson_dump = geojson.dumps(poly_feature_collection, sort_keys=True)

#	with open('ws10_poly.geojson', 'w') as fileout:
#	    fileout.write(poly_geojson_dump)        


	## Experiment for black arrow
	map.quiver(x[points],y[points],-mudata[points],-mvdata[points], color='k', scale=24, headlength=6, headwidth=7, pivot='mid')


	csw = map.contour(x,y,presdata,levs,linewidths=2,colors='k')
	#csw = map.contour(x,y,presdata,linewidths=2,colors='k')
	plt.clabel(csw,inline=1,inline_spacing=1,fontsize=12,fmt='%1.0f',colors='k',fontproperties={'weight': 'bold'})

	line_features = []
	lidx = 0
	for collection in csw.collections:
	#	print "Processing ", collection.properties()
		paths = collection.get_paths()
		color = collection.get_edgecolor()
		for path in paths:
			v = path.vertices
			coordinates = []
			for i in range(len(v)):
				lon = v[i][0]
				lat = v[i][1]
	#			tlon, tlat = map(lon,lat,inverse=True)
	#			coordinates.append((lat, lon))
				tlat, tlon = lat, lon
	#			tlon, tlat = tp(lon,lat,inverse=True)
	#			tlon, tlat = t2(lon,lat,inverse=True)
				coordinates.append((tlon, tlat))
			line = LineString(coordinates)
			properties = {
				"stroke-width": 3,
	            "stroke": rgb2hex(color[0]),
	            "label": '%d'%csw.levels[lidx]
	            }
			line_features.append(Feature(geometry=line, properties=properties))
		lidx=lidx+1

	
	prmsl_feature_properties = {"name":"PRMSL", "level":0, "levelName":"Mean Sea Level"}
	prmsl_feature_collection = FeatureCollection(line_features,properties=prmsl_feature_properties)


#	prmsl_geojson_dump = geojson.dumps(prmsl_feature_collection, sort_keys=True)

#	with open('prmsl_contour.geojson', 'w') as fileout:
#	    fileout.write(prmsl_geojson_dump)        

	prmsl_ws10m_feature_collection = FeatureCollection([poly_feature_collection, prmsl_feature_collection])
	prmsl_ws10m_geojson_dump = geojson.dumps(prmsl_ws10m_feature_collection, sort_keys=True)

#	plt.figure(figsize=(800/dpi,800/dpi))
	#plt.savefig('/home/megha/Synergy/gis_project/development/synergygis_project/synergygis/media/images/10102016_prmsl_wnd10m_cont_120dpi_h24_op5_025_5827.png', bbox_inches='tight', dpi=dpi)

#	plt.show()

	
	return prmsl_ws10m_geojson_dump


#	lon = 290
#	lat = 41

#	lx, ly = map(lon, lat)


#	map.plot(lx, ly, '*', c='k', ms=18, mew=2, latlon=True, label='Location')

	#plt.title('MSL Pressure (mb) & 10m Wind 10/10/2016 12:00',fontsize=10)
	#plt.title('Valid (21/09/2016)')
	#plt.savefig('1010201612_tmp2m_wnd10m.png')

def get_contours(bottom,top,left,right,t,fv):
#	print "Initialising Parameters"
	if os.environ.has_key('dls_path'):
		dls_path = os.environ['dls_path']
	lt1, lt2, ln1, ln2 = bottom,top,left,right
	w,h,dpi,fs=800,600,40,6
	plt.figure(figsize=(w/dpi,h/dpi))

	contmap = Basemap(llcrnrlat=lt1, urcrnrlat=lt2,llcrnrlon=ln1, urcrnrlon=ln2, resolution='h', epsg=4326)
	parallels = np.arange(-90.,91.,1.)

	# Label the meridians and parallels
	contmap.drawparallels(parallels,labels=[False,True,True,False],fontsize=fs)

	# Draw Meridians and Labels
	meridians = np.arange(-180.,181.,1.)
	contmap.drawmeridians(meridians,labels=[False,False,False,True],fontsize=fs)
	contmap.drawcoastlines(color = 'k')

	
#	grib = '/home/megha/Synergy/gis_project/development/experiments/netcdf/SynergyTestData/GRIB/GFS/20161010/06/gfs.t06z.pgrb2.0p25.f006' 
#	grib = '/home/megha/Synergy/gis_project/development/experiments/netcdf/SynergyTestData/GRIB/GFS/%s/%s/gfs.t%02dz.pgrb2.0p25.f%03d' % (t[:8],t[8:11],int(t[8:11]),fv)
	grib = os.path.join(dls_path,'dls-data','%s/%s/gfs.t%02dz.pgrb2.0p25.f%03d' % (t[:8],t[8:11],int(t[8:11]),fv))
	grbs = pygrib.index(grib,'shortName','typeOfLevel','level')
#	grbs = pygrib.open(grib)

#	grbs.seek(0)

#	print "Processing Wind Parameters"
### Wind speed and wind direction	
	uin = grbs.select(shortName='10u',typeOfLevel="heightAboveGround",level=10)[0]
	vin = grbs.select(shortName='10v',typeOfLevel="heightAboveGround",level=10)[0]

	udata, lats, lons = uin.data(lat1=lt1,lat2=lt2,lon1=ln1,lon2=ln2)
	vdata, lats, lons = vin.data(lat1=lt1,lat2=lt2,lon1=ln1,lon2=ln2)

	x, y = contmap(lons, lats)
#	print "\tProcessing Wind Speed"
	##	Wind Speed
	wspeed = np.sqrt(udata*udata + vdata*vdata) * 1.94384
	ws_min = int(np.min(wspeed))
	ws_max = int(np.max(wspeed))
#	ws_diff = (ws_max-ws_min)/5.0
#	ws_levs = range(ws_min,ws_max+1,5)
	ws_levs = range(1,50,5) + range(51,100,10)
	wspeed_contoursf = contmap.contourf(x,y,wspeed,ws_levs,cmap=plt.cm.jet, alpha=.5)	
	#	wspeed_contoursf = map.contourf(x[points],y[points],wspeed[points],cmap=plt.cm.jet, alpha=.5)
	cb = contmap.colorbar(location='right', pad="12%")
	cb.ax.tick_params(labelsize=8)

	import pyproj

	epsg_3395 = pyproj.Proj(init='epsg:3395')
	epsg_3857 = pyproj.Proj(init='epsg:3857')
	epsg_4326 = pyproj.Proj(init='epsg:4326')

	## GeoJSON for windspeed filled contours
	wspeed_features = []
	ws10m_levs = wspeed_contoursf.levels
	for cidx,collection in enumerate(wspeed_contoursf.collections):	
		paths = collection.get_paths()
		color = collection.get_facecolor()
		for pidx,path in enumerate(paths):			
			coordinates = []
			polyscoords = []
			codes = path.codes
			for code,segment in zip(codes,path.iter_segments()):
#				tlon, tlat = pyproj.transform(epsg_3857,epsg_4326, segment[0][0], segment[0][1])
				tlon, tlat = segment[0][0], segment[0][1]
				coordinates.append((tlon, tlat))
				if code == Path.CLOSEPOLY:
					polyscoords.append(coordinates)
					coordinates = []		
			polyhs= Polygon(polyscoords)
			properties = { "stroke-width": 1,"stroke":rgb2hex(color[0]),"stroke-opacity": 0.5,"fill":rgb2hex(color[0]),"fill-opacity": 0.5,"label":wspeed_contoursf.levels[cidx]}
			wspeed_features.append(Feature(geometry=polyhs, properties=properties))

	wspeed_feature_properties = {"name":"WS10m", "level":10, "unit": "m", "levelName":"10 m"}
	wspeed_feature_collection = FeatureCollection(wspeed_features,properties=wspeed_feature_properties)

        u925 = grbs.select(shortName="u",typeOfLevel="isobaricInhPa",level=925)[0]
        v925 = grbs.select(shortName="v",typeOfLevel="isobaricInhPa",level=925)[0]

	u925data, lats, lons = u925.data(lat1=lt1,lat2=lt2,lon1=ln1,lon2=ln2)
	v925data, lats, lons = v925.data(lat1=lt1,lat2=lt2,lon1=ln1,lon2=ln2)

#	x, y = contmap(lons, lats)
#	print "\tProcessing Wind Speed"
	##	Wind Speed
	wspeed925 = np.sqrt(u925data*u925data + v925data*v925data) * 1.94384
	ws925_min = int(np.min(wspeed925))
	ws925_max = int(np.max(wspeed925))
#	ws_diff = (ws_max-ws_min)/5.0
#	ws_levs = range(ws_min,ws_max+1,5)
	ws_levs = range(1,50,5) + range(51,100,10)
	wspeed925_contoursf = contmap.contourf(x,y,wspeed925,ws_levs,cmap=plt.cm.jet, alpha=.5)	
	#	wspeed_contoursf = map.contourf(x[points],y[points],wspeed[points],cmap=plt.cm.jet, alpha=.5)
	cb = contmap.colorbar(location='right', pad="12%")
	cb.ax.tick_params(labelsize=8)

	wspeed925_features = []
	ws925m_levs = wspeed925_contoursf.levels
	for cidx,collection in enumerate(wspeed925_contoursf.collections):	
		paths = collection.get_paths()
		color = collection.get_facecolor()
		for pidx,path in enumerate(paths):			
			coordinates = []
			polyscoords = []
			codes = path.codes
			for code,segment in zip(codes,path.iter_segments()):
#				tlon, tlat = pyproj.transform(epsg_3857,epsg_4326, segment[0][0], segment[0][1])
				tlon, tlat = segment[0][0], segment[0][1]
				coordinates.append((tlon, tlat))
				if code == Path.CLOSEPOLY:
					polyscoords.append(coordinates)
					coordinates = []		
			polyhs= Polygon(polyscoords)
			properties = { "stroke-width": 1,"stroke":rgb2hex(color[0]),"stroke-opacity": 0.5,"fill":rgb2hex(color[0]),"fill-opacity": 0.5,"label":wspeed925_contoursf.levels[cidx]}
			wspeed925_features.append(Feature(geometry=polyhs, properties=properties))

	wspeed925_feature_properties = {"name":"WS925mb", "level":925, "unit": "hpa", "levelName":"925mb"}
	wspeed925_feature_collection = FeatureCollection(wspeed925_features,properties=wspeed925_feature_properties)



        u975 = grbs.select(shortName="u",typeOfLevel="isobaricInhPa",level=975)[0]
        v975 = grbs.select(shortName="v",typeOfLevel="isobaricInhPa",level=975)[0]

	u975data, _, _ = u975.data(lat1=lt1,lat2=lt2,lon1=ln1,lon2=ln2)
	v975data, _, _ = v975.data(lat1=lt1,lat2=lt2,lon1=ln1,lon2=ln2)

#	x, y = contmap(lons, lats)
#	print "\tProcessing Wind Speed"
	##	Wind Speed
	wspeed975 = np.sqrt(u975data*u975data + v975data*v975data) * 1.94384
	ws975_min = int(np.min(wspeed975))
	ws975_max = int(np.max(wspeed975))
#	ws_diff = (ws_max-ws_min)/5.0
#	ws_levs = range(ws_min,ws_max+1,5)
	ws_levs = range(1,50,5) + range(51,100,10)
	wspeed975_contoursf = contmap.contourf(x,y,wspeed975,ws_levs,cmap=plt.cm.jet, alpha=.5)	
	#	wspeed_contoursf = map.contourf(x[points],y[points],wspeed[points],cmap=plt.cm.jet, alpha=.5)
	cb = contmap.colorbar(location='right', pad="12%")
	cb.ax.tick_params(labelsize=8)

	wspeed975_features = []
	ws975m_levs = wspeed975_contoursf.levels
	for cidx,collection in enumerate(wspeed975_contoursf.collections):	
		paths = collection.get_paths()
		color = collection.get_facecolor()
		for pidx,path in enumerate(paths):			
			coordinates = []
			polyscoords = []
			codes = path.codes
			for code,segment in zip(codes,path.iter_segments()):
#				tlon, tlat = pyproj.transform(epsg_3857,epsg_4326, segment[0][0], segment[0][1])
				tlon, tlat = segment[0][0], segment[0][1]
				coordinates.append((tlon, tlat))
				if code == Path.CLOSEPOLY:
					polyscoords.append(coordinates)
					coordinates = []		
			polyhs= Polygon(polyscoords)
			properties = { "stroke-width": 1,"stroke":rgb2hex(color[0]),"stroke-opacity": 0.5,"fill":rgb2hex(color[0]),"fill-opacity": 0.5,"label":wspeed975_contoursf.levels[cidx]}
			wspeed975_features.append(Feature(geometry=polyhs, properties=properties))

	wspeed975_feature_properties = {"name":"WS975mb", "level":975, "unit": "hpa", "levelName":"975mb"}
	wspeed975_feature_collection = FeatureCollection(wspeed975_features,properties=wspeed975_feature_properties)

	ccx, ccy= contmap(lons, lats, inverse=True)

	# 1 degree resolution data
	yy = np.arange(0,y.shape[0], 1)
	xx = np.arange(0,x.shape[0], 1)

	points = np.meshgrid(yy,xx)

#	print "\tProcessing Wind Direction"
## Wind Direction
	mwdir = np.arctan2(udata,vdata) * 180/np.pi

	mudata = uvect(mwdir)
	mvdata = vvect(mwdir)

	## Experiment for black arrow
	contmap.quiver(x[points],y[points],-mudata[points],-mvdata[points], color='k', scale=24, headlength=6, headwidth=7, pivot='mid')

#	print "Processing PRMSL Parameters"
### PRMSL Isolines
	raw_prmsl_data = grbs.select(shortName="prmsl",typeOfLevel="meanSea",level=0)

	prmsl_data, lats, lons = raw_prmsl_data[0].data(lat1=lt1,lat2=lt2,lon1=ln1,lon2=ln2)
	prmsl_data = prmsl_data * 0.01

	prmsl_min = int(math.floor(np.min(prmsl_data)))
	prmsl_max = int(math.ceil(np.max(prmsl_data)))
	prmsl_diff = 1#int(math.ceil((prmsl_max - prmsl_min) / 2.0))

	prmsl_levs = range(prmsl_min,prmsl_max+prmsl_diff,prmsl_diff)
	prmsl_isolines = contmap.contour(x,y,prmsl_data,prmsl_levs,linewidths=2,colors='k')
	#csw = map.contour(x,y,prmsl_data,linewidths=2,colors='k')
	plt.clabel(prmsl_isolines,inline=1,inline_spacing=1,fontsize=12,fmt='%1.0f',colors='k',fontproperties={'weight': 'bold'})

	prmsl_isolines_features = []	
	for lidx,collection in enumerate(prmsl_isolines.collections):
		paths = collection.get_paths()
		color = collection.get_edgecolor()
		coordinates = []
		for patphidx,path in enumerate(paths):		
			for segment in path.iter_segments():
#				tlon, tlat = pyproj.transform(epsg_3857,epsg_4326, segment[0][0], segment[0][1])
				tlon, tlat = segment[0][0], segment[0][1]
				coordinates.append((tlon, tlat))
   			if patphidx%2 == 1:
				line = LineString(coordinates)
				properties = {
					"stroke-width": 3,
		            "stroke": rgb2hex(color[0]),
		            "label": '%d'%prmsl_isolines.levels[lidx]
		            }
				prmsl_isolines_features.append(Feature(geometry=line, properties=properties))
				coordinates = []

		"""		
		for path in paths:
			for segment in path.iter_segments():
				tlon, tlat = segment[0][0], segment[0][1]
				coordinates.append((tlon, tlat))
		line = LineString(coordinates)
		properties = {
			"stroke-width": 3,
            "stroke": rgb2hex(color[0]),
            "label": '%d'%prmsl_isolines.levels[lidx]
            }
		prmsl_isolines_features.append(Feature(geometry=line, properties=properties))
		"""

	
	prmsl_feature_properties = {"name":"PRMSL", "level":0, "levelName":"Mean Sea Level"}
	prmsl_feature_collection = FeatureCollection(prmsl_isolines_features,properties=prmsl_feature_properties)

	plt.cla()
	plt.clf()
	
### Temperature 2m Contour
	rawtempdata = grbs.select(shortName="2t",typeOfLevel="heightAboveGround",level=2)

	tempdata, lats, lons = rawtempdata[0].data(lat1=lt1,lat2=lt2,lon1=ln1,lon2=ln2)
	tempdata = tempdata - 273

	temp_min = int(math.floor(np.min(tempdata)))
	temp_max = int(math.ceil(np.max(tempdata)))
	temp_diff = int(math.ceil((temp_max - temp_min) / 5.0))

#	temp_levs = range(temp_min,temp_max+temp_diff,temp_diff)
	temp_levs = range(-50,61,2)

	temp2m_contours = contmap.contourf(x,y,tempdata,temp_levs,cmap=plt.cm.coolwarm, alpha=.5)
#	temp2m_contours = map.contourf(x[points],y[points],wspeed[points],cmap=plt.cm.jet, alpha=.5)
	cb = contmap.colorbar(location='right', pad="12%")
	cb.ax.tick_params(labelsize=8)

	temp2m_cont_features = []
	temp2m_levs = temp2m_contours.levels
	for cidx,collection in enumerate(temp2m_contours.collections):	
		paths = collection.get_paths()
		color = collection.get_facecolor()
		for pidx,path in enumerate(paths):			
			coordinates = []
			polyscoords = []
			codes = path.codes
			for code,segment in zip(codes,path.iter_segments()):
#				tlon, tlat = pyproj.transform(epsg_3857,epsg_4326, segment[0][0], segment[0][1])
				tlon, tlat = segment[0][0], segment[0][1]
				coordinates.append((tlon, tlat))
				if code == Path.CLOSEPOLY:
					polyscoords.append(coordinates)
					coordinates = []		
			polyhs= Polygon(polyscoords)
			properties = { "stroke-width": 1,"stroke":rgb2hex(color[0]),"stroke-opacity": 0.5,"fill":rgb2hex(color[0]),"fill-opacity": 0.5,"label":temp2m_levs[cidx]}
			temp2m_cont_features.append(Feature(geometry=polyhs, properties=properties))

	temp2m_cont_features_properties = {"name":"TMP2m", "level":2, "unit": "m", "levelName":"2 m"}
	temp2m_cont_features_collection = FeatureCollection(temp2m_cont_features,properties=temp2m_cont_features_properties)

	plt.cla()
	plt.clf()
	
### Humidity 2m Contour	
	rawhumiditydata = grbs.select(shortName="r",typeOfLevel="heightAboveGround",level=2)
	humidity_data, lats, lons = rawhumiditydata[0].data(lat1=lt1,lat2=lt2,lon1=ln1,lon2=ln2)

	humidity_min = int(math.floor(np.min(humidity_data)))
	humidity_max = int(math.ceil(np.max(humidity_data)))
	humidity_diff = int(math.ceil((humidity_max - humidity_min) / 5.0))

#	humidity_levs = range(humidity_min,humidity_max+humidity_diff,humidity_diff)
	humidity_levs = range(1,101,5)
	humidity_contour = contmap.contourf(x,y,humidity_data,humidity_levs,cmap=plt.cm.jet, alpha=.5)
	cb = contmap.colorbar(location='right', pad="12%")
	cb.ax.tick_params(labelsize=8)

	hmdt2m_features = []
	hmdt2m_levs = humidity_contour.levels
	for cidx,collection in enumerate(humidity_contour.collections):	
		paths = collection.get_paths()
		color = collection.get_facecolor()
		for pidx,path in enumerate(paths):			
			coordinates = []
			polyscoords = []
			codes = path.codes
			for code,segment in zip(codes,path.iter_segments()):
				tlon, tlat = segment[0][0], segment[0][1]
				coordinates.append((tlon, tlat))
				if code == Path.CLOSEPOLY:
					polyscoords.append(coordinates)
					coordinates = []		
			polyhs= Polygon(polyscoords)
			properties = { "stroke-width": 1,"stroke":rgb2hex(color[0]),"stroke-opacity": 0.5,"fill":rgb2hex(color[0]),"fill-opacity": 0.5,"label":hmdt2m_levs[cidx]}
			hmdt2m_features.append(Feature(geometry=polyhs, properties=properties))

	hmdt2m_cont_features_properties = {"name":"HMDT2m", "level":2, "unit": "m", "levelName":"2 m"}
	hmdt2m_cont_features_collection = FeatureCollection(hmdt2m_features,properties=hmdt2m_cont_features_properties)

	plt.cla()
	plt.clf()
	plt.get_fignums()

### APCP Contour
	rawapcpdata = grbs.select(shortName="tp",typeOfLevel="surface",level=0)
	apcp_data, lats, lons = rawapcpdata[0].data(lat1=lt1,lat2=lt2,lon1=ln1,lon2=ln2)

	apcp_min = int(math.floor(np.min(apcp_data)))
	apcp_max = int(math.ceil(np.max(apcp_data)))
	apcp_diff = int(math.ceil((apcp_max - apcp_min) / 5.0))

#	apcp_levs = range(apcp_min,apcp_max+apcp_diff,apcp_diff)
	apcp_levs = range(0,81,2)
	apcp_contour = contmap.contourf(x,y,apcp_data,apcp_levs,cmap=plt.cm.jet, alpha=.5)
#	cswf = map.contourf(x[points],y[points],wspeed[points],cmap=plt.cm.jet, alpha=.5)
	cb = contmap.colorbar(location='right', pad="12%")
	cb.ax.tick_params(labelsize=8)

	apcp_features = []
	apcp_levs = apcp_contour.levels
	for cidx,collection in enumerate(apcp_contour.collections):	
		paths = collection.get_paths()
		color = collection.get_facecolor()
		for pidx,path in enumerate(paths):			
			coordinates = []
			polyscoords = []
			codes = path.codes
			for code,segment in zip(codes,path.iter_segments()):
				tlon, tlat = segment[0][0], segment[0][1]
				coordinates.append((tlon, tlat))
				if code == Path.CLOSEPOLY:
					polyscoords.append(coordinates)
					coordinates = []		
			polyhs= Polygon(polyscoords)
			properties = { "stroke-width": 1,"stroke":rgb2hex(color[0]),"stroke-opacity": 0.5,"fill":rgb2hex(color[0]),"fill-opacity": 0.5,"label":apcp_levs[cidx]}
			apcp_features.append(Feature(geometry=polyhs, properties=properties))

	apcp_cont_features_properties = {"name":"APCP", "level":0, "unit": "m", "levelName":"surface"}
	apcp_cont_feature_collection = FeatureCollection(apcp_features,properties=apcp_cont_features_properties)

	plt.cla()
	plt.clf()
	plt.get_fignums()
	plt.close('all')
	other_properties = {"timestamp" : t, "hour": fv}
	prmsl_ws10m_temp2m_feature_collection = FeatureCollection([wspeed_feature_collection,prmsl_feature_collection,temp2m_cont_features_collection,hmdt2m_cont_features_collection,apcp_cont_feature_collection,wspeed925_feature_collection,wspeed975_feature_collection], properties=other_properties)
	prmsl_ws10m_temp2m_geojson_dump = geojson.dumps(prmsl_ws10m_temp2m_feature_collection, sort_keys=True)

	return prmsl_ws10m_temp2m_feature_collection
#	return prmsl_ws10m_temp2m_geojson_dump

def get_multi_contours(bottom,top,left,right,dtm,fv):
	tms = range(1,50,3)
#	tms = [1,4,7,10]
	features = []
	for idx,t in enumerate(tms):
		feature = get_contours(bottom,top,left,right,dtm,t)
		features.append(feature)
   	raster_datas = FeatureCollection(features)
   	return geojson.dumps(raster_datas)


if __name__ ==  "__main__":
#	b=19.926877111209265&t=21.652322721683646&l=70.91198729351163&r=73.21911619976163
#	get_pres_msl_contour(left,bottom,top,right,t,fv)

#	geojson_data = get_pres_msl_contour(69.111198729351163, 18.926877111209265, 22.22322721683646, 72.81911619976163,"2016101006",6)	
#	geojson_data = get_pres_msl_contour(70.80078106373549,13.089288487776358,19.289542354858398,77.12890606373547,"2016111906",6)	
	"""
	dtm = "2017040612"
	tms = [1,4,7,10,13,16,19,22]
	features = []
	for idx,t in enumerate(tms):
		feature = get_contours(13.089288487776358,19.289542354858398,70.80078106373549,77.12890606373547,dtm,t)
		features.append(feature)
   	raster_datas = FeatureCollection(features)
	with open('contours_%s.geojson' % dtm, 'w') as fileout:
		fileout.write(geojson.dumps(raster_datas))
#	    fileout.write(raster_datas)    
	"""
#        locations = [(56.066667,3.133333),(42.683333,4.583333),(72.570314,20.972214),(40.5,288.283333),(24.583333,316.416667)
        locations = [(11.783333,9.916667),(25.766667,54.516667),
		(15.683333,94.283333),(10.511667,100.286667),(4.7775,112.258333),(21.333333,114.85),]
	dtm = "2017040612"

        dt = dtm[:8]
        tm = dtm[8:]
	if os.environ.has_key('dls_path'):
		dls_path = os.environ['dls_path']

	for idx,location in enumerate(locations):
		idx=idx+3
		if location[1] < 2.5:
			ln1,ln2,lt1,lt2 = 0,5,location[0]-2.5,location[0]+2.5
		elif location[1]>357.5:
			ln1,ln2,lt1,lt2 = 355,359.75,location[0]-2.5,location[0]+2.5
		else:			
			lt1, lt2, ln1, ln2 = location[0]-2.5,location[0]+2.5,location[1]-2.5,location[1]+2.5
		#print lt1, lt2, ln1, ln2, dt, tm, grbf			
		wrjson_data = get_multi_contours(lt1, lt2, ln1, ln2,dtm,tm)
#		wjson_data = get_weather_data(lt1, lt2, ln1, ln2, dt, tm)
		ofn = 'lc_raster_%d_%s.geojson' % (idx,dtm)
		ojsonf = os.path.join(dls_path,'dls-data',dt, tm,ofn)
		with open(ojsonf,'w') as wf:
			wf.write(wrjson_data)
		print "Generated geojson %s" % ofn
