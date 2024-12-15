import cv2
import easyocr
import tkinter as tk
from screeninfo import get_monitors
from PIL import Image
import torch
import os
import sys
#import googletrans
import requests

sys.stderr = open(os.devnull, 'w') # Prevent printing warnings
b=[]
reader = easyocr.Reader(['ja'], gpu=True) # this needs to run only once to load the model into memory

def google_tran(inpoot):
    # Define the input text and target language
    text = inpoot
    source_lang = "ja"
    target_lang = "en"

    # URL for Google Translate might not be accessible directly. Example assumes a public translation API endpoint.
    url = f"https://translate.googleapis.com/translate_a/single"
    params = {
        "client": "gtx",
        "sl": source_lang,
        "tl": target_lang,
        "dt": "t",
        #"q": text
        "q": "\n".join(text)
    }

    # Make the GET request
    response = requests.get(url, params=params)

    if response.status_code == 200:
        #return (f"{response.json()[0][0][0]}")
        return [item[0] for item in response.json()[0]]
    else:
        print("Failed to retrieve translation.")

def prime(imgap):
    #print("prime")
    # Load image
    img = cv2.imread(imgap)
    if img is None:
        print("Image not found at path")

    # Inverts Image
    invert = cv2.bitwise_not(img)

    # Cranks up contrast Image
    contrast = cv2.convertScaleAbs(invert, alpha=1.5, beta=1)

    # Greyscales Image
    gray = cv2.cvtColor(contrast, cv2.COLOR_BGR2GRAY)
    
    # Apply threshold to convert to binary image
    threshold_img = cv2.threshold(gray, 128, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]

    #os.environ["CUDA_VISIBLE_DEVICES"] = "-1"
    #torch.device('cpu')
    #print("halit")
    
    result = reader.readtext(threshold_img, text_threshold=0.6, low_text=0.2)
    processed_results = [
    ([list(map(int, bbox)) for bbox in item[0]], item[1], item[2]) 
    for item in result if 0.09 < item[2] < 1
    ]
    # [width x hiegth]

    # Send all text for batch transaltion
    all_text = [item[1] for item in processed_results]
    translated = google_tran(all_text)

    # translated=[]
    # for x in range(len(all_text)):
    #     ddd = all_text[x]
    #     gg = google_tran(ddd)
    #     translated.append(gg)

    for i, item in enumerate(processed_results):
        min_x, min_y = item[0][0][0], item[0][0][1]
        b.append([min_x, min_y, translated[i]])
    # cv2.namedWindow("Image", cv2.WINDOW_NORMAL)  
    # cv2.resizeWindow("Image", 500, 500)         
    # cv2.imshow("Image", gray)                   
    # cv2.waitKey(0)

def exec(ima):
    b.clear()
    prime(ima)
    #print(b)
    for item in b:
        s = int(float(item[0]))
        e = int(float(item[1]))
        # Pass them to the overlay function
        overlay(s, e, item[2], ima)
    # Start the mainloop only if the window exists  
    if hasattr(overlay, "win") and overlay.win.winfo_exists():  
        overlay.win.mainloop()

def overlay(xval, yval, tra_text, imge):
    s = f"{xval}"  # x is the x-coordinate for .place()
    e = f"{yval}"  # y is the y-coordinate for .place()
    g = f"{tra_text}"  # Only tra_text is the label text

    # Create the main window if it's not created already
    if not hasattr(overlay, "win") or not overlay.win.winfo_exists():
        overlay.win = tk.Toplevel()  # Use Toplevel instead of Tk for overlays
        overlay.win.transient()  # Make it modal relative to the parent window
        overlay.win.grab_set()  # Block interaction with other windows

        # Set the geometry and color of the window
        overlay.win.wm_overrideredirect(True)
        overlay.win.geometry("{0}x{1}+0+0".format(overlay.win.winfo_screenwidth(), overlay.win.winfo_screenheight()))
        overlay.win.config(bg='#add123')  # Set background color
        overlay.win.wm_attributes('-transparentcolor', '#add123')  # Make window transparent

        # Handle close event - window won't be destroyed
        overlay.win.protocol("WM_DELETE_WINDOW", lambda: overlay.win.destroy())  # Hide window instead of destroying
        overlay.win.bind("<Button-1>", lambda evt: overlay.win.destroy())  # Hide on click

    overlay.win.update_idletasks()
    drawable_height  = overlay.win.winfo_height()
    img = Image.open(imge)
    img_height = img.height

    # If label goes paset tkinker's drawable_height
    if int(e) > int(drawable_height)-100:
        reduct_val = int(img_height)  - int(drawable_height)
        e = int(e) - reduct_val
    label = tk.Label(overlay.win, text=g, font=("Arial", 12), fg="black")
    label.place(x=int(s), y=int(e))
    #print(int(e))

    overlay.win.deiconify() 

# d=r"C:\Users\tnu20\Downloads\New folder\SLPM-67003_20241208234657.png"
# exec(d)
