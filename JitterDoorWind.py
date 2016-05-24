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


filenames = ['BedroomADoorImputeMedian.txt', 'BedroomAWindowAImputeMedian.txt', 'BedroomAWindowBImputeMedian.txt',
			'BedroomBWindowTwentyImputeMedian.txt', 'EntrywayCDoorAImputeMedian.txt', 'EntrywayCDoorBImputeMedian.txt',
			'MainEntrywayImputeMedian.txt']


filenamesOut = ['BedroomADoorMedJitter.txt', 'BedroomAWindowAMedJitter.txt', 'BedroomAWindowBMedJitter.txt',
			'BedroomBWindowTwentyMedJitter.txt', 'EntrywayCDoorAMedJitter.txt', 'EntrywayCDoorBMedJitter.txt', 'MainEntrywayMedJitter.txt']

''''BedroomADoorMin.txt, BedroomAWindowAMin.txt, BedroomAWindowBMin.txt, BedroomBWindowTwentyMin.txt, EntrywayCDoorAMin.txt, EntrywayCDoorBMin.txt, MainEntrywayMin.txt
'''



file_in = []
file_out = []

f0 = []
f1 = []
f2 = []
f3 = []
f4 = []
f5 = []
f6 = []

file_in_list = [f0, f1, f2, f3, f4, f5, f6]

file_start = []
file_end = []
count = []

len0 = len(filenames)
#print len0 

for item in filenames:
	file_in.append(open(item, 'r'))
#print file_in[0]

for item in filenamesOut:
	file_out.append(open(item, 'w'))


for j in range(len0):
	count = 0 
	for lines in file_in[j]:
		count += 1 
		#print lines 
		tempStrs = lines
		tempStrsSplit = re.split(r'\t', tempStrs)
		nonN = tempStrsSplit[3].rstrip()
		file_in_list[j].append([tempStrsSplit[0], tempStrsSplit[1], tempStrsSplit[2], nonN])
		#print count 

	file_start.append(file_in_list[j][0])
	file_end.append(file_in_list[j][count-1])
print file_start[0][0]	
	#print file_in_list[0][count][0]  #  file_in_list[1][0][0], file_in_list[6][0][0]
#print count
#print file_start
#print file_start[0],file_start[1][0]
def writeline(inlist,fout):
	fout.write(str(inlist[0]))
	file_out[j].write('\t')
	fout.write(str(inlist[1]))
	file_out[j].write('\t')
	fout.write(str(inlist[2]))
	file_out[j].write('\t')
	fout.write(str(inlist[3]))
	file_out[j].write('\n')
