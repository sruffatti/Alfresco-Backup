# -*- coding: utf-8 -*-
"""
Created on Sun Jan  7 18:31:13 2018

NOTICE: Before running, please make sure 'postgres-client' is installed. 
to install run: 'sudo apt-get install postgresql-9.1'

Alter the alfrescoRoot variable to contain the current name of the alfresco dir.
    /opt/<your alfresco root name>/

@author: Sean
"""

import os

#Base directory
currentWorkingDirectory = os.getcwd() #'/opt/alfresco-community/scripts'

#Configure Paths
optDir  = '/opt'
alfrescoRoot = optDir + '/alfresco-community'
dirRoot = alfrescoRoot + '/alf_data'
contentStorePath = dirRoot + '/contentstore'
postgresDatabasePath = alfrescoRoot + '/postgresql/bin'
databaseBackupPath = optDir + '/backup'

#Postgresql Variables
pgHost = '127.0.0.1'
pgPort = '5432'
pgUser = 'postgres'
pgTargetDir = '/opt/backup/pg_dumpall.sql'

#Bash commands
stopTomcatCommand = 'sudo ./alfresco.sh stop tomcat'
pgDumpCommand = 'sudo pg_dumpall -c -h '+ pgHost +' -p '+ pgPort +' -U '+ pgUser +' -f '+ pgTargetDir 

#Stop Tomcat Services
os.chdir(alfrescoRoot) # /opt/alfresco-community'
print('STOPPING Tomcat services...')
os.system(stopTomcatCommand) # requires Root privileges
print('Tomcat services stopped.')

#Postgres Dump 
os.chdir(postgresDatabasePath)
