import pyperclip

import dearpygui.dearpygui as dpg

from . import MenuElementsGUI
from .themes import *
from .fonts import reset_font_binding

class CallbacksGUI(MenuElementsGUI):  # Callbacks Class for the actions of the widgets

    THEMES = { # Themes constants
        "Dark Theme": dark_theme,
        "Light Theme": light_theme,
        "Default Theme": default_theme,
        "Dracula Theme": dracula_theme,
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
        reset_font_binding (None if user_data == "Default Font" else user_data)
        
# Advanced theme settings ----------------------------------------------------------------------------------------------------------------------------
    def advanced_theme_callback(self, app_data, user_data):
        dpg.show_style_editor()

# Right click context menu ---------------------------------------------------------------------------------------------------------------------------
    def right_click_context_menu(self, sender, app_data, user_data):
        def copy():
            pyperclip.copy(user_data)
            dpg.delete_item(popup)

        with dpg.window(popup=True, no_focus_on_appearing=False, no_background=True) as popup:
            dpg.add_button(label="Copy ID: " + str(user_data), callback=copy)

# Loading popup --------------------------------------------------------------------------------------------------------------------------------------
    def show_loading_popup(self, message, loading_pos, popup_tag):
        if dpg.does_item_exist(popup_tag):
            dpg.delete_item(popup_tag)
            
        with dpg.window(label="Loading", modal=True, show=True, tag=popup_tag, 
                    no_title_bar=True, no_move=True, no_resize=True):
            
            dpg.add_text(message)
            dpg.add_spacer(width=100)
            dpg.add_loading_indicator(pos= loading_pos)
            dpg.set_item_pos(popup_tag, [720,400])
            dpg.split_frame()
            
# Refresh method -------------------------------------------------------------------------------------------------------------------------------------
    def refresh(self, popup_tag):
        dpg.delete_item(popup_tag)
        self.show_loading_popup(message="Updating Vagrant environments list...", loading_pos=[177,50], popup_tag=self.TAG_POPUP_STATUS)
        self.get_vagrant_status(None, "search_machines_button")
        dpg.delete_item(self.TAG_POPUP_STATUS)