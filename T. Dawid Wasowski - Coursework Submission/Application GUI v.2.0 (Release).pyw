#This application was produced by T. Dawid Wasowski in early 2019
#This application is the coursework for Foundation Level
#Computer Science - Computer Systems and Software Development 

import DatabaseFunctions
from tkinter import ttk
from tkinter import *
from PIL import Image, ImageTk

#----- GUI FUNCTIONS -----

#Creates a tkinter root window
def createWindow(title, size, colour):
    
    root = Tk()

    root.title(title)
    root.geometry(size)
    root.configure(background=colour)
    
    #Disabling resizing to preserve format
    root.resizable(width=False, height=False)

    return root

#Creates a frame to place in the tkinter window
def createFrame(root, text, colour, row, column, rowspan, columnspan, sticky):

    frame = LabelFrame(root, text=text, bg=colour)
    frame.grid(row=row, column=column, rowspan=rowspan, columnspan=columnspan,
               sticky=sticky, padx=5, pady=5)

    return frame

#Creates a frame with propagate = False, allowing manual frame sizing
def createFrameProp(root, text, colour, row, column, rowspan,
                    columnspan, sticky, width, height):

    frame = LabelFrame(root, text=text, bg=colour, width=width, height=height)
    frame.grid(row=row, column=column, rowspan=rowspan, columnspan=columnspan,
               sticky=sticky, padx=5, pady=5)
    frame.grid_propagate(0)

    return frame

#Creates a label, taking colour parameter to blend in with frame background
def createLabel(frame, text, colour, row, column):

    label = Label(frame, text=text, bg=colour)
    label.grid(row=row, column=column)

    return label

#Creates an entry widget that allows user input
def createField(frame, textvar, row, column):

    field = Entry(frame, textvariable=textvar)
    field.grid(row=row, column=column, padx=5, pady=5)

    #Binds doubleclick to clear, uses lambda to pass itself as a parameter
    field.bind("<Double-Button-1>", lambda event: clearField(event, field))

    return field

#Creates buttons; background colour automatically set to white
def createButton(frame, text, width, command, row, column):

    button = Button(frame, text=text, width=width, command=command, bg="White")
    button.grid(row=row, column=column, padx=5, pady=5)

    return button

#Creates a label for images, taking in the ImageTk parameter
def createImageLabel(frame, row, column, itk):

    img = Label(frame, bg="White", image=itk)
    img.grid(row=row,column=column, padx=5, pady=5)

    return img

#Updates the image by configuring label with a new ImageTk photo
def updateImage(label, name):

    img = Image.open(name).resize((73, 73), Image.ANTIALIAS)
    itk = ImageTk.PhotoImage(img)
    label.configure(image=itk)
    
    #This line is to prevent garbage collection
    label.image = itk

#Creates the treeview widget along with select bindings
def createTreeView(frame, height, columns, row, column, columnspan):

    treeview = ttk.Treeview(frame, height=height, columns=columns)
    treeview.grid(row=row, column=column, columnspan=columnspan, padx=5, pady=5)
    treeview.bind("<ButtonRelease-1>", selectRecord)
    treeview.bind("<Return>", selectRecord)            

    return treeview

#Creates each of the tree widget's columns
def createTreeColumn(treeview, name, text, width):

    treeview.column(name, anchor="center", width=width)
    treeview.heading(name, text=text)

#Creates the tree widget's scrollbar
def createScrollbar(frame, treeview, row, column):

    scrollbar = Scrollbar(frame, command=treeview.yview, orient=VERTICAL)
    scrollbar.grid(row=row, column=column, rowspan=2, sticky=NS, padx=(0,5), pady=5)
    treeview.configure(yscrollcommand=scrollbar.set)

#Udates an object to adjust their colour scheme
def updateMonochrome(obj, colour):

    obj.configure(bg = colour)

#Updates a message by configuring the label and changing the foreground colour
def updateMsg(text, colour):

    global monoCheck
    if monoCheck == False:      
        msg_lbl.configure(text=text, fg=colour)
    else:
        #If monochrome is on the foreground is defaulted to white
        msg_lbl.configure(text=text, fg="White")

