from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

gAuth = GoogleAuth()


file = 'client_secrets.json'
gAuth.LoadClientConfigFile(file)

if gAuth.credentials is None:
    gAuth.LocalWebserverAuth()
elif gAuth.access_token_expired:
    gAuth.Refresh()
else:
    gAuth.Authorize()

gAuth.SaveCredentials(file)

drive = GoogleDrive(gAuth)

file_list = drive.ListFile({'q': "'root' in parents and trashed=false"}).GetList()
for file1 in file_list:
    print('title: %s, id: %s' % (file1['title'], file1['id']))

