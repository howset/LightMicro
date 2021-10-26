# FRAP

This is the R code I use for FRAP.

To use, you have to make sure to format your data correctly (see example - 'Erg24M1.csv') 

My suggestion:
1. First, load (**source**) the function file (FRAPfunctions.R).
2. Then open the script (FRAPscript.R).
3. Now just run the command line-by-line.

Notes:
+ There are only four functions, one to load the csv data, one to make **all** the calculations, and another to make the plot. The last function is only to save the (last) plot. This save plot function is separated from the make plot function just because sometime you just want to make small changes and not necessarily save the plot.
+ Adjustments can be made to the plot functions. This can obviously be done more elegantly by passing arguments, but I am too lazy, and frankly, I dont think it's worth it to put in all that work at this point. So if warranted, adjustments have to made manually **in** the function itself. I made some comments there, hope it's useful. (i.e. just comment out the unnecessary line)
 