#----- BUTTON FUNCTIONS -----


def view():
    
    try:
        #Clears the tree widget before inserting database records
        clearDisplay()

        #Inserting records
        records = DatabaseFunctions.view()
        for row in records:
            disp_tv.insert("", 0, values=row)

        updateMsg("You are currently viewing all student records.",
                  "Blue")    
    except:
        updateMsg("Error: Something went wrong while viewing all student records.",
                  "Red")

def add():

    try:
        #Parameters pulled from student panel entry widgets
        name = stdntFirstName_fld.get()
        surname = stdntLastName_fld.get()
        mark = stdntMark_fld.get()
        img = stdntImgLoc_fld.get()

        #...added to the database
        DatabaseFunctions.add(name, surname, mark, img)

        #Entries are cleared and the display is refreshed with view
        clearEntry()
        view()
        
        updateMsg("You have added a new student record to the database.",
                  "Green")    
    except:
        updateMsg("Error: Something went wrong while adding the student record.",
                  "Red")

def update():

    try:
        #Parameters pulled from student panel entry widgets
        id = stdntID_fld.get()
        name = stdntFirstName_fld.get()
        surname = stdntLastName_fld.get()
        mark = stdntMark_fld.get()
        img = stdntImgLoc_fld.get()
        stat = stdntStatus_fld.get()

        #If the id widget is empty, signal an error
        if id == "":
            updateMsg("Error: Something went wrong while updating the student record.",
                      "Red")
        else:
            #Calls on update function
            DatabaseFunctions.update(id, name, surname, mark, img, stat)

            #Refresh entries and display
            clearEntry()
            view()
        
            updateMsg("You have updated the selected student record.",
                      "Green")
    except:
        updateMsg("Error: Something went wrong while updating the student record.",
                  "Red")

def delete():
    
    try:
        #Pulls id from entry widget
        id = stdntID_fld.get()

        #If empty, throws exception
        if id == "":
            updateMsg("Error: Something went wrong while deleting the student record.",
                      "Red")
        else:
            #Calls on delete function
            DatabaseFunctions.delete(id)
            clearEntry()
            view()
            
            updateMsg("You have deleted the student record from the database.",
                      "Green")
    except:
        updateMsg("Error: Something went wrong while deleting the student record.",
                  "Red")

def search():

    try:
        #Pulls parameters from entries
        id = stdntID_fld.get()
        name = stdntFirstName_fld.get()
        surname = stdntLastName_fld.get()
        mark = stdntMark_fld.get()
        stat = stdntStatus_fld.get()

        #Clears the tree widget
        clearDisplay() 

        #Calls on search function and displays in tree widget
        records = DatabaseFunctions.search(id, name, surname, mark, stat) #fimprove
        for row in records:
            disp_tv.insert("", 0, values=row)
        
        
        updateMsg("You are currently viewing the search results from the database.",
                  "Blue")
    except:
        updateMsg("Error: Something went wrong while searching the database.",
                  "Red")

def clearEntry():

    try:
        #Clears all entry widgets
        stdntID_fld.delete(0, END)
        stdntFirstName_fld.delete(0, END)
        stdntLastName_fld.delete(0, END)
        stdntMark_fld.delete(0, END)
        stdntImgLoc_fld.delete(0, END)
        stdntStatus_fld.delete(0, END)

        #Sets the image back to default
        updateImage(stdntImg_lbl, "Images/default.png")
        
        updateMsg("You have cleared the student panel entry fields.",
                  "Blue")
    except:
        updateMsg("Error: Something went wrong while clearing the entry fields.",
                  "Red")               

def clearDisplay():

    try:
        #Clears the treeview widget
        records = disp_tv.get_children()
        for row in records:
            disp_tv.delete(row)
            
        updateMsg("You have cleared the display panel.",
                  "Blue") 
    except:
        updateMsg("Error: Something went wrong while clearing the display panel.",
                  "Red")

