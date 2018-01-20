# -*- coding: utf-8 -*-
"""
Created on Sun Jan  7 18:31:13 2018
Updated on Sat Jan 20 15:53:00 2018

NOTICE: Before running, please make sure 'postgres-client' is installed. 
to install run: 'sudo apt-get install postgresql-9.1' or current version'

@author: Sean Ruffatti
"""

import os, sys, datetime, shutil, tarfile, subprocess

#Base directory
currentWorkingDirectory = os.getcwd() #'home/alfresco/scripts'


#Time stamp
timeStampDir = datetime.datetime.now().strftime('%Y%m%d')
timeStampDB = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')


#Configure Paths
homeDir  = '/home'
userDir = homeDir + '/alfresco'
alfrescoRoot = userDir + '/alfresco-community'
alfrescoData = alfrescoRoot + '/alf_data'
postgresDatabaseBin = alfrescoRoot + '/postgresql/bin'
alfrescoBackupDir = userDir + '/alfresco-backup/'
pgTargetDir = alfrescoBackupDir + timeStampDir +"/"
pgTargetDirContentStore = pgTargetDir + "/contentstore"
pgFile = pgTargetDir + timeStampDB + '.sql'


#Postgresql pg_dumpall Variables
pgHost = 'localhost'
pgPort = '5432'
pgUser = 'postgres'
pgPasswd = '\"mhc123\"'


#Terminal commands
stopTomcatCommand = './alfresco.sh stop tomcat'
startTomcatCommand = './alfresco.sh start tomcat'
# 'PGPASSWORD= "mhc123" pg_dumpall -c -h 127.0.0.1 -p 5432 -U postgres -f /home/alfresco/alfresco-backup/<time-stamp>/dumped.sql'
pgDumpCommand = 'PGPASSWORD=' + pgPasswd + ' pg_dumpall -c -h '+ pgHost +' -p '+ pgPort +' -U '+ pgUser +' -f '+ pgFile  


#Method for stopping tomcat services
def stopTomcat():
    os.chdir(alfrescoRoot) # home/alfresco/alfresco-community'
    returnCode = subprocess.call(stopTomcatCommand, shell=True)
    if returnCode != 0:
        print('\tTomcat could not be stopped. Exiting script.')
        sys.exit('Tomcat could not be stopped.')
    else:
        print('\tTomcat services stopped')

#Method for starting tomcat services    
def startTomcat():
    os.chdir(alfrescoRoot) # home/alfresco/alfresco-community
    returnCode = subprocess.call(startTomcatCommand, shell=True)
    if returnCode != 0:
        print('\tTomcat failed to start. Start it manually.')
    else:
        print('\tTomcat is running.')
        
#Method to build time stamp directory
def buildTimeStampDirectory():
    print('\tCreating time stamp directory')
    os.chdir(alfrescoBackupDir)
    if not os.path.exists(pgTargetDir):
        os.mkdir(timeStampDir)
  
#Method to check for time Stamp DB file
def checkForTimeStampDB():
    try:
        os.remove(pgFile)
    except OSError:
        pass

#Method to issue postgres pg_dumpall command
def dumpDatabase():
    os.chdir(postgresDatabaseBin)
    print('\tRunning pg_dumpall command')
    returnCode = subprocess.call(pgDumpCommand, shell=True)
    if returnCode != 0:
        print('\tDatabase dump failed. Starting tomcat.')
        startTomcat()
        sys.exit('Database dump failed. Exiting script.')
    else:
        print('\tDatabase dump was successful.')
   
#Method to copy contentstore directory to target directory     
def copyAlfData():
    os.chdir(alfrescoData)
    print('Copying contentstore folder to target directory')
    src = './contentstore'
    try:
        shutil.copytree(src, pgTargetDirContentStore)
    except IOError:
        print('Unable to copt file.')

#method to zip target folder.   
def zipTargetFolder():
    os.chdir(alfrescoBackupDir)
    print('\tZipping target directory')
    currDir = './'+ timeStampDir
    zippedFile = timeStampDB + '.tar.gz'
    tar = tarfile.open(zippedFile, 'w:gz')
    tar.add(currDir)
    tar.close()

#method to remove original directory.
def removeDirectory():
    currDir = './'+ timeStampDir
    shutil.rmtree(currDir)

#Backup Process
stopTomcat()
buildTimeStampDirectory()
checkForTimeStampDB()
dumpDatabase()
copyAlfData()
zipTargetFolder()
removeDirectory()
startTomcat()













