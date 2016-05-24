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
import errno
from dateutil import tz
import numpy;
import numpy as np;
global TimeStampSecListUTC
global TimeMissingRecordList
global MinDur
global MinDur1
global Average
'''path = '/some/path/to/file' 
for filename in os.listdir(path):
    # do your stuff
for filename in glob.glob(os.path.join(path, '*.txt')):'''
#### UTC, SENSOR NAME, ACTIVITY
#finpath ="/Volumes/Seagate Backup Plus Drive/IAQ/OccupancyDataMotionSensor/ExtractMMA/Atmo2/"
# tname = "MainEntryway"
finpath = "/Volumes/Seagate Backup Plus Drive/IAQ/TempDoorWinMotion/ExtractAll/DoorWind/Atmo2/Seperated/"
foutpath = "/Volumes/Seagate Backup Plus Drive/IAQ/TempDoorWinMotion/ExtractAll/DoorWind/Atmo2/"
Dirlist = ["TStamp","MissingRec", "PairedRec", "MissingDuration", "AverageDuration", 
		"AverageSpecialCase", "MedianSpecialCase", "ImputeAveResult", "ImputeMedResult"]

##################################################################
#### make a list of directories under Atmo1 or Atmo2 or ...#######
##################################################################
for dirs in Dirlist:
	try: 
		os.mkdir(os.path.join(foutpath, dirs))
	except OSError:
		if not os.path.isdir(foutpath):
			raise

def utc_to_local(utc_dt):
	# Hardcode zones:
	from_zone = tz.gettz('UTC')
	to_zone = tz.gettz('US/Pacific')
	return utc_dt.replace(tzinfo=from_zone).astimezone(to_zone).replace(tzinfo=None)

def local_to_utc(pst_dt):
	# Hardcode zones:
	from_zone = tz.gettz('US/Pacific')
	to_zone = tz.gettz('UTC')
	return pst_dt.replace(tzinfo=from_zone).astimezone(to_zone).replace(tzinfo=None)


