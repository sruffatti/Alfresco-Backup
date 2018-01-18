# -*- coding: utf-8 -*-
"""
Created on Sun Jan  7 18:31:13 2018

NOTICE: Before running, please make sure 'postgres-client' is installed. 
to install run: 'sudo apt-get install postgresql-9.1' or current version'

Alter the alfrescoRoot variable to contain the current name of the alfresco dir.
    /opt/<your alfresco root name>/

@author: Sean
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
pgHost = '127.0.0.1'
pgPort = '5432'
pgUser = 'postgres'
pgPasswd = 'mhc123'
pgBaseDir = userDir + '/alfresco-backup/'
pgTargetDir = pgBaseDir + timeStamp
pgFileName = pgTargetDir + '/dumped.sql'

#Terminal commands
stopTomcatCommand = './alfresco.sh stop tomcat'
startTomcatCommand = './alfresco.sh start tomcat'
# 'sudo pg_dumpall -c -h 127.0.0.1 -p 5432 -U alfresco -f /home/alfresco/alfresco-backup/<time-stamp>/dumped.sql'
pgDumpCommand = 'PGPASSWORD =' + pgPasswd + 'pg_dumpall -c -h '+ pgHost +' -p '+ pgPort +' -U '+ pgUser +' -f '+ pgFileName  

#Stop Tomcat Services
os.chdir(alfrescoRoot) # home/alfresco/alfresco-community'
print('*****...STOPPING Tomcat services...*****')
os.system(stopTomcatCommand)
print('*****...Tomcat services stopped...*****')

#Build time stamp directory
print('******... CREATING TIME STAMP DIRECTORY...*****')
os.chdir(pgBaseDir)
os.mkdir(timeStamp)

#Postgres Dump 
os.chdir(postgresDatabasePath)
os.system(pgDumpCommand)