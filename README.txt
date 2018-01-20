Alfresco-Linux Backup Script
Author: Sean Ruffatti

This script was built to backup the current instance of Alfresco on DePaul's server.

Overview
 - There are 5 steps necessary to backup Alfresco.
 1. Stop Tomcat services
 2. Run pg_dumpall, store .sql file in target folder.
 3. Copy 'alf_data' or dir.root folder to target folder. 
 4. Tar gzip target folder.
 5. Restart Tomcat services.

Methods
1. stopTomcat()
	stopTomcat() stops tomcat by changing to the '/alfresco-community' directory and running the command './alfresco.sh stop tomcat' 
	The command to stop tomcat is stored in the variable 'stopTomcatCommand'. If this process errors, the script will not proceed with the backup, and log the error. 

2. startTomcat()
	startTomcat() starts tomcat by changing to the '/alfresco-community' directory and running the command './alfresco.sh start tomcat'.
	The command to start tomcat is stored in the variable 'startTomcatCommand'. If this process errors, the error will be logged and tomcat will not resume.

3. buildTimeStampDirectory()
	buildTimeStampDirectory() is responsible for creating the targer folder. First it checks if the folder exists, if it does not exist, then it will create one.
	The time stamp is assigned to the 'timeStampDir' variable using the datetime package. Formatted 'YYYYMMDD' 

4. checkForTimeStampDB()
	checkForTimeStampDB() is responsible for checking if there is a .sql file in the target directory, and if there is, remove the .sql file. 
	'pgFile' is the variable storing the time stamped sql file. Refer to the timeStampDB variable. Formated 'YYYYMMDD_HHMMSS'

5. dumpDatabase()
	dumpDatabase() is responsible for running the pg_dumpall command. First, we change to the '/alfresco-community/postgresql/bin'.
	Then we run the command -  'PGPASSWORD= "mhc123" pg_dumpall -c -h localhost -p 5432 -U postgres -f /home/alfresco/alfresco-backup/<time-stamp>/dumped.sql'
		PGPASSWORD creates an environmental variable and you assign it a password. This is necessary so the script can access all the databases. 
		pg_dumpall writes all postgres databases of a cluster into one script file.
		-c includes SQL commands to clean databases before recreating them.
		-h Specifies the host name of the machine on which the database server is running. We use 'localhost'
		-p Specifies the TCP port
		-U User name to connect as.
		-f Send output to the specified file. If this is omitted, the standard output is used.
	
	If the pg_dumpall command fails, tomcat will restart, the backup will stop and the error will be logged. 

6. copyAlfData()
	copyAlfData() is responsible for taking a copy of alfresco's contentstore directory and placing the copy in the target directory. 

7. zipTargetFolder()
	zipTargetFolder() is responsible for zipping the target folder. It first creates a targz folder, then adds the backup and contentstore and then closes the file.

8. remomveDirectory()
	removeDir() is responbile for removing the non-zipped folder that holds the backup and the contentstore files.