names = []
temptname = " "
count = 0
for filename in glob.glob(os.path.join(finpath, '*.txt')):
 	data = open(filename, 'rU')
 	tempNameSplit = re.split(r"\/", filename)
 	tname = tempNameSplit[-1]
 	print tname
 	count = count + 1
	Tlines = data.readlines()
	data.close()
	#print Tlines, count
	######################################################################################
	################## change time format into time.mktime (Time Stamp, local time)#######
	################## 					calendar.timegm		(UTC)  				   #######
	################## save to TimeStampSecUTCf file and TimeStampSecListUTC list  #######
	################## It's okay to not scan by '\t' or '\b'					   #######
	######################################################################################

	TimeStampSecListUTC = []
	#TimeMissingRecordList = []
	timeTupleOri=()
	timeTupleStam=()
	TimeStampSecUTCf = open(foutpath + "TStamp/" + "TStamp" + tname, 'w')
	for lines in Tlines:

		tempStrs = lines
		tempStrsSplit = re.split(r'\t', tempStrs)
		timeSec = datetime.strptime(tempStrsSplit[0],'%Y-%m-%d %H:%M:%S.%f')  ## UTC
		pst1 = utc_to_local(timeSec)
		timeTupleStam0 = (time.mktime(pst1.timetuple()) + pst1.microsecond / 1000000.0) ### mktime is to change the PST into UTC timeStamp.
		timeTupleStam = Decimal(timeTupleStam0).quantize(Decimal('1e-6'))
		#timeTupleStam = format(timeTupleStam0, '.6f')
		#timeTupleStam = round(timeTupleStam0, 6)
		#timeTupleStam = float(timeTupleStam1)
		#print "timeTupleStam", timeTupleStam
		#timeTupleStam = float("{0:.6f}".format(timeTupleStam0))
		#a=round(float(lines[17:22]))
		#timeTupleOri0 = (int(lines[0:4]), int(lines[5:7]), int(lines[8:10]), int(lines[11:13]), int(lines[14: 16]), float(lines[17:]), 0, 0, 0)
		#timeTupleOri = datetime.strptime(timeTupleOri0, "%Y-%m-%d %H:%M:%S.%f"[:-6])
		#timeTupleStam = calendar.timegm(timeTupleOri)
		#timeSec = datetime.utcfromtimestamp(timeTupleStam)

		#tempStrs = lines
		#tempStrsSplit = re.split(r'\t', tempStrs)

		#print tempStrsSplit[0],tempStrsSplit[1]
		#print tempStrsSplit[1: ]
		TimeStampSecListUTC.append([timeTupleStam, str(timeSec), tempStrsSplit[1], tempStrsSplit[2]])
		TimeStampSecUTCf.write(str(timeTupleStam)) # write into txt must be a string
		TimeStampSecUTCf.write('\t')
		TimeStampSecUTCf.write(str(timeSec))  ## it is okay here since the  TimeStampSecUTCf is written with stamp + the entire line
		TimeStampSecUTCf.write('\t')
		TimeStampSecUTCf.write(str(tempStrsSplit[1]))
		TimeStampSecUTCf.write('\t')
		TimeStampSecUTCf.write(str(tempStrsSplit[2]))
	
	####################################################################################	
	######### scan every line to see if there is on on (on on on) or off off off #######
	######### save to TimeMissingRecordListf file and TimeMissingRecordList list  ######
	######### Need to Scan by '\t', '\n'	PULLING MISSING DATA				  ######
	####################################################################################

	TimeMissingRecordList = []
	TimeMissingRecordListf = open(foutpath + "MissingRec/" + 'MissingRec' + tname,'w')
	sizeT = TimeStampSecListUTC
	for i in range(len(sizeT)-1):
		if (TimeStampSecListUTC[i][3] == TimeStampSecListUTC[i+1][3]):
			#TimeMissingRecordList.append([TimeStampSecListUTC[i], TimeMissingRecordList[i+1]])

			TimeMissingRecordListf.write(str(TimeStampSecListUTC[i]))
			TimeMissingRecordListf.write('\n')
			TimeMissingRecordListf.write(str(TimeStampSecListUTC[i+1]))
			TimeMissingRecordListf.write('\n')
			TimeMissingRecordListf.write('\n')
			
			#print TimeMissingRecordList
			TimeMissingRecordList.append(TimeStampSecListUTC[i])
			TimeMissingRecordList.append(TimeStampSecListUTC[i+1])
	#print TimeMissingRecordList[0]  #[1] #print Y-M-D H-M-S


	'''####################################################################################	
	######### Find the minumun duration from the TimeMissingRecordList           #######
	######### Save the result with TIME STAMP (time.mktine), original time and   #######
	###########################    sensor information  MINIMUM VALUES 			 #######
	####################################################################################

	MinDur = {}
	tempRange = (len(TimeMissingRecordList)-1)
	#print tempRange
	#with open ('BedroomADoorMissingRec.txt','rU') as CalMinDurationf:
	for j in range(0, tempRange, 2):
			#if (TimeMissingRecordList[j][0] != '\n'):
			#print (j, j+1)
		#key=str([j, TimeMissingRecordList[j][0], TimeMissingRecordList[j][1], j+1, TimeMissingRecordList[j+1][0], TimeMissingRecordList[j+1][1]])
		key=str([j, TimeMissingRecordList[j], j+1, TimeMissingRecordList[j+1]])
		MinDur[key] = TimeMissingRecordList[j+1][0]-TimeMissingRecordList[j][0]
			
	MinDur1=min(MinDur.items(), key=lambda x: x[1])  # MinDur1 is a list. 
	MinDurf = open(foutpath + 'MinDuration' + tname,'w')
	MinDurf.write(str(MinDur1))
	#print ("MinDur", int(MinDur1[1]))
	MinDurValue = int(MinDur1[1])'''

	####################################################################################	
	######### scan every line to see if there is paird on off or off on 		 #######
	######### save to TimePairedRecordListf file and TimePairedRecordList list    ######
	######### Need to Scan by '\t', '\n'		 PAIRED							  ######
	####################################################################################
	 
	TimePairedRecordList = []
	#open('BedroomADoorSimple.txt', 'rU') as CountMissingDataf:
	TimePairedRecordListf = open(foutpath + "PairedRec/" + 'PairedRec' + tname,'w')
	#with open(tname +'PairedRec.txt','w') as TimePairedRecordListf:
		#print TimeStampSecListUTC[0][3]
	sizeT = TimeStampSecListUTC
	# print sizeT
	# print TimeStampSecListUTC
	for i in range(0,len(sizeT)-1,1):
		#print TimeStampSecListUTC[i][3] 
		#print i
		#if (intern(TimeStampSecListUTC[0][3]) in (intern('ON'), intern('OPEN'))):
			
		if (intern(TimeStampSecListUTC[i][3].strip()) in (intern('ON'), intern('OPEN'))):
			#print "happy testing line 154 ImputingMS.py happy testing happy testing :) "
			#print TimeStampSecListUTC[i][3], TimeStampSecListUTC[i+1][3]
			if (intern(TimeStampSecListUTC[i+1][3].strip()) in (intern('OFF'),intern('CLOSE'))):
				#print "happy testing line 157 ImputingMS.py happy testing happy testing :) "
				#print TimeStampSecListUTC[i][3]
		#		TimeMissingRecordList.append([TimeStampSecListUTC[i], TimeMissingRecordList[i+1]])
				TimePairedRecordListf.write(str(TimeStampSecListUTC[i]))
				TimePairedRecordListf.write('\n')
				TimePairedRecordListf.write(str(TimeStampSecListUTC[i+1]))
				TimePairedRecordListf.write('\n')
				TimePairedRecordListf.write('\n')
				#print TimeMissingRecordList
				TimePairedRecordList.append(TimeStampSecListUTC[i])
				TimePairedRecordList.append(TimeStampSecListUTC[i+1])
		'''if (intern(TimeStampSecListUTC[0][3]) in (intern("OFF"), intern('CLOSE'))):
			if ((intern(TimeStampSecListUTC[i][3]) in (intern('OFF'),intern('CLOSE'))) and (intern(TimeStampSecListUTC[i+1][3]) in (intern('ON'),intern('OPEN')))):

		#		TimeMissingRecordList.append([TimeStampSecListUTC[i], TimeMissingRecordList[i+1]])
				TimePairedRecordListf.write(str(TimeStampSecListUTC[i]))
				TimePairedRecordListf.write('\n')
				TimePairedRecordListf.write(str(TimeStampSecListUTC[i+1]))
				TimePairedRecordListf.write('\n')
				TimePairedRecordListf.write('\n')
				#print TimeMissingRecordList
				TimePairedRecordList.append(TimeStampSecListUTC[i])
				TimePairedRecordList.append(TimeStampSecListUTC[i+1])'''
				#print TimePairedRecordList

	##########################################################################################
	################# Write the duration of missing data into Duration.txt 			  ########
	##########################################################################################
	Dur = []
	tempRange = (len(TimeMissingRecordList)-1)
	#print tempRange
	#with open ('BedroomADoorMissingRec.txt','rU') as CalMinDurationf:
	Durf = open(foutpath + "MissingDuration/" + 'Duration' + tname,'w')
	#with open(tname +'Duration.txt','w') as Durf:
	for j in range(0, tempRange, 2):
			#if (TimeMissingRecordList[j][0] != '\n'):
			#print (j, j+1)
		#key=str([j, TimeMissingRecordList[j][0], TimeMissingRecordList[j][1], j+1, TimeMissingRecordList[j+1][0], TimeMissingRecordList[j+1][1]])
		Dur.append([j, TimeMissingRecordList[j], j+1, TimeMissingRecordList[j+1],(TimeMissingRecordList[j+1][0]-TimeMissingRecordList[j][0])] )
		Durf.write(str([j, TimeMissingRecordList[j]]))
		Durf.write('\n')
		Durf.write(str([j+1, TimeMissingRecordList[j+1]]))
		Durf.write('\n')
		Durf.write(str((TimeMissingRecordList[j+1][0]-TimeMissingRecordList[j][0])))
		Durf.write('\n')
		#key=str([j, TimeMissingRecordList[j], j+1, TimeMissingRecordList[j+1]])
		#Dur[key] = TimeMissingRecordList[j+1][0]-TimeMissingRecordList[j][0]
