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

    def get_vagrant_status(self, app_data, user_data):
        """Fetch Vagrant global status and update the table dynamically."""

        # Run the command and capture output
        result = subprocess.run(["vagrant", "global-status"], capture_output=True, text=True)

        # Check if command executed successfully
        if result.returncode != 0:
            print("Error running vagrant global-status")
            return

        # Process output into a list of dictionaries
        lines = result.stdout.splitlines()
        data_lines = []
        for line in lines:
            if line.startswith("-" * 10):  # Detects separator
                break
            data_lines.append(line)

        instances = []
        for line in lines[lines.index(data_lines[-1]) + 1:]:
            if not line.strip():
                break  # Stop at the footer information

            parts = line.split()
            if len(parts) < 5:
                continue  # Skip invalid lines

            instance = {
                "id": parts[0],
                "name": parts[1],
                "provider": parts[2],
                "state": parts[3],
                "directory": " ".join(parts[4:]),  # Handle spaces in the directory path
            }
            instances.append(instance)

        # Delete previous table (if it exists) to refresh content
        if dpg.does_item_exist(self.TABLE_TAG):
            dpg.delete_item(self.TABLE_TAG)

        # Create new table dynamically
        with dpg.child_window(auto_resize_x=True,auto_resize_y=True, parent="machineswin"):
            with dpg.table(header_row=True, row_background=True, 
                        borders_innerH=True, borders_outerH=True, 
                        borders_innerV=True, borders_outerV=True, 
                        tag=self.TABLE_TAG, policy=dpg.mvTable_SizingStretchProp,context_menu_in_body=True):

                # Add table columns
                dpg.add_table_column(label="Id",width_fixed=True, init_width_or_weight=0.0)
                dpg.add_table_column(label="Name",width_fixed=True, init_width_or_weight=0.0)
                dpg.add_table_column(label="Provider",width_fixed=True, init_width_or_weight=0.0)
                dpg.add_table_column(label="State",width_fixed=True, init_width_or_weight=0.0)
                dpg.add_table_column(label="Directory",width_fixed=True, init_width_or_weight=0.0)

                # Add rows dynamically
                for machine in instances:
                    with dpg.table_row():
                        for value in machine.values():
                            dpg.add_text(value)