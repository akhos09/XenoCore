import os
import sys
import dearpygui.dearpygui as dpg
import ctypes
from tkinter import messagebox

from .components import MenuElementsGUI  # Correct relative import
from .components.themes import *  # Correct relative import
from .components.fonts import reset_font_binding  # Correct relative import

# Callbacks for GUI elements------------------------------------------------------------------
class CallbacksGUI(MenuElementsGUI):
    THEMES = {
        "Dark Theme": dark_theme,
        "Light Theme": light_theme,
        "Default Theme": default_theme,
        "Dracula Theme": dracula_theme,
        "CyberPunk Theme": cyberpunk_theme,
        "Dark Gruvbox Theme": gruvboxdark_theme,
        "Nyx Theme": nyx_theme
    }

    def theme_callback(self, app_data, user_data):
        theme = self.THEMES.get(user_data)
        if theme:
            dpg.bind_theme(theme())

    def font_callback(self, app_data, user_data):
        reset_font_binding(None if user_data == "Default Font" else user_data)

    def advanced_theme_callback(self, app_data, user_data):
        dpg.show_style_editor()

# Main GUI class------------------------------------------------------------------
class XenoVagrantGUI(CallbacksGUI):
    def __init__(self):
        try:
            ctypes.windll.shcore.SetProcessDpiAwareness(1)  # Enable DPI awareness for high-resolution screens
        except Exception as e:
            messagebox.showerror(title='ERROR', message=f'{e}')
        
        self.icon_path = os.path.join(os.path.dirname(__file__), "../assets/img/test.ico")
        if not os.path.exists(self.icon_path):
            messagebox.showerror(title='ERROR', message='Assets folder not found. Make sure it exists inside src folder.')
            sys.exit(1)

# Main function
def main():
    try:
        app = XenoVagrantGUI()
        app.menu()
    finally:
        dpg.destroy_context()

if __name__ == "__main__":
    main()
