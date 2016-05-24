#!/usr/bin/env python
import sys
import time
import string
import calendar
from decimal import *
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import numpy
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

Atmo1TimeTupStart = (2015, 8, 25, 07, 00, 00, 0, 0, 0 )
Atmo1TimeTupEnd = (2015, 9, 03, 06, 59, 00, 0, 0, 0 )

Atmo2TimeTupStart = (2015, 07, 23, 07, 00, 00, 0, 0, 0 )
Atmo2TimeTupEnd = (2015, 8, 19, 06, 59, 00, 0, 0, 0 )

t1Start = calendar.timegm(Atmo1TimeTupStart)
t1End = calendar.timegm(Atmo1TimeTupEnd)

t2Start = calendar.timegm(Atmo2TimeTupStart)
t2End = calendar.timegm(Atmo2TimeTupEnd)

###################################################
######## START and END Time #######################
###################################################
tStart = float(t2Start)
tEnd = float(t2End)


# Atmo2 under the folder: AfterCombineInsert (adding days before the first data sending back)
#finpath = "/Volumes/Seagate Backup Plus Drive/IAQ/TempDoorWinMotion/ExtractAll/DoorWind/Atmo1/JitterExpandDoorWind/DiffMinu/InsertMissingData/AfterCombineInsert/"
finpath = "/Volumes/Seagate Backup Plus Drive/IAQ/TempDoorWinMotion/ExtractAll/DoorWind/Atmo2/JitterExpandDoorWind/DiffMinu/InsertMissingData/AfterCombineInsert/"
foutpath = "/Volumes/Seagate Backup Plus Drive/IAQ/TempDoorWinMotion/ExtractAll/DoorWind/Atmo2/JitterExpandDoorWind/DiffMinu/InsertMissingData/"

# os.mkdir(os.path.join(foutpath, "IAQTimePeriod"))


for filename in glob.glob(os.path.join(finpath, "*.txt")):
	data = open(filename, 'rU')
	tempNameSplit = re.split(r"\/", filename)
	tname = tempNameSplit[-1]

	Tlines = data.readlines()
	print tname
	TempFile = open(foutpath + "IAQperiod/DW" + tname, 'w')
	for lines in Tlines:
		tempSplit = re.split(r'\t', lines)
		# 1433985300.0	2015-06-11 01:15:00	PST	CLOSE
		if (tStart <= float(tempSplit[0]) <= tEnd):
			#TempFile.write(str(tempSplit[0]))
			#TempFile.write('\t')
			#TempFile.write(str(tempSplit[1]))
			#TempFile.write('\t')
			#timeAt = float(tempSplit[0])
			#datetime1 = datetime.utcfromtimestamp(timeAt)
			TempFile.write(str(tempSplit[2]))
			TempFile.write('\t')
			TempFile.write(str(tempSplit[3].strip()))
			TempFile.write('\n')
			


















