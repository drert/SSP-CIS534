import sys
import os
import IOTools as ios
import GUITools as guis
import GlobalVars as gv

if __name__ == "__main__" :

    # if a storage directory for this app does not exist, create one
    if not os.path.exists(gv.datadir) :
        os.mkdir(gv.datadir)
        print("Storage directory not found, creating new app storage.")
    
    # generate notes path if missing
    ntsdir = os.path.join(gv.datadir, gv.notesdir)
    if not os.path.exists(ntsdir) :
        os.mkdir(ntsdir)

    approot = guis.ssapp()
    approot.mainloop()
    
