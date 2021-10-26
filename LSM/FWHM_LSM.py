#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep  8 15:44:32 2021

@author: howset
"""

############
# Packages #
############

import pylab as plb
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import numpy as np
from numpy import exp
from scipy import stats

#############
# Load data #
#############

#E14
F703 = plb.loadtxt('/home/howset/workspace/lightmicroscopy/LSM/Data/task7_0,3AU.csv', skiprows=1, delimiter=',')
F708 = plb.loadtxt('/home/howset/workspace/lightmicroscopy/LSM/Data/task7_0,8AU.csv', skiprows=1, delimiter=',')
F71 = plb.loadtxt('/home/howset/workspace/lightmicroscopy/LSM/Data/task7_1AU.csv', skiprows=1, delimiter=',')
F715 = plb.loadtxt('/home/howset/workspace/lightmicroscopy/LSM/Data/task7_1,5AU.csv', skiprows=1, delimiter=',')
F72 = plb.loadtxt('/home/howset/workspace/lightmicroscopy/LSM/Data/task7_2AU.csv', skiprows=1, delimiter=',')
F73 = plb.loadtxt('/home/howset/workspace/lightmicroscopy/LSM/Data/task7_3AU.csv', skiprows=1, delimiter=',')
F74 = plb.loadtxt('/home/howset/workspace/lightmicroscopy/LSM/Data/task7_4AU.csv', skiprows=1, delimiter=',')

#T550
F703 = plb.loadtxt('/home/howsetya/workspace/lightmicroscopy/LSM/Data/task7_0,3AU.csv', skiprows=1, delimiter=',')
F708 = plb.loadtxt('/home/howsetya/workspace/lightmicroscopy/LSM/Data/task7_0,8AU.csv', skiprows=1, delimiter=',')
F71 = plb.loadtxt('/home/howsetya/workspace/lightmicroscopy/LSM/Data/task7_1AU.csv', skiprows=1, delimiter=',')
F715 = plb.loadtxt('/home/howsetya/workspace/lightmicroscopy/LSM/Data/task7_1,5AU.csv', skiprows=1, delimiter=',')
F72 = plb.loadtxt('/home/howsetya/workspace/lightmicroscopy/LSM/Data/task7_2AU.csv', skiprows=1, delimiter=',')
F73 = plb.loadtxt('/home/howsetya/workspace/lightmicroscopy/LSM/Data/task7_3AU.csv', skiprows=1, delimiter=',')
F74 = plb.loadtxt('/home/howsetya/workspace/lightmicroscopy/LSM/Data/task7_4AU.csv', skiprows=1, delimiter=',')

#############
# Procedure #    
#############

x = F74[:,0]
y = F74[:,1]

#n = len(x)                          #the number of data
#mean = sum(x*y)/n                   #note this correction
#sigma = sum(y*(x-mean)**2)/n        #note this correction

def gaus(x,a,x0,sigma,offset):
    return a*exp(-(x-x0)**2/(2*sigma**2))+offset

popt,pcov = curve_fit(gaus,x,y,p0=[1,1.5,2,0])
print(popt)

fwhm4 = 2.355*popt[2]
peak = popt[0]
mean = popt[1]
sigma = popt[2]
offs = popt[3]

yh = peak/2
xh0 = mean-fwhm4/2
xh1 = mean+fwhm4/2

# string = 'FWHM= '+str(fwhm4)+'\npeak= ' +str(peak)+'\nmean= '+str(mean)+'\nsigma= '+str(sigma)+'\noffset='+str(offs)
fwhm4 = "{:.3f}".format(fwhm4)
string='FWHM='+str(fwhm4)

fig = plt.figure(dpi=200)
plt.grid(color='grey', linestyle=':')
plt.rcParams['axes.facecolor'] = '#eceff4' # nord6 white
plt.plot(x,y,'+:',color='#5e81ac',label='data')
plt.plot(x,gaus(x,*popt),color='#bf616a',label='fit')
#plt.plot([xh0,xh1],[yh,yh])
plt.legend()
plt.title('Gauss fit 4 AU')
plt.xlabel('Distance')
plt.ylabel('Intensity')
plt.text(3.5, 37000, string)
plt.show()

#######################################################

x = F72[:,0]
y = F72[:,1]

def gaus(x,a,x0,sigma,offset):
    return a*exp(-(x-x0)**2/(2*sigma**2))+offset

popt,pcov = curve_fit(gaus,x,y,p0=[1,2,1,1])
print(popt)

fwhm2 = 2.355*popt[2]
peak = popt[0]
mean = popt[1]
sigma = popt[2]
offs = popt[3]

# string = 'FWHM= '+str(fwhm2)+'\npeak= ' +str(peak)+'\nmean= '+str(mean)+'\nsigma= '+str(sigma)+'\noffset='+str(offs)
fwhm2 = "{:.3f}".format(fwhm2)
string='FWHM='+str(fwhm2)

fig = plt.figure(dpi=200)
plt.grid(color='grey', linestyle=':')
plt.plot(x,y,'+:',color='#5e81ac',label='data')
plt.plot(x,gaus(x,*popt),'#bf616a',label='fit')
plt.legend()
plt.title('Gauss fit 2 AU')
plt.xlabel('Distance')
plt.ylabel('Intensity')
plt.text(3.5, 37000, string)
plt.show()

#######################################################

x = F715[:,0]
y = F715[:,1]

def gaus(x,a,x0,sigma,offset):
    return a*exp(-(x-x0)**2/(2*sigma**2))+offset

popt,pcov = curve_fit(gaus,x,y,p0=[1,1.5,1,1])
print(popt)

fwhm15 = 2.355*popt[2]
peak = popt[0]
mean = popt[1]
sigma = popt[2]
offs = popt[3]

# string = 'FWHM= '+str(fwhm15)+'\npeak= ' +str(peak)+'\nmean= '+str(mean)+'\nsigma= '+str(sigma)+'\noffset='+str(offs)
fwhm15 = "{:.3f}".format(fwhm15)
string='FWHM='+str(fwhm15)

fig = plt.figure(dpi=200)
plt.grid(color='grey', linestyle=':')
plt.plot(x,y,'+:',color='#5e81ac',label='data')
plt.plot(x,gaus(x,*popt),'#bf616a',label='fit')
plt.legend()
plt.title('Gauss fit 1.5 AU')
plt.xlabel('Distance')
plt.ylabel('Intensity')
plt.text(2.7, 37000, string)
plt.show()

#######################################################

x = F71[:,0]
y = F71[:,1]

def gaus(x,a,x0,sigma,offset):
    return a*exp(-(x-x0)**2/(2*sigma**2))+offset

popt,pcov = curve_fit(gaus,x,y,p0=[1,2,1,1])
print(popt)

fwhm1 = 2.355*popt[2]
peak = popt[0]
mean = popt[1]
sigma = popt[2]
offs = popt[3]

# string = 'FWHM= '+str(fwhm1)+'\npeak= ' +str(peak)+'\nmean= '+str(mean)+'\nsigma= '+str(sigma)+'\noffset='+str(offs)
fwhm1 = "{:.3f}".format(fwhm1)
string='FWHM='+str(fwhm1)

fig = plt.figure(dpi=200)
plt.grid(color='grey', linestyle=':')
plt.plot(x,y,'+:',color='#5e81ac',label='data')
plt.plot(x,gaus(x,*popt),'#bf616a',label='fit')
plt.legend()
plt.title('Gauss fit 1 AU')
plt.xlabel('Distance')
plt.ylabel('Intensity')
plt.text(2.5, 27000, string)
plt.show()

#######################################################

x = F708[:,0]
y = F708[:,1]

def gaus(x,a,x0,sigma,offset):
    return a*exp(-(x-x0)**2/(2*sigma**2))+offset

popt,pcov = curve_fit(gaus,x,y,p0=[1,2,1,1])
print(popt)

fwhm08 = 2.355*popt[2]
peak = popt[0]
mean = popt[1]
sigma = popt[2]
offs = popt[3]

# string = 'FWHM= '+str(fwhm08)+'\npeak= ' +str(peak)+'\nmean= '+str(mean)+'\nsigma= '+str(sigma)+'\noffset='+str(offs)
fwhm08 = "{:.3f}".format(fwhm08)
string='FWHM='+str(fwhm08)

fig = plt.figure(dpi=200)
plt.grid(color='grey', linestyle=':')
plt.plot(x,y,'+:',color='#5e81ac',label='data')
plt.plot(x,gaus(x,*popt),'#bf616a',label='fit')
plt.legend()
plt.title('Gauss fit 0.8 AU')
plt.xlabel('Distance')
plt.ylabel('Intensity')
plt.text(2.1, 27000, string)
plt.show()

#######################################################

x = F703[:,0]
y = F703[:,1]

def gaus(x,a,x0,sigma,offset):
    return a*exp(-(x-x0)**2/(2*sigma**2))+offset

popt,pcov = curve_fit(gaus,x,y,p0=[1,1.5,1,1])
print(popt)

fwhm03 = 2.355*popt[2]
peak = popt[0]
mean = popt[1]
sigma = popt[2]
offs = popt[3]

# string = 'FWHM= '+str(fwhm03)+'\npeak= ' +str(peak)+'\nmean= '+str(mean)+'\nsigma= '+str(sigma)+'\noffset='+str(offs)
fwhm03 = "{:.3f}".format(fwhm03)
string='FWHM='+str(fwhm03)

fig = plt.figure(dpi=200)
plt.grid(color='grey', linestyle=':')
plt.plot(x,y,'+:',color='#5e81ac',label='data')
plt.plot(x,gaus(x,*popt),'#bf616a',label='fit')
plt.legend()
plt.title('Gauss fit 0.3 AU')
plt.xlabel('Distance')
plt.ylabel('Intensity')
plt.text(3.3, 32000, string)
plt.show()

#######################################################

FWHM ={'4 AU':float(fwhm4),'2 AU':float(fwhm2),'1.5 AU':float(fwhm15),'1 AU':float(fwhm1),'0.8 AU':float(fwhm08),'0.3 AU':float(fwhm03)}
yFWHM =(float(fwhm4),float(fwhm2),float(fwhm15),float(fwhm1),float(fwhm08),float(fwhm03))
xFWHM = (4,2,1.5,1,0.8,0.3)

gradient, intercept, r_value, p_value, std_err = stats.linregress(xFWHM,yFWHM)

mn=np.min(xFWHM)
mx=np.max(xFWHM)

x1=np.linspace(mn,mx,500)
y1=gradient*x1+intercept

gradient = "{:.2f}".format(gradient)
intercept = "{:.2f}".format(intercept)
r_value = "{:.2f}".format(r_value)
line = 'y='+str(gradient)+'x+'+str(intercept)+'\nr_val='+r_value

fig = plt.figure(dpi=200)
plt.grid(color='grey', linestyle=':')
plt.plot(xFWHM,yFWHM,'+:',color='#5e81ac',label='data')
plt.plot(x1,y1,'#bf616a',label='fit')
plt.legend()
plt.title('FWHM')
plt.xlabel('Pinhole opening (AU)')
plt.ylabel('Width (um)')
plt.text(2.5, 0.8, line)
plt.show()

#######################################################

# =============================================================================
# other option for lin regression
# coef = np.polyfit(xFWHM,yFWHM,1)
# poly1d_fn = np.poly1d(coef) 
# 
# plt.plot(xFWHM,yFWHM,'b+:',label='data')
# plt.plot(xFWHM, poly1d_fn(xFWHM), 'r',label='fit')
# plt.legend()
# plt.title('FWHM')
# plt.xlabel('AU')
# plt.ylabel('Width')
# plt.show()
# =============================================================================

# if wrapping up in functions is necessary
#############
# Functions #
#############

def makeplot(dat,titl) :
    x = dat[:,0]
    y = dat[:,1]
    plt.plot(x,y,'b+:',label=dat)
    plt.title(titl)

# def makefit(dat) :
#     x = dat[:,0]
#     y = dat[:,1]
    
#     def gaus(x,a,x0,sigma,offset):
#         return a*exp(-(x-x0)**2/(2*sigma**2))+offset

#     popt,pcov = curve_fit(gaus,x,y,p0=[1,1.5,2,0.0])
#     #print(popt)
    
#     fwhm = 2.355*popt[2]
#     peak = popt[0]
#     mean = popt[1]
#     sigma = popt[2]
#     offs = popt[3]

#     string = 'FWHM= '+str(fwhm)+'\npeak= ' +str(peak)+'\nmean= '+str(mean)+'\nsigma= '+str(sigma)+'\noffset='+str(offs)

#     plt.plot(x,y,'b+:',label='data')
#     plt.plot(x,gaus(x,*popt),'ro:',label='fit')
#     plt.legend()
#     plt.title('Gauss fit %s', tlist[t])
#     plt.xlabel('Distance')
#     plt.ylabel('intensity')
#     plt.show()
    
