# University of Rochester - Rettner Media Lab

## Main Display - Automated Display  

The slideshow is run on a Raspberry Pi 3 Model B and updates periodically with current news, events, or other important information. It automatically downloads images from a specified folder and a specified Google account. 

## Expected Features: 

- Automatically remove old files if they are removed from the Google Drive folder
- Check for new files multiple times per day 
- Only show high-res images (relative to the display output) 
- Implement threading for asynchronous downloading and updating images 


## Updates:

~~Update 12/14/19: Fixed the image rescaling issue.~~

Update 12/15/19: Integrated Google Drive API. Upon start up, the program searches for files to download in a given folder

Update 12/16/19: Instead of scaling images, the program now crops images and center-aligns them. Easier to maintain picture quality 

##

Note: This project is based on the original code and project **Python Slideshow with Time and Weather** by [andrewdelph](https://github.com/andrewdelph/python-slideshow-with-time-and-weather). 

This project is maintained by Rettner Help Desk Staff. 

[Ronald Rettner Hall, University of Rochester](https://www.rochester.edu/college/rettnerhall/), 2018-2019