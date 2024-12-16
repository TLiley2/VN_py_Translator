import tkinter as tk

def boxy(exe_Name):
    def close_window():
        root.quit()

    def move_app(e):
        root.geometry(f'+{e.x_root}+{e.y_root}')

    def on_resize_top_left(event):
        new_width = root.winfo_width() - (event.x_root - root.winfo_rootx())
        new_height = root.winfo_height() - (event.y_root - root.winfo_rooty())
        root.geometry(f"{new_width}x{new_height}+{event.x_root}+{event.y_root}")

    def on_resize_top_right(event):
        new_width = event.x_root - root.winfo_rootx()
        new_height = root.winfo_height() - (event.y_root - root.winfo_rooty())
        root.geometry(f"{new_width}x{new_height}+{root.winfo_x()}+{event.y_root}")

    def on_resize_bottom_left(event):
        new_width = root.winfo_width() - (event.x_root - root.winfo_rootx())
        new_height = event.y_root - root.winfo_rooty()
        root.geometry(f"{new_width}x{new_height}+{event.x_root}+{root.winfo_y()}")

    def on_resize_bottom_right(event):
        new_width = event.x_root - root.winfo_rootx()
        new_height = event.y_root - root.winfo_rooty()
        root.geometry(f"{new_width}x{new_height}+{root.winfo_x()}+{root.winfo_y()}")


    root = tk.Toplevel()
    root.transient()  # Make it modal relative to the parent window
    root.grab_set()  # Block interaction with other windows
    root.geometry("400x300")

    # Remove the default title bar
    root.overrideredirect(True)  

    # Add a background color to the Main rootdow
    root.config(bg = '#add123')

    #Create a transparent rootdow
    root.wm_attributes('-transparentcolor','#add123')
    root.attributes('-topmost',True)

    # Create a custom title bar
    title_bar = tk.Frame(root, bg="white")
    title_bar.pack(side="top", fill="x")
    title_bar.bind("<B1-Motion>", move_app)

    close_button = tk.Button(title_bar, text="X", command=close_window, fg="red", height=int(0.5))
    close_button.pack(side="right")

    offset=5
    main_frame = tk.Frame(root, bg="#add123")
    main_frame.pack(fill="both", expand=True)
    main_frame.bind("<B1-Motion>", move_app)
    main_frame.configure(highlightbackground="red", highlightcolor="red", highlightthickness=offset)

    def cor():
        main_frame.update()

        x1 = main_frame.winfo_rootx()
        y1 = main_frame.winfo_rooty()

        x2 = x1 + main_frame.winfo_width()
        y2 = y1 + main_frame.winfo_height()
        import backend
        backend.check_Status(exe_Name, x1+offset,y1+offset,x2-offset,y2-offset, 1)

    # Resize zones (all four corners)
    corner_size = 10

    # Top-left corner
    top_left = tk.Frame(main_frame, width=corner_size, height=corner_size, bg="gray")
    top_left.place(x=0, y=0, anchor="nw")
    top_left.bind("<B1-Motion>", on_resize_top_left)
    top_left = tk.Frame(root, width=corner_size, height=corner_size, bg="gray")
    top_left.place(x=0, y=0, anchor="nw")
    top_left.bind("<B1-Motion>", on_resize_top_left)

    # Top-right corner
    top_right = tk.Frame(main_frame, width=corner_size, height=corner_size, bg="gray")
    top_right.place(relx=1.0, y=0, anchor="ne")
    top_right.bind("<B1-Motion>", on_resize_top_right)
    top_right = tk.Frame(root, width=corner_size, height=corner_size, bg="gray")
    top_right.place(relx=1.0, y=0, anchor="ne")
    top_right.bind("<B1-Motion>", on_resize_top_right)

    # Bottom-left corner
    bottom_left = tk.Frame(main_frame, width=corner_size, height=corner_size, bg="gray")
    bottom_left.place(x=0, rely=1.0, anchor="sw")
    bottom_left.bind("<B1-Motion>", on_resize_bottom_left)

    # Bottom-right corner
    bottom_right = tk.Frame(main_frame, width=corner_size, height=corner_size, bg="gray")
    bottom_right.place(relx=1.0, rely=1.0, anchor="se")
    bottom_right.bind("<B1-Motion>", on_resize_bottom_right)

    w = tk.Button(root, text="click", command=lambda: cor())
    w.pack()

    root.mainloop()

#boxy()