def monochromeMode():

    #Importing global variable that checks whether monochrome mode is enabled
    global monoCheck

    if monoCheck == False:
        #Polychrome settings
        spc, apc, dpc, mpc = "LightGrey", "Gray", "Gray65", "Gray35"
        msg = "You have switched the colour scheme to monochrome."
        monochrome_btn.configure(text = "Polychrome")

        #Sets monochrome check on
        monoCheck = True
        
    else:
        #Poluchrome settings
        spc, apc, dpc, mpc = stdntColour, actColour, dispColour, msgColour
        msg = "You have switched the colour scheme to polychrome."
        monochrome_btn.configure(text = "Monochrome")

        #Set monochrome check off
        monoCheck = False
    
    #Colour change for the student panel
    updateMonochrome(stdntFrame, spc)
    updateMonochrome(stdntImgFrame, spc)
    
    updateMonochrome(stdntID_lbl, spc)
    updateMonochrome(stdntFirstName_lbl, spc)
    updateMonochrome(stdntLastName_lbl, spc)
    updateMonochrome(stdntMark_lbl, spc)
    updateMonochrome(stdntImgLoc_lbl, spc)
    updateMonochrome(stdntStatus_lbl, spc)

    #Colour change for the action panel
    updateMonochrome(actFrame, apc)

    #Colour change for the display panel
    updateMonochrome(dispFrame, dpc)

    #Colour change for the message panel
    updateMonochrome(msgFrame, mpc)
    updateMonochrome(msg_lbl, mpc)

    updateMsg(msg, "Blue")

def quit():

    #Destroys the root window, ending the mainloop and closing the application
    root.destroy()

#----- EVENT FUNCTIONS -----

def clearField(event, field):

    #Upon clearing a field, sets the image back to default
    updateImage(stdntImg_lbl, "Images/default.png")

    #Clears the entry widget
    field.delete(0, END)

def selectRecord(event):

    try:
        #Assigns selection
        record = disp_tv.item(disp_tv.selection())

        #Clears the entry widget
        clearEntry()

        #Inserts data from treeview into the student panel entries
        stdntID_fld.insert(END, record["values"][0])
        stdntFirstName_fld.insert(END, record["values"][1])
        stdntLastName_fld.insert(END, record["values"][2])
        stdntMark_fld.insert(END, record["values"][3])
        stdntImgLoc_fld.insert(END, record["values"][4])
        stdntStatus_fld.insert(END, record["values"][5])

        #Attempts to display the image, sets default if it cannot find one
        try:
            updateImage(stdntImg_lbl, "Images/"+record["values"][4])
        except:
            updateImage(stdntImg_lbl, "Images/default.png")


        updateMsg("You have selected a record from the database.", "Blue")

    except:
        updateMsg("Error: Something went wrong while selecting your record.", "Red")
                    

#----- WINDOW -----

#Creating tkinter root window
root = createWindow("Student Record Managemer", "609x492", "White")

#----- PANELS -----

    #Student:

#Setting the panel and label colours
stdntColour = "LightBlue1"

#Creating the frame of the student panel
stdntFrame = createFrame(root, "Student Panel", stdntColour, 0, 0, 1, 1, NW)

#Creating student ID label and field
stdntID_lbl = createLabel(stdntFrame, "Student ID:", stdntColour, 0, 0)
stdntID_txt = StringVar()
stdntID_fld = createField(stdntFrame, stdntID_txt, 0, 1)

#Creating student first name label and field
stdntFirstName_lbl = createLabel(stdntFrame, "First Name:", stdntColour, 1, 0)
stdntFirstName_txt = StringVar()
stdntFirstName_fld = createField(stdntFrame, stdntFirstName_txt, 1, 1)

#Creating student last name label and field
stdntLastName_lbl = createLabel(stdntFrame, "Last Name:", stdntColour, 2, 0)
stdntLastName_txt = StringVar()
stdntLastName_fld = createField(stdntFrame, stdntLastName_txt, 2, 1)

#Creating student attendance mark label and field
stdntMark_lbl = createLabel(stdntFrame, "Mark:", stdntColour, 0, 2)
stdntMark_txt = StringVar()
stdntMark_fld = createField(stdntFrame, stdntMark_txt, 0, 3)

