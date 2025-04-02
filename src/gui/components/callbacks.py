import os
import sys
import subprocess

import dearpygui.dearpygui as dpg
import ctypes
from tkinter import messagebox

from . import MenuElementsGUI
from .themes import *
from .fonts import reset_font_binding

class CallbacksGUI(MenuElementsGUI): # Callbacks Class for the actions of the widgets------------------------------------------
    TABLE_TAG = "vagrant_table"
    POPUP_TAG = "searching_machines"
    TEMPWIN_TAG = "table_tempwin"
    THEMES = {
        "Dark Theme": dark_theme,
        "Light Theme": light_theme,
        "Default Theme": default_theme,
        "Dracula Theme": dracula_theme,
        "CyberPunk Theme": cyberpunk_theme,
        "Dark Gruvbox Theme": gruvboxdark_theme,
        "Nyx Theme": nyx_theme
    }

    def theme_callback(self, app_data, user_data): # Theme selector----------------------------------------------------------------------
        theme = self.THEMES.get(user_data)
        if theme:
            dpg.bind_theme(theme())

    def font_callback(self, app_data, user_data): # Font selector----------------------------------------------------------------------
        reset_font_binding(None if user_data == "Default Font" else user_data)

    def advanced_theme_callback(self, app_data, user_data): # Advanced Settings----------------------------------------------------------------------
        dpg.show_style_editor()

    def get_vagrant_status(self, app_data, user_data): # Machines List Table-----------------------------
        with dpg.window(label="Loading", modal=True, show=False, tag=self.POPUP_TAG, no_title_bar=True, no_move=True, no_resize=True):
            dpg.add_text("Searching for Vagrant environments...")
            dpg.add_spacer(width=100)
            dpg.add_loading_indicator(pos=[170,50])
            dpg.set_item_pos(self.POPUP_TAG, [720,400])
            dpg.show_item(self.POPUP_TAG)
        try:                
            command_status = subprocess.run(["vagrant", "global-status"], capture_output=True, text=True)
        except Exception as e:
            messagebox.showerror(title='ERROR', message=f'Machines on your system could not be found. Make sure Vagrant is installed\n\n{e}')
            return
        
        
        dpg.delete_item(self.POPUP_TAG)
            
        # Process output into a list of dictionaries---------------------------------------------------------------------------------------
        lines = command_status.stdout.splitlines()
        data_lines = []
        for line in lines:
            if line.startswith("-" * 10):
                break
            data_lines.append(line)

        instances = []
        for line in lines[lines.index(data_lines[-1]) + 1:]:
            if not line.strip():
                break 

            parts = line.split()
            if len(parts) < 5:
                continue

            instance = {
                "id": parts[0],
                "name": parts[1],
                "provider": parts[2],
                "state": parts[3],
                "directory": " ".join(parts[4:]),
            }
            
            instances.append(instance)

        # Delete the previous table if it exists (refresh)----------------------------------------------------------------------
        if dpg.does_item_exist(self.TABLE_TAG):
            dpg.delete_item(self.TABLE_TAG)

        # Table for the environments----------------------------------------------------------------------
        with dpg.child_window(auto_resize_x=True, auto_resize_y=True, parent="machineswin", tag=self.TEMPWIN_TAG):
            with dpg.table(header_row=True, row_background=True, 
                        borders_innerH=True, borders_outerH=True, 
                        borders_innerV=True, borders_outerV=True, 
                        tag=self.TABLE_TAG, policy=dpg.mvTable_SizingStretchProp,context_menu_in_body=True):

                # Columns of environments----------------------------------------------------------------------
                dpg.add_table_column(label="Id",width_fixed=True, init_width_or_weight=0.0)
                dpg.add_table_column(label="Name",width_fixed=True, init_width_or_weight=0.0)
                dpg.add_table_column(label="Provider",width_fixed=True, init_width_or_weight=0.0)
                dpg.add_table_column(label="State",width_fixed=True, init_width_or_weight=0.0)
                dpg.add_table_column(label="Directory",width_fixed=True, init_width_or_weight=0.0)

                # Add data of the environments into the table--------------------------------------------------
                for machine in instances:
                    with dpg.table_row():
                        for value in machine.values():
                            
                            if value.find("no active Vagrant environments on this computer!"):
                                messagebox.showinfo(title='INFO', 
                                                    message=f'You dont have any Vagrant environment in your computer. Try creating one with the options below.'
                                                    )
                                
                                dpg.delete_item(self.TABLE_TAG)
                                dpg.delete_item(self.TEMPWIN_TAG)
                                return
                            else:    
                                dpg.add_text(value)