import platform
import subprocess
import threading
from tkinter import filedialog as fd
from tkinter import Tk, messagebox

import dearpygui.dearpygui as dpg

from .themes import default_theme, dark_theme, light_theme, cyberpunk_theme, gruvboxdark_theme, nyx_theme
from .fonts import reset_font_binding
from .constants import TagsCoreGUI

class CallbacksGUI(TagsCoreGUI):
    
    ENV_DIS_ITEMS = [TagsCoreGUI.PACK_ENV_BTN_TAG, TagsCoreGUI.SEARCH_MACHINES_BTN_TAG, TagsCoreGUI.FOLDER_SELECTION_BTN_TAG]
    ENV_HID_ITEMS =  [TagsCoreGUI.PLUGINS_TAB, TagsCoreGUI.OTHER_TAB, TagsCoreGUI.ENV_HELP_RCLK_TAG]
    
    THEMES = {
        "Dark Theme": dark_theme,
        "Light Theme": light_theme,
        "Default Theme": default_theme,
        "CyberPunk Theme": cyberpunk_theme,
        "Dark Gruvbox Theme": gruvboxdark_theme,
        "Nyx Theme": nyx_theme
    }
    
# Theme selector -----------------------------------------------------------------------------------
    def theme_callback(self, app_data, user_data):
        theme = self.THEMES.get(user_data)
        if theme:
            dpg.bind_theme(theme())
            
# Font selector ------------------------------------------------------------------------------------
    def font_callback(self, app_data, user_data):
        reset_font_binding(None if user_data == "Default Theme" else user_data)
        
# Advanced theme selector --------------------------------------------------------------------------
    def advanced_theme_callback(self, app_data, user_data):
        check_settings = messagebox.askokcancel("INFO",
        f"This menu could break the appeareance of the app. Are you sure to continue?")
        
        if check_settings:
            dpg.show_style_editor()

# Show tooltip function -----------------------------------------------------------------------------------
    def tooltip(self, text):
        with dpg.tooltip(parent=dpg.last_item(), hide_on_activity=True):
            dpg.add_text(text)
            
# Select folder function ----------------------------------------------------------------------------------
    def select_folder(self, text="Select a folder"):

        result = {"path": None}

        def run_dialog():
            try:
                root = Tk()
                root.withdraw()
                result["path"] = fd.askdirectory(title=text, parent=root)
            finally:
                root.destroy()

        thread = threading.Thread(target=run_dialog)
        thread.start()
        thread.join()
        
        return result["path"]
            
# Topmost Tk messagebox -----------------------------------------------------------------------------------
    def show_topmost_messagebox(self, title, message, error=False):
        def run_messagebox():
            try:
                root = Tk()
                root.withdraw()
                root.wm_attributes("-topmost", 1)

                if error:
                    messagebox.showerror(title, message, parent=root)
                else:
                    messagebox.showinfo(title, message, parent=root)
            finally:
                try:
                    root.destroy()
                except:
                    pass

        thread = threading.Thread(target=run_messagebox)
        thread.start()
        
    def ask_save_path(self, default_name="output.box"):
        def run_dialog():
            try:
                root = Tk()
                root.withdraw()
                root.wm_attributes("-topmost", 1)

                path = fd.asksaveasfilename(
                    title="Save .box file",
                    defaultextension=".box",
                    initialfile=default_name,
                    filetypes=[("Vagrant Box", "*.box")]
                )
                self.save_path = path  # store result
            finally:
                try:
                    root.destroy()
                except:
                    pass

        thread = threading.Thread(target=run_dialog)
        thread.start()
        thread.join()
        return getattr(self, "save_path", None)


# Unified right click context menu-----------------------------------------------------------------------------------
    def right_click_context_menu(self, sender, app_data, user_data, menu_type):
                
        if dpg.does_item_exist("right_click_popup"):
            dpg.delete_item("right_click_popup")

        with dpg.window(tag="right_click_popup", popup=True, no_focus_on_appearing=False,
                        height=120 if menu_type == "plugin" else 90, width=130, no_background=False):

            if menu_type == "env":
                dpg.add_button(label="Start " + str(user_data), callback=self.start_vagrant_env, user_data=user_data)
                dpg.add_button(label="Stop " + str(user_data), callback=self.stop_vagrant_env, user_data=user_data)
                dpg.add_button(label="Reload " + str(user_data), callback=self.reload_vagrant_env, user_data=user_data)
                dpg.add_button(label="Delete " + str(user_data), callback=self.delete_vagrant_env, user_data=user_data)
                dpg.add_button(label="Connect " + str(user_data), callback=self.connect_vagrant_env, user_data=user_data)

                
            elif menu_type == "plugin":
                pass
                # dpg.add_button(label="Uninstall " + str(user_data), callback=uninstall)
                # dpg.add_button(label="Update " + str(user_data), callback=update)
                # dpg.add_button(label="Repair " + str(user_data), callback=repair)

# Disable gui env ----------------------------------------------------------------------------------------------------
    def env_disable_gui (self,text,text_tag):
        dpg.add_text(f'{text}', color=[255, 255, 0], parent=self.OPTIONS_ENV_TAG, tag=text_tag)
        
        for i in self.ENV_HID_ITEMS:
            dpg.hide_item(i)
            
        for i in self.ENV_DIS_ITEMS:
            dpg.disable_item(i)
            
    def env_enable_gui (self, text_tag):
        dpg.delete_item(text_tag)
        self.get_vagrant_status(None, "search_machines_btn")
        
        for i in self.ENV_HID_ITEMS:    
            dpg.show_item(i)
            
        for i in self.ENV_DIS_ITEMS:

            dpg.enable_item(i)
# Disable gui plgs ----------------------------------------------------------------------------------------------------
    def plg_disable_gui (self,text,text_tag):
        dpg.add_text(f'{text}', color=[255, 255, 0], parent=self.OPTIONS_ENV_TAG, tag=text_tag)
        
        for i in self.ENV_HID_ITEMS:
            dpg.hide_item(i)
            
        for i in self.ENV_DIS_ITEMS:
            dpg.disable_item(i)
            
    def plg_enable_gui (self, text_tag):
        dpg.delete_item(text_tag)
        self.get_vagrant_status(None, "search_machines_btn")
        
        for i in self.ENV_HID_ITEMS:    
            dpg.show_item(i)
            
        for i in self.ENV_DIS_ITEMS:
            dpg.enable_item(i)