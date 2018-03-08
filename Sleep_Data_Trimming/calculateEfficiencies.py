#trims actigraph data in order to calculate sleep efficiency
#outputs calculated sleep efficiencies to 'Sleep_Efficiency.csv'
#Henry Rossiter - hr7588 - henry.rossiter@utexas.edu

import csv
import os

#returns a list of the indexes of redcap_sleepsurvey that correspont the subject (num)'s sleep data
def getIndexes(num):
	print(num)
	ret = []
	with open('redcap_sleepsurvey.csv', newline='') as csvfile:
		dr = csv.DictReader(csvfile)
		count = 0
		try:
			for a in dr:
				if int(a['record_id'])==num:
					ret.append(count)
				count = count + 1
			return ret
		except:
			print("column record_id was not found. Check column naming and make sure file is comma delimited")
			sys.exit(1)

#returns int sum of activity values	 for [sleepStartIndex, Wake Index] and orderedDict subjectData
def sumActivity(sleepStartIndex,WakeIndex,subjectData):
	tot = 0
	for i in range(sleepStartIndex,WakeIndex+1):
		tot = tot+ int(subjectData[i]['SleepWake'])
	return tot

# adjusts sleep start time based to the first instance of five minutes with at least 60% sleep values, based on actigraphs
# automatically computed sleep/wake output
def adjustSleepStart(reportedStart, subjectData, dayNumber):
	startIndex = getTimeIndex(reportedStart, subjectData, dayNumber)-1
	fiveInRow = False
	while not(fiveInRow):
		startIndex = startIndex + 1
		totNextTen = 0
		for i in range(0,10):
			totNextTen = totNextTen + int(subjectData[startIndex+i]['SleepWake'])
		fiveInRow = (totNextTen <= 4)
	return startIndex

# finds index in orderedDict subjectData given a dayNumber int and a time string in format HH:MM:SS or H:MM:SS
def getTimeIndex(time, subjectData, dayNumber):
	ind = dayNumber * 2880
	if time[1:2] == ':': #handle discrepancy of time format
		time = "0"+time
		#print(time+' ' +str(dayNumber))
	while not subjectData[ind]['Time'][:-3] == time:
		try:
			ind=ind + 1
		except:
			print("reached end of subject's data file before finding "+time+" on day "+str(dayNumber))
			sys.exit(1)
	return ind

# returns 'adjusted' sleep start index. 'adjusted' time is set by finding the first instance of five minutes with at least 60% wake values
def adjustWakeup(reportedWake, subjectData, dayNumber):
	startIndex = getTimeIndex(reportedWake, subjectData, dayNumber)-59
	endIndex = startIndex+120
	fiveInRow = False
	while (not fiveInRow) and startIndex<endIndex:
		startIndex = startIndex + 1
		totNextTen = 0
		for i in range(0,10):
			totNextTen = totNextTen + int(subjectData[startIndex-i]['SleepWake'])
		fiveInRow = (totNextTen >= 6)
	if startIndex>=endIndex:
		print('there was not an instance with substantial activity within 30 minutes of wakeup time')
	return startIndex

#Gather all subject actigraph data files in directory
files = [f for f in os.listdir('.') if f.endswith('Analysis.csv')]

#rows is a list of orderedDicts
rows = []
with open('redcap_sleepsurvey.csv', newline='') as csvfile:
	#log is a dictreader, creates (nSubjects x nDayspersubject) orderedDicts
	log = csv.DictReader(csvfile)
	for a in log:
		rows.append(a)

#make new output file to record calculated sleep efficiencies
with open('Sleep_Efficiency.csv', 'w', newline='') as csvfile:
	output = csv.writer(csvfile)
	output.writerow(['subject id', 'day 1', 'day 2', 'day 3', 'day 4', 'day 5', 'day 6', 'day 7']) #column titles for output csv file
	for f in files:
		#trialData is a list of orderedDicts
		#each index of trialData will correspond with the 'line' column on the subject's csv sheet
		trialData = []
		#find subject number
		num = int(f[2:f.find('_')])
		#find trial length
		days = getIndexes(num)
		print('subject number: '+str(num)+' trial length: '+str(len(days))+' nights.'+'\n')

		# column titles for new csv to be outputted
		fieldNames = ['Line','Date','Time','Activity','Marker','WhiteLight','SleepWake','IntervalStatus']
		with open(f, newline='') as csvtrialfile:
			trial = csv.DictReader(csvtrialfile,fieldNames)
			rowNum = 0
			for a in trial:
				if (a['Marker']=='0'): #use this to cut of meta data when copying to trialData
					trialData.append(a)

		dayNum = 0	#reset day index for new participant
		efficiencyVals =[] # array of the current subject's calculated sleep efficiencies

		#find subject number
		num = int(f[2:f.find('_')])
		#find trial length
		days = getIndexes(num)
		print('subject number: '+str(num)+' trial length: '+str(len(days))+' nights.'+'\n')
		#iterates through each day in the subject's file, adjusting sleep times and calculating sleep efficiency
		for day in days:
			print("now calculating day "+str(dayNum+1))
			reportedSleepStart = rows[day]['sleep_time']
			adjustedSleepStart = adjustSleepStart(reportedSleepStart, trialData, dayNum)
			#print('adjusted sleep start '+ str(adjustedSleepStart))
			reportedWakeUp = rows[day]['wakeup_time']
			adjustedWakeup = adjustWakeup(reportedWakeUp, trialData, dayNum)
			#print('adjusted wakup ' + str(adjustedWakeup))
			sleepTime = (adjustedWakeup-adjustedSleepStart)/120
			#print('after adjustment, on day '+str(dayNum)+' the subject slept for '+ str(sleepTime) +' hours')
			totActivity = sumActivity(adjustedSleepStart,adjustedWakeup,trialData)
			totInactivity = (sleepTime*120)-totActivity
			sleepEfficiency = totInactivity/(sleepTime*120)
			#print('their total activity was '+str(totActivity)+', reulting in a sleep efficiency score of: '+str(sleepEfficiency)+'\n')
			efficiencyVals.append(sleepEfficiency)
			dayNum = dayNum + 1
			#print(efficiencyVals)

		#make array of subject number and sleep efficiency values
		# -- NOTE -- only outputs subjects' sleep efficiencies if at least 3 nights worth of sleep efficiencies could be obtained!"
		if len(efficiencyVals)>2:
			newRow = [str(num)]
			for i in range(0,len(days)):
				newRow.append( str(efficiencyVals[i]))
			#add newRow array to output csv file
			output.writerow(newRow)
			print("sleep efficiencies calculated for subject "+str(num)+"!")
		else:
			print("subject did not have enough usable data to obtain a reliable sleep efficiency")

#allows user to see error messages when ran from python shell
x = input('press enter key to close')
