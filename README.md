# Wallpaper Slideshow Application

## Overview

The Wallpaper Slideshow Application is a Python-based tool that allows you to create a slideshow of images or GIF frames as your desktop wallpaper on Windows. You can choose the folder containing your images, specify a temporary folder for GIF frames, set your desired wallpaper style, and adjust the interval between changes.

## Features

- Supports various image formats: JPG, JPEG, PNG, BMP, and GIF.
- Extracts and displays frames from GIFs as individual images.
- Allows you to set different wallpaper styles: Fill, Fit, Stretch, Tile, Center.
- Configurable slideshow interval.

## Requirements

- Python 3.x
- Required Python packages:
  - `ctypes`
  - `os`
  - `time`
  - `random`
  - `glob`
  - `PIL` (Pillow)
  - `winreg`
  - `tkinter`

## Installation

1. **Install Python**: Make sure you have Python 3.x installed on your system. You can download it from [python.org](https://www.python.org/downloads/).

2. **Install Required Packages**: You need to install the Pillow library. You can do this via pip:

    ```sh
    pip install pillow
    ```

3. **Download the Script**: Save the script provided as `wallpaper_slideshow.py` to your local machine.

## Usage

1. **Run the Script**: Execute the script using Python. Open a command prompt and run:

    ```sh
    python wallpaper_slideshow.py
    ```

2. **Configure Settings**:
    - **Folder Path**: Select the folder containing your image files.
    - **Temporary Folder for GIF Frames**: Choose a temporary folder where GIF frames will be extracted.
    - **Wallpaper Style**: Choose the style for the wallpaper.
    - **Interval (seconds)**: Specify the time interval between wallpaper changes.

3. **Start Slideshow**: Click the "Start Slideshow" button to begin the wallpaper slideshow.

## Troubleshooting

- **Error: No image files found in the specified folder.**
  - Ensure the folder path is correct and contains image files.
  - Verify the supported image formats.

- **Error: Invalid interval. Please enter a number.**
  - Ensure you are entering a valid numeric value for the interval.

- **Wallpaper does not change.**
  - Verify the `temp_folder` exists and has write permissions.
  - Check if the `set_wallpaper_style` function correctly updates the wallpaper style.

## Notes

- The application is designed to work on Windows systems.
- Ensure you have permissions to change the desktop wallpaper and write to the temporary folder.
