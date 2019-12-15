from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

import os
import stat

gAuth = GoogleAuth()
gAuth.LocalWebserverAuth()

drive = GoogleDrive(gAuth)

file_list = drive.ListFile({'q': "'root' in parents and trashed=false"}).GetList()
for file1 in file_list:
    print('title: %s, id: %s' % (file1['title'], file1['id']))

file = 'client_secrets.json'
gAuth.LoadClientConfigFile(file)
