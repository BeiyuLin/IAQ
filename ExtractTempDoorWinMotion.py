######## Extract the Motion/Motion Area Sensors' Data ##############################
######## To predict whether or not there is at least one person in the room ########
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

fpath = "/Volumes/Seagate Backup Plus Drive/atmo/new/atmo1.dat"
#f1readNames = "/Volumes/Seagate Backup Plus Drive/IAQ/TempDoorWinMotion/ExtractAll/Temp/"
f2readNames = "/Volumes/Seagate Backup Plus Drive/IAQ/TempDoorWinMotion/ExtractAll/DoorWind/"
#f3readNames = "/Volumes/Seagate Backup Plus Drive/IAQ/TempDoorWinMotion/ExtractAll/MotionSensor/"
freadNames = f2readNames
#tname = "AllTemp.txt"
tname = "AllDoorWin.txt"

data = open(fpath, 'rU')
lines = data.readlines()
data.close()
a = {}
a1 = {}
f_out = open(freadNames + "Atmo1/" + tname , 'w')
for line in lines:
	if (("OPEN" in line) or ("CLOSE" in line)):  ## extract the WINDOW/DOOR data 
	#if ("Control4-Temperature" in line):  ## extract the temp data 
		tempStrsSplit = re.split(r'\|', line)
		#### Skip some special notation by using if-condition like ---------+------ ####
		#if len(tempStrsSplit) < 2:
		#	continue
		#if (tempStrsSplit[6].rstrip() )
		#int_list = [int(x) for x in lines.split()]
		#print int_list
		t1 = tempStrsSplit[4].strip()
		t2 = tempStrsSplit[5].strip()
		t3 = tempStrsSplit[6].rstrip()
		t4 = tempStrsSplit[9].rstrip()
		a[t1, t2, t3.replace(" ","")] = t4.replace(" ","")
		a1[t1, t2, t4.replace(" ","")] = t3.replace(" ","")
		#a[tempStrsSplit[4].strip(), tempStrsSplit[5].rstrip(), tempStrsSplit[6].rstrip()] = tempStrsSplit[9].rstrip()
		#a1[tempStrsSplit[4].strip(), tempStrsSplit[5].rstrip(), tempStrsSplit[9].rstrip()] = tempStrsSplit[6].rstrip()
		f_out.write(str(t1))
		f_out.write('\t')
		f_out.write(str(t2))
		f_out.write('\t')
		f_out.write(str(t4.replace(" ","")))
		f_out.write('\t')
		f_out.write(str(t3.replace(" ","")))
		f_out.write('\n')
f_out.close()
#print a 	
 # 423766141 | db77490f-9e25-4b9c-9992-6d74aaea0ed5 | 0006800000021752 | 2015-07-20 19:55:44.353048+00 
 #	| 2015-07-20 19:55:44.353048 | 2015-07-20 12:55:44.353048 | 21.5           
 # 	| ZigbeeAgent | state    | RelayB               | c4:cardaccess_inhome:WCS10-R  | Control4-Temperature   
 # 	| rawevents | atmo2  | America/Los_Angeles

############################################################################################
############################## sort/classified same SENSOR LABLEs together  ################
############################################################################################
count = 0
c = []
c1 = []
b=sorted(a.items(), key=lambda x: x[1])   
b1=sorted(a1.items(), key=lambda x: x[1])   
blen = len(b)
b1len = len(b1)
#print b[0]
# ('2016-03-05 10:26:56.55808', ' 2016-03-05 02:26:56.55808', ' OK'), ' BathroomATemperature'),
#print b[0][0]
#('2016-03-05 10:26:56.55808', ' 2016-03-05 02:26:56.55808', ' OK')
#print b[1][0]
c.append(b[0][1])
c1.append(b1[0][1].replace(" ",""))
for i in range(blen-1):
	if (b[i][1] != b[i+1][1]):  ## if sesnor names are different. (b is a listed with a dictionary format)
		count += 1
		c.append(b[i+1][1].replace(" ", ""))
print c
for i in range(b1len-1):
	if (b1[i][1] != b1[i+1][1]):  ## if sesnor names are different. (b is a listed with a dictionary format)
		count += 1
		c1.append(b1[i+1][1].replace(" ",""))
print c1
#####################################################################################
############## EXCLUDE the OUTDOOR temp #############################################
#####################################################################################
'''list1 = ["BedroomAWindow","BedroomBWindow","DiningRoomAWindowA","DiningRoomAWindowB",
		"OfficeAWindowA","OfficeAWindowB"]
listR1 = list(set(c) - set(list1)) ## listR1 is the indoor temperature sensor data
print listR1, len(listR1), len(c), len(list1)'''

# atmo 1 with outside temperature
#[' BathroomATemperature', ' BedroomAWindow', ' BedroomBWindow', ' DiningRoomAWindowA', 
#' DiningRoomAWindowB', ' EntrywayBDoor', ' EntrywayCDoor', ' EntrywayDDoor', ' KitchenATemperature',
# ' MainDoor', ' OfficeAWindowA', ' OfficeAWindowB', ' RelayA', ' RelayB', ' RelayC', ' RelayD', ' RelayE']
# atmo 2 with outside temperature
#[' BathroomATemperature', ' BathroomAWindowA', ' BathroomBTemperature', ' BedroomAWindowA', 
#' BedroomAWindowB', ' DoorB', ' DoorC', ' DoorD', ' DoorE', ' DoorF', ' KitchenATemperature', 
#' KitchenAWindowA', ' MainDoor', ' OfficeAWindowA', ' RelayA', ' RelayB', ' RelayC', 
#' RelayD', ' RelayE', ' TRelayE']

############################################################################################################
############################## Write different sensor data into each file   ################################
############################################################################################################
#f1_out = open(freadNames + "Atmo1/" + ".txt", 'w')
data1 = open(freadNames + "Atmo1/" + tname, 'rU')
lines1 = data1.readlines()
data1.close()
############################################################################################################
############################## DONOT FORGET TO REMOVE ALL *.txt in Atmo1/Seperated/ before run #############
############################################################################################################
for line1 in lines1:
	tempStrsSplit1 = re.split(r"\t", line1)
	# print tempStrsSplit1
	# ['2016-03-11 21:27:47.181427', '2016-03-11 13:27:47.181427', 'MainDoor', '21.5\n']
	if (tempStrsSplit1[2] in c):
		#print tempStrsSplit1
		#a=round(float(tempStrsSplit1[0][17:22]))
		#timeTupleOri = (int(tempStrsSplit1[0][0:4]), int(tempStrsSplit1[0][5:7]), int(tempStrsSplit1[0][8:10]), 
		#				int(tempStrsSplit1[0][11:13]), int(tempStrsSplit1[0][14:16]), a, 0, 0, 0)
		#timeTupleStam = calendar.timegm(timeTupleOri)
		#timeSec = datetime.utcfromtimestamp(timeTupleStam)
		f1_out = open(freadNames + "Atmo1/Seperated/" + tempStrsSplit1[2] + ".txt", 'ab')
		#f1_out.write(str(timeTupleStam) + '\t')
		f1_out.write(str(tempStrsSplit1[0].strip()) + '\t')
		f1_out.write(str(tempStrsSplit1[2].strip()) + '\t')
		f1_out.write(str(tempStrsSplit1[3].strip()) + '\n')  ## tempStrsSplit1[3] already has \n
		f1_out.close()

#### wc -l RelayA.txt 
###  7241 RelayA.txt










