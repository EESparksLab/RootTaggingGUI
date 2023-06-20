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
from tkinter import * # Keep at top
from PIL import Image, ImageTk, ImageDraw
from imutils import paths
from tkinter.ttk import Style
from collections import defaultdict



"""
CLASS - Tagger_View
This class handles everything display related in the model view controller scheme. There should be no logic here, just image
adding and removal and the likes.

    ATTRIBUTES:
        - root(Tkinter widget): This is the parent of all the widgets.
        - should_resize(boolean): Resizes the image if the users screen is particularly small.
        - data_list(list): List to hold references to the data text drawn on-screen.
        - has_changed(boolean): True if the next image has been scrolled to.
        - count(int): This keeps track of the index the image being viewed is at.
        - height(int): The height of the canvas in pixels that is displayed on-screen.
        - width(int): The with of the canvas in pixels that is displayed on-screen.
        - canvas(Tkinter widget): This is a Tkinter object that spans the area of the screen. It is used to display everything in the GUI.
        - image_list(list): A list of pathnames which represent the images from the stalk_images directory.
        - display_image(image): Holds an instance of the image that is displayed on screen.
        - display_image_reference(image): Holds a reference to the display image, useful for opening a new image or resizing.
        - braceroot_entry_box(Tkinter widget): A box for entering text. The user should enter the number of braceroots in a plant.
        - braceroot_text_box(Tkinter widget): Displays some text above the entry box letting you know this is where to enter braceroot count.
        - plant_count(int): For displaying the current plant you're working with.
        - circle_list(list): 2d List to hold ids of the circles drawn on each screen.
        - has_started(boolean): True if the user has made it past the start screen, false otherwise.

    METHODS:
        - __init__: This is the constructor, sets up buttons to be clicked.
        - resize_main: Updates the height and width when the canvas is resized. This is a callback bound to the canvas resize event.
        - resize_manager: Handles resizing various other objects on screen. Like keeping the display image centered.
        - initialize_screen: Makes the buttons,puts the first image on the screen.
        - scroll_images: Handles the logic for clickinig through the images with the next and previous buttons.
        - open_compatible_image: Opens an image in a way that makes it suitable to be displayed in a Tkinter canvas.
        - make_buttons: Makes the next and previous buttons. They are automatically resizable due to the nature of the button creation.
        - on_click_left: Recieves an event for a left click and calls methods for handling tagging.
"""


# CONSTANTS
TRIC_LIMEGREEN = "#00ff00"
TRIC_RED = "#ff0000"


