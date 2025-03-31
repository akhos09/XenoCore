import os
import sys

import dearpygui.dearpygui as dpg
import ctypes

from assets import *

#Callbacks for GUI elements------------------------------------------------------------------
class CallbacksGUI(MenuElementsGUI):
    
    def theme_callback(self, app_data, user_data, themes):
        themes = {
            "Dark Theme": dark_theme,
            "Light Theme": light_theme,
            "Default Theme": default_theme,
            "Dracula Theme": dracula_theme,
            "CyberPunk Theme": cyberpunk_theme,
            "Dark Gruvbox Theme": gruvboxdark_theme,
            "Nyx Theme": nyx_theme
        }
        
        theme = themes.get(user_data)
        if theme:
            dpg.bind_theme(theme())

    def font_callback(self, app_data, user_data):
        if user_data == "Default Font":
            reset_font_binding()
        elif user_data in fonts:
            reset_font_binding(user_data)

    def advanced_theme_callback(self, app_data, user_data):
        dpg.show_style_editor()

# Main GUI class------------------------------------------------------------------
class XenoVagrantGUI(CallbacksGUI):
    def __init__(self):
        try:
            ctypes.windll.shcore.SetProcessDpiAwareness(1)  # Enable DPI awareness for high-resolution screens
        except:
            print("Could not set DPI awareness. Check help or about and contact @akhos09")
        
        self.icon_path = "./assets/test.ico"
        if not os.path.exists(self.icon_path):
            print(f"""
                  Icon file not found: {self.icon_path}
                  Make sure you execute the app inside its folder.
                  """)
            sys.exit(1)

#Main function--------------------------------------------------------------------------------
def main():
    try:
        app = XenoVagrantGUI()
        app.menu()
    finally:
        dpg.destroy_context()

if __name__ == "__main__":
    main()