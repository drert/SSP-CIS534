
from GlobalVars import *
from tkinter import *
import IOTools as ios
import pandas as pd
import os
from tkinter import scrolledtext
# multiframe app design framework from GforG
stinfo = None
seminfo = []
duedates = []

ROW_TB_OFFSET = 1
COL_TB_OFFSET = 1

class ssapp(Tk) :
    def __init__(self, *args, **kwargs) :
        Tk.__init__(self, *args, **kwargs)

        container = Frame(self)
        container.pack(side="top", fill="both", expand=True)

        container.grid_rowconfigure(0,weight=1)
        container.grid_columnconfigure(0,weight=1)
        global stinfo, seminfo, duedates

        stinfo = ios.load_student_info()
        sminfo = ios.load_semester_info()
        ddates = ios.load_due_dates()

        self.frames = {}

        for F in (start, schedule, tasks, profile, exit_frame, notes) :
            frame = F(container,self)

            self.frames[F] = frame

            frame.grid(row=0,column=0,sticky="NWSE")

        if stinfo is None :
            self.show_frame(profile)
        else :  
            self.show_frame(start)

    def show_frame(self, cont) :
        frame = self.frames[cont]
        frame.tkraise()

class start(Frame) :
    def __init__(self, parent, controller) : 
        Frame.__init__(self, parent)
        self.update_frame(controller)

    def update_frame(self, controller) :
        global stinfo
        
        # clear frame
        for w in self.winfo_children() :
            w.destroy()
        
        if stinfo is not None :
            intro_text = Label(self, text=stinfo[0]+"'s Planner", font=MENU_FONT)
            intro_text.grid(row=0, column=0, padx=15, pady=15)

        # generate buttons needed
        sch_butt = Button(self, text="Schedule", font=LG_BUTTON_FONT,
                          command = lambda : controller.show_frame(schedule))
        ddt_butt = Button(self, text="Assignments", font=LG_BUTTON_FONT,
                          command = lambda : controller.show_frame(tasks))
        ext_butt = Button(self, text="Quit", font=LG_BUTTON_FONT,
                          command = controller.destroy)
        prf_butt = Button(self, text="Profile", font=INFO_FONT,
                          command = lambda : controller.show_frame(profile))
        nts_butt = Button(self, text="Notes", font=LG_BUTTON_FONT,
                          command = lambda : controller.show_frame(notes))

        # grid place buttons
        sch_butt.grid(row=1,column=0, padx=5, pady=15)
        ddt_butt.grid(row=2,column=0, padx=5, pady=15)
        ext_butt.grid(row=4,column=0, padx=5, pady=15)
        prf_butt.grid(row=1,column=1, padx=5, pady=15)
        nts_butt.grid(row=3,column=0, padx=5, pady=15)

class tbds_frame(Frame) :
    # "TaBular Data Storage Frame" - generalized framework for both the schedule and due_dates storage components

    # New versions must override save function to save to different location.

    def __init__(self, parent, controller, headers) :
        self.headers = headers 
        Frame.__init__(self, parent)
        # self.update_frame(controller)
 
    def update_frame(self, controller, data) :
        # clear frame
        for w in self.winfo_children() :
            w.destroy()

        self.generate_table(controller, data)
        return
    
    def generate_table(self, controller, data) : 
        ret_butt = Button(self, text="Back", font=SM_BUTTON_FONT,
                          command = lambda : controller.show_frame(start))
        ret_butt.grid(row=0, column=0)

        edits = []
        dels = []

        # start at offset (used if no data present)
        disp_row = ROW_TB_OFFSET-1
        disp_col = COL_TB_OFFSET-1

        for i,row in enumerate(data) :
            # headers offset the row display index
            disp_row = i + ROW_TB_OFFSET

            for j,datum in enumerate(row) :
                # left side buttons offset column display index
                disp_col = j + COL_TB_OFFSET

                entry = Label(self, width=10, text=datum)
                entry.grid(row=disp_row, column=disp_col)


            # generate edit, delete buttons
            edits.append(Button(self, text="Edit", font=SM_BUTTON_FONT, 
                              command = lambda row=disp_row : self.new_entry_prompt(controller, row, data, True)))
            dels.append(Button(self, text="Delete", font=SM_BUTTON_FONT, 
                              command = lambda row=i: self.delete_row(controller, row)))
            
            # grid the edit and delete buttons after the rows
            edits[i].grid(row=disp_row, column=disp_col+1)
            dels[i].grid(row=disp_row, column=disp_col+2)

        # make and place headers
        for i,head in enumerate(self.headers):
            header = Label(self, text=head)
            header.grid(row=0,column=i+1, padx=10, pady=2)

        # make and place "new entry" button
        new_button = Button(self, text="New", font=SM_BUTTON_FONT,
                            command = lambda : self.new_entry_prompt(controller, disp_row+1, data))
        new_button.grid(row=1,column=0)
        
        return
    
    def new_entry_prompt(self, controller, disp_row, data, replace=False) :
        data_index = disp_row - ROW_TB_OFFSET

        # generate and place entry boxes to enter a new row
        self.entrys = []
        for i,entry in enumerate(self.headers) :
            self.entrys.append(Entry(self))
            self.entrys[i].grid(row = disp_row, column=i+COL_TB_OFFSET)

        if replace :
            info = data[data_index]
            
            # if this is an edit, prepopulate the text boxes with existing information
            for entry in self.entrys :
                entry.insert(END, info[i])

            # label button and its function accordingly
            txt = "Save"
            comm = lambda : self.data_addinfo(controller, data_index)

        else :
            # if not an edit, do standard procedure
            txt = "Add"
            comm = lambda : self.data_addinfo(controller)

        # save button generation
        save_butt = Button(self, text=txt, font=SM_BUTTON_FONT, command = comm)
        save_butt.grid(row=disp_row, column=len(self.headers)+1)

        return 
    
    def data_addinfo(self) :
        info = [entry.get() for entry in self.entrys]
        return info
    
