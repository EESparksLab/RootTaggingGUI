#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
#######################​####### TRIC ROBOTICS LLC. ###################​###########

root_tagging_gui: Fall 2019

main.py -
This file is used to launch the GUI. I personally like starting the program this way
because it allows the default current directory to be at the top level of the project.

Date Created: 	11/4/2019
Author(s): 		William Cantera (wcantera@udel.edu)

####################​###########################################​#################
"""

# Imports
import tagging
import tagging.tagger_controller

tagging.tagger_controller.start()
