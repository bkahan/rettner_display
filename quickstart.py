from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

import os
import stat

gAuth = GoogleAuth()

gAuth.LoadCredentialsFile("currentCreds.txt")

if gAuth.credentials is None: # check to see if there are stored credentials
    gAuth.LocalWebserverAuth() # load the web verification if not 
elif gAuth.access_token_expired:
    gAuth.Refresh()
else:
    gAuth.Authorize()
    
gAuth.SaveCredentialsFile("currentCreds.txt")

drive = GoogleDrive(gAuth)



