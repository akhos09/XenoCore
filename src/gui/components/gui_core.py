import pyperclip
import subprocess
from tkinter import filedialog as fd
from tkinter import Tk
from tkinter import messagebox

import dearpygui.dearpygui as dpg

from .menu import MenuElementsGUI
from .plg_core import CallbacksCorePlg
from .env_core import CallbacksCoreEnv
from .themes import default_theme, dark_theme, light_theme, cyberpunk_theme, gruvboxdark_theme, nyx_theme
from .fonts import reset_font_binding

class CallbacksGUI(MenuElementsGUI):  # Callbacks Class for the actions of the widgets

    THEMES = { # Themes constants
        "Dark Theme": dark_theme,
        "Light Theme": light_theme,
        "Default Theme": default_theme,
        "CyberPunk Theme": cyberpunk_theme,
        "Dark Gruvbox Theme": gruvboxdark_theme,
        "Nyx Theme": nyx_theme
    }

# Themes selector-------------------------------------------------------------------------------------------------------------------------------------
    def theme_callback(self, app_data, user_data): 
        theme = self.THEMES.get(user_data)
        if theme:
            dpg.bind_theme(theme())
            
# Fonts selector--------------------------------------------------------------------------------------------------------------------------------------
    def font_callback(self, app_data, user_data): 
        reset_font_binding (None if user_data == "Default Theme" else user_data)
        
# Advanced theme settings ----------------------------------------------------------------------------------------------------------------------------
    def advanced_theme_callback(self, app_data, user_data):
        dpg.show_style_editor()

# Loading popup --------------------------------------------------------------------------------------------------------------------------------------
    def show_loading_popup(self, message, loading_pos, popup_tag):
        if dpg.does_item_exist(popup_tag):
            dpg.delete_item(popup_tag)
            
        with dpg.window(label="Loading", modal=True, show=True, tag=popup_tag, 
                    no_title_bar=True, no_move=True, no_resize=True,autosize=True):
            
            dpg.add_text(message)
            dpg.add_spacer(width=100)
            dpg.add_loading_indicator(pos= loading_pos)
            dpg.set_item_pos(popup_tag, [720,400])
            dpg.split_frame()
            
# Refresh method -------------------------------------------------------------------------------------------------------------------------------------
    def refresh(self, popup_tag):
        dpg.delete_item(popup_tag)
        self.show_loading_popup(message="Updating Vagrant environments list...", loading_pos=[177,50], popup_tag=self.POPUP_STATUS_TAG)
        self.get_vagrant_status(None, "search_machines_btn")
        dpg.delete_item(self.POPUP_STATUS_TAG)
        
# Tooltip method -------------------------------------------------------------------------------------------------------------------------------------
    def tooltip(self, text):
        with dpg.tooltip(parent=dpg.last_item(), hide_on_activity=True):
            dpg.add_text(text)
            
# Select folder method -------------------------------------------------------------------------------------------------------------------------------    
    def select_folder(self, text):
        root = Tk()
        root.withdraw()
        root.wm_attributes("-topmost", 1)
        
        try:
            messagebox.showinfo(title='INFO', 
            message=f'{text}')
            folder_selected = fd.askdirectory(title=f"{text}")
            return folder_selected
        finally:
            root.destroy()
            
# Topmost messagebox method --------------------------------------------------------------------------------------------------------------------------                
    def show_topmost_messagebox(self, title, message, error=False):
        root = Tk()
        root.withdraw() 
        root.wm_attributes("-topmost", 1)
        
        if error:
            messagebox.showerror(title, message, parent=root)
        else:
            messagebox.showinfo(title, message, parent=root)
        
        root.destroy()
        
# Env Right click context menu ---------------------------------------------------------------------------------------------------------------------------
    def env_right_click_context_menu(self, sender, app_data, user_data):
        def copy():
            pyperclip.copy(user_data)
            dpg.delete_item("right_click_popup")

        def connect():
            try:
                cmd = f'start powershell -NoExit -Command "$Env:VAGRANT_PREFER_SYSTEM_BIN=0; vagrant ssh {user_data}"'
                subprocess.run(cmd, shell=True, check=True)
            except subprocess.CalledProcessError as e:
                messagebox.showerror("Error", f"Failed to connect to the environment (Vagrant error): {e}")
            except Exception as e:
                messagebox.showerror("Error", f"Unexpected error: {str(e)}")

        if dpg.does_item_exist("right_click_popup"):
            dpg.delete_item("right_click_popup")

        with dpg.window(tag="right_click_popup", popup=True, no_focus_on_appearing=False, height=90, width=100,no_background=False):
            dpg.add_button(label="Copy " + str(user_data), callback=copy)
            dpg.add_button(label="Connect " + str(user_data), callback=connect)    
    
# Plugins Right click context menu ---------------------------------------------------------------------------------------------------------------------------
    def plg_right_click_context_menu(self, sender, app_data, user_data):
        def copy():
            pyperclip.copy(user_data)
            dpg.delete_item("right_click_popup")

        def connect():
            try:
                cmd = f'start powershell -NoExit -Command "$Env:VAGRANT_PREFER_SYSTEM_BIN=0; vagrant ssh {user_data}"'
                subprocess.run(cmd, shell=True, check=True)
            except subprocess.CalledProcessError as e:
                messagebox.showerror("Error", f"Failed to connect to the environment (Vagrant error): {e}")
            except Exception as e:
                messagebox.showerror("Error", f"Unexpected error: {str(e)}")

        if dpg.does_item_exist("right_click_popup"):
            dpg.delete_item("right_click_popup")

        with dpg.window(tag="right_click_popup", popup=True, no_focus_on_appearing=False, height=90, width=100,no_background=False):
            dpg.add_button(label="Uninstall " + str(user_data), callback=self.uninstall_vagrant_plg, user_data=user_data)
            dpg.add_button(label="Update " + str(user_data), callback=connect)   
            dpg.add_button(label="Repair "+ str(user_data), callback=connect)