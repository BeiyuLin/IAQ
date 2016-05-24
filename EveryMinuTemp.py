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
from dateutil import tz
from pytz import timezone
import pytz
import re
import os 
import glob
import math


finpath = "/Volumes/Seagate Backup Plus Drive/IAQ/TempDoorWinMotion/ExtractAll/Temp/Atmo1/Minutes/"
foutpath = "/Volumes/Seagate Backup Plus Drive/IAQ/TempDoorWinMotion/ExtractAll/Temp/Atmo1/Minutes/EveryMinutesPST/"

def UTCToPST(utc_dt):
	# Hardcode zones:
	from_zone = tz.gettz('UTC')
	to_zone = tz.gettz('US/Pacific')
	return utc_dt.replace(tzinfo=from_zone).astimezone(to_zone).replace(tzinfo=None)

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
	len1 = len(a)
	i = 0
	while (i < len1 - 1):
		d = (float(a[i+1][0]) - float(a[i][0]))/60
		writeline(a[i], f_out)
		if (d == 0):
			writeline(a[i+1], f_out)

		if (d >= 1):
			for j in range(1, int(d)):
				templ = []
				tstamp = float(a[i][0]) + j*60
				utcTime = datetime.utcfromtimestamp(tstamp)
				pstTime = UTCToPST(utcTime)
				ttemp = a[i][3]
				templ.append([tstamp, utcTime, pstTime, ttemp])
				writeline(templ[0], f_out)
		i = i + 1








