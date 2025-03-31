import dearpygui.dearpygui as dpg 
from assets.themes import * 
from assets.fonts import *
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
    
    def advanced_theme_settings(self, app_data, user_data):
            dpg.show_style_editor()    

    def menu(self):
        dpg.create_context()
        load_fonts()
        dpg.bind_font(fonts["Default"])
        
        dpg.create_viewport(
            title="XenoVagrant", 
            width=1280, 
            height=720,
            small_icon=self.icon_path,
            large_icon=self.icon_path,
        )
        with dpg.window(tag="main_window"):
            with dpg.tab_bar(tag="tab_bar"):
                with dpg.tab(label="Machines", tag="machines"):
                    with dpg.child_window(label="machineswin", use_internal_label=True, border=True, auto_resize_x=True, auto_resize_y=True):
                        dpg.add_text("Machines Management")
                
                with dpg.tab(label="Plugins", tag="plugins"):
                    with dpg.child_window(label="pluginswin", use_internal_label=True, border=True, auto_resize_x=True, auto_resize_y=True):
                        with dpg.group(horizontal=True):
                            dpg.add_text("Plugins Management")
                
                with dpg.tab(label="Help", tag="help"):
                    with dpg.child_window(label="helpwin", use_internal_label=True, border=True, auto_resize_x=True, auto_resize_y=True):
                        with dpg.group(horizontal=True):
                            dpg.add_text("Help Section")
                
                with dpg.tab(label="About", tag="about"):
                    with dpg.child_window(label="aboutwin", use_internal_label=True, border=True, auto_resize_x=True, auto_resize_y=True):
                        with dpg.group(horizontal=True):
                            dpg.add_text("About XenoVagrant")
                
                with dpg.tab(label="Settings", tag="settings"):
                    with dpg.child_window(label="settingswin", use_internal_label=True, border=True,auto_resize_x=True,auto_resize_y=True):
                        with dpg.group(horizontal=True):
                            with dpg.group(horizontal=False):
                                dpg.add_combo(
                                    label="Theme Selector",
                                    items=["Default Theme","Dark Theme", "Light Theme", "Dracula Theme", "CyberPunk Theme", "Dark Gruvbox Theme", "Nyx Theme"], 
                                    callback=self.theme_callback,
                                    default_value="Default Theme",
                                    width=300,
                                    tag="theme_selector"
                                )
                                dpg.add_combo(
                                    label="Font Selector",
                                    items=["Default Font", "Conthrax-SemiBold", "Average-Regular"], 
                                    callback=self.font_callback,
                                    default_value="Default Font",
                                    width=300,
                                    tag="font_selector"
                                )
                            dpg.add_spacer(width=435)
                            dpg.add_button(label="Appearance Advanced Settings", tag="theme_advance_settings")
                            with dpg.popup(tag="theme_settings_alert",modal=False, mousebutton=0,parent=dpg.last_item(),min_size=[150,150]):
                                dpg.set_item_pos(dpg.last_item(),pos=[250,100])
                                dpg.add_spacer(height=20)
                                dpg.add_text("Be careful with these settings. They could break the appearance of the app.")
                                dpg.add_spacer(height=30)
                                dpg.add_separator()
                                dpg.add_spacer(width=100,height=80)
                                dpg.add_button(label="Go to Default Theme Settings", tag="theme_settings",callback=self.advanced_theme_settings)    
                                dpg.set_item_pos(dpg.last_item(),pos=[250,130])
        dpg.set_primary_window("main_window", True)
        dpg.setup_dearpygui()
        dpg.show_viewport()
        dpg.start_dearpygui()

def main():
    try:
        app = XenoVagrantGUI()
        app.menu()
    finally:
        dpg.destroy_context()

if __name__ == "__main__":
    main()