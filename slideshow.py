"""
original code: https://github.com/andrewdelph/python-slideshow-with-time-and-weather

updated for rettner media lab, author: ben kahan 2019

"""
import argparse
import os
import stat
import sys
import time
import datetime
import PIL
from PIL import Image
import threading
from queue import Queue
import pygame
from pygame.locals import QUIT, KEYDOWN, K_ESCAPE
import pyowm

import googleDrive as gd

location = 'Rochester,NY,USA'
tempUnit = 'fahrenheit'
folderName = 'Rettner Files'
owm_api_key = '98b2dc257732f2825cf3a14eaff380bd'


file_list = []  # a list of all images being shown
title = "Rettner Media Lab"  # caption of the window...
wait_time = 5  # default time to wait between images (in seconds)


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


def input(events):
    """A function to handle keyboard/mouse/device input events. """
    for event in events:  # Hit the ESC key to quit the slideshow.
        if (event.type == QUIT or
                (event.type == KEYDOWN and event.key == K_ESCAPE)):
            pygame.quit()


def timeSince(lastTime, interval):
    if (time.time() - lastTime) >= interval:
        return True
    else:
        return False


def cropImage(image_list, width, height):
    for image in image_list:
        img = Image.open(image)
        img_width, img_height = img.size
        left = (img_width - width) / 2
        top = (img_height - height) / 2
        right = (img_width + width) / 2
        bottom = (img_height + height) / 2
        # Crop the center of the image
        img = img.crop((left, top, right, bottom))
        img.save(image)


def main(start_dir="."):
    # gd.authenticateUser()  # authenticate the user
    # toDownload = gd.getFileList(folderName)
    # gd.downloadFiles(toDownload)

    lastSwitch = time.time()
    lastWeather = time.time()

    owm = pyowm.OWM(owm_api_key)
    observation = owm.weather_at_place(location)
    w = observation.get_weather()
    temperature = (w.get_temperature(tempUnit))['temp']
    status = w.get_status()

    pygame.init()

    # Test for image support
    if not pygame.image.get_extended():
        print("Your Pygame isn't built with extended image support.")
        print("It's likely this isn't going to work.")
        sys.exit(1)

    walktree(start_dir, addtolist)
    if len(file_list) == 0:
        print("Sorry. No images found. Exiting.")
        sys.exit(1)

    modes = pygame.display.list_modes()
    pygame.display.set_mode(max(modes))

    screen = pygame.display.get_surface()
    screen_width, screen_height = screen.get_size()

    cropImage(file_list, screen_width, screen_height)

    pygame.display.set_caption(title)
    pygame.display.set_mode(max(modes), pygame.RESIZABLE)
    pygame.mouse.set_visible(0)

    # create font
    timeFont = pygame.font.Font("indulta/Indulta-SemiSerif-boldFFP.otf", 100)
    dateFont = pygame.font.Font("indulta/Indulta-SemiSerif-boldFFP.otf", 60)
    weatherFont = pygame.font.Font("indulta/Indulta-SemiSerif-boldFFP.otf", 60)

    current = 0
    num_files = len(file_list)  # need to update num_files -> update file_list 

    while True:
        try:
            img = pygame.image.load(file_list[current])
            screen.blit(img, (0, 0))

            # gets current weather
            if timeSince(lastWeather, 30):
                observation = owm.weather_at_place(location)
                w = observation.get_weather()
                temperature = (w.get_temperature(tempUnit))['temp']
                status = w.get_status()
                print(status)
                lastWeather = time.time()
                print("updating weather")

            # gets the current time and displays it
            timeText = datetime.datetime.now().strftime("%I:%M%p")
            dateText = datetime.datetime.now().strftime("%B %d, %Y")
            weatherText = str(int(temperature)) + "'F  " + status

            timeLabel = timeFont.render(timeText, 1, (255, 255, 255))
            dateLabel = dateFont.render(dateText, 1, (255, 255, 255))
            weatherLabel = weatherFont.render(weatherText, 1, (255, 255, 255))

            timeWidth, timeHeight = timeLabel.get_size()
            dateWidth, dateHeight = dateLabel.get_size()
            weatherWidth, weatherHeight = weatherLabel.get_size()

            screen.blit(weatherLabel, (0, screen_height - weatherHeight))

            screen.blit(timeLabel, (screen_width - timeWidth, screen_height - timeHeight - dateHeight))
            screen.blit(dateLabel, (screen_width - dateWidth, screen_height - dateHeight))

            pygame.display.flip()

            input(pygame.event.get())
            time.sleep(1 / 60)

        except pygame.error as err:
            print("Failed to display %s: %s" % (file_list[current], err))
            sys.exit(1)

        # When we get to the end, re-start at the beginning
        if timeSince(lastSwitch, wait_time):
            current = (current + 1) % num_files
            lastSwitch = time.time()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Recursively loads images '
                    'from a directory, then displays them in a Slideshow.'
    )

    parser.add_argument(
        'path',
        metavar='ImagePath',
        type=str,
        default='pictures',
        nargs="?",
        help='Path to a directory that contains images'
    )
    parser.add_argument(
        '--waittime',
        type=int,
        dest='waittime',
        action='store',
        default=1,
        help='Amount of time to wait before showing the next image.'
    )
    parser.add_argument(
        '--title',
        type=str,
        dest='title',
        action='store',
        default="Rettner Media Lab",
        help='Set the title for the display window.'
    )
    args = parser.parse_args()
    title = args.title
    main(start_dir=args.path)
