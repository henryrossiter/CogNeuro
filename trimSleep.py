#trims actigraph data in order to calculate sleep efficiency
#Henry Rossiter
import csv
import os
from datetime import datetime, date

#returns a list of the indexes of redcap_sleepsurvey that correspont the subject (num)'s sleep data
def getIndexes(num):
    ret = []
    with open('redcap_sleepsurvey.csv', newline='') as csvfile:
        dr = csv.DictReader(csvfile)
        count = 0
        for a in dr:
            if int(a['record_id'])==num:
                ret.append(count)
            count = count + 1
        return ret
    
#returns int sum of activity values  for [sleepStartIndex, Wake Index] and orderedDict subjectData    
def sumActivity(sleepStartIndex,WakeIndex,subjectData):
    tot = 0
    for i in range(sleepStartIndex,WakeIndex+1):
        tot = tot+ int(subjectData[i]['SleepWake'])
    return tot

# adjusts sleep start time based to the first instance of five straight minutes of sleep, based on actigraphs
# automatically computed sleep/wake output
def adjustSleepStart(reportedStart, subjectData, dayNumber):
    startIndex = getTimeIndex(reportedStart, subjectData, dayNumber)-1
    fiveInRow = False
    while not(fiveInRow):
        startIndex = startIndex + 1
        totNextTen = 0
        for i in range(0,10):
            totNextTen = totNextTen + int(subjectData[startIndex+i]['SleepWake'])
        fiveInRow = (totNextTen == 0)
    return startIndex

# finds index in orderedDict subjectData given a dayNumber int and a time in format HH:MM:SS or H:MM:SS
def getTimeIndex(time, subjectData, dayNumber):
    ind = dayNumber * 2880
    if time[1:2] == ':': #handle discrepancy of time format
        time = "0"+time
    while not subjectData[ind]['Time'][:-3] == time:
        ind = ind+1
    return ind

#returns 'adjusted' sleep start index. 'adjusted' time is set by finding the first 10 consecutive epochs of wake values after reported wake time
def adjustWakeup(reportedWake, subjectData, dayNumber):
    startIndex = getTimeIndex(reportedWake, subjectData, dayNumber)-59
    endIndex = startIndex+120
    fiveInRow = False
    while (not fiveInRow) and startIndex<endIndex:
        startIndex = startIndex + 1
        totNextTen = 0
        for i in range(0,10):
            totNextTen = totNextTen + int(subjectData[startIndex-i]['SleepWake'])
        fiveInRow = (totNextTen == 10)
    if startIndex>=endIndex:
        print('there was not an instance with 5 minutes of activity within 30 minutes of wakup time')
    return startIndex

files = [f for f in os.listdir('.') if os.path.isfile(f)]
files.remove('redcap_sleepsurvey.csv')
files.remove('trimSleep.py')
if 'Sleep_Efficiency.csv' in files:
    files.remove('Sleep_Efficiency.csv')

#rows is a list of orderedDicts
rows = []
with open('redcap_sleepsurvey.csv', newline='') as csvfile:
    log = csv.DictReader(csvfile)
    for a in log:
        rows.append(a)
        
#go through each subject's csv sheet
with open('Sleep_Efficiency.csv', 'w', newline='') as csvfile:
    output = csv.writer(csvfile)
    output.writerow(['subject id', 'day 1', 'day 2', 'day 3', 'day 4', 'day 5', 'day 6', 'day 7'])
    for f in files:
        #trialData is a list of orderedDicts
        #each index of trialData will correspond with the 'line' column on the subject's csv sheet
        trialData = []
        #find subject number
        num = int(f[3:f.find('_')])
        #find trial length
        days = getIndexes(num)
        print('subject number: '+str(num)+' trial length: '+str(len(days))+' nights.'+'\n')
        
        # column titles for new csv to be outputted
        fieldNames = ['Line','Date','Time','Activity','Marker','WhiteLight','SleepWake','IntervalStatus']
        with open(f, newline='') as csvtrialfile:
            trial = csv.DictReader(csvtrialfile,fieldNames)
            rowNum = 0
            for a in trial:
                rowNum = rowNum +1
                if rowNum > 17: #cuts off useless information at top of each subject's csv
                    trialData.append(a)
        dayNum = 0
        efficiencyVals =[] # array of the current subject's calculated sleep efficiencies
        #iterates through each day in the subject's file, adjusting sleep times and calculating sleep efficiency
        for day in days:
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
            print(efficiencyVals)


        newRow = [str(num)]
        for i in range(0,len(days)):
            newRow.append( str(efficiencyVals[i]))
        output.writerow(newRow)
x = input('press enter key to close')
