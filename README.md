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
