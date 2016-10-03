#!/usr/bin/python
# Youtube videos (investary)
#Basic Python Tutorial 34 - Creating a Graphical User Interface (GUI) 
#Basic Python Tutorial 35 - Creating Buttons and Labels for GUI 
#Basic Python Tutorial 36 - How to Use Object Oriented Programming (OOP) to create GUI
#Basic Python Tutorial 37 - Binding and Creating the Event Handler 
#Basic Python Tutorial 38 - Using Text and Entry Widgets 
#
#reference example game program for organization of updates with GUI interface:
# http://forum.codecall.net/topic/76208-tkinter-ball-snake-game/


from tkinter import *
# for 3.0 or higher use tkinter

""" 
tkiniter.ttk causes widgets to have a more coherent look across platforms, however does change some widget options
such as fg and bg, use ttk.Style class. information on this found here:
https://docs.python.org/3/library/tkinter.ttk.html
"""
from tkinter.ttk import *

#import methods in other files
from alertUser import *

# import python system libraries
import sys, getopt
import os
import time
import datetime
from Utilities import *

class Application():
    """ This will define the primary Take A Break window """

    def __init__(self, testmode):
        """ 
        The above line I found in all my tutorials, so I added it, although it may not be necessary
        I think it explicitly instantiates the Frame class
        """
        self.root = Tk()
        self.testmode = testmode
        self.w = 400
        self.h = 250
        
        self.pos_win() 

        self.initUI()

        print('Test mode status: ', testmode)

    def initUI(self):
        		
        """ This is the title block """
        self.root.title("Take-A-Break")

        """ This is setting a default window Icon """
        self.root.iconbitmap(r'images\TAB_16x16_ico.ico')

        """ Apply a theme for the widgets """
        self.root.style = Style()
        self.root.style.theme_use("default")

        """
        initialize the input file monitor, as input file changes new coordinates are available
        this is the simulation of the computer vision API sending coordinates of the monitored points
        """
        self.filename = "inputApi.json"

        # Initialize coordinates
        # determine if the input file exists
        self.lastmod, self.mtime = GetInputApiModTime(self.filename)
        if self.mtime == 0:
            self.filetext = "no input available"
            self.parsed_json = {}
        else:
            #if file exists, get coordinates
            self.filetext, self.parsed_json = read_JSONfile(self.filename)
        #self.lastmod, self.mtime, self.filetext, self.parsed_json = GetInputApiCoordinates()
        print ("last modified: ", str(time.ctime(self.mtime)))

        # if test mode, starts with this value
        self.monitoring = False

        if not self.testmode:
            # this method creates the widgets on the GUI
            self.create_widgets()
            #this variable keeps track of whether we are currently monitoring
            # first call to StartMonitor essentially starts the clock
            self.monitoring = True
            self.StartMonitor()
            self.root.mainloop()
    
    """
    This function sets the window postiont in the lower right hand corner of the screen
    and sets the size. This will scale to any screen sized, but windw size is fixed
    """    
    def pos_win(self):

        # w is width in h is height
        self.w = 400
        self.h = 250

        #variables that takes in the width and height of screen
        sw = self.root.winfo_screenwidth()
        sh = self.root.winfo_screenheight()

        x = (sw - self.w - 20) 
        y = (sh - self.h - 40) 

        #This line places the window using the varables above
        self.root.geometry('%dx%d+%d+%d' % (self.w, self.h, x, y))

    def create_widgets(self):
        """ Create GUI elements """

        """ START MAIN FRAME 1 """

        """ Menu """
        """ http://www.python-course.eu/tkinter_menus.php """

        menu = Menu(self.root)
        self.root.config(menu = menu)
        filemenu = Menu(menu)
        menu.add_cascade(label = "File", menu = filemenu)
       
        #this should sllow the user to create a profile at some point
        filemenu.add_command(label = "New Profle")
        
        #This should also have a command = to allow load of user profile
        filemenu.add_command(label = "Open")
        filemenu.add_separator()
        
        #Add command to gracefulley exit application
        filemenu.add_command(label = "Exit")

        helpmenu = Menu(menu)
        menu.add_cascade(label = "Help", menu = helpmenu)
        
        #Load a about dialog window here
        helpmenu.add_command(label = "About...", command = self.MenuAbout)


        """ START FRAME 1 """
        
        """ This frame holds the user input fields and labels """
        frame1 = Frame(self.root, relief = RAISED, borderwidth = 2)
        frame1.pack(fill = X)

        """ This is the row for inputting the timeout period and controls for field """
        lbl1 = Label(frame1, text = "Set timeout in seconds: ", width = 24)
        lbl1.pack(side = LEFT, padx = 5, pady = 5)

        timeoutPeriod = IntVar()

        self.timeoutPeriod = Entry(frame1, textvariable = timeoutPeriod)
        timeoutPeriod = 1200
        self.timeoutPeriod.delete(0, END)
        self.timeoutPeriod.insert(0, str(timeoutPeriod))
        self.timeoutPeriod.pack(side = LEFT, fill = X, expand = True, padx = 5, pady = 5)
        print(self.timeoutPeriod.get())
        
        """ END FRAME 1 """

        """ START FRAME 2 """
        
        """ Create Frame t encapsulate the rest period input """
        frame2 = Frame(self.root, relief = RAISED, borderwidth = 2)
        frame2.pack(fill = X)

        """ Enter the timeouts for length of break 
            if user input stops for this period of time, assume a break was taken
            reset the timer for notifying of break
        """
        lbl2 = Label(frame2, text = "Set break period in seconds: ", width = 24)
        lbl2.pack(side = LEFT, padx = 5, pady = 5)

        restPeriod = IntVar()
        self.restPeriod = Entry(frame2, textvariable = restPeriod)
        restPeriod = 300
        self.restPeriod.delete(0, END)
        self.restPeriod.insert(0, str(restPeriod))
        self.restPeriod.pack(fill = X, expand = True, padx = 5, pady = 5)
        print(self.restPeriod.get())

        """ END FRAME 2 """

        """ START FRAME 3 """
        """ This Frame will display the curent time """
        frame3 = Frame(self.root, relief = RAISED, borderwidth = 2)
        frame3.pack(fill = X)

        #create label with current time
        timeLabelText = ""
        lbl3 = Label(frame3, text = "Current Time:  ", width = 24)
        lbl3.pack(side = LEFT, padx = 5, pady = 5)

        self.timeLabel = Label(frame3)
        self.timeLabel.pack(fill = BOTH, padx = 5, pady =5)

        self.submit_button = Button(self.root, text = "Start Monitor", command = self.StartMonitor)
        self.submit_button.pack(side = RIGHT, padx = 5, pady = 5)

        """ END FRAME 3 """

        """ START FRAME 4 """
        """ This frame will display posture coordinates and last modified time """
        """ [TODO] Notify user if posture data is stale in a more user friendly way """
        frame4 = Frame(self.root, relief = RAISED, borderwidth = 2)
        frame4.pack(fill = X)

        #create label to hold the posture coordinates
        lbl4 = Label(frame4, width = 100)
        lbl4.pack(side = LEFT, padx = 5, pady = 5)

        self.clock = Label(lbl4)
        self.clock.pack(fill = BOTH, padx = 5, pady = 5)
        self.posture = Label(frame4)
        self.posture.pack(fill = BOTH, padx = 5, pady =5)

        """ END FRAME 4 """


        """ Here we create a second frame that is raised to show clear definition to hold buttons"""
        #frame = Frame(self.root, relief = RAISED, borderwidth = 2)
        #frame.pack(fill = BOTH, expand = True)

        
        """ 
        This is the Quit button Positioned to the bottom right corner with fixed padding
        This button needs functionality added
        """
        #frame.submit_button = Button(self.root, text = "Start Monitor", command = self.StartMonitor)
        #frame.submit_button.pack(side = RIGHT, padx = 5, pady = 5)

       
        """
        This is the ok button Positioned to the bottom right corner with fixed padding 
        This button needs functionality added for setting alert configuration
        """
        #frame.okButton = Button(self.root, text = "Configure Alerts")
        #frame.okButton.pack(side = RIGHT)


        #timeoutPeriodLabelText = "Set timeout period(seconds): "
        #self.timeoutPeriodLabelText = Label()
        
        """ END MAIN FRAME 1 """

    def StartMonitor(self):
        """ On button click start monitor function """
        # when the button is pressed, toggle it's state
        self.monitoring = not(self.monitoring)
        if self.monitoring == False:
            #print ("start monitor")
            self.submit_button["text"] = "Start Monitor"
            self.clock['text'] = ""
            self.posture['text'] = ""
            self.UpdateClock()
        else:
            print ("stop monitor")            
            self.submit_button["text"] = "Stop Monitor"
            self.time=0
            self.DisplayCoordinates()

    def DisplayCoordinates(self):
        """ monitor inputs from inputApi.json file for posture coordinates
            montior notification alert """
        """ Update clock """
        #create label with current time
        timeLabelText = GetCurrentTime()
        #print(timeLabelText)
        self.timeLabel['text'] = timeLabelText
        self.timeLabel.pack()

        """ Display coordinates if file updated """
        if self.monitoring == True:
            # update the timer
            self.time+=1
            self.clock['text']="TIME:" + str(self.time//100)
 
            #  check for alert
            alertResult = AlertUser(self)
            if alertResult == 1:
                # [TODO] make a pop up for TakeABreak
                # for now print a notification
                print('Take a Break notification')

            elif alertResult == 2:
                # [TODO] make a pop up for BackToWork
                # for now, reset the timer so we don't keep getting alert print
                print('Back to Work notification')

            #lastmodTime, self.mtime, self.filetext, self.parsed_json = GetInputApiCoordinates()
            # Determine if the inputApi file has been updated
            lastmodTime, self.mtime = GetInputApiModTime(self.filename)
            if not(self.lastmod == lastmodTime):
                # if there are new posture coordinates, update the display
                lastmodText = "last modified: %s" % time.ctime(self.mtime)
                self.lastmod = lastmodTime
                self.filetext, parsed_json = read_JSONfile(self.filename)
                self.posture['text']=lastmodText + '\n' + self.filetext
                print(self.posture['text'])
            self.root.after(10, self.DisplayCoordinates) 

    def UpdateClock(self):
        """ Update Clock """
        if self.monitoring == False:
            #create label with current time
            timeLabelText = GetCurrentTime()
            #print(timeLabelText)
            self.timeLabel['text'] = timeLabelText
            self.timeLabel.pack()
            self.root.after(10, self.UpdateClock)
    

    """ https://pythonprogramming.net/tkinter-popup-message-window/ """
    def MenuAbout(self):
        popup = Tk()
        popup.wm_title("About...")
        
        #popup.PosAbout()
        # w is width in h is height
        self.w = 400
        self.h = 250

        #variables that takes in the width and height of screen
        sw = popup.winfo_screenwidth()
        sh = popup.winfo_screenheight()

        x = (sw - self.w - 20) / 2
        y = (sh - self.h - 40)  / 2

        #This line places the window using the varables above
        popup.geometry('%dx%d+%d+%d' % (self.w, self.h, x, y))


        lbl1 = Label(popup, text = "Take-A-Break\n CS361 Su 2016\n Vision: Stephanie Creamer\n Developed by Team: 13\nCorinna Huffaker\nHeath Breinholt\nNick Hartley\nShae Judge\nAlex Wood\n ")
        lbl1.pack(side = TOP, fill = X, pady = 10)

        b1 = Button(popup, text="Ok", command = popup.destroy)
        b1.pack(fill = BOTH)
        popup.mainloop()



