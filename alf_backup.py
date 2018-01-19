# -*- coding: utf-8 -*-
"""
Created on Sun Jan  7 18:31:13 2018

NOTICE: Before running, please make sure 'postgres-client' is installed. 
to install run: 'sudo apt-get install postgresql-9.1' or current version'

@author: Sean Ruffatti
"""

import os
import datetime

#Base directory
currentWorkingDirectory = os.getcwd() #'home/alfresco/scripts'

#Time stamp
timeStamp = datetime.datetime.now().strftime('%m-%d-%Y')

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
pgTargetDir = pgBackupDir + timeStamp
pgFileName = pgTargetDir + '/database ' + timeStamp + '.sql'

#Terminal commands
stopTomcatCommand = './alfresco.sh stop tomcat'
startTomcatCommand = './alfresco.sh start tomcat'
# 'PGPASSWORD= "mhc123" pg_dumpall -c -h 127.0.0.1 -p 5432 -U postgres -f /home/alfresco/alfresco-backup/<time-stamp>/dumped.sql'
pgDumpCommand = 'PGPASSWORD=' + pgPasswd + ' pg_dumpall -c -h '+ pgHost +' -p '+ pgPort +' -U '+ pgUser +' -f '+ pgFileName  

#Stop Tomcat Services
os.chdir(alfrescoRoot) # home/alfresco/alfresco-community'
print('*****...STOPPING Tomcat services...*****')
os.system(stopTomcatCommand)
print('*****...Tomcat services stopped...*****')

#Build time stamp directory
print('******... CREATING TIME STAMP DIRECTORY...*****')
os.chdir(pgBackupDir)
if not os.path.exists(pgTargetDir):
    os.mkdir(timeStamp)
print('******... TIME STAMP DIRECTORY CREATED ...******')

#Postgres Dump 
print('*****... CHANGING TO /postgresql/bin FOLDER...******')
os.chdir(postgresDatabasePath)
print('*****... RUNNING PG_DUMPALL COMMAND...******')
os.system(pgDumpCommand)
print('******... Databases were dumped...******')

#Copy alfresco data folder to target folder
print('*****... CHANGING TO /alfresco-community/alf_data FOLDER...******')
os.chdir(dirRoot)


#Tar gzip target folder.
print('******... CHANGING TO TARGET DIRECTORY...******')
os.chdir(pgTargetDir)
print('******... ZIPPING TARGET DIRECTORY...******')

#Start Tomcat services
print('******...STARTING Tomcat services...******')
os.chdir(alfrescoRoot)
os.system(startTomcatCommand)
print('******...Tomcat services started...******')
print('******...Alfresco backup was successful...******')














