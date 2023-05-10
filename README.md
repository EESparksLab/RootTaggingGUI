# root_tagging_gui
This package is used to quickly tag features in images of roots. It can be used to measure angles and heights for any number of features, but it is currently set up to only measure several. It outputs a .csv with the measurements and the GUI parses each image.

The RootTaggingGUI was used in a publication:
Hostetler AN, Erndwein L, Reneau JW, Stager A, Tanner HG, Cook DD and Sparks EE.
“Multiple brace root phenotypes promote anchorage and limit root lodging in maize” PCE, 2022.
https://doi.org/10.1111/pce.14289

A user video can be found on our lab YouTube Channel: https://youtu.be/kbDPeC8ewCQ


## Installation on MacOS & Linux
Clone this repo, then open up a terminal in the RootTaggingGui directory and execute the command
```sh
./python_install.sh
```
This will create a custom python environment with all the libraries needed to run the application.
Now you can use the app by running
```sh
./GNUlauncher.sh
```
## Installation on Windows
Clone the repo, open a command prompt in RootTaggingGui directory and execute the command
```bat
python_install.cmd
```
This will create a custom python environment with all the libraries needed to run the application.
Now you can use the app by running
```bat
WinLauncher.bat
```

## User Guide
### Import photos to tag
Copy & paste the images into RootTaggingGui/stalk_images

### Start RootTaggingGUI
On Linux & MacOS
```sh
./GNUlauncher.sh
```
On Windows
```bat
WinLauncher.bat
```
### Press "start" to get to the tagging window
Features & keybinds of the tagging window include:
* "R" key resets all markers & entry boxes
* "L" key will redraw the image, rotated 90 degrees
* "V" key will open the viewfinder

> Using the Viewfinder
note: you may need to expand the viewfinder window to see the full image
Hit "L" top rotate 90 degrees, if needed
Click & Drag to draw a bounding box around the subject
Hit "P" to push the new image back to the tagging window

### Place scale markers
The image should have a reference popsicle stick that is a known width. Right-click on either edge
of the popsicle stick to place a marker (little red dot). After placing markers on both sides of the
popsicle stick the pythagoeran distance formula will be used to calculate the distance in pixels
between the two markers.
Hit "Enter" to continue to the next mode

### Brace Root Count
Manually count the number of brace roots emerging from each whorl and enter that value into the
entry boxes. The boxes are organized such that the lowest whorl is the lowest box.

Hit "Enter" to continue to the next mode

### Stalk width & brace root width
This operation is largly the same as placeing the scale markers
Place markers on either side of the stalk
Hit "Enter"
Place markers on either side of the right-most brace root
>Process root pixel data seems to make the assumption that it is the right-most brace root. I am partial to this for consistency purposes

Hit "Enter" to proceed to the next mode

### Triangles
With mouse-right-click, draw a triangle that extends from the emerging point of the top brace root, down to the ground, and out to the point where the brace roots meet the ground.
Do this on both sides of the stalk.
Hit "Enter" to Finish tagging, there should be an indicator that the tagging process is complete and then you can click the "Next" button to move on.