#print Dur[0][4]
#print Dur[0][1][0]  ## 1433984582.0

	####################################################################################	
	#########  				Calculate the Median Duration MEDIAN 				 #######
	#########  				write into the file: *AverageMedianSecData.txt 		 #######
	####################################################################################
	#with open(tname + 'MedianDuration.txt', 'w') as MedianDurationf:
	MedianDurationList = []
	#print TimePairedRecordList
	for i in range(0,len(TimePairedRecordList)-1,2):
		#print TimePairedRecordList[i+1][0], TimePairedRecordList[i][0]
		temp = float(TimePairedRecordList[i+1][0])- float(TimePairedRecordList[i][0])
		#print "happy testing PAIRED DURATION line 191 ImputingMS.py Happy Testing Happy Testing"
		#print temp 

		MedianDurationList.append(temp)
	Median = round(np.median(MedianDurationList), 6)
	Median0 = float(round(np.median(MedianDurationList), 6))
	print 'Median:' + tname , Median

	####################################################################################	
	#########  				Calculate the Average Duration				 		 #######
	####################################################################################
	AverageSecDataf = open(foutpath + "AverageDuration/" + 'AverageSecData' + tname,'w')
	#with open(tname +'AverageMedianSecData.txt','w') as AverageSecDataf:
	AverageSecDataList = []	
	#print TimePairedRecordList
	for i in range(0,len(TimePairedRecordList)-1,2):
		temp = TimePairedRecordList[i+1][0]-TimePairedRecordList[i][0]
		AverageSecDataList.append(temp)
	sumdata = sum(AverageSecDataList)
	#print AverageSecDataList
	#print AverageSecDataList
	Average = round(numpy.mean(AverageSecDataList),6)
	print 'Average:' + tname, Average 
	#print ("Average", Average)
	########### Write Average into file ###############
	AverageSecDataf.write(tname)
	AverageSecDataf.write('\t')
	AverageSecDataf.write("Rounded Average:")
	AverageSecDataf.write(str(Average))
	AverageSecDataf.write('\t')
	AverageSecDataf.write("len:")
	AverageSecDataf.write(str(len(AverageSecDataList)))
	AverageSecDataf.write('\t')
	AverageSecDataf.write("Sum:")
	AverageSecDataf.write(str(sumdata))
	AverageSecDataf.write('\t')
	AverageSecDataf.write("Median:")
	AverageSecDataf.write(str(Median))

	##########################################################################################
	################# Compare the duration of missing data with AVERAGE SPECIAL CASES ########
	#################         write into specialCase.txt   						##############
	##########################################################################################
	lenDur = len(Dur)
	#print lenDur 
	count0 = 0
	SpecialCase = []
	for i in range(lenDur-1):
		if (int(Dur[i][4]) <= Average):
			#print Dur[i], Average
			count0 +=1
			SpecialCase.append(Dur[i][1])
			SpecialCase.append(Dur[i][3])
			#print SpecialCase, Dur[i][4],Average
	print 'okay okay Average Speical Cases'
	lenSpecialCase = len(SpecialCase)
	RecordSpecialStamp = {}
	Sf = open(foutpath + "AverageSpecialCase/" + 'AverageSpecialCase' + tname,'w')
	#with open(tname+'specialCase.txt','w') as Sf:
	for i in range(0,lenSpecialCase,2):
		RecordSpecialStamp[SpecialCase[i][1]] = SpecialCase[i][0]
		Sf.write(str(SpecialCase[i][0]))
		Sf.write('\t')
		Sf.write(str(SpecialCase[i][2]))
		Sf.write('\n')
	
	#RecordSpecialStamp.append(SpecialCase[i][0])
	lenDicMis = len(RecordSpecialStamp)
	print "Average Special Cases:", lenDicMis
	#print SpecialCase, RecordSpecialStamp