#Creating student image location label and field
stdntImgLoc_lbl = createLabel(stdntFrame, "Image:", stdntColour, 1, 2)
stdntImgLoc_txt = StringVar()
stdntImgLoc_fld = createField(stdntFrame, stdntImgLoc_txt, 1, 3)


#Creating student status label and field
stdntStatus_lbl = createLabel(stdntFrame, "Status:", stdntColour, 2, 2)
stdntStatus_txt = StringVar()
stdntStatus_fld = createField(stdntFrame, stdntStatus_txt, 2, 3)

#Creating a frame to house the student image
stdntImgFrame = createFrame(root, "Student Image", stdntColour, 0, 1, 1, 1, NW)

#Creating a student ImageTk photo and setting it to default at startup
stdntImg_itk = ImageTk.PhotoImage(Image.open("Images/default.png").\
                                  resize((73, 73), Image.ANTIALIAS))

#Creating an image lable to house the student image in the frame                                         
stdntImg_lbl = createImageLabel(stdntImgFrame, 0, 0, stdntImg_itk)
    
    #Action:

#Sets action colour and creates the frame of the action panel
actColour = "Pink"
actFrame = createFrameProp(root, "Action Panel", actColour,
                           0, 2, 2, 1, NW, 108, 432)

#Creates a view button
view_btn = createButton(actFrame, "View All", 12, view, 0, 0)

#Creates a search button
search_btn = createButton(actFrame, "Search", 12, search, 1, 0)

#Creates an add button
add_btn = createButton(actFrame, "Add Record", 12, add, 2, 0)

#Creates an update button
update_btn = createButton(actFrame, "Update Record", 12, update, 3, 0)

#Creates a delete button
delete_btn = createButton(actFrame, "Delete Record", 12, delete, 4, 0)

#Creates a button to clear the entry fields
clearEnt_btn = createButton(actFrame, "Clear Entry", 12, clearEntry, 5, 0)

#Creates a button to clear the treeview display
clearDisp_btn = createButton(actFrame, "Clear Display", 12, clearDisplay, 6, 0)

#Creates a monochrome mode button to change the application into grayscale
monochrome_btn = createButton(actFrame, "Monochrome", 12, monochromeMode, 7, 0)
monoCheck = False

#Creates a quit button
quit_btn = createButton(actFrame, "Quit", 12, quit, 8, 0)

    #Display:

#Sets display colour and creates the display frame
dispColour = "OliveDrab1"
dispFrame = createFrame(root, "Display Panel", dispColour, 1, 0, 1, 2, N)

#Creates the treeview widget
disp_tv = createTreeView(dispFrame, 13, 5, 1, 0, 2)

#Assigns the column IDs and hides 'root' column
disp_tv["columns"] = ("stdntID", "stdntFirstName", "stdntLastName",
                       "stdntMark", "stdntImgLoc", "stdntStatus")
disp_tv["show"] = "headings"

#Creates each column in the treeview widget
createTreeColumn(disp_tv, "stdntID", "Student ID", 77)
createTreeColumn(disp_tv, "stdntFirstName", "First Name", 77)
createTreeColumn(disp_tv, "stdntLastName", "Last Name", 77)
createTreeColumn(disp_tv, "stdntMark", "Mark", 55)
createTreeColumn(disp_tv, "stdntImgLoc", "Image Location", 101)
createTreeColumn(disp_tv, "stdntStatus", "Status", 55)

#Creates the treeview scrollbar
createScrollbar(dispFrame, disp_tv, 0, 7)

    #Message:

#Sets message panel colour and creates the message frame
msgColour = "LightGoldenrod1"
msgFrame = createFrameProp(root, "Message Panel", msgColour,
    2, 0, 1, 3, NW, 599, 40)

#Creates the initial message label
msg_lbl = createLabel(msgFrame, "", msgColour, 0, 0)

#Updates the message to startup default
updateMsg("This window will display any important information.", "Blue")

#----- MAINLOOP -----

#Mainloop that keeps the GUI running
root.mainloop()

