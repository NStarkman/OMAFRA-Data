#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#Update .csv data file to be used with ONVegetables Blog PowerBI weather dashboard
#Run Download_climate_2.0.py and download_nasapowerfiles.R prior to using
#all files should be contained in the same working directory
#Created by Mariaelisa Polsinelli for OMAFRA, 2022, updated by Nathan Starkman, 2023
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
if (!require("tidyverse")){
  install.packages("tidyverse")
}
library("tidyverse")

setwd("C:/Users/StarkmNa/Documents/Code/OMAFRA-main")

station_list <- c("Bruce", "Chatham-Kent", "Durham", "Essex", "Huron", "Kemptville",
                  "Lambton", "Middlesex", "Norfolk", "Peterborough", "Renfrew", "Simcoe", "Sudbury",
                  "Timiskaming", "Thunder Bay", "Wellington Centre", "Wellington North")


#------------------------------------------------------------------------------

#check if vcr_dashboard_data.csv exists. If not create file.
file_nm <- paste(getwd(), "/", "vcr_dashboard_data.csv", sep="")

if (file.exists(file_nm)){
  unlink(file_nm)
}
 vcr_file <- data.frame("Longitude"=as.double(), "Latitude"= as.double(), "County"= as.character(), "Date"= as.character(), 	
                         	"Max Temp."=as.double(),	"Min Temp."=as.double(), "Precipitation"=as.double(),
                          "GDD"=as.double(),	"Carrot Rust Fly"=as.double(),	"Onion Maggot"=as.double(), 
                         "Carrot Weevil"=as.double(),	"Aster Leafhopper"=as.double(), 
                          "Tarnished Plant Bug"=as.double(), "Cabbage Maggot"=as.double(), "Seedcorn Maggot"=as.double(),	"European Corn Borer"=as.double(), check.names = F)
  write.csv(vcr_file, file = "vcr_dashboard_data.csv", col.names = T, row.names = F)
  new_instance <- T
#If not a new instance, check for new stations
new_stations <- c()
if (!new_instance){
  for (station in station_list){
    if (!station %in% vcr_file$County){
      new_stations <- append(new_stations, station)
    }
  }
}
  


#FUNCTIONS--------------------------------------------------------------
read_ECCC_file <- function(county_name, year) {
  #select station name, date, min and max temp, and total precip columns and months march (3) through november (11)
  ECCC_fp <- paste(getwd(),"/",county_name, "/",year, "/", county_name,"_",year,"_","ECCC",".csv", sep="")
  ECCC_data <- read.csv(ECCC_fp) %>% subset(select = c(1, 2, 3, 5, 6, 7, 8, 10, 12, 24))
  colnames(ECCC_data) <- c("Longitude","Latitude","County","Date","Year","Month","Day","Max Temp.", "Min Temp.", "Precipitation")
  ECCC_data$County <- county_name
  return(ECCC_data[!(ECCC_data$Month==1 | ECCC_data$Month==2| ECCC_data$Month==12),])
}


read_NP_file <- function(county_name) {
  #read corresponding NasaPower file for county
  NP_fp <- paste(getwd(), "/", county_name,"_","nasapower","_",".csv", sep="")
  NP_data <- read.csv(NP_fp)
  return(NP_data)
}

