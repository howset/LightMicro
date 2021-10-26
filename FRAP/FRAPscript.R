# This file contains the line-by-line command to run

### set working directory, adjust as necessary
# setwd("~/Desktop/Desktop Files/FRAP") #E14
# setwd("~/Dropbox/MataKuliah/LightMicro/FRAP") #T550
setwd("~/workspace/lightmicroscopy/FRAP/csvs/") # from git

### choose one to run
frap_read("NE81M1.csv")
frap_calc(CellProts)
frap_plot(CellProts)
# frap_saveplot() # uncomment to save 

frap_read("NE81M2.csv")
frap_calc(CellProts)
frap_plot(CellProts)
# frap_saveplot()

frap_read("Erg24M1.csv")
frap_calc(CellProts)
frap_plot(CellProts)
# frap_saveplot()

frap_read("Erg24M2.csv")
frap_calc(CellProts)
frap_plot(CellProts)
# frap_saveplot()

### combine
### NE81
# make combined results
frap_read("NE81M1.csv")
frap_calc(CellProts)
DF1 <- as.data.frame(cbind(CellProts$RealTime,CellProts[,23:29])) # 1st placeholder df
colnames(DF1)[1] <- 'RealTime'
frap_read("NE81M2.csv")
frap_calc(CellProts)
DF2 <- as.data.frame(cbind(CellProts[,23:29])) # 2nd placeholder df 
DF3 <- as.data.frame(cbind(DF1,DF2)) # the combined df
DF3 <- na.omit(DF3)

DF3$Av <- rowMeans(DF3[,2:(length(colnames(DF3)))])
DF3$Sd <- apply(DF3[,-1],1,sd) #-1 to exclude first column

Source <- 'CTL-H-NE81'
frap_plot(DF3)
#frap_saveplot()

### Erg24
frap_read("Erg24M1.csv")
frap_calc(CellProts)
DF1 <- as.data.frame(cbind(CellProts$RealTime,CellProts[,19:23]))
DF1 <- head(DF1,60) # remove last row, to make it compatible with DF2
colnames(DF1)[1] <- 'RealTime'
frap_read("Erg24M2.csv")
frap_calc(CellProts)
DF2 <- as.data.frame(cbind(CellProts[,19:23]))
DF3 <- as.data.frame(cbind(DF1,DF2))
DF3 <- na.omit(DF3)

DF3$Av <- rowMeans(DF3[,2:(length(colnames(DF3)))])
DF3$Sd <- apply(DF3[,-1],1,sd) #-1 to exclude first column

Source <- 'CTL-H-Erg24'
frap_plot(DF3)
#frap_saveplot()
