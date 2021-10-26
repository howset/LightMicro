#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep 22 12:10:36 2021

@author: howsetya
"""

############
# Packages #
############

import glob, re, os
import pandas as pd
import numpy as np
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt

#############
# Functions #
#############

def get_list(path,sername):
    '''
    Returns a list of all the series' filenames in a given path.' 
    '''
    os.chdir(path)
    filelist = glob.glob('*.csv')
    filelist.sort()
    c1=[]
    c2=[]
    c3=[]
    c4=[]
    for file in filelist:
        if re.search(sername,file):
            # print(file)
            if re.search('c1',file):
                c1.append(file)
            elif re.search('c2',file):
                c2.append(file)
            elif re.search('c3',file):
                c3.append(file)
            elif re.search('c4',file):
                c4.append(file)
    chanlist = [c1,c2,c3,c4]
    return(chanlist)

def get_profile(chanlist):
    '''
    Loads the data according to get_list.
    '''
    lineprofile=[[0] * 3 for i in range(4)] # create empty list with this dimension (same to chanlist)
    m=-1
    for i in chanlist:
        m=m+1
        n=-1
        for j in i:
            n=n+1
            lineprofile[m][n]=pd.read_csv(chanlist[m][n])
    return(lineprofile)

def get_fwhm(df,plot='',ti='',save=''):
    '''
    Plot fit and/or get fwhm from a single dataframe.
    Option plot takes either 'yes' or 'y' to make plot.
    Please pass ti option with the .csv, so saving can work as is (if saving is wished).
    Option save takes 'y' to save, only if set to plot.
    Optimal initial paramaters are adjusted manually.
    '''
    x=df.iloc[:,0]
    y=df.iloc[:,1]
    # initialize parameters
    a = 1
    mean = 2 #sum(x)/len(x) # https://stackoverflow.com/questions/10950733/gaussian-curve-fitting-algorithm
    sigma = 0.31 #np.sqrt(1/(len(x)-1)*(sum(x)-mean))
    # offset = 0
    def gaus(x,A,mean,sigma):
        return A*np.exp(-(x-mean)**2/(2*sigma**2)) #+offset
        # return a/np.sqrt(sigma)*exp(-(x-x0)**2/(2.*sigma**2)) # https://stackoverflow.com/questions/47773178/gaussian-fit-returning-negative-sigma
    popt,pcov = curve_fit(gaus,x,y,p0=[a,mean,sigma])
    fwhm = 2.355*abs(popt[2]) # shortcut
    print('series name',ti)
    print('fwhm:',fwhm)
    # print(popt)
    if plot =='yes' or plot =='y':
        fwhm = "{:.4f}".format(fwhm)
        fig = plt.figure(dpi=200) # default dpi is 100
        plt.rcParams['axes.facecolor'] = '#eceff4' # nord6 white
        plt.grid(color='grey', linestyle=':')
        plt.plot(x,y,'+:',color='#5e81ac',label='data') # nord10 blue
        plt.plot(x,gaus(x,*popt),'#bf616a',label='fit') # nord11 red
        plt.legend()
        plt.title('Gauss fit, FWHM={0}'.format(fwhm))
        plt.xlabel('Distance')
        plt.ylabel('Intensity')
        if ti == '':
            plt.title('Gauss fit, FWHM={0}'.format(fwhm))
        else:
            plt.title('Gauss fit {1}, FWHM={0}'.format(fwhm,ti))
        if save == 'y':
            fig.savefig(ti[0:-4],dpi=fig.dpi) # shortcut ti for filename, inherit dpi from display
        plt.show()
        return(fwhm)
    elif plot == '':
        return(fwhm)
    else:
        print('Calculating but not plotting, wrong/no plot argument.')
        return(fwhm)

def get_av(lineprofile,clist,plot=''):
    '''
    Calls get_fwhm and averages the 3 values of a channel and put in a dataframe.
    '''
    m=-1
    # c=0
    average=[]
    stdev=[]
    for i in lineprofile:
        m=m+1
        n=-1
        lmr=[]
        for j in i:
            z=get_fwhm(j,plot=plot,ti=clist[m][n])
            lmr.append(z)
            # c=c+1
            # print(z,c)
        # print(lmr)
        ave = sum(lmr)/len(lmr)
        sdev = np.std(lmr)
        # print('Average = ',average)
        average.append(ave)
        stdev.append(sdev)
    # name=clist[m][n][0:-7]
    print('\n',clist[m][n][0:-7])
    print('FWHM average of Ch1, Ch2, Ch3, Ch4: \n',average,'\n')
    print('\n',clist[m][n][0:-7])
    print('FWHM st dev of Ch1, Ch2, Ch3, Ch4: \n',stdev,'\n')
    dfaverage = pd.DataFrame(average,columns=[clist[m][n][0:-7]])
    dfaverage= dfaverage.rename(index={0:'Ch1',1:'Ch2',2:'Ch3',3:'Ch4'})
    dfstdev = pd.DataFrame(stdev,columns=[clist[m][n][0:-7]])
    dfstdev= dfstdev.rename(index={0:'Ch1',1:'Ch2',2:'Ch3',3:'Ch4'})
    return(dfaverage,dfstdev)

#############
# Procedure #
#############

sernames=['input',
          'itercalc','itertheo',
          'fastcalc','fasttheo',
          'invfilcalc','invfiltheo'] # Put the series in a list to loop over later.

path='/home/howsetya/workspace/lightmicroscopy/Deconvolution/BeadsLineProfile/' # T550
path='/home/howset/workspace/lightmicroscopy/Deconvolution/BeadsLineProfile/' # E14

# clist = get_list(path,sernames[0])
# lineprofile = get_profile(clist)

# get_av(lineprofile,clist)
# get_av(lineprofile,clist,plot='y')

# Inspect fit (make plots) and save plots (if necessary)
for i in sernames:
    clist = get_list(path,i)
    lineprofile = get_profile(clist)
    m=-1
    for j in clist:
        m=m+1
        n=-1
        for k in j:
            n=n+1
            get_fwhm(lineprofile[m][n],plot='y',ti=clist[m][n],save='y')
del(i,j,k,m,n)
del(clist,lineprofile)

# Get average values for further use
fdf_ave=pd.DataFrame()
fdf_std=pd.DataFrame()
m=-1
for i in sernames:
    m=m+1
    clist = get_list(path,i)
    lineprofile = get_profile(clist)
    df1,df2=get_av(lineprofile,clist)
    fdf_ave = pd.concat([fdf_ave,df1],axis=1)
    fdf_std = pd.concat([fdf_std,df2],axis=1)
del(i,m,df1,df2)
del(clist,lineprofile)

# Save result
os.chdir('/home/howsetya/workspace/lightmicroscopy/Deconvolution/') # T550
fdf_ave.to_csv('av_tab.csv')
fdf_std.to_csv('av_tab.csv')

## Make grouped plots

fdf_ave=fdf_ave*1000 # make nm
fdf_std=fdf_std*1000

fdf_ave=fdf_ave.reindex(columns=['input',
                         'invfiltheo','invfilcalc',
                         'itertheo','itercalc',
                         'fasttheo','fastcalc'])

fdf_std=fdf_std.reindex(columns=['input',
                         'invfiltheo','invfilcalc',
                         'itertheo','itercalc',
                         'fasttheo','fastcalc'])

fdf_ave.rename(columns={'input': 'Input',
                   'invfiltheo': 'Inverse Filter (T)','invfilcalc': 'Inverse Filter (M)',
                   'itertheo': 'Iterative (T)','itercalc': 'Iterative (M)',
                   'fasttheo': 'Fast Iterative (T)','fastcalc': 'Fast Iterative (M)'}, inplace=True)

colors = {'Input': '#b48ead',
          'Inverse Filter (T)': '#a3be8c',
          'Inverse Filter (M)': '#ebcb8b',
          'Iterative (T)': '#d08770',
          'Iterative (M)': '#bf616a',
          'Fast Iterative (T)': '#5e81ac',
          'Fast Iterative (M)': '#4c566a'}

plt.rcParams['figure.dpi'] = 200
plt.rcParams['axes.facecolor'] = '#eceff4' # nord6 white
fdf_ave.plot(kind='bar', # barh --> horizontal, switch x & y label!
             alpha = 0.8,
             yerr=fdf_std.values.T, # add st.dev as error bars https://stackoverflow.com/questions/26614224/how-to-add-error-bars-to-a-data-frame-grouped-bar-plot-or-even-an-array-of-array
             error_kw=dict(ecolor='darkslategrey', lw=1, capsize=1.5, capthick=1),
             title='FWHM',
             color=colors)
plt.grid(color='grey', linestyle=':')
plt.legend(bbox_to_anchor=(1.0, 1.0))
plt.xticks(rotation=30, horizontalalignment="center")
plt.xlabel("Channels")
plt.ylabel("Width (nm)")
plt.show()

