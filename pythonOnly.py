import ctypes
import os
import time
import random
import glob
import winreg

def set_wallpaper(image_path, style):
    # Validate the image path
    if not os.path.isfile(image_path):
        raise ValueError(f"File not found: {image_path}")

    # Define constants for SystemParametersInfoW
    SPI_SETDESKWALLPAPER = 20
    SPIF_UPDATEINIFILE = 0x01
    SPIF_SENDCHANGE = 0x02

    # Call the SystemParametersInfoW function from user32.dll
    ctypes.windll.user32.SystemParametersInfoW(
        SPI_SETDESKWALLPAPER,
        0,
        image_path,
        SPIF_UPDATEINIFILE | SPIF_SENDCHANGE
    )

    # Apply the style (stretch, fit, fill, etc.)
    set_wallpaper_style(style)

def set_wallpaper_style(style):
    # Define the registry key and values
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
        # Open the registry key
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, registry_path, 0, winreg.KEY_SET_VALUE) as key:
            # Set the wallpaper style value
            winreg.SetValueEx(key, value_name, 0, winreg.REG_SZ, styles[style])
            # Notify Windows of the change
            ctypes.windll.user32.SendMessageW(0xFFFF, 0x001A, 0, 0)
    except Exception as e:
        print(f"Failed to set wallpaper style: {e}")

def get_image_files(folder_path):
    # Pattern to match image files (you can add more extensions if needed)
    image_patterns = ['*.jpg', '*.jpeg', '*.png', '*.bmp', '*.gif']
    image_files = []
    for pattern in image_patterns:
        image_files.extend(glob.glob(os.path.join(folder_path, pattern)))
    return image_files

if __name__ == "__main__":
    # Replace this with the path to your folder containing image files
    folder_path = r"C:\Users\Usuario\Desktop\Sigmas\dancingdog"
    
    # Get all image files from the folder
    image_files = get_image_files(folder_path)
    
    if not image_files:
        raise ValueError("No image files found in the specified folder.")

    # Define wallpaper style (one of 'fill', 'fit', 'stretch', 'tile', 'center')
    wallpaper_style = 'stretch'  # Change this to your desired wallpaper style

    # Set the interval for changing wallpapers (in seconds)
    interval = 0.01  # Change this to your desired interval

    while True:
        for image_path in image_files:
            set_wallpaper(image_path, wallpaper_style)
            time.sleep(interval)  # Wait for the specified interval before changing the wallpaper
