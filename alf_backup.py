# -*- coding: utf-8 -*-
"""
Created on Sun Jan  7 18:31:13 2018

NOTICE: Before running, please make sure 'postgres-client' is installed. 
to install run: 'sudo apt-get install postgresql-9.1' or current version'

@author: Sean Ruffatti
"""

import os
import datetime
import shutil
import tarfile

#Base directory
currentWorkingDirectory = os.getcwd() #'home/alfresco/scripts'

#Time stamp
timeStampDir = datetime.datetime.now().strftime('%Y%m%d')
timeStampDB = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')

#Configure Paths
homeDir  = '/home'
userDir = homeDir + '/alfresco'
alfrescoRoot = userDir + '/alfresco-community'
dirRoot = alfrescoRoot + '/alf_data'
contentStorePath = dirRoot + '/contentstore'
postgresDatabasePath = alfrescoRoot + '/postgresql/bin'

#Postgresql Variables
pgHost = 'localhost'
pgPort = '5432'
pgUser = 'postgres'
pgPasswd = '\"mhc123\"'
pgBackupDir = userDir + '/alfresco-backup/'
pgTargetDir = pgBackupDir + timeStampDir +"/"
pgTargetDirContentStore = pgTargetDir + "/contentstore"
pgFileName = pgTargetDir + timeStampDB + '.sql'

#Terminal commands
stopTomcatCommand = './alfresco.sh stop tomcat'
startTomcatCommand = './alfresco.sh start tomcat'
# 'PGPASSWORD= "mhc123" pg_dumpall -c -h 127.0.0.1 -p 5432 -U postgres -f /home/alfresco/alfresco-backup/<time-stamp>/dumped.sql'
pgDumpCommand = 'PGPASSWORD=' + pgPasswd + ' pg_dumpall -c -h '+ pgHost +' -p '+ pgPort +' -U '+ pgUser +' -f '+ pgFileName  

#Stop Tomcat Services
os.chdir(alfrescoRoot) # home/alfresco/alfresco-community'
os.system(stopTomcatCommand)
print('\tTomcat services stopped')

#Build time stamp directory
print('\tCreating time stamp directory')
os.chdir(pgBackupDir)
if not os.path.exists(pgTargetDir):
    os.mkdir(timeStampDir)
    
#Check for time Stamp DB before 
try:
    os.remove(pgFileName)
except OSError:
    pass

#Postgres Dump 
os.chdir(postgresDatabasePath)
print('\tRunning pg_dumpall command')
os.system(pgDumpCommand)
print('\tDatabases were dumped')

#Copy alfresco data folder to target folder
os.chdir(dirRoot)
print('\tCopying contentstore folder to target directory')
contentStore = './contentstore'
shutil.copytree(contentStore, pgTargetDirContentStore)

#Tar gzip target folder.
os.chdir(pgBackupDir)
print('\tTar zipping target directory')
currDir = './' + timeStampDir
zippedFile = timeStampDB + '.tar.gz'
tar = tarfile.open(zippedFile, 'w:gz')
tar.add(currDir)
tar.close()

#Remove unzipped directory and all of its contents
shutil.rmtree(currDir)

#Start Tomcat services
print('\tStarting tomcat services')
os.chdir(alfrescoRoot)
os.system(startTomcatCommand)
print('\tTomcat services started')
print('\tAlfresco backup successful')














