#!/bin/bash

#It is best practice to create virtual environments for projects that require many packages installed
python3 -m venv ./python_environment  #Creates a new virtual environmnet in PWD
source ./python_environment/bin/activate  #swithces to our new virtual environment

#Now we can install the needed packages using pip
python3 -m pip install --upgrade pip
pip install numpy opencv-python pillow imutils



