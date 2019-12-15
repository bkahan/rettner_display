from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
import os

foldertofind = 'Rettner Files'
folderfound = False
filestodownload = []

gAuth = GoogleAuth()


def authenticateUser():
    gAuth.LoadCredentialsFile("credentials.txt")
    if gAuth.credentials is None:
        gAuth.LocalWebserverAuth()
    elif gAuth.access_token_expired:
        gAuth.Refresh()
    else:
        gAuth.Authorize()
    gAuth.SaveCredentialsFile("credentials.txt")


def getFileList():
    global folderfound
    file_list = drive.ListFile({'q': "'root' in parents and trashed=false"}).GetList()
    for folder in file_list:
        if folder['title'] == foldertofind:
            folderfound = True
            break
        else:
            print('There is no folder called ' + foldertofind + '. Try again.')
    if folderfound is True:
        file_list = drive.ListFile({'q': " '1t0HENJysR4JbM2EtMl-4--NrF4JC0kVK' in parents and trashed=false"}).GetList()
        return file_list


def downloadFiles(file_list=None):
    path = './pictures'
    os.chdir(path)
    for f in file_list:
        fileName = f['title']
        print('downloading {}'.format(fileName))
        f_ = drive.CreateFile({'id': f['id']})
        f_.GetContentFile(fileName)
    os.chdir('..')


drive = GoogleDrive(gAuth)


def main():
    authenticateUser()
    toDownload = getFileList()
    downloadFiles(toDownload)


main()