class schedule(tbds_frame) :
    def __init__(self, parent, controller) :
        # override init to call custom update_frame
        super().__init__(parent, controller, headers= ["Subject", "Cat. Number", "Days (M/T/W/Th/F)", "Hours (x:xx-x:xx)"])
        self.update_frame(controller)

    def update_frame(self, controller):
        # override update frame to "set" data to be used
        global seminfo
        seminfo = ios.load_semester_info()
        
        # call super update frame once correct data is established
        super().update_frame(controller, seminfo)


    def data_addinfo(self, controller, row=-1):
        # override save info to correct data 

        global seminfo
        info = super().data_addinfo()
        if row == -1 :
            seminfo.append(info)
        else :
            seminfo[row] = info
        ios.save_semester_info(seminfo)
        self.update_frame(controller)

    def delete_row(self, controller, row) :
        global seminfo
        # row = super().delete_row( row)
        seminfo.pop(row)
        ios.save_semester_info(seminfo)
        self.update_frame(controller)
    
class tasks(tbds_frame) :
    def __init__(self, parent, controller) :
        super().__init__(parent, controller, headers= ["Course", "Assignment Name", "Due Date", "Notes"])

        self.update_frame(controller)
    
    def update_frame(self, controller) :
        global duedates
        duedates = ios.load_due_dates()
        super().update_frame(controller, duedates)

    def data_addinfo(self, controller, row=-1) :
        print("tasks addinfo reached")
        global duedates
        info = super().data_addinfo()
        print(info)
        if row == -1 :
            duedates.append(info)
        else :
            duedates[row] = info
        ios.save_due_dates(duedates)
        self.update_frame(controller)

    def delete_row(self, controller, row) :
        global duedates
        duedates.pop(row)
        ios.save_due_dates(duedates)
        self.update_frame(controller)

class profile(Frame) :
    def __init__(self, parent, controller) : 
        Frame.__init__(self, parent)
        self.update_frame(controller)

    def update_frame(self, controller) :
        # clear frame
        for w in self.winfo_children() :
            w.destroy()

        global stinfo
        stinfo = ios.load_student_info()

        # if no student info is found, prompt for entry immediately.
        if stinfo is None :
            ttext = "Enter profile information below.\n Required fields are denoted with an asterisk (*)."
            btext = "Submit"
            t1 = t2 = t3 = ""
        else :
            ttext = "Edit profile information below."
            btext = "Save"
            t1,t2,t3 = tuple(stinfo)
            ret_butt = Button(self, text="Back", font=SM_BUTTON_FONT,
                command = lambda : (controller.show_frame(start)))  
            ret_butt.grid(row=0, column=0, padx=10, pady=10)

        topmsg = Label(self, text=ttext)
        topmsg.grid(row=0, column=1, padx=10, pady=10)
            


            
        txt1 = Label(self, text="Name*")
        txt2 = Label(self, text="Student ID")
        txt3 = Label(self, text="Graduation Year")

        txt1.grid(row=1,column=0,padx=10,pady=10)
        txt2.grid(row=2,column=0,padx=10,pady=10)
        txt3.grid(row=3,column=0,padx=10,pady=10)

        self.name_box = Entry(self)
        self.stid_box = Entry(self)
        self.year_box = Entry(self)

        self.name_box.insert(0,t1)
        self.stid_box.insert(0,t2)
        self.year_box.insert(0,t3)

        self.name_box.grid(row=1, column=1, padx=10, pady=10)
        self.stid_box.grid(row=2, column=1, padx=10, pady=10)
        self.year_box.grid(row=3, column=1, padx=10, pady=10)
            
        save_butt = Button(self, text=btext, font=SM_BUTTON_FONT,
            command = lambda : self.save_stinfo(controller))
        save_butt.grid(row=4, column=1, padx=10, pady=10)

    def save_stinfo(self, controller) :
        global stinfo

        name = self.name_box.get()
        stid = self.stid_box.get()
        year = self.year_box.get()

        stinfo = [[name, stid, year]]
        ios.save_student_into(stinfo)

        controller.show_frame(start)
        
        self.update_frame(controller)
        return
    