for j in range(len0):
	tempNum = 0 
	#for k in range(file_start[j][0], file_end[j][0], 600):
	istamp = int(float(file_start[j][0])+600)
	#print file_end[j][0]
	while (istamp < int(float(file_end[j][0]))):
		#print istamp, istamp-600
		#print file_start[j]

		tempStart = tempNum
		#print file_in_list[j][tempNum][0]
		while (float(file_in_list[j][tempNum][0]) <= float(istamp)):
			#print file_in_list[j][tempNum][0]
			tempNum += 1

		#tempNum = tempNum -1
		#print file_in_list[j][tempStart], file_in_list[j][tempNum]

		#print  file_in_list[0][tempNum]
		if (file_in_list[j][tempStart][3] in ('ON','OPEN') and file_in_list[j][tempNum-1][3] in ('OFF', 'CLOSE')):
			writeline(file_in_list[j][tempStart], file_out[j])

			#file_out[j].write(str(file_in_list[j][tempStart]))
			writeline(file_in_list[j][tempNum-1], file_out[j])
			#file_out[j].write(str(file_in_list[j][tempNum-1]))
			
			

		elif (file_in_list[j][tempStart][3] in ('ON','OPEN') and file_in_list[j][tempNum-1][3] in ('ON','OPEN') and file_in_list[j][tempStart][0] != file_in_list[j][tempNum-1][0] and tempNum-1-tempStart>1):
			writeline(file_in_list[j][tempStart], file_out[j])
			#file_out[j].write(str(file_in_list[j][tempStart]))
			writeline(file_in_list[j][tempNum-2], file_out[j])
			#file_out[j].write(str(file_in_list[j][tempNum-2]))
			

		elif (file_in_list[j][tempStart][3] in ('ON','OPEN') and file_in_list[j][tempNum-1][3] in ('ON','OPEN') and file_in_list[j][tempStart][0] == file_in_list[j][tempNum-1][0]):
			writeline(file_in_list[j][tempNum-1], file_out[j])
			#file_out[j].write(str(file_in_list[j][tempNum-1]))
			
	

		elif (file_in_list[j][tempStart][3] in ('OFF', 'CLOSE') and file_in_list[j][tempNum-1][3] in ('OFF', 'CLOSE') and file_in_list[j][tempStart][0] != file_in_list[j][tempNum-1][0]):
			writeline(file_in_list[j][tempStart+1], file_out[j])
			#file_out[j].write(str(file_in_list[j][tempStart+1]))
			writeline(file_in_list[j][tempNum-1], file_out[j])
			#file_out[j].write(str(file_in_list[j][tempNum-1]))
			#file_out[j].write('\n')		

		elif (file_in_list[j][tempStart][3] in ('OFF', 'CLOSE') and file_in_list[j][tempNum-1][3] in ('OFF', 'CLOSE') and file_in_list[j][tempStart][0] == file_in_list[j][tempNum-1][0]):
			writeline(file_in_list[j][tempNum-1], file_out[j])
			#file_out[j].write(str(file_in_list[j][tempNum-1]))
			#file_out[j].write('\n')

		elif (file_in_list[j][tempStart][3] in ('OFF', 'CLOSE') and file_in_list[j][tempNum-1][3] in ('ON','OPEN') and tempNum-1-tempStart>1):
			writeline(file_in_list[j][tempStart+1], file_out[j])
			#file_out[j].write(str(file_in_list[j][tempStart+1]))
			#file_out[j].write('\n')
			writeline(file_in_list[j][tempNum-2], file_out[j])
			#file_out[j].write(str(file_in_list[j][tempNum-2]))
			#file_out[j].write('\n')	

		elif (file_in_list[j][tempStart][3] in ('OFF', 'CLOSE') and file_in_list[j][tempNum-1][3] in ('ON','OPEN') and tempNum-1-tempStart == 1):
			writeline(file_in_list[j][tempStart], file_out[j])
			#file_out[j].write(str(file_in_list[j][tempStart]))
			#file_out[j].write('\n')	
			writeline(file_in_list[j][tempNum-1], file_out[j])
			#file_out[j].write(str(file_in_list[j][tempNum-1]))
			#file_out[j].write('\n')		

		istamp = int(float(file_in_list[j][tempNum][0]))+600
		#print istamp 
		
		#print istamp 

'''
		if ((tempNum-tempStart) % 2 == 0 and tempNum-tempStart >= 2 ): 
			file_out[j].write(str(file_in_list[j][tempStart]))
			file_out[j].write('\n')
			file_out[j].write(str(file_in_list[j][tempNum-1]))
			file_out[j].write('\n')
		elif ((tempNum-tempStart) % 2 != 0 and tempNum-tempStart == 1): 
			file_out[j].write(str(file_in_list[j][tempStart]))
			file_out[j].write('\n')
		elif ((tempNum-tempStart) % 2 != 0 and tempNum-tempStart >= 3): 
			file_out[j].write(str(file_in_list[j][tempStart]))
			file_out[j].write('\n')
			file_out[j].write(str(file_in_list[j][tempNum-2]))
			file_out[j].write('\n')
'''
		#elif ((tempNum-tempStart) % 2 != 0 and tempNum-tempStart >= 1): 
		#	file_out[j].write(str(file_in_list[j][tempStart]))
		#	file_out[j].write('\n')
			#file_out[j].write(str(file_in_list[j][tempNum-2]))
			#file_out[j].write('\n')

	#tempStamp0 = file_start[j][0] + 600
	#tempNum0 = 0


	#elif (file_in_list[j][tempNum][0] > tempStamp):
	#	tempStamp = tempStamp + 600


	

		
		