class Tagger_View(Frame):
    """
    __init__: constructor

    Consumes: Nothing
    Produces: Nothing
    """
    def __init__(self, root, height, width, image_paths, should_resize):
        Frame.__init__(self, root)
        self.root = root
        self.should_resize = should_resize
        self.data_list = []
        self.has_changed = True
        self.count = 0
        self.prev_count = 0
        self.height = height
        self.width = width
        self.canvas = Canvas(root, width = width, height = height, background = "grey25")
        self.image_list = image_paths
        self.display_image = None
        self.display_image_reference = None
        self.braceroot1_entry_box = Entry(self.canvas)
        self.braceroot1_entry_box.insert(0,"whrl 1")
        self.braceroot2_entry_box = Entry(self.canvas)
        self.braceroot2_entry_box.insert(0,"whrl 2")
        self.braceroot3_entry_box = Entry(self.canvas)
        self.braceroot3_entry_box.insert(0,"whrl 3")
        self.braceroot4_entry_box = Entry(self.canvas)
        self.braceroot4_entry_box.insert(0,"whrl 4")
        self.plant_id_entry_box = Entry(self.canvas)
        self.plant_id_entry_box.insert(0,"PlantID")
        self.plant_count = 0
        self.oval_dict = defaultdict(list)
        self.circle_dict = defaultdict(list)
        self.mode_text = None
        self.mode_textbox = None
        self.has_started = False
        self.rotation_factor = 0
        self.bind_events()
        self.make_intro_screen()


    """
    bind_events, binds certain events to callbacks that will do things if that event happens. Such as screen  resizing, or left clicks.

    Consumes: Nothing
    Produces: Nothing
    """
    def bind_events(self):
        self.canvas.pack(fill = "both", expand = "yes") # Put canvas on-screen, make sure it fills whole screen and resizes
        self.canvas.bind("<Configure>", self.resize_main) # For setting canvas height/width


    """
    update_mode, redraws the mode onscreen when enter is pressed.

    Consumes: Nothing
    Produces: Nothing
    """
    def update_mode(self):
        self.canvas.delete(self.mode_textbox)
        size = "Times 24 bold"
        width = 300
        height = -100
        if "draw_triangles" in self.mode_text:
            size = "Times 12 bold"
            width = 300
        if self.should_resize:
            width += 200
            height += 200
        self.mode_textbox = self.canvas.create_text(width, height, fill = "lawn green", font = size, text = "Mode: " + self.mode_text)


    """
    resize_main, callback for updating the height and width attributes whenever the screen is resized. This method also calls the resize manager to
                 handles resizing of other objects.

    Consumes: event(screen resize)
    Produces: Nothing
    """
    def resize_main(self, event):
        self.resize_manager(self.height, self.width, event) # Handle moving before attributes are updated
        self.height = event.height
        self.width = event.width


    """
    resize_manager, handles resizing certain elements when the screen is resized.

    Consumes: Nothing
    Produces: Nothing
    """
    def resize_manager(self, height, width, event):
        height_diff = (height/2 - event.height/2)*-1
        width_diff = (width/2 - event.width/2)*-1
        if self.has_started:
            self.canvas.move(self.display_image, width_diff, height_diff)
            self.canvas.move(self.braceroot1_window, width_diff, height_diff)
            self.canvas.move(self.braceroot2_window, width_diff, height_diff)
            self.canvas.move(self.braceroot3_window, width_diff, height_diff)
            self.canvas.move(self.braceroot4_window, width_diff, height_diff)
            self.canvas.move(self.braceroot_text_box, width_diff, height_diff)
            self.canvas.move(self.ab_text, width_diff, height_diff)
            self.canvas.move(self.root_width_text, width_diff, height_diff)
            self.canvas.move(self.scale_text, width_diff, height_diff)
            self.canvas.move(self.stalk_width_text, width_diff, height_diff)
            self.canvas.move(self.triangle_text, width_diff, height_diff)
            self.canvas.move(self.mode_textbox, width_diff, height_diff)
        self.canvas.move(self.intro_text, width_diff, height_diff)
        self.canvas.move(self.start_button, width_diff, height_diff)

    """
    make_intro_scene, makes a scene with some instructional text and a button to stsrt the main portion of the app.

    Consumes: Nothing
    Produces: Nothing
    """
    def make_intro_screen(self):
        self.intro_text = self.canvas.create_text(self.width/2, (self.height/2), fill = TRIC_RED, font = "Times 20 bold", text = "\tPlease use fullscreen\n\n\nClick to draw circles\n, place them according to the mode you are in.\nhit the enter key to change modes.\nyou are done with a plant when the text\n'done, click next' appears.\nHit 'r' to reset the progress\nmade for the current plant..")
        start_button = start_button = Button(text = "Start", command = self.initialize_screen)
        self.start_button = self.canvas.create_window(self.width/2, self.height-150, window = start_button)



    """
    initialize_screen, this method just calls some of the other methods in this class to start the GUI up. It makes the buttons, places the first image.

    Consumes: Nothing
    Produces: Nothing
    """
    def initialize_screen(self):
        self.canvas.delete(self.start_button)
        self.canvas.delete(self.intro_text)
        self.update_mode()
        self.make_buttons()
        self.open_compatible_image()
        self.make_input_boxes()
        self.draw_text(True)
        self.draw_data_labels()
        self.has_started = True


    """
    scroll_images, used for scrolling through the images in the image_list attribute. Clicking next adds one the the count attribute, clicking previous
                   subtracts one. Go to far to the left or right and the display_end method is called to display the graph of the tags made or let the
                   user know they are at the end of the list.

    Consumes: direction (string), root(tkinter window)
    Produces: Nothing
    """
    def scroll_images(self, direction, root):
        self.prev_count = self.count
        if direction == "forward":
            self.count += 1
        elif direction == "backward":
            self.count -= 1

        if (self.count < len(self.image_list)) and not (self.count < 0):
            self.update(True)
            self.has_changed = True


    def update(self, should_draw_label):
        # Delete the previous image
        self.canvas.delete("all")
        # Clear the entry boxes
        self.braceroot1_entry_box.delete(0, END)
        self.braceroot2_entry_box.delete(0, END)
        self.braceroot3_entry_box.delete(0, END)
        self.braceroot4_entry_box.delete(0, END)
        # Creates a Tkinter compatible image
        self.open_compatible_image()
        self.draw_data_labels()
        self.make_input_boxes()
        self.draw_text(False)
        # Restore circles
        self.mode_text = "image_scale"
        self.update_mode()
        if should_draw_label == True:
            self.restore_circles()



    """
    draw_data_labels, draws the labels for the data above where it is displayed on the screen.

    Consumes: Nothing
    Produces: Nothing
    """
    def draw_data_labels(self):
        x = self.width/2 - 800
        y = self.height/2 + 200
        x1 = 1100
        x2 = 1150
        x3 = 1500
        y1 = 800
        y2 = 700
        if self.should_resize:
            x1 -= 200
            x2 -= 200
            x3 -= 200
            y1 -= 200
            y2 -= 200
        self.scale_text = self.canvas.create_text(x+x1, y-y1, fill = "lawn green", font = "Times 20 bold", text = "Scale")
        self.root_width_text = self.canvas.create_text(x+x3, y-y1, fill = "lawn green", font = "Times 20 bold", text = "Root Width")
        self.stalk_width_text = self.canvas.create_text(x+x2, y-y2, fill = "lawn green", font = "Times 20 bold", text = "Stalk Width")
        self.triangle_text = self.canvas.create_text(x+x3, y-y2, fill = "lawn green", font = "Times 20 bold", text = "Triangles")



    """
    draw_data, draws the data collected on-screen.

    Consumes: A string
    Produces: Nothing
    """
    def draw_data(self, data):
        x_mod1 = 300
        y_mod1 = 550
        if self.should_resize:
            x_mod1 -= 200
            y_mod1 -= 200
        x = self.width/2+x_mod1
        y = self.height/2-y_mod1
        i = 0
        if len(self.data_list) != 0:
            for item in self.data_list:
                self.canvas.delete(item)
        self.data_list *= 0 # Remove objects from list entirely
        for value in data:
            lengthAfter = str(value).split(".")
            if len(lengthAfter[1]) > 2:
                lengthAfter[1] = lengthAfter[1][:-1] # Get rid of last character, it is a "]" for some reason
                rounded = str(round(float("." + lengthAfter[1]), 2))
                rounded = rounded[1:] # Get rid of the extra zero on left hand side of decimal
                value = lengthAfter[0] + rounded
            if i >= 3:
                temp = self.canvas.create_text(x, y, fill = "lawn green", font = "Times 25 bold", text = "Complete")
                break
            else:
              temp = self.canvas.create_text(x, y, fill = "lawn green", font = "Times 25 bold", text = str(value)+"px")
            self.data_list.append(temp)
            if i % 2:
                x -= 400
                y += 100
            else:
                x += 400
            i += 1



    """
    destroy_circles, gets rid of the circles on the current screen.

    Consumes: Nothing
    Produces: Nothing
    """
    def destroy_circles(self):
        for i  in range(len(self.circle_dict[self.count])):
            self.canvas.delete(self.oval_dict[self.count][i])


    """
    restore_circles, redraws the circles you had drawn on previous screens if you go back to that scene

    Consumes: Nothing
    Produces: Nothing
    """
    def restore_circles(self):
        for key, value in self.circle_dict.items():
            if int(key) == self.count:
                for coords in value:
                    self.canvas.create_oval(coords[0]-10, coords[1]-10, coords[0]+10, coords[1]+10, fill = "red") # Redraw all of the circles


    """
    open_compatible_image, opens an image from the image list and makes it compatible with Tkinter. The image is put onto the canvas. Compatibile meaning
                           the image is just opened in accordance with the Tkinter module, so the image is solely for viewinig purposes, it cannot be
                           manipulated in the sense of changes being made to its location in disk space.

    Consumes: Nothing
    Produces: Nothing
    """
    def open_compatible_image(self):
        # Gets an image compatible with Tkinter
        image = Image.open(self.image_list[self.count]).convert("RGBA")
        img_w, img_h = image.size
        new_size = (int(img_w/2), int(img_h/2)) # Images are very large
        image = image.resize(new_size)
        if self.should_resize == True: # Handle displaying the image on a small screen
            w, h = image.size
            even_smaller = (int(w/1.3), int(h/1.3))
            image = image.resize(even_smaller)
       # image = image.rotate(-90) # For fixing python auto rotating the image when loaded.
        self.display_image_reference = ImageTk.PhotoImage(image)
        self.display_image = self.canvas.create_image(int(self.width/2), int(self.height/2), image = self.display_image_reference, anchor = CENTER)

    def rotate_image(self):
        print("rotate was called")
        self.rotation_factor += 1
        image = Image.open(self.image_list[self.count]).convert("RGBA")
        img_w, img_h = image.size
        new_size = (int(img_w/2), int(img_h/2)) # Images are very large
        image = image.resize(new_size)
        if self.should_resize == True: # Handle displaying the image on a small screen
            w, h = image.size
            even_smaller = (int(w/1.3), int(h/1.3))
            image = image.resize(even_smaller)


        image = image.rotate(self.rotation_factor * 90)


        self.display_image_reference = ImageTk.PhotoImage(image)
        self.display_image = self.canvas.create_image(int(self.width/2), int(self.height/2), image = self.display_image_reference, anchor = CENTER)

    def view_finder(self):
        print("vf was called")
        global vf_rotation_factor
        vf_rotation_factor = 0
        vf_window = Toplevel(self.root)
        vf_canvas = Canvas(vf_window, bg="blue")
        global image
        image = Image.open(self.image_list[self.count]).convert("RGBA")
        img_w, img_h = image.size
        new_size = (int(img_w/2), int(img_h/2)) # Images are very large
        image = image.resize(new_size)

        photo = ImageTk.PhotoImage(image)
        vf_canvas.create_image(0,0,image=photo, anchor="nw")
        vf_canvas.image = photo
        vf_canvas.pack(fill="both", expand=True)


        def rotate_image(event):
            global vf_rotation_factor
            vf_rotation_factor += 1
            image = Image.open(self.image_list[self.count]).convert("RGBA")
            image = image.rotate(vf_rotation_factor*90)
            new_size = (int(img_w/2), int(img_h/2)) # Images are very large
            image = image.resize(new_size)
            photo = ImageTk.PhotoImage(image)
            vf_canvas.create_image(0,0,image=photo, anchor="nw")
            vf_canvas.image = photo



        def on_mouse_down(event):
            global start_x, start_y
            start_x = vf_canvas.canvasx(event.x)
            start_y = vf_canvas.canvasy(event.y)
            vf_canvas.create_rectangle(start_x, start_y, start_x, start_y, outline="red", tags="bbox")

        def on_mouse_move(event):
            curX = vf_canvas.canvasx(event.x)
            curY = vf_canvas.canvasy(event.y)
            vf_canvas.coords("bbox", start_x, start_y, curX, curY)
            global crop_box_x0, crop_box_y0, crop_box_x1, crop_box_y1
            crop_box_x0 = start_x
            crop_box_y0 = start_y
            crop_box_x1 = curX
            crop_box_y1 = curY

        def on_mouse_up(event):
            pass

        def capture(event):

            print("capture called",crop_box_x0,crop_box_y0,crop_box_x1,crop_box_y1,vf_rotation_factor)
            image = Image.open(self.image_list[self.count]).convert("RGBA")


            new_size = (int(img_w/2), int(img_h/2)) # Images are very large
            image = image.resize(new_size)
            if(vf_rotation_factor):
                image = image.rotate(vf_rotation_factor * 90)
            cropped = image.crop((crop_box_x0,crop_box_y0,crop_box_x1,crop_box_y1))

            self.display_image_reference = ImageTk.PhotoImage(cropped)
            self.display_image = self.canvas.create_image(int(self.width/2), int(self.height/2), image = self.display_image_reference, anchor = CENTER)
            vf_window.destroy()

        vf_canvas.bind("<Button-1>", on_mouse_down)
        vf_canvas.bind("<B1-Motion>", on_mouse_move)
        vf_canvas.bind("<ButtonRelease-1>", on_mouse_up)
        vf_canvas.bind("<p>", capture)
        vf_canvas.bind("<l>", rotate_image)
        vf_canvas.focus_set()


    """
    make_input_boxes, makes the input boxes for inputting the number of braceroots.

    Consumes: Nothing
    Produces: Nothing
    """
    def make_input_boxes(self):
        x_mod1 = 700
        y_mod1 = 200
        y_mod2 = 100
        if self.should_resize:
            x_mod1 -= 200
            y_mod1 -= 20
            y_mod2 -= 20
        self.braceroot4_window = self.canvas.create_window(self.width/2-x_mod1, self.height/2-y_mod1, window = self.braceroot4_entry_box)  # top box
        self.braceroot3_window = self.canvas.create_window(self.width/2-x_mod1, self.height/2-y_mod2, window = self.braceroot3_entry_box)
        self.braceroot2_window = self.canvas.create_window(self.width/2-x_mod1, self.height/2, window = self.braceroot2_entry_box)
        self.braceroot1_window = self.canvas.create_window(self.width/2-x_mod1, self.height/2+y_mod2, window = self.braceroot1_entry_box)
        self.plant_id_window = self.canvas.create_window(self.width/2-x_mod1, self.height/2-y_mod1-100, window = self.plant_id_entry_box)

    """
    draw_text

    Consumes: Nothing
    Produces: Nothing
    """
    def draw_text(self, should_increment):
        x_mod1 = 600
        y_mod1 = 250
        x_mod2 = 700
        y_mod2 = 300
        if self.should_resize:
            x_mod1 -= 200
            x_mod2 -= 200
            y_mod1 -= 50
            y_mod2 -= 50
        self.braceroot_text_box = self.canvas.create_text(self.width/2-x_mod1, self.height/2+y_mod1, fill = "lawn green", font = "Times 25 bold", text = "Enter # of brace-roots\nlowest level goes in\nlowest input box.")
        #a_or_b = "ERROR"
       # plant_count = "ERROR"
       # if self.count % 2 == 0:
        #    if should_increment:
       #        self.plant_count += 1
       # if self.count % 2 == 0:
       #     a_or_b = "A"
       # else:
       #     a_or_b = "B"
      #  print(self.count)
       # print(self.image_list)
        image_name = self.image_list[self.count]
        plant_name = image_name
        #plant_name = image_name.split("/")[1].split("_")[0] + str("_") + image_name.split("/")[1].split("_")[2].split(".")[0]
        #self.ab_text = self.canvas.create_text(self.width/2-x_mod2, self.height/2-y_mod2, fill = "lawn green", font = "Times 30 bold", text = "Plant: %s, Side: %s" % (plant_name, a_or_b))



    """
    make_buttons, makes the next and previous buttons in th GUI, a lambda function is deployed to do in-line handling of the command the buttons
                  should execute.

    Consumes: Nothing
    Produces: Nothing
    """
    def make_buttons(self):
        # Making a button to go to the next image
        right_frame = Frame(self.canvas)
        right_frame.pack(side = RIGHT)
        next_button = Button(right_frame, text = "Next", bg = TRIC_RED, fg = "black",
        command = lambda *args: self.scroll_images("forward", self.canvas), height = self.height, width = 6)
        next_button.pack(side = RIGHT)

        # Making a button to go to the previous image
        left_frame = Frame(self.canvas)
        left_frame.pack(side = LEFT)
        previous_button = Button(left_frame, text = "Previous", bg = TRIC_RED, fg = "black",
        command = lambda *args: self.scroll_images("backward", self.canvas), height = self.height, width = 6)
        previous_button.pack(side = LEFT)


    """
    draw_circle, draws a circle on the screen of a certain radius

    Consumes: An event(mouse action)
    Produces: Nothing
    """
    def draw_circle(self, action):
        radius = 4
        x0 = action.x - radius
        y0 = action.y - radius
        x1 = action.x + radius
        y1 = action.y + radius
        color = "red"
        if "draw_triangles" in self.mode_text:
            color = "purple"
        oval = self.canvas.create_oval(x0, y0, x1, y1, fill = color)
        self.oval_dict[self.count].append(oval)
        self.circle_dict[self.count].append([action.x, action.y])
