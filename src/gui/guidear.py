import dearpygui.dearpygui as dpg 
from src.gui.assets.themes import * 
import ctypes
import os
import sys

class XenoVagrantGUI:
    def __init__(self):
        try:
            ctypes.windll.shcore.SetProcessDpiAwareness(1)
        except:
            print("Could not set DPI awareness. Check help or about and contact @akhos09")
        
        self.icon_path = "test.ico"
        if not os.path.exists(self.icon_path):
            print(f"Icon file not found: {self.icon_path}")
            sys.exit(1)
    
    def theme_callback(self, app_data, user_data):
        dark_theme = create_theme_imgui_dark()
        light_theme = create_theme_imgui_light()
        if user_data == "Light Mode":
            dpg.bind_theme(light_theme)
        elif user_data=="Black Mode":
            dpg.bind_theme(dark_theme)
        else:
            pass    

    def menu(self):
        dpg.create_context()
        dpg.create_viewport(title="XenoVagrant", width=1280, height=720)
        
        dpg.set_viewport_small_icon(self.icon_path)
        dpg.set_viewport_large_icon(self.icon_path)
        
        with dpg.window(tag="App"):
            dpg.add_combo(
            label="Theme Selector",
            items=["Black Mode", "Light Mode"], 
            default_value="Black Mode",
            callback=self.theme_callback,
            width=200,
            tag="theme_selector"
        )
        
        dpg.set_primary_window("App", True)
        
        dpg.setup_dearpygui()
        dpg.show_viewport()
        dpg.start_dearpygui()

if __name__ == "__main__":
    app = XenoVagrantGUI()
    app.menu()
    dpg.destroy_context()