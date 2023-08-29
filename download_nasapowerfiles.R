#-----------------------------
#Pull nasapower data from multiple coordinates/weather stations and save as .csv
#Mariaelisa Polsinelli for OMAFRA and AAFC
#May 2022
#-----------------------------

if (!require("nasapower")){
  install.packages("nasapower")
}
library(nasapower)


#set working directory to save files into
#default is the source directory
setwd(getwd())


#list of weather station names and coordinates to extract data from
#add new station as sc[[number]] <- c("county name", longitude, latitude)
sc <- list()
sc[[1]] <- c("Norfolk", -80.55,42.87)
sc[[2]] <- c("Essex", -82.9, 42.03)
sc[[3]] <- c("Sudbury", -80.8, 46.63)
sc[[4]] <- c("Chatham-Kent", -81.88, 42.45)
sc[[5]] <- c("Peterborough", -78.36, 44.23)
sc[[6]] <- c("Huron", -81.72, 43.77)
sc[[7]] <- c("Durham", -78.88, 43.92)
sc[[8]] <- c("Thunder Bay", -89.32, 48.37)
sc[[9]] <- c("Bruce", -81.11, 44.74)
sc[[10]] <- c("Kemptville", -75.63, 45)
sc[[11]] <- c("Lambton",-82.3, 43)
sc[[12]] <- c("Middlesex", -81.15, 43.03)
sc[[13]] <- c("Renfrew", -77.25, 45.88)
sc[[14]] <- c("Simcoe", -79.78, 44.23)
sc[[15]] <- c("Trenton", -77.53, 44.12)
sc[[16]] <- c("Wellington Centre", -80.42, 43.65)
sc[[17]] <- c("Wellington North", -80.75, 43.98)
sc[[18]] <- c("Timiskaming", -79.85, 47.7)

#parameters - selected weather data types
#all data types and their abbreviations can be found here https://power.larc.nasa.gov/#resources
#"ALLSKY_SFC_SW_DWN" - all sky surface shortwave downward irradiance (MJ/m^2/day)
#"T2M_MAX" - max temperature (C)
#"T2M_MIN" - min temperature (C)
#"PRECTOTCORR" - precipitation (mm)
climate_data <- c("T2M_MAX","T2M_MIN","PRECTOTCORR")

#choose "hourly", "daily" or "monthly"
time_period <- "daily"

#select date range of data to download (start and end date as "yyyy-mm-dd")
#as.character(Sys.Date()) = current date
date_ranges <- c("2011-03-01", as.character(Sys.Date()-2))

#---CODE BEGINS---------------------------------------------------------------------------

#function to cal get_power for one coordinate set
download_nasapower = function(coordinates, pars_list, date_list,temporal_type ){
  output_file <- get_power(community = "ag",lonlat = coordinates, pars = pars_list, dates = date_list, temporal_api = temporal_type)
  return(output_file)
}

#while loop to parse through station list and call download_nasapower for each coordinate
i <- 1
while (i <= length(sc)){
  power_file <-  download_nasapower(c(as.numeric(sc[[i]][2]),as.numeric(sc[[i]][3])), climate_data, date_ranges, time_period)
  filename <- paste(sc[[i]][1], "nasapower",".csv",sep="_")
  write.csv(power_file, file = filename )
  i <- i + 1
}