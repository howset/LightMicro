### This file contains all the functions

### set working directory, adjust as necessary
setwd("~/workspace/lightmicroscopy") # from git

### read function integrated with filename extraction
frap_read <- function(filename){
  CellProts <<- read.csv(filename)
  Source <<- substr(filename,1,nchar(filename)-4)
}

### make calculations (everything)
frap_calc <- function(cellprots){
  ## get background mean
  BGmean <- mean(cellprots$BG,na.rm = TRUE)
  
  ## remove background
  colna <- colnames(cellprots)
  for (x in 1:length(colna)) {
    if (grepl('Cell',colna[x])) {
      substracted <- cellprots[x]-BGmean
      cellprots[x] <- substracted
    }
  }
  
  ## make average of three cells and append to data frame
  ## choose 3 cells with most entry 
  ## --> this part is wrong, this should be done to unbleached cells
  ## kept only for posterity reasons
  if (grepl('NE81M1',Source)) {
    ThreeCellsAv <- ((cellprots$Cell8)+(cellprots$Cell9)+(cellprots$Cell10))/3
  } else if (grepl('NE81M2',Source)) {
    ThreeCellsAv <- ((cellprots$Cell4)+(cellprots$Cell5)+(cellprots$Cell6))/3
  } else if (grepl('Erg24M1',Source)) {
    ThreeCellsAv <- ((cellprots$Cell1)+(cellprots$Cell2)+(cellprots$Cell5))/3
  } else if (grepl('Erg24M2',Source)) {
    ThreeCellsAv <- ((cellprots$Cell3)+(cellprots$Cell4)+(cellprots$Cell5))/3
  }
  cellprots$TCAv <- ThreeCellsAv
  
  ## make normalization of Unbleached by the first two (unbleached)
  ## measurements and append
  Normfac<-mean(head(cellprots$Unbleached),2)
  cellprots$UnbleachedNorm <- (cellprots$Unbleached)/Normfac

  ## find gradient(slope/steepness) and *-1
  m <- coef(lm(cellprots$UnbleachedNorm~cellprots$X))
  m <- m[2]*-1
  attr(m,'names') <- NULL
  m <- round(m, digits = 4)
  
  ## set timepoints and make corrected time (?), then set real time (?)
  cellprots$TimePoints <- (cellprots$X)-1
  cellprots$CorrTime <- (cellprots$TimePoints)*m
  cellprots$RealTime <- (cellprots$TimePoints)*1.2
  
  ## normalize cells entries
  colna1 <- colnames(cellprots)
  for (x in 1:length(colna1)) {
    if (grepl('Cell',colna1[x])) {
      NormfacC <- mean(cellprots[1:2,x])
      TempCol <- (cellprots[x])/NormfacC
      colnames(TempCol) <- sprintf('%sNormd',colna1[x])
      cellprots <- cbind(cellprots,TempCol)
    }
  }

  ## correction to cells entries
  colna2 <- colnames(cellprots)
  TempCol3 <- as.data.frame(cellprots$RealTime)
  for (x in 1:length(colna2)) {
    if (grepl('Normd',colna2[x])) {
      TempCol2 <- (cellprots[x]+(cellprots[x]*cellprots$CorrTime))
      colnames(TempCol2) <- sprintf('%sCorrd',colna2[x])
      cellprots <- cbind(cellprots,TempCol2)
      TempCol3 <- cbind(TempCol3,TempCol2)
    }
  }
  TempCol3$`cellprots$RealTime` <- NULL
  
  ## average all corrected cells and get std dev
  cellprots$Av <- rowMeans(TempCol3)
  cellprots$Sd <- apply(TempCol3,1,sd)
  
  CellProts<<-print(cellprots)
  return(CellProts)
}

### make plot (scatter plot, with errorbars, trendline, equation)
frap_plot <- function(cellprotscalc){
  library(tidyverse)
  ## To help plotting
  CellProtsDF <- as.data.frame(cbind(cellprotscalc$RealTime,cellprotscalc$Av,cellprotscalc$Sd))
  colnames(CellProtsDF) <- c('RealTime','Av','Sd')
  CellProtsDF <- na.omit(CellProtsDF)
  
  ## Sliced data frame to exclude unbleached points
  Dat = slice(CellProtsDF, c(3:length(rownames(CellProtsDF))))
  
  ## Trendline equation
  lm_eq <- function(CellProtsDF){
    m <- lm(Av ~ RealTime, Dat);
    # eq <- substitute(italic(y) == a + b ~italic(x)*","~~italic(R)^2~"="~r2,
    #                  list(a = format(unname(coef(m)[1]), digits = 2),
    #                       b = format(unname(coef(m)[2]), digits = 2),
    #                       r2 = format(summary(m)$r.squared, digits = 3)))
    eq <- substitute(italic(y) == a + b ~italic(x),
                     list(a = format(unname(coef(m)[1]), digits = 2),
                          b = format(unname(coef(m)[2]), digits = 2)))
    as.character(as.expression(eq));
  }
  
  ## Make plot (scatter plot, with errorbars, trendline, and equation)
  fluoplot <- ggplot(data = CellProtsDF, mapping = aes(x = RealTime, y = Av)) +
    geom_point(shape=1,color='#5e81ac') +
    geom_errorbar(aes(ymin=Av-Sd, ymax=Av+Sd),width=.2,color='#5e81ac') + # to add errorbar
    geom_smooth(method = "lm", data = Dat, se=FALSE,color='#bf616a') # to add trendline
  f <- fluoplot + 
    annotate("text", x = 30, y = 1, label = lm_eq(Dat), parse = TRUE) + #to show equation
    labs(title = Source,
         x = "Time",
         y = "Fluorescence (Normalized)") 
  print(f)
}

### save plot as image separately, only last plotted image, no arguments
frap_saveplot <- function(){
  savename <- sprintf('%sBGsd.png',Source)
  ggsave(savename,
         plot=last_plot()#,
         #width = 9,
         #height = 6,
         #units = 'cm'
  )
}
