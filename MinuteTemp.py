#!/usr/bin/env python
import sys
import time
import string
import calendar
import matplotlib
from decimal import *
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import numpy
import csv
import pylab
import matplotlib.dates as mdates
import calendar
import datetime
from datetime import datetime
from pytz import timezone
import pytz
import re
import os 
import glob
import math

finpath = "/Volumes/Seagate Backup Plus Drive/IAQ/TempDoorWinMotion/ExtractAll/Temp/Atmo1/Seperated/"
foutpath = "/Volumes/Seagate Backup Plus Drive/IAQ/TempDoorWinMotion/ExtractAll/Temp/Atmo1/Minutes/"

def writeline(inlist,fout):
	fout.write(str(inlist[0]) + '\t')
	fout.write(str(inlist[1]) + '\t')
	fout.write(str(inlist[2]) + '\t')
	fout.write(str(inlist[3]) + '\n')

count = 0
t = 0
aidx = 0

for filename in glob.glob(os.path.join(finpath, '*.txt')):
	a = []
 	data = open(filename, 'rU')
 	tempNameSplit = re.split(r"\/", filename)
 	tname = tempNameSplit[-1]
	#datafirstline = data.read()
	#first_line = datafirstline.split('\n', 1)[0]
	Tlines = data.readlines()
	data.close()
	f_out = open (foutpath + tname, 'w')

	for lines in Tlines:
		tempStrsSplit = re.split(r'\t', lines)
		# print tempStrsSplit
		# 1434750188.0	2015-06-19 21:43:08	BedroomBWindow	CLOSE
		timeAt = math.floor(float(tempStrsSplit[0])/60)*60
		datetime1 = datetime.utcfromtimestamp(timeAt)
		a.append([timeAt, datetime1, tempStrsSplit[2], tempStrsSplit[3].strip()])
		#a.append(tempStrsSplit)
		#a[-1][3] = a[-1][3].strip()

	###################################################################################### 
	###################### mean if there are multiple temp in one minute##################
	######################################################################################
	len1 = len(a)
	b = []
	i = 0 
	while(i < len1 - 1):
		tempT = []
		t = i 
		tempT.append(float(a[t][3]))
		if (a[i+1][0] != a[t][0]):
			writeline(a[i], f_out)
			i = i + 1

		else:
			while (a[i+1][0] == a[t][0]):
				tempT.append(float(a[i+1][3]))
				i = i + 1
	
			tempV = numpy.average(tempT)
			a[i-1][3] = str(tempV)
			writeline(a[i-1], f_out)
			i = i + 1


	

		
		

		
		




	