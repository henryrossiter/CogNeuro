# -*- coding: utf-8 -*-
"""
Henry Rossiter
henry.rossiter@utexas.edu 

This program reformats and trims actigraph data:
 -removes all NaN values at the beginning and end of data file
 -linearly interpolates up to 3 consecutive NaN values in the middle of the file
 -trims additional data off end of file if necessary

date should be in YYYY-MM-DD HH:MM:SS or YYYY/MM/DD HH:MM:SS format
@notes: http://strftime.org/
"""
#logging
import logging as errorlog
import os  # handy system and path functions
from subprocess import check_output
import sys

#set up logging to file
errorlog.basicConfig(
    filename='error.log', 
    filemode='w', 
    level=errorlog.WARNING, 
    format='%(asctime)s %(levelname)s %(name)s %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S')

logger=errorlog.getLogger(__name__)

import platform
import _winreg
def get_registry_value(key, subkey, value):
    key = getattr(_winreg, key)
    handle = _winreg.OpenKey(key, subkey)
    (value, type) = _winreg.QueryValueEx(handle, value)
    return value
    
def cpu():
    try:
        cputype = get_registry_value(
            "HKEY_LOCAL_MACHINE", 
            "HARDWARE\\DESCRIPTION\\System\\CentralProcessor\\0",
            "ProcessorNameString")
    except:
        import wmi, pythoncom
        pythoncom.CoInitialize() 
        c = wmi.WMI()
        for i in c.Win32_Processor ():
            cputype = i.Name
        pythoncom.CoUninitialize()
 
    if cputype == 'AMD Athlon(tm)':
        c = wmi.WMI()
        for i in c.Win32_Processor ():
            cpuspeed = i.MaxClockSpeed
        cputype = 'AMD Athlon(tm) %.2f Ghz' % (cpuspeed / 1000.0)
    elif cputype == 'AMD Athlon(tm) Processor':
        import wmi
        c = wmi.WMI()
        for i in c.Win32_Processor ():
            cpuspeed = i.MaxClockSpeed
        cputype = 'AMD Athlon(tm) %s' % cpuspeed
    else:
        pass
    return cputype
    
log_system = platform.system() +" " + platform.win32_ver()[0]#windows 7
log_cpu = cpu() #cpu
#log_video = subprocess.Popen('cmd.exe', stdin = subprocess.PIPE, stdout = subprocess.PIPE)
log_video = check_output("wmic path win32_VideoController get VideoProcessor")
log_video = (' '.join(log_video.split())).replace("VideoProcessor ","")

errorlog.error(log_system)
errorlog.error(log_cpu)
errorlog.error(log_video)

