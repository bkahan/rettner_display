from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
import os
import time
import stat

gAuth = GoogleAuth()
drive = GoogleDrive(gAuth)
time_to_sleep = 5 * 60
file_list = []


def getNewPhotos(folder_name=None):
    authenticateUser()
    walktree('./pictures', addtolist)
    toDownload = getFileList(folder_name)
    downloadFiles(toDownload)
    time.sleep(time_to_sleep)


def walktree(top, callback):
    """recursively descend the directory tree rooted at top, calling the
    callback function for each regular file. Taken from the module-stat
    example at: http://docs.python.org/lib/module-stat.html
    """
    for f in os.listdir(top):
        pathname = os.path.join(top, f)
        mode = os.stat(pathname)[stat.ST_MODE]
        if stat.S_ISDIR(mode):
            # It's a directory, recurse into it
            walktree(pathname, callback)
        elif stat.S_ISREG(mode):
            # It's a file, call the callback function
            callback(pathname)
        else:
            # Unknown file type, print a message
            print('Skipping %s' % pathname)


def addtolist(file, extensions=None):
    """Add a file to a global list of image files."""
    if extensions is None:
        extensions = ['.png', '.jpg', '.jpeg', '.gif', '.bmp']
    filename, ext = os.path.splitext(file)
    e = ext.lower()
    # Only add common image types to the list.
    if e in extensions:
        print('Adding to list: ', file)
        file_list.append(file)
    else:
        print('Skipping: ', file, ' (NOT a supported image)')


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
