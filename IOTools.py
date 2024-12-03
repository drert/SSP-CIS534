import pandas as pd
import numpy as np
import os

from GlobalVars import *
from pathlib import Path
delim = ","

def wr_file (input: list, path: str) :
    # save info to path
    np.savetxt(path, input, delimiter=delim, fmt="%s")
    return

def rd_file (path: str) :
    # load info from path
    return np.loadtxt(path, delimiter=delim, dtype=str).tolist()

def load_student_info() :
    path = os.path.join(datadir, stinfo_filename)
    try :
        stinfo = rd_file(path)
        return stinfo
    except Exception as error :
        print(error)
        return None

def load_semester_info() :
    path = os.path.join(datadir, seminfo_filename)
    try :
        stinfo = rd_file(path)

        # correction for single entry being read as 1D list
        if isinstance(stinfo[0],str) : 
            return [stinfo] 
        
        return stinfo
    except Exception as error :
        if print_errors :
            print(error)
        return []

def load_due_dates() :
    path = os.path.join(datadir, assignments_filename)
    try :
        dd_info = rd_file(path)

        # correction for single entry being read as 1D list
        if isinstance(dd_info[0], str) :
            return [dd_info]
        
        return dd_info
    except Exception as error :
        if print_errors :
            print(error)
        return []

def save_student_into(stinfo : list) :
    wr_file(stinfo, os.path.join(datadir, stinfo_filename))
    return

def save_semester_info(sem_info : list) :
    wr_file(sem_info, os.path.join(datadir, seminfo_filename))
    return

def save_due_dates(due_dates : list) :


    wr_file(due_dates, os.path.join(datadir, assignments_filename))
    return

def get_notes_folders() :
    dir = os.path.join(datadir, notesdir)
    if not os.path.exists(dir) :
        os.mkdir(dir)
    
    return os.listdir(dir)
    
def read_note(dir) :
    with open(dir, "r") as file:
        note = file.read()
    return note

def save_note(classdir, data, name, dir=None) :
    if name is None :
        print("Must enter file name!")
        return
    
    if (dir is None) or (os.path.split(dir)[-1] is not name) :
        dir = os.path.join(datadir, notesdir, classdir)

        if not os.path.exists(dir) :
            os.mkdir(dir)
        
        filepath = Path(os.path.join(dir, name))
    else :
        filepath = Path(dir)

    with filepath.open("w") as file :
        file.write(data)
        print("Saved!")

    return

def delete_note(notedir) :
    os.remove(notedir)
    return
