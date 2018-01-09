# -*- coding: utf-8 -*-
"""
Created on Sun Jan  7 18:31:13 2018

@author: Sean
"""

import subprocess

#Base directory
basedir = subprocess.check_output('pwd', shell=True)

#Configure Paths
alfrescoRoot = 'opt/alfresco-community'
dirRoot = alfrescoRoot + '/alf_data'
contentStorePath = dirRoot + '/contentstore'
postgresDatabasePath = alfrescoRoot + '/postgresql'

