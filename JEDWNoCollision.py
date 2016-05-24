#!/usr/bin/env python
import sys
import time
import string
import calendar
import matplotlib
from decimal import *
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import numpy as np
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
from dateutil import tz

finpath = "/Volumes/Seagate Backup Plus Drive/IAQ/TempDoorWinMotion/ExtractAll/DoorWind/Atmo1/JitterExpandDoorWind/"
foutpath = "/Volumes/Seagate Backup Plus Drive/IAQ/TempDoorWinMotion/ExtractAll/DoorWind/Atmo1/JitterExpandDoorWind/DiffMinu/"

def UTCToPST(utc_dt):
	# Hardcode zones:
	from_zone = tz.gettz('UTC')
	to_zone = tz.gettz('US/Pacific')
	return utc_dt.replace(tzinfo=from_zone).astimezone(to_zone).replace(tzinfo=None)

def writeline(inlist,fout):
	fout.write(str(inlist[0]) + '\t')
	fout.write(str(inlist[1]) + '\t')
	fout.write(str(inlist[2]) + '\t')
	fout.write(str(inlist[3]))

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
	timePrev = 0
	f_out = open (foutpath + tname, 'w')
	for lines in Tlines:
		tempStrsSplit = re.split(r'\t', lines)
		# print tempStrsSplit
		#1433981220.0	2015-06-11 00:07:00	MainDoor	OPEN
		timeAt = float(tempStrsSplit[0])
		if (timeAt == timePrev):
			timeAt = timeAt + 60
		datetime1 = datetime.utcfromtimestamp(timeAt)
		writeline([timeAt, datetime1, UTCToPST(datetime1), tempStrsSplit[3]], f_out)
		timePrev = timeAt
	f_out.close()



				

