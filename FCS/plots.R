#############
# Procedure #
############# 
library(ggplot2)
library(dplyr)

###############################################################################
# Calibration EGFP in vitro and in vivo
egfpsol <- read.csv('Data/egfpsol.csv', header = TRUE)
colnames(egfpsol) <- c('x','y')
egfp1 <- read.csv('Data/egfp1.csv', header = TRUE)
colnames(egfp1) <- c('x','y')

egfp <- data.frame(x1 = egfpsol$x,
                   y1 = egfpsol$y,
                   x2 = egfp1$x,
                   y2 = egfp1$y)

lm_eq <- function(df){
    m <- lm(y ~ 0+x, df); #intercept at 0,0
    eq <- substitute(italic(y) ==  b ~italic(x)*','~~italic(R)^2~'='~r2,
                     list(b = format(unname(coef(m)[1]), digits = 3),
                          r2 = format(summary(m)$r.squared, digits = 3)))
    as.character(as.expression(eq));
}

ggplot(egfp) + 
    geom_point(aes(x1,y1), colour='#7fcdbb') + geom_smooth(aes(x=x1,y=y1,colour='in vitro'), method=lm, se=FALSE) +
    geom_point(aes(x2,y2), colour='#1d91c0') + geom_smooth(aes(x=x2,y=y2,colour='in vivo'), method=lm, se=FALSE, linetype = 'dashed') +
    annotate('text', x = 270, y = -10, label = lm_eq(egfpsol), parse = TRUE) +
    annotate('text', x = 1300, y = 600, label = lm_eq(egfp1), parse = TRUE) +
    scale_color_manual(name = "Series",             
                       values = c('in vitro' = '#7fcdbb',  
                                  'in vivo' = '#1d91c0')) +
    labs(x = 'Image intensity (kHz)', y = 'Concentration (nM)')

###############################################################################
# Plot yeast N_corrected against Volume with reg_line and correlation
# Only mother & buds
rpl <- read.csv('Data/rpl3.csv',sep=';', header = TRUE)
## Exclude whole cells
idtf <- rpl[,2]!='whole cell'
rpl <- rpl[idtf,]
lm_eq <- function(df){
    m <- lm(Number_corrected ~ 0+Volume, df);
    corr <- cor.test(df[[3]],df[[4]])
    eq <- substitute(~~Correlation~'='~c *','~~pval~'='~p, #only corr, no regression
                     list(c = format(unname(corr$estimate), digits = 5),
                          p = format(corr$p.value, digits = 5)))
    as.character(as.expression(eq));
}
fluoplot <- ggplot(data = rpl, mapping = aes(x = Volume, y = Number_corrected)) +
    geom_point(shape=1,color='#5e81ac') +
    geom_smooth(method = "lm", data = rpl, se=FALSE,color='#bf616a') # to add trendline
f <- fluoplot + 
    annotate("text", x = 40, y = 0.5e5, label = lm_eq(rpl), parse = TRUE) + #to show equation
    ggtitle('Amount of ribosome and volume') +
    xlab(~'Volume' (mu * m^3))+
    ylab(~N[ribosome]) 
print(f)

###############################################################################
# Plot yeast Density against Volume with 2 dashed lines
# whole cells
rpl <- read.csv('Data/rpl3.csv',sep=';', header = TRUE)
## Only whole cells
idtf <- rpl[,2]=='whole cell'
rpl <- rpl[idtf,]
lm_eq <- function(df){
    m <- lm(Volume ~ 0+Density, df);
    corr <- cor(df[4],df[5])
    eq <- substitute(Correlation~'='~c,
                     list(c = format(corr, digits = 5)))
    as.character(as.expression(eq));
}
fluoplot <- ggplot(data = rpl, mapping = aes(x = Volume, y = Density)) +
    geom_point(shape=1,color='#5e81ac') +
    geom_hline(yintercept=8000, linetype="dashed", color = "#bf616a") + #dash1
    geom_hline(yintercept=5000, linetype="dashed", color = "#bf616a") #dash2
f <- fluoplot + 
    ggtitle('Density and volume') +
    xlab(~'Volume' (mu * m^3))+
    ylab(~'Density' (N[ribosome]/mu * m^3)) 
print(f)

###############################################################################
# Grouped boxplot of whole cells (density) vs all cell cycle phase
rpl <- read.csv('Data/rpl3.csv',sep=';', header = TRUE)
## Only whole cells
idtf <- rpl[,2]=='whole cell'
rpl <- rpl[idtf,]
rpl <- rpl[c(1,2,5)] #Choose only relevant columns
colnames(rpl) <- c('CellCyclePhase', 'Morphology','Density') #Rename cols for better legends
ylgnbl <- c(#'#c7e9b4',
    #'#41b6c4',
    '#253494')
rpl$Morphology<-factor(rpl$Morphology) #Set this column as factor
rpl$CellCyclePhase<-factor(rpl$CellCyclePhase)
bp <- ggplot(rpl, aes(CellCyclePhase, Density, colour=Morphology,fill=Morphology)) +
    geom_boxplot(outlier.shape = 21,alpha=0.6)+
    ylab(~'Density' (N[ribosome]/mu * m^3))+
    xlab('Cell Cycle Phase')
bp + 
    scale_fill_manual(values=ylgnbl) + 
    scale_colour_manual(values=ylgnbl) + 
    theme(legend.position = "bottom")

###############################################################################
# Grouped boxplot of mother & bud (density) vs cellcycle phase 
rpl <- read.csv('Data/rpl3.csv',sep=';', header = TRUE)
## Exclude whole cells
idtf <- rpl[,2]!='whole cell'
rpl <- rpl[idtf,]
rpl <- rpl[c(1,2,5)] #Choose only relevant columns
colnames(rpl) <- c('CellCyclePhase', 'Morphology','Density') #Rename cols for better legends
ylgnbl <- c(#'#c7e9b4',
    '#41b6c4',
    '#253494')
rpl$Morphology<-factor(rpl$Morphology) #Set this column as factor
rpl$CellCyclePhase<-factor(rpl$CellCyclePhase)
bp <- ggplot(rpl, aes(CellCyclePhase, Density, colour=Morphology,fill=Morphology)) +
    geom_boxplot(outlier.shape = 21,alpha=0.6)+
    ylab(~'Density' (N[ribosome]/mu * m^3))+
    xlab('Cell Cycle Phase')
bp + 
    scale_fill_manual(values=ylgnbl) + 
    scale_colour_manual(values=ylgnbl) + 
    theme(legend.position = "bottom")

###############################################################################
# Grouped boxplot all
rpl <- read.csv('Data/rpl3.csv',sep=';', header = TRUE)
rpl <- rpl[c(1,2,5)] #Choose only relevant columns
colnames(rpl) <- c('CellCyclePhase', 'Morphology','Density') #Rename cols for better legends
ylgnbl <- c('#7fcdbb',
            '#1d91c0',
            '#253494')
rpl$Morphology<-factor(rpl$Morphology) #Set this column as factor
rpl$CellCyclePhase<-factor(rpl$CellCyclePhase)
bp <- ggplot(rpl, aes(CellCyclePhase, Density, colour=Morphology,fill=Morphology)) +
    geom_boxplot(outlier.shape = 21,alpha=0.6)+
    ylab(~'Density' (N[ribosome]/mu * m^3))+
    xlab('Cell Cycle Phase')
bp + 
    scale_fill_manual(values=ylgnbl) + 
    scale_colour_manual(values=ylgnbl) + 
    theme(legend.position = "bottom")

