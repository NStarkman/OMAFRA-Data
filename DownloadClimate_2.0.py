# Download file automatically using urllib.request and Python 3:
# https://stackoverflow.com/a/8286449
# Download page:
# http://climate.weather.gc.ca/historical_data/search_historic_data_e.html
# Download daily/hourly climate data csv files from EnvCan for given year.
# Kristen Murchinson for AAFC
import os
import time
import calendar
import urllib.request
from datetime import date

#search of stations with available weather data: http://climate.weather.gc.ca/historical_data/search_historic_data_stations_e.html?searchType=stnProv&timeframe=1&lstProvince=&optLimit=yearRange&StartYear=1840&EndYear=2019&Year=2019&Month=7&Day=28&selRowPerPage=25
#station ID's can be found in the url of a data file that is being viewed


class Station:
	def __init__(self, name, id, firstyear, lastyear):
		self.name = name
		self.id = id
		self.firstyear = firstyear
		self.lastyear = lastyear


# creating list        
list = []

list.append( Station('Norfolk', '27528', 2011, date.today().year) )
list.append( Station('Simcoe', '27604', 2011, date.today().year) )
list.append( Station('Wellington Centre', '41983', 2011, date.today().year) )
list.append( Station('Wellington North', '7844', 2011, date.today().year))
list.append( Station('Huron', '7747', 2011, date.today().year) )
list.append( Station('Essex', '30266', 2011, date.today().year) )
list.append( Station('Kemptville', '27534', 2011, date.today().year) )
list.append( Station('Durham', '48649', 2011, date.today().year) )
list.append( Station('Peterborough', '48952', 2011, date.today().year) )
list.append( Station('Chatham-Kent', '32473', 2011, date.today().year) )
list.append( Station('Sudbury', '50840', 2011, date.today().year) )
list.append( Station('Timiskaming', '47687', 2011, date.today().year) )
list.append( Station('Lambton', '44323', 2011, date.today().year) )
list.append( Station('Trenton', '5126', 2011, date.today().year) )
list.append( Station('Middlesex', '10999', 2011, date.today().year) )
list.append( Station('Bruce', '54259', 2011, date.today().year) )
list.append( Station('Renfrew', '6900', 2011, date.today().year))
list.append( Station('Thunder Bay', '49389', 2011, date.today().year))

root = os.getcwd()
for obj in list:
	station_name = obj.name
	# create a folder for the station ...
	# define the name of the directory to be created

	path = root+'/'+str(obj.name)

	try:
		os.mkdir(path)
	except OSError:
		print ("Creation of the directory %s failed or it already exists" % path)
	else:
		print ("Successfully created the directory %s " % path)

	# moving into station folder
	os.chdir(path)

	# create file name in right format eng-daily-01012017-12312017.csv
	A=('01','02','03','04','05','06','07','08','09','10','11','12')  #array of month numbers
	dwn='urllib' #options firefox explorer urllib <-- urllib works, firefox and explorer currently do not
	parent=os.getcwd()

	for k in range(obj.firstyear,obj.lastyear + 1): #set year range
		yr=k

		if calendar.isleap(yr)==True:
			B=('31','29','31','30','31','30','31','31','30','31','30','31') #array of last day of month numbers (leap year)
		else:
			B=('31','28','31','30','31','30','31','31','30','31','30','31') #array of last day of month numbers (not leap year)



		# create a folder for each iteration and name it by year ...
		# define the name of the directory to be created
		path = parent+'/'+str(k)

		try:
			os.mkdir(path)
		except OSError:
			print ("Creation of the directory %s failed or it already exists" % path)
		else:
			print ("Successfully created the directory %s " % path)

		# moving into folder to download csv(s)
		os.chdir(path)

		#downloading the daily data (1 file for the selected year) and hourly data (12 files)


		#URL
		print(obj.id, obj.name)
		url = 'http://climate.weather.gc.ca/climate_data/bulk_data_e.html?format=csv&stationID=' + obj.id + '&Year=' + str(yr) + '&Month=12&Day=1&timeframe=2&submit=Download+Data'
		filename = str(obj.name) + '_' + str(yr) + '_ECCC.csv'
		print(r"Downloading file %s.csv", filename)
		urllib.request.urlretrieve(url, filename)

		#for i in range(0,13):
			#ulr1=('http://climate.weather.gc.ca/climate_data/bulk_data_e.html?format=csv&stationID='+obj.id+'&Year='+str(yr)+'&Month='+str(i)+'&Day='+B[i-1]+'&timeframe=1&submit=Download+Data')
			#fname=('eng-hourly-'+A[i-1]+'01'+str(yr)+'-'+A[i-1]+B[i-1]+str(yr)+'.csv')
			#print(r'downloading  %s' %fname)

			#download request
			#urllib.request.urlretrieve(ulr1, fname)

		os.chdir(parent)
		# return to root dir
	print(root)
	os.chdir(root)
    
