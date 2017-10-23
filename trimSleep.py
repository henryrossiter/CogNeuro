import csv
import os
from datetime import datetime, date
#returns a list of the indexes of redcap_sleepsurvey that correspont th subject (num)'s sleep data
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
def sumActivity(sleepStartIndex,WakeIndex,subjectData):
    tot = 0
    for i in range(sleepStartIndex,WakeIndex+1):
        tot = tot+ int(subjectData[i]['SleepWake'])
    return tot
def adjustSleepStart(reportedStart, subjectData, dayNumber):
    startIndex = getTimeIndex(reportedStart, subjectData, dayNumber)-1
    #print("startIndex: "+str(startIndex))
    fiveInRow = False
    while not(fiveInRow):
        startIndex = startIndex + 1
        totNextTen = 0
        for i in range(0,10):
            totNextTen = totNextTen + int(subjectData[startIndex+i]['SleepWake'])
        fiveInRow = (totNextTen == 0)
    return startIndex
def getTimeIndex(time, subjectData, dayNumber):
    ind = dayNumber * 2880
    if time[1:2] == ':':
        time = "0"+time
    while not subjectData[ind]['Time'][:-3] == time:
        ind = ind+1
    return ind
def adjustWakeup(reportedWake, subjectData, dayNumber):
    startIndex = getTimeIndex(reportedWake, subjectData, dayNumber)+1
    #print("startIndex: "+str(startIndex))
    fiveInRow = False
    while not(fiveInRow):
        startIndex = startIndex - 1
        totNextTen = 0
        for i in range(0,10):
            totNextTen = totNextTen + int(subjectData[startIndex-i]['SleepWake'])
        fiveInRow = (totNextTen == 3)
    return startIndex

files = [f for f in os.listdir('.') if os.path.isfile(f)]
files.remove('redcap_sleepsurvey.csv')
files.remove('trimSleep.py')
#for f in files:
#    print(f)
    # do something
#rows is a list of orderedDicts
rows = []
with open('redcap_sleepsurvey.csv', newline='') as csvfile:
    log = csv.DictReader(csvfile)
    for a in log:
        rows.append(a)
#go through each subject's csv sheet
for f in files:
    #trialData is a list of orderedDicts
    #each index of trialData will correspond with the 'line' column on the subject's csv sheet
    trialData = []
    #find subject number
    num = int(f[3:f.find('_')])
    #find trial length
    days = getIndexes(num)
    print('subject number: '+str(num)+' trial length: '+str(len(days))+' nights.'+'\n')
    #for i in days:
        #print(rows[i])
        #print(log['sleep_time'])
    fieldNames = ['Line','Date','Time','Activity','Marker','WhiteLight','SleepWake','IntervalStatus']
    with open(f, newline='') as csvtrialfile:
        trial = csv.DictReader(csvtrialfile,fieldNames)
        rowNum = 0
        for a in trial:
            rowNum = rowNum +1
            if rowNum > 17: #cuts off useless information at top of each subject's csv
                trialData.append(a)
    trialDataStartTime = datetime.strptime(trialData[1]['Time'], '%H:%M:%S').time()
    dayNum = 0
    for day in days:
        reportedSleepStart = rows[day]['sleep_time']
        adjustedSleepStart = adjustSleepStart(reportedSleepStart, trialData, dayNum)
        print('adjusted sleep start '+ str(adjustedSleepStart))
        reportedWakeUp = rows[day]['wakeup_time']
        adjustedWakeup = adjustWakeup(reportedWakeUp, trialData, dayNum)
        print('adjusted wakup ' + str(adjustedWakeup))
        sleepTime = (adjustedWakeup-adjustedSleepStart)/120
        print('after adjustment, on day '+str(dayNum)+' the subject slept for '+ str(sleepTime) +' hours')
        totActivity = sumActivity(adjustedSleepStart,adjustedWakeup,trialData)
        totInactivity = (sleepTime*120)-totActivity
        sleepEfficiency = totInactivity/(sleepTime*120)
        print('their total activity was '+str(totActivity)+', reulting in a sleep efficiency score of: '+str(sleepEfficiency)+'\n')
        dayNum = dayNum + 1
x = input('press enter key to close')