class exit_frame(Frame) :
    def __init__(self, parent, controller) :
        Frame.__init__(self, parent)

class notes(Frame) :

    def __init__(self, parent, controller) : 
        Frame.__init__(self, parent)
        self.update_frame(controller)

    def update_frame(self, controller) :
        # clear frame
        try :
            for w in self.winfo_children() :
                w.destroy()
        except :
            return # solution preventing errors from extra call on close. trace reason later
        
        # back button returns to start frame
        ret_butt = Button(self, text="Back", font=SM_BUTTON_FONT,
                          command = lambda : (controller.show_frame(start)))  
        ret_butt.grid(row=0, column=0, padx=10, pady=10)

        # new file button
        new_butt = Button(self, text="New", font=SM_BUTTON_FONT,
                          command = lambda : self.new_note(controller))
        new_butt.grid(row=1, column=0, padx=10, pady=10, sticky="n")


        # make frame to grid all of the directory display
        foldersframe = Frame(self)
        foldersframe.grid(row=1, column=1)

        # access notes directory
        ntsdir = os.path.join(datadir, notesdir)
        fgridrow = 0

        # for each subfolder in notes folder, create a label
        for folder in os.listdir(ntsdir) :
            Label(foldersframe, text=folder, anchor="w", justify="left").grid(row=fgridrow, column=0, sticky="w")
            fgridrow += 1
            folderdir = os.path.join(ntsdir, folder)

            # for each file in the subfolder, make a label and 2 buttons (open, delete)
            for file in os.listdir(folderdir) :
                filedir = os.path.join(folderdir, file)
                Label(foldersframe, text="   |______" + file, anchor="w", justify="left").grid(row=fgridrow, column=0, sticky="w")
                
                Button(foldersframe, text="Open", font=SM_BUTTON_FONT,
                       command = lambda fd = filedir: [self.open_note(controller, fd),
                                                       self.update_frame(controller)]).grid(row=fgridrow, column=1)
                
                Button(foldersframe, text="Delete", font=SM_BUTTON_FONT,
                       command = lambda fd = filedir:[ios.delete_note(fd), 
                                                      self.update_frame(controller)]).grid(row=fgridrow, column=2)
                fgridrow += 1

    def new_note(self, controller) :
        note_frame(self, controller)
        return
    
    def open_note(self, controller, dir) :
        note_frame(self, controller, dir)
        return
    

def note_frame(master, controller, dir=None) :
    nrt = Tk() 
    nrt.title("Notepad") 

    # make header its own frame
    header = Frame(nrt)

    # make strolling text box
    text_area = scrolledtext.ScrolledText(nrt, wrap=WORD, width=80, height=16, font=("Arial", 12)) 
    text_area.grid(column=0, row=2, pady=10, padx=10)  
    text_area.focus() 



    # file name entry
    fname_entry = Entry(header)

    # if a directory is provided, prefill the file name and display course name
    if dir :
        note = ios.read_note(dir)
        text_area.insert("1.0", note)
        split = os.path.split(dir)
        fname = split[-1]
        course = os.path.split(split[-2])[-1]

        fname_entry.insert(0, fname)
        var = StringVar(nrt)
        var.set(course)
        coursename = Label(header, text=course)
        coursename.grid(row=0, column=0, padx=10)

    # make dropdown only if a course must be selected (no dir)
    else :
        # insert default filename
        fname_entry.insert(0, "FILENAME")


        # get semester info for dropdown
        seminfo = ios.load_semester_info()
        options = [seminfo[i][0] + seminfo[i][1] for i in range(len(seminfo))]
        options.append("Other")

        # set string variable
        var = StringVar(nrt)
        var.set(options[len(options)-1])

        # generate dropdown with above settings
        dropdown = OptionMenu(header, var, *options)
        
        # grid dropdown to header
        dropdown.grid(row=0, column=0, padx=10)

    # save button gets data and course 
    save_butt = Button(header, text="Save", font=SM_BUTTON_FONT,
                       command = lambda : [ios.save_note(var.get(), 
                                                         text_area.get("1.0", END), 
                                                         fname_entry.get(), 
                                                         dir),
                                           master.update_frame(controller)])
    exit_butt = Button(header, text="Exit", font=SM_BUTTON_FONT,
                       command = lambda : [header.destroy(),
                                        nrt.destroy()])

    # grid header
    fname_entry.grid(row=0, column = 1, padx=10)
    save_butt.grid(row=0,column=2, padx=10)
    exit_butt.grid(row=0,column=3, padx=10)
    
    header.grid(row=0, column=0)
    nrt.mainloop()





if __name__ == "__main__" :
    nrt = ssapp()
    nrt.mainloop()