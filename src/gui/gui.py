import os
import sys
import shutil
from tkinter import messagebox

import ctypes
import dearpygui.dearpygui as dpg

from .components.menu import MenuElementsGUI
from .components.themes import *

class XenoCoreGUI(MenuElementsGUI):    
# ------- Sets DPI Awareness for high resolution screens and checks if the assets folder is in the right path ------- 
    def __init__(self):
        super().__init__()
        if sys.platform == "win32":
            try:
                ctypes.windll.shcore.SetProcessDpiAwareness(1)
            except Exception as e:
                self.show_topmost_messagebox(title='ERROR', message=f'DPI Awareness could not be set.\n\n{e}', error=True)

        self.icon_path = os.path.join(os.path.dirname(__file__), "../assets/img/app_icon.ico")
        if not os.path.exists(self.icon_path):
            self.show_topmost_messagebox(title='ERROR', message='Assets folder not found. Make sure it exists inside the src folder.', error=True)
            sys.exit(1)

# ------- Entrypoint of the app (checks if Vagrant is in the system and executes the GUI) -------
def main():
    if not shutil.which("vagrant"):
        messagebox.showerror(title='ERROR', message='Vagrant is not installed. Ensure is installed and registered in the PATH.')
        sys.exit(1)
        
    try:
        app = XenoCoreGUI()
        app.menu()
    finally:
        dpg.destroy_context()