# Files for ONVegetables Blog PowerBi Weather Dashboard

**** Mariaelisa Polsinelli for OMAFRA, 2022 *****

***This readme is outdated. To understand how to properly run the codebase, read the provided VCR Data Guidelines document given with the link to this codebase***

***The files below should be run in the listed order and will be if executing the update_dashboard_files.bat - be sure to update .bat file with the respective file paths on your computer***

**running 3.update_vcr_dashboard.R before running 1. and 2. may result in errors**

1. DownloadClimate_2.0.py
2. download_nasapowerfiles.R
3. update_vcr_dashboard.R
4. gen_10yravgs.R

IMPORTANT:
- **All files should be in the same folder/working directory**
- **Weather stations should be listed as their intended county name (not the ECCC station name) and have the
same form/case in DownloadClimate_2.0.py, 
download_nasapowerfiles.R and update_vcr_dashboard.R**

--------------------------------------
1. DownloadClimate_2.0.py
--------------------------------------
***Created by Kristen Murchinson for AAFC***<br />
Download ECCC climate files for each county listed<br />
Files are saved in seperate folders for each county and then for each year<br />
-> set working directory before running for the first time

add new station as:<br />
list.append("County Name", station ID, year start, year end)<br />
e.g:<br />
list.append( Station('Norfolk', '27528', 2011, date.today().year) )<br />
Here the data from weather station 27528 will be downloaded for Norfolk county from year 2011 to the current year

->saves files under each year folder as 'County name_year_ECCC.csv'<br />
e.g under the file Norfolk will be subfolders 2011, 2012,..., etc. A file in 2011 will be Norfolk_2011_ECCC.csv<br />

--------------------------------------
2. download_nasapowerfiles.R
--------------------------------------
downloads nasapower files for each listed weather station which can be used to replace missing data<br />
-> set working directory before running for the first time

add a new weather station as as sc[[previous number + 1]] <- c("county name", station longitude, station latitude)<br />
station longitude and latitude can be obtained from ECCC weather stations.

-> saves files to the working directory as 'County name_nasapower_.csv'<br />

--------------------------------------
3. update_vcr_dashboard.R
--------------------------------------
Updates or generates new .csv called "vcr_dashboard_data.csv" for the dasboard<br />
-> set working directory before running for the first time<br />
-> If generating a new .csv, at least 11 years of weather satation data are required (make sure to edit years in 1. and 2.)<br />
-> Assumes all weather stations are updated to the same day<br />

To add a new weather station, add new county name to the 'station_list' varaible with quotations ""<br />
e.g. station_list <- c("Bruce", "Thunder Bay", "New County Name")

-> generates or adds data to vcr_dashboard_data.csv

--------------------------------------
4. gen_10yravgs.R
--------------------------------------
creates a .csv file with the averages of the last 11 full years of data (e.g. if 2022, will average years 2011-2021)<br />
Will then be summed in PowerBI to show cumulative averages.<br />
-> set working directory before running for the first time<br />

-> This code only needs to be run once at the beginning of the year to generate a .csv file with data from the past 10 year range. <br /> I.e. if the year is 2022, the 10 year average is calculated from 2011-2021<br />
-> But can be run again if new weather station is added

-> generates or updates ten_year_averages.csv

-------------------------------------
Running update_dashboard_files.bat will run each file in order in the background and can be scheduled with a task scheduler to run daily.
-------------------------------------

