import os
import sys

import dearpygui.dearpygui as dpg
import ctypes
from tkinter import messagebox

from . import MenuElementsGUI
from .themes import *
from .fonts import reset_font_binding

class CallbacksGUI(MenuElementsGUI): # Callbacks Class for the actions of the widgets------------------------------------------
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