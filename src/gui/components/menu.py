import dearpygui.dearpygui as dpg

import webbrowser

from .themes import *
from .fonts import *

class MenuElementsGUI: #Elements from GUI--------------------------------------------------------------------------------
    def initial_settings(self): #Initial settings(viewport)--------------------------------------------------------------------------------
        dpg.create_context()
        dpg.create_viewport(
            title="XenoVagrant", 
            width=1280, 
            height=720,
            small_icon=self.icon_path,
            large_icon=self.icon_path,
            decorated=True
        )

    def gui_components(self): #Components and structure--------------------------------------------------------------------------------
        
        with dpg.window(tag="main_window"): #Main Window--------------------------------------------------
            
            with dpg.tab_bar(tag="tab_bar"): #Machines Tab--------------------------------------------------
                with dpg.tab(label="Machines", tag="machines"):
                    with dpg.child_window(label="machineswin", use_internal_label=True, border=True, auto_resize_x=True, auto_resize_y=True):
                        dpg.add_text("Machines Management")
                
                with dpg.tab(label="Plugins", tag="plugins"): #Plugins Tab--------------------------------------------------
                    with dpg.child_window(label="pluginswin", use_internal_label=True, border=True, auto_resize_x=True, auto_resize_y=True):
                        with dpg.group(horizontal=True):
                            dpg.add_text("Plugins Management")
                
                with dpg.tab(label="Other", tag="other"): #Other Tab--------------------------------------------------
                    with dpg.child_window(label="otherwin", use_internal_label=True, border=True, auto_resize_x=False, auto_resize_y=False):
                        with dpg.group(horizontal=False):
                            with dpg.tab_bar():
                                with dpg.tab(label="Help", tag="help_tab"):
                                    with dpg.child_window(autosize_x=True, autosize_y=True):
                                        
                                        with dpg.collapsing_header(label="Troubleshooting"):
                                            with dpg.tree_node(label="Connection Problems"):
                                                dpg.add_text("Check network settings", bullet=True)
                                                dpg.add_text("Verify credentials", bullet=True)
                                            
                                            with dpg.tree_node(label="Performance Issues"):
                                                dpg.add_text("Reduce concurrent operations", bullet=True)
                                                dpg.add_text("Allocate more resources", bullet=True)
                                        

                                        with dpg.collapsing_header(label="Support"):
                                            dpg.add_text("For additional help:", bullet=True)
                                            
                                            with dpg.group(horizontal=True):
                                                dpg.add_text("GitHub Issues:", bullet=True)
                                                dpg.add_button(
                                                    label="Open Issue",
                                                    callback=lambda: webbrowser.open("https://github.com/akhos09/XenoVagrant/issues"),
                                                    width=135
                                                )

                                            dpg.add_text("Email: discordpbl09@gmail.com", bullet=True)
                                            dpg.add_text("Discord: pabi09", bullet=True)
                                        
                                with dpg.tab(label="About"):
                                    with dpg.collapsing_header(label="Quick Start Guide"):
                                        dpg.add_text("1. Configure your settings in the Settings tab", bullet=True)
                                        dpg.add_text("2. Add new machines in the Machines tab", bullet=True)
                                        dpg.add_text("3. Manage plugins in the Plugins tab", bullet=True)
                                        dpg.add_text("4. Use the status bar to monitor operations", bullet=True)

                                    with dpg.collapsing_header(label="Application Overview"):
                                        dpg.add_text("Version: 1.0.0", bullet=True)
                                        dpg.add_text("License: Apache License 2.0", bullet=True)
                                        dpg.add_text("Author: @akhos09", bullet=True)

                                        with dpg.group(horizontal=True):
                                            dpg.add_text("Documentation:", bullet=True)
                                            dpg.add_button(
                                                label="GitHub README",
                                                callback=lambda: webbrowser.open("https://github.com/akhos09/XenoVagrant/blob/main/README.md"),
                                                width=180
                                            )
                                            
                                with dpg.tab(label="Appearance"):
                                    with dpg.child_window(label="appearancetab", use_internal_label=True, border=True, auto_resize_x=False, auto_resize_y=False):
                                        with dpg.group(horizontal=False):
                                            with dpg.group(horizontal=False):
                                                dpg.add_combo(
                                                    label="  Theme Selector",
                                                    items=["Default Theme", 
                                                            "Dark Theme", 
                                                            "Light Theme", 
                                                            "Dracula Theme", 
                                                            "CyberPunk Theme", 
                                                            "Dark Gruvbox Theme", 
                                                            "Nyx Theme"
                                                            ], 
                                                    callback=self.theme_callback,
                                                    default_value="Default Theme",
                                                    width=300,
                                                    tag="theme_selector"
                                                )
                                                
                                                dpg.add_combo(
                                                    label="  Font Selector",
                                                    items=["Default Font", 
                                                            "Conthrax-SemiBold", 
                                                            "Average-Regular"
                                                            ], 
                                                    callback=self.font_callback,
                                                    default_value="Default Font",
                                                    width=300,
                                                    tag="font_selector"
                                                )
                                                
                                                dpg.add_button(label="Advanced Appearance Settings", tag="theme_advance_settings")
                                            
                                            with dpg.popup(tag="theme_settings_alert", modal=False, mousebutton=0, parent=dpg.last_item(), min_size=[150,150], no_move=True):
                                                dpg.set_item_pos(dpg.last_item(), pos=[250,100])
                                                dpg.add_spacer(height=20)
                                                dpg.add_text("Be careful with these settings. They could break the appearance of the app.")
                                                dpg.add_spacer(height=30)
                                                dpg.add_separator()
                                                dpg.add_spacer(width=100, height=80)
                                                dpg.add_button(label="Go to Default Theme Settings", tag="theme_settings", callback=self.advanced_theme_callback)    
                                                dpg.set_item_pos(dpg.last_item(), pos=[250,130])
        
    def final_setup_menu(self): #Final setup--------------------------------------------------
        load_fonts()
        dpg.bind_font(fonts["Default"])
        dpg.bind_theme(default_theme())
        dpg.set_primary_window("main_window", True)                    
        dpg.setup_dearpygui()
        dpg.show_viewport()
        dpg.start_dearpygui()
    
    def menu(self): #Menu startup--------------------------------------------------
        self.initial_settings()
        self.gui_components()
        self.final_setup_menu()
        

