#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Sep 10 16:50:05 2021

@author: howsetya
"""

import pylab as plb
import matplotlib.pyplot as plt

task2 = plb.loadtxt('/home/howsetya/workspace/lightmicroscopy/LSM/Data/task2_spectra.csv', skiprows=1, delimiter=',')

fig = plt.figure(dpi=200)
plt.grid(color='grey', linestyle=':')
plt.rcParams['axes.facecolor'] = '#eceff4' # nord6 white
plt.plot(task2[:,0],task2[:,1],'#bf616a',label='Ch 1') #nord11 red
plt.plot(task2[:,0],task2[:,2],'#a3be8c',label='Ch 2') #nord14 green
plt.plot(task2[:,0],task2[:,3],'#5e81ac',label='Ch 3') #nord10 blue
plt.legend()
plt.title('Emission Spectra')
plt.xlabel('wavelength')
plt.ylabel('Intensity')
plt.show()
