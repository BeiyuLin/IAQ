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


finpath = "/Volumes/Seagate Backup Plus Drive/IAQ/TempDoorWinMotion/ExtractAll/DoorWind/Atmo1/JitterExpandDoorWind/DiffMinu/"
foutpath = "/Volumes/Seagate Backup Plus Drive/IAQ/TempDoorWinMotion/ExtractAll/DoorWind/Atmo1/JitterExpandDoorWind/DiffMinu/InsertMissingData/"


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
		#1433982300.0	2015-06-11 00:25:00	OfficeAWindowAA	OPEN
		#1433982360.0	2015-06-11 00:26:00	OfficeAWindowAA	CLOSE
		timeAt = float(tempStrsSplit[0])
		utcTime1 = datetime.utcfromtimestamp(timeAt)
		PSTdatetime1 = UTCToPST(utcTime1)
		a.append([tempStrsSplit[0],tempStrsSplit[1], PSTdatetime1, tempStrsSplit[3].strip()])
		#a.append(tempStrsSplit) ## a is Stamp, UTC, PST, OPNE/CLOSE
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








