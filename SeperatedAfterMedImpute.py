#!/usr/bin/env python
import sys
import time
import string
import calendar
from decimal import *
import matplotlib
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
from dateutil import tz

fpath = "/Volumes/Seagate Backup Plus Drive/IAQ/TempDoorWinMotion/ExtractAll/DoorWind/Atmo2/FinalMergeMedian.txt"
tname0 = "test"
tname1 = "Sorted"
freadNames = "/Volumes/Seagate Backup Plus Drive/IAQ/TempDoorWinMotion/ExtractAll/DoorWind/"
a = {}
b = []
c = []


def utc_to_local(utc_dt):
	# Hardcode zones:
	from_zone = tz.gettz('UTC')
	to_zone = tz.gettz('US/Pacific')
	return utc_dt.replace(tzinfo=from_zone).astimezone(to_zone).replace(tzinfo=None)

def UTCToPST(utc_dt):
	# Hardcode zones:
	from_zone = tz.gettz('UTC')
	to_zone = tz.gettz('US/Pacific')
	return utc_dt.replace(tzinfo=from_zone).astimezone(to_zone).replace(tzinfo=None)

with open(fpath, 'rU') as f_in:
	for lines in f_in:
		tempStrs = lines
		tempStrsSplit = re.split(r'\t', tempStrs)
		#print tempStrsSplit
		a[tempStrsSplit[0].rstrip(), tempStrsSplit[1].rstrip(), tempStrsSplit[3].rstrip()] = tempStrsSplit[2].rstrip()
		#a.append(tempStrsSplit[5].rstrip())
		#a.append(tempStrsSplit[6].rstrip())
		#a.append(tempStrsSplit[9].rstrip())
#print a
############################################################################################
############################## sort/classified same SENSOR LABLEs together  ################
############################################################################################
count = 0
#with open("./Atmo2/" + tname0 + tname1+'BySensorNames.txt','w') as f1_out:
b=sorted(a.items(), key=lambda x: x[1])  ### here only use x[1] because a is a dictionarys
#print "happy testing bbbbbbbbbbb line 44 happy testing!!!"
#print b
blen = len(b)
#print blen
c.append(b[0][1])
#print b
for i in range(blen-1):
	if (b[i][1] != b[i+1][1]):  ## if sesnor names are different. (b is a listed with a dictionary format)
		count += 1
		c.append(b[i+1][1])
#print c  # c is all the sensors for temperature. 
#print count
# c is: 
# ['BathroomAWindowA', 'BathroomBWindowA', 'BedroomAWindowA', 'BedroomAWindowB', 
#'DoorB', 'DoorC', 'DoorD', 'DoorE', 'DoorF', 'KitchenAWindowA', 'MainDoor', 'OfficeAWindowA']

fmerge = open(fpath, 'rU')
Tlines = fmerge.readlines()
fmerge.close()

for lines in Tlines:
	tempStrsSplit1 = re.split(r"\t", lines)
	# print tempNameSplit
	# ['1458865088.0', '2016-03-25 00:18:08', 'DoorD', 'OPEN\n']
	if (tempStrsSplit1[2] in c):
		f1_out = open(freadNames + "Atmo2/AfterCompleteImputeSeperated/" + tempStrsSplit1[2] + ".txt", 'ab')
		#f1_out.write(str(timeTupleStam) + '\t')
		# from Atmo1MeidanSpecialCases.py: newStamp = Decimal((float(List1[i+1][0])+float(List1[i][0]))/2).quantize(Decimal('1e-6')) 
		a00 = Decimal(float(tempStrsSplit1[0].strip())).quantize(Decimal('1e-6'))
		utcTime = (datetime.utcfromtimestamp(a00)).strftime('%Y-%m-%d %H:%M:%S:%f')
		#newTempPST = utc_to_local(utcTime)
		newTempPST = (datetime.fromtimestamp(a00)).strftime('%Y-%m-%d %H:%M:%S:%f')
		#newTempPST = pstTime.strftime("%Y-%m-%d %H:%M:%S:%f")
		f1_out.write(str(a00) + '\t')
		f1_out.write(str(tempStrsSplit1[1].strip()) + '\t')
		f1_out.write(str(newTempPST) + '\t')
		f1_out.write(str(tempStrsSplit1[3].strip()) + '\n')  ## tempStrsSplit1[3] already has \n
		f1_out.close()




	
		

