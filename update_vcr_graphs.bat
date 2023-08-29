@echo off
echo 'Create Precipitation Graphs'
rem Run the Python Precip script
cd "C:\Users\StarkmNa\Documents\Code\OMAFRA-main"
py "C:\Users\StarkmNa\Documents\Code\OMAFRA-main\plot_precip.py"

echo 'Create GDD Graphs'
rem Run the Python GDD script
py "C:\Users\StarkmNa\Documents\Code\OMAFRA-main\plot_gdd.py"

echo 'Create Threshhold Table'
rem Run html script
py "C:\Users\StarkmNa\Documents\Code\OMAFRA-main\html_gen.py"

echo 'update complete'

TIMEOUT/T 5

exit