#print SpecialCase[0][0]   #: [1433984582.0, '2015-06-11 01:03:02', 'BedroomADoor', 'OFF']


	##########################################################################################
	################# Compare the duration of missing data with MEDIAN SPECIAL CASES  ########
	#################         write into specialCaseMedian.txt   					  ########
	##########################################################################################
	
	Mcount0 = 0
	SpecialCaseMedian = []
	for i in range(lenDur):
		#print "happy testing Duration line 228 ImputingMS.py Happy Testing Happy Testing"
		#print int(Dur[i][4])
		if (int(Dur[i][4]) < Median):
			#print Dur[i], Average
			Mcount0 +=1
			SpecialCaseMedian.append(Dur[i][1])
			SpecialCaseMedian.append(Dur[i][3])
			#print SpecialCase, Dur[i][4],Average
	print 'okay okay Median'
	lenSpecialCaseMedian = len(SpecialCaseMedian)
	RecordSpecialStampMedian = {}
	SfMedian = open(foutpath + "MedianSpecialCase/" + 'MedianSpecialCase' + tname,'w')
	#with open(tname+'specialCaseMedian.txt','w') as SfMedian:
	for i in range(0,lenSpecialCaseMedian,2):
		RecordSpecialStampMedian[SpecialCaseMedian[i][1]] = SpecialCaseMedian[i][0]
		SfMedian.write(str(SpecialCaseMedian[i][0]))
		SfMedian.write('\t')
		SfMedian.write(str(SpecialCaseMedian[i][2]))
		SfMedian.write('\n')
	
	#RecordSpecialStamp.append(SpecialCase[i][0])
	lenDicMisMedian = len(RecordSpecialStampMedian)
	print "Median Special Cases: ", lenDicMisMedian
	#print SpecialCase, RecordSpecialStamp
