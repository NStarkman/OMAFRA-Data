#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#creates a .csv file containing 10 years of weather station data to be used 
#with the VCR weather dashboard to calculate the 10 year averages for precipitation and temperature
#requires vcr_dashboard_data.csv with at least 11 years of data for each weather station
#run once at beginning of year
#Created by Mariaelisa Polsinelli for OMAFRA, 2022
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
if (!require("dplyr")){
  install.packages("dplyr")
}
if (!require("lubridate")){
  install.packages("lubridate")
}
library("dplyr")
library("lubridate")

setwd("C:/Users/StarkmNa/Documents/Code/OMAFRA-main")
file_nm <- paste(getwd(), "/", "vcr_dashboard_data.csv", sep="")
curyr <- as.integer((format(as.Date(Sys.Date()), "%Y")))

range <- c((curyr-11), (curyr-1))
vcr_file <- read.csv(file_nm, header = T, sep = ",", check.names = F)
tenyrs <- vcr_file[as.integer(format(as.Date(vcr_file$Date), "%Y")) >= range[1] & as.integer(format(as.Date(vcr_file$Date), "%Y")) <= range[2],]
tenyrs$Date <- format(as.Date(tenyrs$Date), "%m-%d")

averages <- tenyrs %>% group_by(County, Date) %>% summarise_at(vars(Precipitation, GDD,`Carrot Rust Fly`,`Onion Maggot`,
                                                        `Carrot Weevil`, `Aster Leafhopper`, `Tarnished Plant Bug`, `Cabbage Maggot`, `Seedcorn Maggot`,
                                                        `European Corn Borer`), mean)

averages$Date <- as.Date(parse_date_time(averages$Date, c('md', 'ymd')))
year(averages$Date) <- curyr

# Add the Month column here
averages$Month <- format(as.Date(averages$Date), "%m")

# Write the CSV file with the added Month column
write.csv(averages, "ten_year_averages.csv")
