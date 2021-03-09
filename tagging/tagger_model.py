#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
#######################​####### TRIC ROBOTICS LLC. ###################​###########

root_tagging_gui: Fall 2019

main.py -
This file is used to launch the GUI. Uses pythons subprocess librarie to do so. I
personally like starting the program this way because it allows the default current directory to
be at the top level of the project.

Date Created: 	11/4/2019
Author(s): 		William Cantera (wcantera@udel.edu)

####################​###########################################​#################
"""

# Imports
from imutils import paths
import re
import math


"""
CLASS - Tagger_Model
This class handles all of the logic in the model view controller scheme

    ATTRIBUTES:
        - braceroot_count(int): The number of braceroots in a given image. This must be entered by the user


    METHODS:
        - __init__: Constructor
    
"""
class Tagger_Model():
    LABEL_HEIGHT = 10 # Centimeters
    """
    __init__: Constructor

    Consumes: Nothing
    Produces: Nothing
    """
    def __init__(self):
        self.braceroot_count = 0
        self.image_paths = [ img for img in paths.list_images("stalk_images") ]
        self.sort_paths()
    

    def sort_paths(self):
        temp = []
        for file_name in self.image_paths:
            split_name = file_name.split("_") #
            curr_index = ''.join(x for x in split_name[3] if x.isdigit()) # Analyzes the filename after the first number
            a_or_b = re.search("[AB]", split_name[3]).group()
            temp.append([int(curr_index), a_or_b, file_name])

        temp.sort(key = lambda x: x[0])
        for i in range(len(temp)-1):
            if i % 2 == 0 and "B" in temp[i]:
                temp2 = temp[i]
                temp[i] = temp[i+1]
                temp[i+1] = temp2        
        self.image_paths *= 0 # Clear the plant_directories list 
        self.image_paths = [ paths[2] for paths in temp ] # Dirs[1] is the sorted pathname, I no longer need the index 
    

    """
    get_pixel_distance, finds the distance in pixels between two coordinates, presumably drawn by the user

    Consumes: coords(list)
    Produces: distancce(float)
    """
    def get_pixel_distance(self, coords):
        x0 = coords[len(coords)-2][0]
        y0 = coords[len(coords)-2][1]
        x1 = coords[len(coords)-1][0]
        y1 = coords[len(coords)-1][1]
        # Distance formula, returns distance in pixels
        return math.sqrt(math.pow(x0 - x1, 2) + math.pow(y0 - y1, 2))
        
 
