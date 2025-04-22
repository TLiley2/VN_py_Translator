import tkinter as tk
from tkinter import ttk
import subprocess
import keyboard
import sys
import time


# Reads API & Shortcut
import backend
global APIreader
APIreader=backend.read_SET("API_key")
global shortKey
shortKey=backend.read_SET("Shortcut")
global scanmed
scanmed=backend.read_SET("scan_method")

# Adds current API key as temp text in entry box
def on_focus_in(e):
   e.widget.delete(0,"end")
def on_focus_out(e):
    if e.widget == username_entry:
        e.widget.insert(0, APIreader)
    elif e.widget == username_entry2:
        e.widget.insert(0, shortKey)
        
# Open settings window
def displaySetttings():
    global username_entry
    global username_entry2
    newWindow = tk.Toplevel(root)
    newWindow.title("Class Display")
    newWindow.geometry('900x900')
    newWindow.minsize(400, 200)
    newWindow.maxsize(600, 400)
    newWindow.configure(bg='grey')
    root.columnconfigure(0, weight=1)
    root.columnconfigure(1, weight=3)

    intro_label = tk.Label(newWindow, text='Please restart after making\n changes')
    intro_label.grid(column=1, row=0, sticky=tk.W, padx=5, pady=5)
    
    username_label = tk.Label(newWindow, text="API Key:")
    username_label.grid(column=0, row=1, sticky=tk.E, padx=5, pady=5)
    
    username_entry = tk.Entry(newWindow)
    username_entry.grid(column=1, row=1, sticky=tk.W, padx=5, pady=5)
    username_entry.insert(0, APIreader)
    username_entry.bind("<FocusIn>", on_focus_in)
    username_entry.bind("<FocusOut>", on_focus_out)
    
    # Chanages API key to entrybox text
    button = tk.Button(newWindow, text="Save", command=lambda: backend.modi_SET("API_key",username_entry.get()))
    button.grid(column=2, row=1, padx=5, pady=5)

    username_label2 = tk.Label(newWindow, text="Activation shortcut:")
    username_label2.grid(column=0, row=2, sticky=tk.W, padx=5, pady=5)
    
    username_entry2 = tk.Entry(newWindow)
    username_entry2.grid(column=1, row=2, sticky=tk.W, padx=5, pady=5)
    username_entry2.insert(0, shortKey)
    username_entry2.bind("<FocusIn>", on_focus_in)
    username_entry2.bind("<FocusOut>", on_focus_out)
    
    # Chanages Shortcut to entrybox text
    button2 = tk.Button(newWindow, text="Save", command=lambda: backend.modi_SET("Shortcut",username_entry2.get()))
    button2.grid(column=2, row=2, padx=5, pady=5)

    caution_Label = tk.Label(newWindow, text='Remeber to add " + " \nin between keys')
    caution_Label.grid(column=1, row=3, sticky=tk.W, padx=5, pady=5)

    username_label3 = tk.Label(newWindow, text="scan_method:")
    username_label3.grid(column=0, row=4, sticky=tk.E, padx=5, pady=5)
    
    username_entry3 = tk.Entry(newWindow)
    username_entry3.grid(column=1, row=4, sticky=tk.W, padx=5, pady=5)
    username_entry3.insert(0, scanmed)
    username_entry3.bind("<FocusIn>", on_focus_in)
    username_entry3.bind("<FocusOut>", on_focus_out)
    
    # Chanages Shortcut to entrybox text
    button3 = tk.Button(newWindow, text="Save", command=lambda: backend.modi_SET("scan_method",username_entry3.get()))
    button3.grid(column=2, row=4, padx=5, pady=5)

    wr_label = tk.Label(newWindow, text='0 = Whole Screen \n1 = scan box')
    wr_label.grid(column=1, row=5, sticky=tk.W, padx=5, pady=5)
    
    newWindow.mainloop()

# Main GUI
print("Starting GUI setup...")
start = time.time()
root = tk.Tk()
print(f"Tkinter root setup: {time.time() - start:.2f} seconds")

root.minsize(400, 200)
root.maxsize(600, 400)
root.configure(bg='grey')
root.title("VN_py_Translator")
start = time.time()

def on_closing():
    root.destroy()  # Close the Tkinter window
    sys.exit()     # Exit the program completely

root.protocol("WM_DELETE_WINDOW", on_closing)  # Bind the close button to `on_closing`

root.columnconfigure(0, weight=9)
root.columnconfigure(1, weight=1)
root.rowconfigure(0, weight=1)
root.rowconfigure(1, weight=1)
root.rowconfigure(2, weight=1)

# image = Image.open("cog.png")
# resized_image = image.resize((20, 20))
# photo = ImageTk.PhotoImage(resized_image)

n = tk.StringVar()

# List of currenly running app  
a=[]

# Searches Apps currently running 
cmd = ('powershell "gps | where {$_.MainWindowTitle} | select -ExpandProperty Path | Split-Path -Leaf')
proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
for line in proc.stdout:
    if line.rstrip():
       # print(line.decode().rstrip())
       a.append(line.decode().rstrip())

# Drop down menu
monthchoosen = ttk.Combobox(root, values=a, width = 27, textvariable = n)
monthchoosen.grid(column = 0, row = 1) 
monthchoosen.current() 

# Buttons
label = tk.Label(root, text="Please select the game \nyou are currently running",font=("Arial", 10, "bold"))
label.grid(column=0, row=0, sticky=tk.S, padx=5, pady=5)

label = tk.Label(root, text="v1.1",font=("Arial", 10, "bold"))
label.grid(column=1, row=2, sticky=tk.S, padx=5, pady=5)

def stopmed():
    if int(scanmed) ==0:
        backend.check_Status(n.get(), None,None,None,None,0)
    elif int(scanmed) ==1 or (n.get())!= None:
        exe_Name=n.get()
        import scanbox
        scanbox.boxy(exe_Name)

button = tk.Button(root, text="Activate", command=lambda: stopmed())
button2 = tk.Button(root, text="Set", command=displaySetttings)
#button2.image = photo

button.grid(column=0, row=2, padx=5, pady=5)
button2.grid(column=1, row=0, sticky=tk.NE, padx=10, pady=10)

# Keyboard shortcut for using "Activate"
keyboard.add_hotkey(str(shortKey), button.invoke)
root.mainloop()
