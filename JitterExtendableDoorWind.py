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

finpath = "/Volumes/Seagate Backup Plus Drive/IAQ/TempDoorWinMotion/ExtractAll/DoorWind/Atmo2/AfterCompleteImputeSeperated/"
foutpath = "/Volumes/Seagate Backup Plus Drive/IAQ/TempDoorWinMotion/ExtractAll/DoorWind/Atmo2/JitterExpandDoorWind/"

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
	for lines in Tlines:
		tempStrsSplit = re.split(r'\t', lines)
		# print tempStrsSplit
		# 1434750188.0	2015-06-19 21:43:08	psttime	CLOSE
		timeAt = math.floor(float(tempStrsSplit[0])/60)*60
		datetime1 = datetime.utcfromtimestamp(timeAt)
		a.append([tempStrsSplit[0], tempStrsSplit[1], tempStrsSplit[2], tempStrsSplit[3]])
		#a[-1][3] = a[-1][3].strip()
	file_length = count
	file_end = a[count - 1]  ## last line 
	countdown = 0
	f_out = open (foutpath + tname, 'w')
	len1 = len(a)
	## decide the first index number since the first line could be "OFF" (if so, just donot count this line in for JitterExtend)
	if (a[0][3].strip() == "OPEN"):
		saidx = 0
		aidx = 0
	else:
		saidx = 1
		aidx = 1
	file_start = a[aidx]  ## first line
	status = a[aidx][3].strip()

	while (aidx < len1 -3):
		tfix = saidx  ## open 
		while ((aidx < len1 -3) and int(float(a[aidx + 2][0])) - int(float(a[aidx + 1][0])) < 540):
			aidx = aidx + 2 
		saidx = aidx + 2
		#print a[tfix], a[aidx+1]
		writeline(a[tfix], f_out)
		writeline(a[aidx+1], f_out)
		aidx = aidx + 2
	f_out.close()

		
'''#print float(file_start[0]), float(file_end[0]), (float(file_end[0]) - float(file_start[0]))/60
	# WRONG 
	while (float(file_start[0]) < float(file_end[0])):
		tfix = aidx  # open
		aidx = aidx + 1 # next line	
		while (int(float(a[aidx][0])) - int(float(a[tfix][0])) < 600):
			aidx = aidx + 1
		if (a[aidx][3].strip() == "OPEN"):
			aidx = aidx + 1
		print "happy testing  happy testing  happy testing "
		print a[aidx]
		print a[tfix]
		print float(a[aidx][0]) - float(a[tfix][0])
	aidx = 0	'''
'''
		 a[aidx][3].strip() == 'OPEN'):
			print "happy testign line 63 find windows JitterExpandDoorWind.py HAPPY TESTING HAPPY TESTING"
			t = aidx + 1
			writeline(a[aidx], f_out)
			file_start = a[aidx+1]
			print a[aidx+1]
		# consider the last one: 
	if (t < count -1):
		writeline(a[aidx+1], f_out)
		writeline(a[count - 1], f_out)'''



				