#print SpecialCase[0][0]   #: [1433984582.0, '2015-06-11 01:03:02', 'BedroomADoor', 'OFF']


	##########################################################################################
	################# Impute missing data with timing Average Period Time 	IMPUTE	 #########
	##########################################################################################
	def utcCalc(updatedStamp):
		return datetime.utcfromtimestamp(updatedStamp)

	def WriteIthLine(file0,imput0):
		file0.write(str(imput0[0]))  
		file0.write('\t')
		file0.write(str(imput0[1]))
		file0.write('\t')
		file0.write(str(imput0[2].strip()))
		file0.write('\t')
		file0.write(str(imput0[3].strip()))
		file0.write('\n')
		#f_out.write(str(TimeStampSecListUTC[i]))
		#f_out.write(str(TimeStampSecListUTC[i]))   # write into FILE
		#file0.write('\n')


	def inputActivity(ImputeAct):
		if (ImputeAct == "ON"):
			ImputeAct = "OFF"
		elif (ImputeAct == "OPEN"):
			ImputeAct = "CLOSE"
		elif (ImputeAct == "OFF"):
			ImputeAct = "ON"
		elif (ImputeAct == "CLOSE"):
			ImputeAct = "OPEN"
		return ImputeAct


	def ipuls1minusAverage(file1, imput1,imput1plus1):
		global a0 
		TemNewTimeStam = Decimal(float(imput1plus1[0]) - Average).quantize(Decimal('1e-6'))
		TempNewtimeUTC = (utcCalc(TemNewTimeStam)).strftime('%Y-%m-%d %H:%M:%S:%f')
		#datetime.timedelta(microseconds=1)
		#TempNewtimeUTC0 = datetime(*MTempNewtimeUTC0[:6])
		#TempNewtimeUTC = datetime.strptime(TempNewtimeUTC0, "%Y-%m-%d %H:%M:%S:%f")
		file1.write(str(TemNewTimeStam))  
		file1.write('\t')
		file1.write(str(TempNewtimeUTC))
		file1.write('\t')
		file1.write(str(imput1[2].strip()))
		file1.write('\t')

		a0 = inputActivity(imput1plus1[3].strip())
		#print imput1plus1[3], a0
		file1.write(str(a0))
		file1.write('\n')

	def iplusAverage(file2, imput2):
		global a1 
		TemNewTimeStam = Decimal(float(imput2[0]) + Average).quantize(Decimal('1e-6'))
		TempNewtimeUTC = (utcCalc(TemNewTimeStam)).strftime('%Y-%m-%d %H:%M:%S:%f')
		#TempNewtimeUTC0 = datetime(*MTempNewtimeUTC0[:6])
		#TempNewtimeUTC = datetime.strptime(TempNewtimeUTC0, "%Y-%m-%d %H:%M:%S:%f")
		file2.write(str(TemNewTimeStam))  
		file2.write('\t')
		file2.write(str(TempNewtimeUTC))
		file2.write('\t')
		file2.write(str(imput2[2].strip()))
		file2.write('\t')

		a1 = inputActivity(imput2[3].strip())
		#print imput1plus1[3], a0
		file2.write(str(a1))
		file2.write('\n')

	def ipuls1minusMedian(Mfile1, Mimput1, Mimput1plus1):
		global a0 
		MTemNewTimeStam = Decimal(float(Mimput1plus1[0]) - Median).quantize(Decimal('1e-6'))
		MTempNewtimeUTC = (utcCalc(MTemNewTimeStam)).strftime('%Y-%m-%d %H:%M:%S:%f')
		#MTempNewtimeUTC = datetime(*MTempNewtimeUTC0[:6])
		#MTempNewtimeUTC = datetime.strptime(str(MTempNewtimeUTC0), "%Y-%m-%d %H:%M:%S:%f")
		Mfile1.write(str(MTemNewTimeStam))  
		Mfile1.write('\t')
		Mfile1.write(str(MTempNewtimeUTC))
		Mfile1.write('\t')
		Mfile1.write(str(Mimput1[2].strip()))
		Mfile1.write('\t')

		a0 = inputActivity(Mimput1plus1[3].strip())
		#print imput1plus1[3], a0
		Mfile1.write(str(a0))
		Mfile1.write('\n')
		#Mfile1.write('\n')

	def iplusMedian(Mfile2, Mimput2):
		global a1 
		MTemNewTimeStam = Decimal(float(Mimput2[0]) + Median).quantize(Decimal('1e-6'))
		MTempNewtimeUTC = (utcCalc(MTemNewTimeStam)).strftime('%Y-%m-%d %H:%M:%S:%f')
		#MTempNewtimeUTC = datetime(*MTempNewtimeUTC0[:6])
		#MTempNewtimeUTC = datetime.strptime(str(MTempNewtimeUTC0), "%Y-%m-%d %H:%M:%S:%f")
		Mfile2.write(str(MTemNewTimeStam))  
		Mfile2.write('\t')
		Mfile2.write(str(MTempNewtimeUTC))
		Mfile2.write('\t')
		Mfile2.write(str(Mimput2[2].strip()))
		Mfile2.write('\t')

		a1 = inputActivity(Mimput2[3].strip())
		#print imput1plus1[3], a0
		Mfile2.write(str(a1))
		Mfile2.write('\n')
		#Mfile2.write('\n')

	#TempTimeStampSecListUTC = []
	newTimeStampUTC = []
	##########################################################################################
	################# Impute missing data with timing Average Period Time IMPUTE Average #####
	##########################################################################################
	f_in = open(foutpath + 'TStamp/' +'TStamp' + tname, 'r')
	f_out = open(foutpath + "ImputeAveResult/" + 'IAver' + tname, 'w')
	#with open(tname +'Simple.txt', 'r') as f_in, open(tname +'ImputeAverage.txt','w') as f_out:
	#		for lines in f_in:
	#			TempTimeStampSecListUTC.append(lines)
			#TimeStampSecListUTC
	size = len(sizeT)-1
	for i in range(size): 
		WriteIthLine(f_out,TimeStampSecListUTC[i])
		#for j in range(lenSpecialCase/2):
			#print RecordSpecialStamp[j]
			#print 
		if ((TimeStampSecListUTC[i][0] not in RecordSpecialStamp.values()) and TimeStampSecListUTC[i][3] == TimeStampSecListUTC[i+1][3]):
			if (TimeStampSecListUTC[0][3] in ('ON', 'OPEN') and TimeStampSecListUTC[i][3] in ('OFF', 'CLOSE')):
				ipuls1minusAverage(f_out, TimeStampSecListUTC[i],TimeStampSecListUTC[i+1])
				#print "Happy Testing line 449 ImputeDoorWin.py Happy Testing Happy Testing."
			elif (TimeStampSecListUTC[0][3] in ('ON', 'OPEN') and TimeStampSecListUTC[i][3] in ('ON', 'OPEN')):
				iplusAverage(f_out, TimeStampSecListUTC[i])
				#print "Happy Testing line 452 ImputeDoorWin.py Happy Testing Happy Testing."
			#elif (TimeStampSecListUTC[0][3] in ('OFF', 'CLOSE') and TimeStampSecListUTC[i][3] in ('ON', 'OPEN')):
			#		ipuls1minusAverage(f_out, TimeStampSecListUTC[i],TimeStampSecListUTC[i+1])	
					
			#elif (TimeStampSecListUTC[0][3] in ('OFF', 'CLOSE') and TimeStampSecListUTC[i][3] in ('OFF', 'CLOSE')):
			#		iplusAverage(f_out, TimeStampSecListUTC[i])
	##########################################################################################
	################# Impute missing data with timing MEDIAN Period Time IMPUTE MEDIAN #######
	##########################################################################################
	newTimeStampUTCM = []
	Mf_out = open(foutpath + "ImputeMedResult/" +'IMed' + tname, 'w')
	#with open(tname +'Simple.txt', 'r') as f_in, open(tname +'ImputeMedian.txt','w') as Mf_out:
	Msize = len(sizeT)-1
	for i in range(0, Msize): 
		WriteIthLine(Mf_out,TimeStampSecListUTC[i])
		TimeStampSecListUTC[0][3] = TimeStampSecListUTC[0][3].strip()
		TimeStampSecListUTC[i][3] = TimeStampSecListUTC[i][3].strip()
		TimeStampSecListUTC[i+1][3] = TimeStampSecListUTC[i+1][3].strip()
		#print TimeStampSecListUTC[0], TimeStampSecListUTC[i]
		#print TimeStampSecListUTC[0][3],TimeStampSecListUTC[i][3], TimeStampSecListUTC[i+1][3]
		if ((TimeStampSecListUTC[i][0] not in RecordSpecialStampMedian.values()) and TimeStampSecListUTC[i][3] == TimeStampSecListUTC[i+1][3]):
			#print "OKAY OKAY OKAY OKAYOKAY OKAYOKAY OKAYOKAY OKAYOKAY OKAYOKAY OKAYOKAY OKAY LINE 469 IMPUTEDOORWIN.PY"
			if (TimeStampSecListUTC[0][3] in ('ON', 'OPEN') and TimeStampSecListUTC[i][3] in ('OFF', 'CLOSE')):
				ipuls1minusMedian(Mf_out, TimeStampSecListUTC[i],TimeStampSecListUTC[i+1])
				#print "Happy Testing line 470 ImputeDoorWin.py Happy Testing Happy Testing."
			elif (TimeStampSecListUTC[0][3] in ('ON', 'OPEN') and TimeStampSecListUTC[i][3] in ('ON', 'OPEN')):
				iplusMedian(Mf_out, TimeStampSecListUTC[i])
				#print "Happy Testing line 473 ImputeDoorWin.py Happy Testing Happy Testing."
				#print TimeStampSecListUTC[0], TimeStampSecListUTC[i]
			#print "Happy Testing line 452 ImputeDoorWin.py Happy Testing Happy Testing."
			elif (TimeStampSecListUTC[0][3] in ('OFF', 'CLOSE') and TimeStampSecListUTC[i][3] in ('ON', 'OPEN')):
				iplusMedian(Mf_out, TimeStampSecListUTC[i])	
					
			elif (TimeStampSecListUTC[0][3] in ('OFF', 'CLOSE') and TimeStampSecListUTC[i][3] in ('OFF', 'CLOSE')):
				if ( (float(TimeStampSecListUTC[i+1][0]) - Median0) < float(TimeStampSecListUTC[i][0])):
					print "special case line 572'"
					print TimeStampSecListUTC[i]
					print TimeStampSecListUTC[i+1]
					continue
				else:
					ipuls1minusMedian(Mf_out, TimeStampSecListUTC[i],TimeStampSecListUTC[i+1])
		

