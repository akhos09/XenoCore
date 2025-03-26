import dearpygui.dearpygui as dpg 
from assets.themes import * 
import ctypes
import os
import sys

class XenoVagrantGUI:
    def __init__(self):
        try:
            ctypes.windll.shcore.SetProcessDpiAwareness(1)
        except:
            print("Could not set DPI awareness. Check help or about and contact @akhos09")
        
        self.icon_path = "./assets/test.ico"
        if not os.path.exists(self.icon_path):
            print(f"""
                  Icon file not found: {self.icon_path}
                  Make sure you execute the app inside his folder.
                  """)
            sys.exit(1)
    
    def theme_callback(self, app_data, user_data):
        dark_theme = create_theme_imgui_dark()
        light_theme = create_theme_imgui_light()
        if user_data == "Light Theme":
            dpg.bind_theme(light_theme)
        elif user_data=="Dark Theme":
            dpg.bind_theme(dark_theme)
        else:
            dpg.bind_theme(None)
            pass    

    def menu(self):
        dpg.create_context()
        dpg.create_viewport(title="XenoVagrant", width=1280, height=720,small_icon=self.icon_path,large_icon=self.icon_path)
        
        with dpg.window(tag="main_window"):
            dpg.add_combo(
            label="Theme Selector",
            items=["Default Theme","Dark Theme", "Light Theme"], 
            callback=self.theme_callback,
            default_value="Default Theme",
            width=200,
            tag="theme_selector"
        )
        
        dpg.set_primary_window("main_window", True)
        
        dpg.setup_dearpygui()
        dpg.show_viewport()
        dpg.start_dearpygui()

if __name__ == "__main__":
    app = XenoVagrantGUI()
    app.menu()
    dpg.destroy_context()