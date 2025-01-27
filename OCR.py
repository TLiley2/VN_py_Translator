import easyocr
import tkinter as tk
import os
import sys

sys.stderr = open(os.devnull, 'w') # Prevent printing warnings
b=[]
sys.stderr = open(os.devnull, 'w') # Prevent printing warnings
b=[]
if getattr(sys, 'frozen', False):
    script_dir = os.path.dirname(os.path.abspath(sys.argv[0]))
else:
    script_dir = os.path.dirname(os.path.abspath(__file__))
reader = easyocr.Reader(['ja'], gpu=True)

def google_tran(inpoot):
    import requests
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
    import cv2
    print("prime")

    # Load image
    img = cv2.imread(imgap)
    if img is None:
        print("Image not found at path")

    # Increase contrast
    contrast = cv2.convertScaleAbs(img, alpha=1.5, beta=1)

    # Greyscale
    gray = cv2.cvtColor(contrast, cv2.COLOR_BGR2GRAY)

    # Denoise the image with Gaussian Blur
    #blurred = cv2.GaussianBlur(gray, (3, 3), 0)

    # Threshold the image (binary)
    _, threshold_img = cv2.threshold(gray, 128, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    # Calculate the percentage of black pixels
    import numpy as np
    black_pixels = np.sum(threshold_img == 0)
    total_pixels = threshold_img.size
    black_ratio = black_pixels / total_pixels

    # Invert the image if black pixels dominate
    if black_ratio > 0.75:
        processed_img = cv2.bitwise_not(threshold_img)
    else:
        processed_img = threshold_img

    # Perform OCR on the processed image
    result = reader.readtext(processed_img, text_threshold=0.7, low_text=0.5)
    #print(result)
    processed_results = [
    ([list(map(int, bbox)) for bbox in item[0]], item[1], item[2]) 
    for item in result if 0.05 < item[2] < 1
    ]
    # [width x hiegth]
    # [x x y]

    # existing_items = [
    # item for item in processed_results
    # if abs(int(item[0][0][1])-int(item[0][0][1]))<=5]

    # print(existing_items)

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
        trans_text=translated[i]
        b.append([min_x, min_y, trans_text])
        #print(b)

    # height, width = img.shape[:2]
    # aspect_ratio = height / width
    # new_height = int(800 * aspect_ratio)
    # cv2.namedWindow("Image", cv2.WINDOW_NORMAL)  
    # cv2.resizeWindow("Image", 800, new_height)         
    # cv2.imshow("Image", processed_img)                   
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
    from PIL import Image
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

# d=r"C:\Users\tnu20\Downloads\sw34.png"
# #d=r"C:\Users\tnu20\OneDrive\Documents\Documents\LIGMA\swstella_system_cg1.jpg"
# exec(d)
