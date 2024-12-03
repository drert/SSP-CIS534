import os
datadir = './Files'
stinfo_filename = "StudentInfo.txt"
seminfo_filename = "Courses.txt"
assignments_filename = "Tasks.txt"

notesdir = 'Notes'

WINDOW_HEIGHT = 750
WINDOW_LENGTH = 1000

font_family_button = "Arial"
font_family_text = "Courier"

MENU_FONT = (font_family_text, 35)
INFO_FONT = (font_family_text, 10)
LG_BUTTON_FONT = (font_family_button, 20)
SM_BUTTON_FONT = (font_family_button, 8)
# RF_BUTTON_FONT = ("Courier", 15)

print_errors = False

COLORS = ["blue", "green", "yellow", "skyblue", "purple"]

ntsdir = os.path.join(datadir, notesdir)