'''count1=len(open("/Volumes/Seagate Backup Plus Drive/IAQ/OccupancyDataMotionSensor/TestFiles/Atmo2/TStamp/TStampUtilityAArea.txt").readlines())
count2=len(open("/Volumes/Seagate Backup Plus Drive/IAQ/OccupancyDataMotionSensor/TestFiles/Atmo2/ImputeAveResult/IAverUtilityAArea.txt").readlines())
count3=len(open("/Volumes/Seagate Backup Plus Drive/IAQ/OccupancyDataMotionSensor/TestFiles/Atmo2/MissingRec/MissingRecUtilityAArea.txt").readlines())
count4=len(open("/Volumes/Seagate Backup Plus Drive/IAQ/OccupancyDataMotionSensor/TestFiles/Atmo2/ImputeMedResult/IMedUtilityAArea.txt").readlines())
print "Original:" + tname , count1, "Total Missing:" + tname, count3/3, 
print "Total after Impute Average:" + tname, count2 , "Special Case Average:" + tname,lenDicMis, "ImputeDataAverage:" + tname,count3/3-lenDicMis
print "Total after Impute Median:" + tname, count4 , "Special Case Median:" + tname,lenDicMisMedian, "ImputeDataMedian:" + tname ,count3/3-lenDicMisMedian'''








