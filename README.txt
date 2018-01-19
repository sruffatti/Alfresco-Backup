Alfresco-Linux Backup Script

This script was built to backup the current instance of Alfresco on DePaul's server.

Overview
 - There are 5 steps necessary to have a valuable backup of Alfresco.
 1. Stop Tomcat services
 2. Run pg_dumpall, store .sql file in target folder.
 3. Copy 'alf_data' or dir.root folder to target folder. 
 4. Tar gzip target folder.
 5. Start Tomcat services.