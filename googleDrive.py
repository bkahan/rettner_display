from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
import os
from PIL import Image


gAuth = GoogleAuth()
drive = GoogleDrive(gAuth)


def authenticateUser():
    gAuth.LoadCredentialsFile("credentials.txt")  # checks and loads a file holding the credentials of the user,
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


def getFileList(search_for=None):
    photo_list = []
    file_list = drive.ListFile({'q': "'root' in parents and trashed=false"}).GetList()
    try:
        for folder in file_list:
            if search_for in folder['title']:
                folder_ID = folder['id']
                photo_list = drive.ListFile({'q': " '{}' in parents and trashed=false".format(folder_ID)}).GetList()
        return photo_list
    except:
        print("Nothing to search for. Exiting.")
        print('There is no folder called ' + search_for + '. Try again.')


def downloadFiles(file_list=None):
    picture_path = './pictures'  # download files to the path the slideshow looks in
    if file_list is None:
        print("No files found")
    else:
        os.chdir(picture_path)
        for f in file_list:
            fileName = f['title']
            print('Downloading {}'.format(fileName))
            f_ = drive.CreateFile({'id': f['id']})
            f_.GetContentFile(fileName)
    os.chdir('..')  # return to the tld
