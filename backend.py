import psutil 
import tkinter as tk
import pygetwindow as gw
import pyautogui
from PIL import Image
import subprocess
import os
import sys

from pathlib import Path

#Return exe name selected by drop box
def pass_exe_name():
    if len(sys.argv) > 2:  # Check if a value was passed
        received_value = sys.argv[1]
        ffd = (f"{received_value}")
        result = ffd 
        #print(result)
        return result 
    else:
        print("No value was passed")

#return activation key
def acti():
    if len(sys.argv) > 2:  # Check if a value was passed
        received_value2 = sys.argv[2]
        ddf = (f"{received_value2}")
        activ_code = ddf  
        #print(activ_code)
        return activ_code 
    else:
        print("No value was passed")

#passed retur to variables
name_exe=pass_exe_name()
matrix=acti()

# Read text line if it conatins string
# def read_Line():
#     # Reaads directory of py file
#     if getattr(sys, 'frozen', False):
#         script_dir = os.path.dirname(os.path.abspath(sys.argv[0]))
#     else:
#         script_dir = os.path.dirname(os.path.abspath(__file__))
#     # Constructs the file path for settings file
#     path_set = os.path.join(script_dir, "settings.ini")
#     with open(path_set, 'r') as file:
#         content = file.readlines()
#         row_without_None = [name.strip() for name in content]
#         for item in row_without_None:  # 'item' takes each value from the list in turn
#             if "testing_name" in item:
#                 #Return line where string is found
#                 cu = item
#                 #Return the text on line (cu) 
#                 index = row_without_None.index(cu)
#                 #Removes spaces that line
#                 lines = content[index].strip()
#                 #return lines
#                 #splits line into chars are reutrn last elemts
#                 last_element = lines.split()[-1]
#                 return last_element

#Reads of Shirtcut key in setting          
def read_Short():
    if getattr(sys, 'frozen', False):
        script_dir = os.path.dirname(os.path.abspath(sys.argv[0]))
    else:
        script_dir = os.path.dirname(os.path.abspath(__file__))
    path_set = os.path.join(script_dir, "settings.ini")
    with open(path_set, 'r') as file:
        content = file.readlines()
        row_without_None = [name.strip() for name in content]
        for item in row_without_None:  # 'item' takes each value from the list in turn
            if "Shortcut" in item:
                cu = item
                index = row_without_None.index(cu)
                lines = content[index].strip()
                spl_word = '= '
                res = lines.split(spl_word, 1)
                splitString = res[1]
                return splitString

#Reads of API key in setting          
def read_API():
    if getattr(sys, 'frozen', False):
        script_dir = os.path.dirname(os.path.abspath(sys.argv[0]))
    else:
        script_dir = os.path.dirname(os.path.abspath(__file__))
    path_set = os.path.join(script_dir, "settings.ini")
    with open(path_set, 'r') as file:
        content = file.readlines()
        row_without_None = [name.strip() for name in content]
        for item in row_without_None:  # 'item' takes each value from the list in turn
            if "API_key" in item:
                cu = item
                index = row_without_None.index(cu)
                lines = content[index].strip()
                spl_word = '= '
                res = lines.split(spl_word, 1)
                splitString = res[1]
                return splitString

#Modifies testing var in setting            
# def modi_var():
#     if getattr(sys, 'frozen', False):
#         script_dir = os.path.dirname(os.path.abspath(sys.argv[0]))
#     else:
#         script_dir = os.path.dirname(os.path.abspath(__file__))
#     # Construct the path for saving the screenshot
#     path_set = os.path.join(script_dir, "settings.ini")
#     with open(path_set, 'r+') as file:
#         content = file.readlines()
#         row_without_None = [name.strip() for name in content]
#         for item in row_without_None:  
#             if "testing_co" in item:
#                 cu = item
#                 index = row_without_None.index(cu)
#                 print(index)
#                 lines = content[index].strip()
#                 last_element = lines.split()[-1]
#                 s1 = lines.replace(last_element, "3")
#                 file.seek(0)
#                 content[index] = s1 + '\n'
#                 file.writelines(content)
#                 return s1
      
#Modifies of API key in setting 
def modi_API(key):
    if getattr(sys, 'frozen', False):
        script_dir = os.path.dirname(os.path.abspath(sys.argv[0]))
    else:
        script_dir = os.path.dirname(os.path.abspath(__file__))
    path_set = os.path.join(script_dir, "settings.ini")
    with open(path_set, 'r+') as file:
        content = file.readlines()
        row_without_None = [name.strip() for name in content]
        for item in row_without_None:
            if "API_key" in item:
                cu = item
                index = row_without_None.index(cu)
                lines = content[index].strip()
                last_element = lines.split()[-1]
                s1 = lines.replace(last_element, key)
                file.seek(0)
                content[index] = s1 + '\n'
                file.writelines(content)
                file.truncate()
                return s1

# Checks if the seleceted .exe is currently open
def check_Status(exe_name):
    mic_Check=exe_name in (i.name() for i in psutil.process_iter())
    if mic_Check == True:
        #print(exe_name)
        print("yes1")
        appl_name=exe_name.replace(".exe","")
        screenshot(appl_name)
    elif mic_Check == False :
        NOPE = tk.Tk()
        NOPE.title("Error 404")
        NOPE.minsize(300, 200)
        NOPE.maxsize(600, 200)
        NOPE.configure(bg='grey')
        NOPE.columnconfigure(0, weight=1)
        NOPE.columnconfigure(1, weight=1)
        NOPE.columnconfigure(2, weight=1)
        NOPE.rowconfigure(0, weight=1)
        l = tk.Label(NOPE,text="Error 404: Program is not runnning \n 1.)Please fully close this application\n 2.)Start your desired game\n 3.)restart this application and try again\n Sorry for the inconvience ;-)", font=("Noto Sans JP Bold", 10))
        l.grid(column=1, row=0)
        NOPE.mainloop()

# Takes screenshot of the program       
def screenshot(app_name):
    exe_ad = app_name

    # Returns the programs current window title
    cmd = f'powershell -Command "$OutputEncoding = [System.Text.Encoding]::UTF8; chcp 65001; Get-Process -Name {exe_ad} | ForEach-Object {{ $_.MainWindowTitle }}"'
    proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    w = None
    for line in proc.stdout:
        if line.strip():  # Skip empty lines
            try:
                w = line.decode('utf-8').strip()  # Attempt UTF-8 decoding
            except UnicodeDecodeError:
                print("Failed to decode output with UTF-8. Trying UTF-16.")
                w = line.decode('utf-16-le').strip()  # Try UTF-16LE as a fallback

    if not w:
        print("No window title found. Is the application running?")
        return

    window_title = w  # Replace with the actual window title
    #print(window_title)

    # Returns the the dimensions of the app's window
    window = gw.getWindowsWithTitle(window_title)[0]
    left, top, right, bottom = window.left, window.top, window.right, window.bottom

    # Construct the path for saving the screenshot
    if getattr(sys, 'frozen', False):
        path = os.path.dirname(os.path.abspath(sys.argv[0]))
    else:
        path = Path(__file__).parent.absolute() /  "result.png"

    # Take a screenshot of the window region and save it to the specified path
    screenshot = pyautogui.screenshot(region=(left, top, right - left, bottom - top))
    screenshot.save(path)

    #Activates OCR file
    import OCR
    OCR.exec(path)
 
#If activitaion key is sent by button
if "1" in str(matrix):
    check_Status(name_exe)

# ff=read_API()
# print(ff)