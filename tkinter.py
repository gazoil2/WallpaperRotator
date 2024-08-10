import ctypes
import os
import time
import random
import glob
from PIL import Image
import winreg
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from threading import Thread

def extract_frames_from_gif(gif_path, output_folder):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    with Image.open(gif_path) as img:
        frame_number = 0
        while True:
            frame_path = os.path.join(output_folder, f"frame_{frame_number}.png")
            img.save(frame_path, format='PNG')
            frame_number += 1
            try:
                img.seek(img.tell() + 1)
            except EOFError:
                break

def set_wallpaper(image_path, style):
    if not os.path.isfile(image_path):
        raise ValueError(f"File not found: {image_path}")

    SPI_SETDESKWALLPAPER = 20
    SPIF_UPDATEINIFILE = 0x01
    SPIF_SENDCHANGE = 0x02

    ctypes.windll.user32.SystemParametersInfoW(
        SPI_SETDESKWALLPAPER,
        0,
        image_path,
        SPIF_UPDATEINIFILE | SPIF_SENDCHANGE
    )

    set_wallpaper_style(style)

def set_wallpaper_style(style):
    registry_path = r"Control Panel\Desktop"
    value_name = "WallpaperStyle"
    styles = {
        "fill": "10",
        "fit": "6",
        "stretch": "2",
        "tile": "0",
        "center": "1"
    }
    
    if style not in styles:
        raise ValueError(f"Unsupported style: {style}")

    try:
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, registry_path, 0, winreg.KEY_SET_VALUE) as key:
            winreg.SetValueEx(key, value_name, 0, winreg.REG_SZ, styles[style])
            ctypes.windll.user32.SendMessageW(0xFFFF, 0x001A, 0, 0)
    except Exception as e:
        print(f"Failed to set wallpaper style: {e}")

def get_image_files(folder_path):
    image_patterns = ['*.jpg', '*.jpeg', '*.png', '*.bmp', '*.gif']
    image_files = []
    for pattern in image_patterns:
        image_files.extend(glob.glob(os.path.join(folder_path, pattern)))
    return image_files

def start_slideshow(folder_path, temp_folder, wallpaper_style, interval):
    image_files = get_image_files(folder_path)
    
    if not image_files:
        messagebox.showerror("Error", "No image files found in the specified folder.")
        return

    while True:
        for image_path in image_files:
            if image_path.lower().endswith('.gif'):
                extract_frames_from_gif(image_path, temp_folder)
                frames = get_image_files(temp_folder)
                for frame in frames:
                    set_wallpaper(frame, wallpaper_style)
                    time.sleep(interval)
                for frame in frames:
                    os.remove(frame)
            else:
                set_wallpaper(image_path, wallpaper_style)
                time.sleep(interval)
    

def browse_folder(entry):
    folder = filedialog.askdirectory()
    if folder:
        entry.delete(0, tk.END)
        entry.insert(0, folder)

def start_thread(folder_path, temp_folder, wallpaper_style, interval):
    thread = Thread(target=start_slideshow, args=(folder_path, temp_folder, wallpaper_style, interval))
    thread.daemon = True
    thread.start()

def on_start_button_click(folder_entry, temp_folder_entry, style_var, interval_entry):
    folder_path = folder_entry.get()
    temp_folder = temp_folder_entry.get()
    wallpaper_style = style_var.get()
    try:
        interval = float(interval_entry.get())
    except ValueError:
        messagebox.showerror("Error", "Invalid interval. Please enter a number.")
        return
    start_thread(folder_path, temp_folder, wallpaper_style, interval)

def create_gui():
    root = tk.Tk()
    root.title("Wallpaper Slideshow")

    tk.Label(root, text="Folder Path:").grid(row=0, column=0, padx=10, pady=10, sticky="e")
    folder_entry = tk.Entry(root, width=50)
    folder_entry.grid(row=0, column=1, padx=10, pady=10)
    tk.Button(root, text="Browse", command=lambda: browse_folder(folder_entry)).grid(row=0, column=2, padx=10, pady=10)

    tk.Label(root, text="Temporary Folder for GIF Frames:").grid(row=1, column=0, padx=10, pady=10, sticky="e")
    temp_folder_entry = tk.Entry(root, width=50)
    temp_folder_entry.grid(row=1, column=1, padx=10, pady=10)
    tk.Button(root, text="Browse", command=lambda: browse_folder(temp_folder_entry)).grid(row=1, column=2, padx=10, pady=10)

    tk.Label(root, text="Wallpaper Style:").grid(row=2, column=0, padx=10, pady=10, sticky="e")
    style_var = tk.StringVar(value="stretch")
    style_menu = ttk.Combobox(root, textvariable=style_var, values=["fill", "fit", "stretch", "tile", "center"])
    style_menu.grid(row=2, column=1, padx=10, pady=10)

    tk.Label(root, text="Interval (seconds):").grid(row=3, column=0, padx=10, pady=10, sticky="e")
    interval_entry = tk.Entry(root, width=10)
    interval_entry.grid(row=3, column=1, padx=10, pady=10)
    interval_entry.insert(0, "5")

    tk.Button(root, text="Start Slideshow", command=lambda: on_start_button_click(folder_entry, temp_folder_entry, style_var, interval_entry)).grid(row=4, column=1, padx=10, pady=20)

    root.mainloop()

if __name__ == "__main__":
    create_gui()
