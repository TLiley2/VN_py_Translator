import psutil 
import tkinter as tk
import pygetwindow as gw
import pyautogui
from PIL import Image
import subprocess
import os
import sys
from pathlib import Path
import screeninfo
import cv2 
import numpy as np

#Reads setting values                
def read_SET(set_Name):
    if getattr(sys, 'frozen', False):
        script_dir = os.path.dirname(os.path.abspath(sys.argv[0]))
    else:
        script_dir = os.path.dirname(os.path.abspath(__file__))
    path_set = os.path.join(script_dir, "settings.ini")
    with open(path_set, 'r') as file:
        content = file.readlines()
        row_without_None = [name.strip() for name in content]
        for item in row_without_None:  # 'item' takes each value from the list in turn
            if str(set_Name) in item:
                cu = item
                index = row_without_None.index(cu)
                lines = content[index].strip()
                spl_word = '= '
                res = lines.split(spl_word, 1)
                splitString = res[1]
                return splitString
            
def modi_SET(set_Name, vari):
    if getattr(sys, 'frozen', False):
        script_dir = os.path.dirname(os.path.abspath(sys.argv[0]))
    else:
        script_dir = os.path.dirname(os.path.abspath(__file__))
    path_set = os.path.join(script_dir, "settings.ini")
    with open(path_set, 'r+') as file:
        content = file.readlines()
        row_without_None = [name.strip() for name in content]
        for item in row_without_None:  # 'item' takes each value from the list in turn
            if str(set_Name) in item:
                cu = item
                index = row_without_None.index(cu)
                lines = content[index].strip()
                spl_word = ' = '
                splitString2 = lines.split(spl_word, 1)[0]
                print(splitString2)
                result = ' '.join([splitString2, "=", vari])
                file.seek(0)
                content[index] = result + '\n'
                file.writelines(content)
                file.truncate()
                return result
      
# Checks if the seleceted .exe is currently open
def check_Status(exe_name,x1,y1,x2,y2,acti):
    mic_Check=exe_name in (i.name() for i in psutil.process_iter())
    if mic_Check == True:
        if acti == 0:
            appl_name=exe_name.replace(".exe","")
            screenshot(appl_name, None,None,None,None,0)
        elif acti== 1:
            screenshot(None,x1,y1,x2,y2,1)
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
def screenshot(app_name,x1,y1,x2,y2,acti):
    if acti == 0:
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
    elif acti== 1:
        left, top, right, bottom = x1,y1,x2,y2

    print(left, top, right, bottom)

    if getattr(sys, 'frozen', False):
        script_dir = os.path.dirname(os.path.abspath(sys.argv[0]))
    else:
        script_dir = os.path.dirname(os.path.abspath(__file__))
    path_set = os.path.join(script_dir, "result.png")
    print(path_set)

    # Take a screenshot of the window region and save it to the specified path
    screenshot = pyautogui.screenshot(region=(left, top, right - left, bottom - top))
    if acti == 0:
        screenshot.save(path_set)
    if acti == 1:
        screen = screeninfo.get_monitors()[0]
        width = screen.width
        height = screen.height
        screenshot_np = np.array(screenshot)
        img_pil = Image.fromarray(cv2.cvtColor(screenshot_np, cv2.COLOR_BGR2RGB))
        im = Image.new(mode="RGB", size=(width, height),color = (255, 255, 255))
        im.paste(img_pil, (x1, y1))
        im.save(path_set)

    #Activates OCR file
    import OCR
    OCR.exec(path_set)
 
