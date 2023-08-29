@echo off
echo 'dowloading ECCC data'
rem Run the Python script
cd "C:\Users\StarkmNa\Documents\Code\OMAFRA-main"
py "C:\Users\StarkmNa\Documents\Code\OMAFRA-main\DownloadClimate_2.0.py"


echo 'downloading Nasa Power files'

rem Run the R script
Rscript "C:\Users\StarkmNa\Documents\Code\OMAFRA-main\download_nasapowerfiles.R"

echo 'updating or generating vcr_dashboard_data.csv'
rem Run another R script
Rscript "C:\Users\StarkmNa\Documents\Code\OMAFRA-main\update_vcr_dashboard.R"

echo 'update complete'

TIMEOUT/T 5

exit