while True:
    try:
        try:
            import pandas
            import datetime
        except ImportError:
            import pip
            pip.main(['install', 'pandas'])
            pip.main(['install', 'datetime'])
            import pandas
            import datetime
            
        try: #use _file_ in most cases
            dir = os.path.dirname(__file__)
        except NameError:  #except when running python from py2exe script
            import sys
            dir = os.path.dirname(sys.argv[0])
        
        #directory
        oldD = os.path.join(dir, 'old')
        newD = os.path.join(dir, 'new')
        
        
        #preparing
        #rows to skip
        range(0, 22) + [24]
        
        #errorCount = counter for errors
        #allCount = counter for all files
        allCount = 1
        
        #list of all files
        l_aCount = []
        l_aFile = []
        l_aNum = []
        l_aResult = []

        redcapData = pandas.read_csv(os.path.join(dir,'AgingDecMem_DATA_2017-11-27_1502.csv'))
        
        #prepare text file      
        for filename in os.listdir(oldD):
            if filename.endswith('.csv'):
                print(filename)
                #read and remove meta data
                oldcsv = os.path.join(oldD, filename)
                df = pandas.read_csv(oldcsv, skiprows=range(0, 22) + [23])
                #format date to pandas datetime    
                df['Time'] = pandas.to_datetime(df['Time']).dt.strftime('%H:%M:%S')
                #combine to new column - datetime
                df['Datetime'] = df[['Date', 'Time']].apply(lambda x: ' '.join(x), axis=1)
                #keep specific columns
                df = df[['Datetime','Activity']]

                #clip data to 15 mins before the reported time of actigraph removal
                subjectNum = int(filename[1:5])
                print(subjectNum)
                
                #not missing datapoints
                missingNum = df['Activity'].isnull().sum()
                if missingNum == 0:
                    df=df.rename(columns = {'Datetime':'Time'}) #relabel
                    newcsv = os.path.join(newD, filename) #name
                    df.to_csv(newcsv, index = False, index_label = None) #name
                    result = 'normal'
                 
                #remove all NaN values at the beginning
                i = 0
                while i==df['Activity'].head(i).isnull().sum():
                    i=i+1
                df = df.iloc[i-1:]
                #remove all NaN values at the end
                i = 0
                while i==df['Activity'].tail(i).isnull().sum():
                    i=i+1
                df = df.iloc[:-i]
                
                missingNum = df['Activity'].isnull().sum()
                    
                #if not missing datapoints after the beginning and ends are trimmed
                if missingNum == 0:
                    df=df.rename(columns = {'Datetime':'Time'}) #relabel
                    newcsv = os.path.join(newD, filename) #name
                    df.to_csv(newcsv, index = False, index_label = None) #name
                    result = 'trimmed'

                #interpolate values with a maximum of 3 consecutive values
                else:
                    df['Activity'].interpolate(limit=3, inplace=True) 
                    df=df.rename(columns = {'Datetime':'Time'}) #relabel
                    missingNum = df['Activity'].isnull().sum()
                    #if not missing any values after interpolation, we're good to go!
                    if missingNum == 0:
                        newcsv = os.path.join(newD, filename) #name
                        df.to_csv(newcsv, index = False, index_label = None) #save
                        result = 'interpolated'
                    #start halfway throught the file and iterate downwards
                    
                    else:
                        #start halfway down dataset
                        i = df.shape[0]/2
                        # while i isnt at the end and x% of the total remaining rows < the amount of non-NaN cells between i and the end
                        while (i<=df.shape[0] - 1 and (df.shape[0] - i)*.3 < df['Activity'].tail(df.shape[0]-i).count()):
                            i = i+1
                        # if i is not at the index of the last item

                        #not missing datapoints
                        missingNum = df['Activity'].isnull().sum()
                 
                        if i<df.shape[0] - 1:
                            
                            df = df.iloc[:i]
                            if missingNum==0:
                                df=df.rename(columns = {'Datetime':'Time'}) #relabel
                                newcsv = os.path.join(newD, filename) #name
                                df.to_csv(newcsv, index = False, index_label = None) #name
                                result = 'edited'
                            else:
                                result = 'skipped'
                        
                        #if still missing data discard whole dataset
                        else:
                            result = 'skipped'

                #append all lists
                l_aCount.append(allCount)
                l_aFile.append(filename)
                l_aNum.append(missingNum)        
                l_aResult.append(result)
                allCount = allCount + 1
            #if non csv file
            else:
                continue
        
        #log all files
        aCount_df = pandas.DataFrame({'index': l_aCount, 'file': l_aFile, 'count': l_aNum, 'result': l_aResult})
        aCount_df = aCount_df[['index','file','count','result']]
        aFilename = "#all_" + datetime.datetime.now().strftime("%Y-%m-%d-%H%M")
        Acsv = os.path.join(newD, aFilename + ".csv")
        aCount_df.to_csv(Acsv, index = False, index_label = None)
        
        del aCount_df, Acsv, aFilename, l_aCount, l_aFile, l_aNum
       
    except Exception, e:
        logger.warning(e, exc_info=True)
        sys.exit(3)        
    break
    
