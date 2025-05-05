import platform
import subprocess
from tkinter import filedialog as fd
from tkinter import Tk, messagebox

import dearpygui.dearpygui as dpg
import pyperclip

from .themes import default_theme, dark_theme, light_theme, cyberpunk_theme, gruvboxdark_theme, nyx_theme
from .fonts import reset_font_binding
from .constants import TagsCoreGUI

class CallbacksGUI(TagsCoreGUI):

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

# Unified right click context menu-----------------------------------------------------------------------------------
    def show_loading_popup(self, message, loading_pos, popup_tag):
        if dpg.does_item_exist(popup_tag):
            dpg.delete_item(popup_tag)

        with dpg.window(label="Loading", modal=True, show=True, tag=popup_tag,
                        no_title_bar=True, no_move=True, no_resize=True, autosize=True):
            dpg.add_text(message)
            dpg.add_spacer(width=100)
            dpg.add_loading_indicator(pos=loading_pos)
            dpg.set_item_pos(popup_tag, [720, 400])
            dpg.split_frame()
            
# Unified right click context menu-----------------------------------------------------------------------------------
    def refresh(self, popup_tag):
        dpg.delete_item(popup_tag)
        self.show_loading_popup(message="Updating Vagrant environments list...", loading_pos=[177, 50], popup_tag=self.POPUP_STATUS_TAG)
        self.get_vagrant_status(None, "search_machines_btn")
        dpg.delete_item(self.POPUP_STATUS_TAG)
        
# Unified right click context menu-----------------------------------------------------------------------------------
    def tooltip(self, text):
        with dpg.tooltip(parent=dpg.last_item(), hide_on_activity=True):
            dpg.add_text(text)
            
# Unified right click context menu-----------------------------------------------------------------------------------
    def select_folder(self, text):
        root = Tk()
        root.withdraw()
        root.wm_attributes("-topmost", 1)
        try:
            messagebox.showinfo(title='INFO', message=f'{text}')
            folder_selected = fd.askdirectory(title=f"{text}")
            return folder_selected
        finally:
            root.destroy()
            
# Unified right click context menu-----------------------------------------------------------------------------------
    def show_topmost_messagebox(self, title, message, error=False):
        root = Tk()
        root.withdraw()
        root.wm_attributes("-topmost", 1)

        if error:
            messagebox.showerror(title, message, parent=root)
        else:
            messagebox.showinfo(title, message, parent=root)

        root.destroy()

# Unified right click context menu-----------------------------------------------------------------------------------
    def right_click_context_menu(self, sender, app_data, user_data, menu_type):
        def copy():
            pyperclip.copy(user_data)
            dpg.delete_item("right_click_popup")

        def connect(user_data):
            try:
                if platform.system() == "Windows":
                    # Windows: Use PowerShell to run the Vagrant SSH command
                    cmd = f'start powershell -NoExit -Command "$Env:VAGRANT_PREFER_SYSTEM_BIN=0; vagrant ssh {user_data}"'
                else:
                    # Linux/Mac: Just run the Vagrant SSH command
                    cmd = f"vagrant ssh {user_data}"

                subprocess.run(cmd, shell=True, check=True)
            
            except subprocess.CalledProcessError as e:
                self.show_topmost_messagebox(title='ERROR', message=f"Failed to connect to the environment (Vagrant error): {e}", error=True)
            except Exception as e:
                self.show_topmost_messagebox(title='ERROR', message=f"Unexpected error: {str(e)}", error=True)

        def uninstall():
            self.uninstall_vagrant_plg(user_data)
        
        def update():
            self.update_vagrant_plg(user_data)
        
        def repair():
            self.repair_vagrant_plg(user_data)

        if dpg.does_item_exist("right_click_popup"):
            dpg.delete_item("right_click_popup")

        with dpg.window(tag="right_click_popup", popup=True, no_focus_on_appearing=False,
                        height=120 if menu_type == "plugin" else 90, width=130, no_background=False):
            dpg.add_button(label="Copy " + str(user_data), callback=copy)

            if menu_type == "env":
                dpg.add_button(label="Connect " + str(user_data), callback=connect)
            elif menu_type == "plugin":
                dpg.add_button(label="Uninstall " + str(user_data), callback=uninstall)
                dpg.add_button(label="Update " + str(user_data), callback=update)
                dpg.add_button(label="Repair " + str(user_data), callback=repair)

# Aliases for the right click context menus--------------------------------------------------------------
    def env_right_click_context_menu(self, sender, app_data, user_data):
        self.right_click_context_menu(sender, app_data, user_data, menu_type="env")

    def plg_right_click_context_menu(self, sender, app_data, user_data):
        self.right_click_context_menu(sender, app_data, user_data, menu_type="plugin")
