from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
import os

# foldertofind = 'Rettner Files'
folderfound = False
gAuth = GoogleAuth()
drive = GoogleDrive(gAuth)


def authenticateUser():
    gAuth.LoadCredentialsFile("credentials.txt")  # checks and loads a file holding the credentials of the user,
    # still needs the client_secrests.json file to authenticate with google drive API
    if gAuth.credentials is None:
        gAuth.LocalWebserverAuth()  # open a local webserver to authenticate, only needs to be loaded once
    elif gAuth.access_token_expired:
        try:
            gAuth.Refresh()
        except:
            print("Offline. Need to reauthenticate")
            gAuth.LocalWebserverAuth()
    else:
        gAuth.Authorize()
    gAuth.SaveCredentialsFile("credentials.txt")


def getFileList(searchFor=None):
    global folderfound, folderID
    if searchFor is None:
        print("Nothing to search for. Exiting.")
    file_list = drive.ListFile({'q': "'root' in parents and trashed=false"}).GetList()
    for folder in file_list:
        if searchFor in folder['title']:
            folderID = folder['id']
            folderfound = True
            break
        else:
            print('There is no folder called ' + searchFor + '. Try again.')
    if folderfound is True:
        file_list = drive.ListFile({'q': " '{}' in parents and trashed=false" .format(folderID)}).GetList()
        return file_list  # returns a list of files to be downloaded


def downloadFiles(file_list=None):
    path = './pictures'  # download files to the path the slideshow looks in
    os.chdir(path)
    for f in file_list:
        fileName = f['title']
        print('Downloading {}'.format(fileName))
        f_ = drive.CreateFile({'id': f['id']})
        f_.GetContentFile(fileName)
    os.chdir('..')  # return to the tld
