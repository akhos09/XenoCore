import os
import sys
from tkinter import messagebox

import ctypes

from .components import MenuElementsGUI
from .components.core import CallbacksCore
from .components.gui_core import CallbacksGUI
from .components.themes import *
from .components.fonts import reset_font_binding

# Main GUI class (Screen and Icon settings)------------------------------------------------------------------
class XenoVagrantGUI(CallbacksGUI, CallbacksCore):
    def __init__(self):
        try:
            ctypes.windll.shcore.SetProcessDpiAwareness(1)  # Enable DPI awareness for high-resolution screens
        except Exception as e:
            messagebox.showerror(title='ERROR', message=f'DPI Awareness could not be set. Contact @akhos09 or open an issue in the repo.\n\n{e}')
        
        self.icon_path = os.path.join(os.path.dirname(__file__), "../assets/img/test.ico")
        if not os.path.exists(self.icon_path):
            messagebox.showerror(title='ERROR', message='Assets folder not found. Make sure it exists inside src folder.')
            sys.exit(1)

# Main function------------------------------------------------------------------
def main():
    try:
        app = XenoVagrantGUI()
        app.menu()
    finally:
        dpg.destroy_context()

if __name__ == "__main__":
    main()