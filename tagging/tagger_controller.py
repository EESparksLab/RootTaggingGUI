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
from tkinter import *
import tagging.tagger_model as m
import tagging.tagger_view as v
import csv


"""
CLASS - Tagger_Controller
This class is the controller for the model view controller scheme. It runs all of the code and allows for communication
between the model and the view.

    ATTRIBUTES:
        - model: Instance of the model class for handling logic in this project.
        - view: Instance of the view class for handling the display of the project.


    METHODS:
        - __init__: Constructor, instantiates the model and view classes, binds buttons to certain actions for Tkinter.
"""
DRAW_TRIANGLES_MSG = "draw_triangles\ndraw the triangles starting with the highest\npoint first and connect it to the point right\nbelow it (same x value). Then draw the third \n to the left or right of the bottom\nof the vertical dots."
STEP_LIST = ["image_scale", "braceroot_count", "braceroot_width", "stalk_width", DRAW_TRIANGLES_MSG]
TAG_HEIGHT_CM = 10 # Height of the tag in centimeters
class Tagger_Controller(object):
    """
    __init__: constructor, instantiates the model and view classes

    Consumes: model(object), view(object)
    Produces: Nothing
    """
    def __init__(self, model, view, root):
        self.root = root
        self.model = model
        self.view = view
        self.root.bind("<Button 1>", self.on_click_left) # Bind Left Mouse Button
        self.root.bind("<r>", self.reset_data)
        self.root.bind("<Return>", self.switch_mode)
        self.root.bind("<l>", self.rotate_image_call)
        self.root.bind("<v>",self.view_finder_call)
        self.pixel_data_list = []
        self.mode = STEP_LIST[0]
        self.view.mode_text = self.mode
        self.mode_index = 0
        self.hasLabels = False

    def rotate_image_call(self, event):
        self.view.rotate_image()
    def view_finder_call(self,event):
        self.view.view_finder()

    def switch_mode(self, event):
        if self.view.has_changed == True:
            if self.mode_index+1 < len(STEP_LIST):
                self.mode_index += 1
                self.mode = STEP_LIST[self.mode_index]
                self.view.mode_text = self.mode
                self.view.update_mode()
                self.view.draw_data(self.pixel_data_list)
            else:
                self.view.has_changed = False
                self.view.draw_data(self.pixel_data_list)
                self.mode_index = 0
                self.write_data() # Once all the steps are finished, write the data
                self.mode = "image_scale"
                self.view.mode_text = "Done, click next"
                self.view.update_mode()
                self.pixel_data_list *= 0


    """
    reset_data, callback for when the 'r' key is pressed. Resets the progress made on the current plant to let the
                user start over.

    Consumes: An event
    Produces: Nothing
    """
    def reset_data(self, event):
        self.pixel_data_list *= 0
        self.mode_index = 0
        self.mode = STEP_LIST[0]
        self.mode_text = self.mode
        self.view.update(False)
        self.view.destroy_circles()
        self.view.has_changed = True




    def on_click_left(self, event):
        coords = self.view.circle_dict[self.view.count]

        if self.view.has_started and self.view.has_changed == True:
            if event.x > 100 and event.x < self.view.width-100 and self.mode != "braceroot_count": # I don't know
                self.view.draw_circle(event)
            if self.mode == "image_scale" and len(coords) % 2 == 0:
                print("scale")
                distance_pixels = self.model.get_pixel_distance(coords)
                self.pixel_data_list.append(distance_pixels)
            elif self.mode == "braceroot_count":
                pass
            elif self.mode == "braceroot_width" and len(coords) % 2 == 0:
                print("root width")
                self.pixel_data_list.append(self.model.get_pixel_distance(coords))
            elif self.mode == "stalk_width" and len(coords) % 2 == 0:
                print("Stalk width")
                self.pixel_data_list.append(self.model.get_pixel_distance(coords))
            elif "draw_triangles" in self.mode and len(coords) % 3 == 0:
                print("triangles")
                length = len(coords)
                coords[length-2][0] = coords[length-3][0]
                coords[length-1][1] = coords[length-2][1]
                points = [coords[length-3][0],coords[length-3][1],coords[length-2][0],coords[length-2][1],coords[length-1][0],coords[length-1][1]]
                self.view.canvas.create_polygon(points, fill = "lime green", width = 3)
                height = [coords[length-3], coords[length-2]]
                length = [coords[length-2], coords[length-1]]
                self.pixel_data_list.append(self.model.get_pixel_distance(height))
                self.pixel_data_list.append(self.model.get_pixel_distance(length))


    def write_data(self):
        hasLabels = False
        with open("pixel_data.csv", "a") as pixel_file:
            writer = csv.writer(pixel_file, delimiter = ",")
            if not self.hasLabels:
                writer.writerow(["Plant ID", "  Pixels/Label Height", "  W1 roots", "  W2 roots", "  W3 roots", "  W4 roots", "    Left root Width", "  Stalk Width", "  Root Height Left", "  Root Len Left", "  Root ht Right", "    Root Len Right"])
                self.hasLabels = True
           # a_or_b = "B"
            #if self.view.count % 2 == 0:
             #   a_or_b = "A"

            filename = self.view.image_list[self.view.count] #str(self.view.count) + a_or_b
            #plant_ID = filename
            plant_ID = "                " + str(self.view.plant_id_entry_box.get())
            #plant_ID = filename.split("/")[1].split("_")[0] + str("_") + filename.split("/")[1].split("_")[2].split(".")[0]
            image_scale = "          " + str(round(self.pixel_data_list[0], 3)) # First get image scale
            braceroot1_count = "                " + str(self.view.braceroot1_entry_box.get()) # Gets the input from the entry
            braceroot2_count = "          " + str(self.view.braceroot2_entry_box.get()) # Gets the input from the entry
            braceroot3_count = "          " + str(self.view.braceroot3_entry_box.get()) # Gets the input from the entry
            braceroot4_count = "          " + str(self.view.braceroot4_entry_box.get()) # Gets the input from the entry
            braceroot_width = "          " + str(round(self.pixel_data_list[1], 3)) # Width of braceroots
            stalk_width = "           " + str(round(self.pixel_data_list[2], 3)) # Width of the stalk
            height_left = "          " + str(round(self.pixel_data_list[3], 3))
            length_left = "          " + str(round(self.pixel_data_list[4], 3))
            height_right = "         " + str(round(self.pixel_data_list[5], 3))
            length_right = "         " + str(round(self.pixel_data_list[6], 3))
            writer.writerow([plant_ID, image_scale, braceroot1_count, braceroot2_count, braceroot3_count, braceroot4_count, braceroot_width, stalk_width, height_left, length_left, height_right, length_right])


#--------------------------------------------------------------------------------------------------------------------------------------------------
# Code Run By Main


def start():
    root = Tk()
    width = root.winfo_screenwidth()
    height = root.winfo_screenheight()
    should_resize = False
    if height < 2160:
        should_resize = True
    canvas_height, canvas_width = 1200, 1200
    model = m.Tagger_Model()
    view = v.Tagger_View(root, canvas_height, canvas_width, model.image_paths, should_resize)
    controller = Tagger_Controller(model, view, root)

    # Adds the title and color of the background for the app
    frame = Frame(root)
    frame.pack()
    root.title("Root Tagger")
    root.geometry(str(width) + "x" + str(height))
    root.configure(background = "purple")

    # Start the GUI
    root.mainloop()