get_ECCC_data <- function(county_name, year, dates) {
  #retrieve ECCC data for each date listed in dates and append to vcr_file
  ECCC <- read_ECCC_file(county_name,year)
  ECCC <- ECCC[ECCC$Date >= dates[1] & ECCC$Date <= dates[length(dates)],]
  NP <- read_NP_file(county_name)
  if (!nrow(ECCC)==0){
    for (x in dates){
      #check if value missing and if true get value from NasaPower file
      if (as.Date(x) %in% as.Date(ECCC$Date)){
        i <- match(as.Date(x), as.Date(ECCC$Date))
        if (is.na(ECCC$`Max Temp.`[i])){
          ECCC$`Max Temp.`[i] <- get_missing(NP,NP$T2M_MAX,as.Date(x))
        }
        if (is.na(ECCC$`Min Temp.`[i])){
          ECCC$`Min Temp.`[i] <- get_missing(NP,NP$T2M_MIN,as.Date(x))
        }
        if (is.na(ECCC$Precipitation[i])){
          ECCC$Precipitation[i] <- get_missing(NP, NP$PRECTOTCORR, as.Date(x))
        }
        #Calculate GDD, pest thresholds    
        mean_temps <- mean(c(ECCC$`Max Temp.`[i],ECCC$`Min Temp.`[i]))
        ECCC$GDD[i] <- max(0,mean_temps-5)
        ECCC$`Carrot Rust Fly`[i] <- max(0,mean_temps-3)
        ECCC$`Onion Maggot`[i] <- max(0,mean_temps-4)
        ECCC$`Carrot Weevil`[i] <- max(0,mean_temps-7)
        ECCC$`Aster Leafhopper`[i] <- max(0,mean_temps-9)
        ECCC$`Tarnished Plant Bug`[i] <- max(0,mean_temps-12)
        ECCC$`Cabbage Maggot`[i] <- max(0,mean_temps-6)
        ECCC$`Seedcorn Maggot`[i] <- max(0,mean_temps-4)
        ECCC$`European Corn Borer`[i] <- max(0,mean_temps-10)
      }
    }
    #append new data to vcr_dashboard_data.csv
    write.table(subset(ECCC,select = c(1,2,3,4,8,9,10,11,12,13,14,15,16,17,18,19)), file = file_nm, append=T, row.names=F, col.names=F, sep="," )
  }
}

get_missing <- function(NP_file, NP_col, date){
  #return nasapower value for given date, column
  return(NP_col[match(date, as.Date(NP_file$YYYYMMDD))])
}

#----------------------------------------------------------------------------

if (length(new_stations) > 0){
  #If there are new stations, add 11 years of new station data up until last date in vcr_file for each station
  yrrange <- seq(as.integer((format(as.Date(Sys.Date()), "%Y")))-11, as.integer((format(as.Date(Sys.Date()), "%Y"))))
  for (county in new_stations){
    for (y in yrrange){
      start <- as.Date(paste(as.character(y), "-03", "-01", sep=""))
      if (y != as.integer((format(as.Date(Sys.Date()), "%Y")))){
        end <- as.Date(paste(as.character(y), "-11", "-30", sep=""))
      }else {
        end <- max(as.Date(vcr_file$Date,format="%Y-%m-%d"))
        if (end<start){
          end <- Sys.Date()-1
        }
      }
      cur_dates <- seq(start,end, by ="day")
      get_ECCC_data(county,y,cur_dates)
    }
  }
}

if (new_instance){
 #populate empty vcr_file
  yrrange <- seq(as.integer((format(as.Date(Sys.Date()), "%Y")))-11, as.integer((format(as.Date(Sys.Date()), "%Y"))))
  for (county in station_list){
    for (y in yrrange){
      start <- as.Date(paste(as.character(y), "-03", "-01", sep=""))
      if (y != as.integer((format(as.Date(Sys.Date()), "%Y")))){
        end <- as.Date(paste(as.character(y), "-11", "-30", sep=""))
      }else {
        end <- Sys.Date()-1
      }
      cur_dates <- seq(start,end, by ="day")
      get_ECCC_data(county,y,cur_dates)
    }
      
  }
    
  
} else {
  #add new data from the last date updated
  last_date <- (as.Date("2023-05-10"))
  yr <- format(last_date,"%Y")
  date_range <- seq(as.Date(last_date), Sys.Date()-1,by="day")
  
  if (yr != format(Sys.Date(), "%Y")) {
    #last date year is not the same year as current year
    diff_yrs = T
  } else{
    diff_yrs = F
  }
  
  if (diff_yrs){
    yrs <- seq(as.integer((format(as.Date(last_date), "%Y"))), as.integer((format(as.Date(Sys.Date()), "%Y"))))
    for (county in station_list){
      for (y in yrs){
        get_ECCC_data(county, y,date_range)
      }
    }
    
  } else {
    for (county in station_list){
      get_ECCC_data(county, yr, date_range)
    }
  }
}