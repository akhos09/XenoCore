import os
import sys
import subprocess
import tkinter
from tkinter import filedialog as fd
from tkinter import Tk
from contextlib import contextmanager
from datetime import datetime

import dearpygui.dearpygui as dpg
import ctypes
from tkinter import messagebox

from . import MenuElementsGUI
from .themes import *
from .fonts import reset_font_binding

@contextmanager
def change_directory(target_dir):
    current_dir: str  = os.getcwd()
    os.chdir(target_dir)
    try:
        yield
    finally:
        os.chdir(current_dir)

class CallbacksGUI(MenuElementsGUI): # Callbacks Class for the actions of the widgets------------------------------------------
    TABLE_TAG = "vagrant_table"
    POPUPSTAT_TAG = "searching_machines"
    POPUPSTOP_TAG = "stopping_machine"
    TEMPWIN_TAG = "table_tempwin"
    IDENV_DEL_TAG = "id_input_delete"
    IDENV_STOP_TAG = "id_input_stop"
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

    def get_vagrant_status(self, app_data, user_data): # Machines List Table------------------------------------------------------------------------

        with dpg.window(label="Loading", modal=True, show=False, tag=self.POPUPSTAT_TAG, no_title_bar=True, no_move=True, no_resize=True):
            dpg.add_text("Searching for Vagrant environments...")
            dpg.add_spacer(width=100)
            dpg.add_loading_indicator(pos=[170,50])
            dpg.set_item_pos(self.POPUPSTAT_TAG, [720,400])
            dpg.show_item(self.POPUPSTAT_TAG)
        
        try:                
            command_status = subprocess.run(["vagrant", "global-status"], capture_output=True, text=True)
        except Exception as e:
            messagebox.showerror(title='ERROR', message=f'Machines on your system could not be found. Make sure Vagrant is installed\n\n{e}')
            dpg.delete_item(self.POPUPSTAT_TAG)
            return
        
        dpg.delete_item(self.POPUPSTAT_TAG)
        
        # Check for no environments first
        if "no active Vagrant environments" in command_status.stdout:
            messagebox.showinfo(title='INFO', 
                            message='You dont have any Vagrant environment in your computer. Try creating one with the options below.')
            # Clear any existing table
            if dpg.does_item_exist(self.TABLE_TAG):
                dpg.delete_item(self.TABLE_TAG)
            if dpg.does_item_exist(self.TEMPWIN_TAG):
                dpg.delete_item(self.TEMPWIN_TAG)
            return
        
        # Process output into a list of dictionaries
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

        # Delete the previous table if it exists (refresh)
        if dpg.does_item_exist(self.TABLE_TAG):
            dpg.delete_item(self.TABLE_TAG)
        if dpg.does_item_exist(self.TEMPWIN_TAG):
            dpg.delete_item(self.TEMPWIN_TAG)

        # Table for the environments---------------------------------------------------------------------------
        with dpg.child_window(auto_resize_x=True, auto_resize_y=True, parent="envheader", tag=self.TEMPWIN_TAG):
            with dpg.table(header_row=True, row_background=True, 
                        borders_innerH=True, borders_outerH=True, 
                        borders_innerV=True, borders_outerV=True, 
                        tag=self.TABLE_TAG, policy=dpg.mvTable_SizingStretchProp, context_menu_in_body=True):

                # Columns of the data---------------------------------------------------------------------------
                dpg.add_table_column(label="ID", width_fixed=True, init_width_or_weight=0.0)
                dpg.add_table_column(label="Name", width_fixed=True, init_width_or_weight=0.0)
                dpg.add_table_column(label="Provider", width_fixed=True, init_width_or_weight=0.0)
                dpg.add_table_column(label="State", width_fixed=True, init_width_or_weight=0.0)
                dpg.add_table_column(label="Directory", width_fixed=True, init_width_or_weight=0.0)

                # Add data of the environments into the table--------------------------------------
                for machine in instances:
                    with dpg.table_row():
                        dpg.add_text(machine["id"])
                        dpg.add_text(machine["name"])
                        dpg.add_text(machine["provider"])
                        dpg.add_text(machine["state"])
                        dpg.add_text(machine["directory"])
    
    def create_vagrant_env(self, app_data, user_data): # Creation of the environment------------------------------------------------------------------------
        def select_folder():
            root = Tk()
            root.withdraw()
            root.wm_attributes("-topmost", 1)
            
            try:
                folder_selected = fd.askdirectory(title="Select the folder containing the Vagrantfile")
                return folder_selected
            finally:
                root.destroy()

        # Get folder selection
        folder_selected = select_folder()
        
        if not folder_selected:
            messagebox.showwarning("Warning", "No directory selected")
            return

        if not os.path.exists(folder_selected):
            messagebox.showerror("Error", f"Directory does not exist: {folder_selected}")
            return

        # Run Vagrant command
        try:
            with change_directory(folder_selected):
                # date = datetime.today().strftime('%Y-%m-%d %H:%M:%S')
                subprocess.Popen(f'start cmd /K vagrant up', shell=True)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to start Vagrant: {str(e)}")
    
    def delete_vagrant_env(self, app_data, user_data): # Delete Vagrant environment------------------------------------------------------------------------
        id_env_delete = dpg.get_value(self.IDENV_DEL_TAG) # Gets the ID of the input_text widget
        check_delete = messagebox.askokcancel("Info",
                                             f"This option will delete all of the files (but not the Vagrantfile and the additional ones) of the environment {id_env_delete}\nAre you sure to do this?")
        if check_delete:
            try:
                subprocess.Popen(f'start cmd /K vagrant destroy -f {id_env_delete}', shell=True)
            except Exception as e:
                messagebox.showerror("Error", f"Failed to delete the environment: {str(e)}")
                
    
    def stop_vagrant_env(self, app_data, user_data): # Delete Vagrant environment------------------------------------------------------------------------
        id_env_stop = dpg.get_value(self.IDENV_STOP_TAG) # Gets the ID of the input_text widget

        with dpg.window(label="Stopping the environment", modal=True, show=False, tag=self.POPUPSTOP_TAG, no_title_bar=True, no_move=True, no_resize=True):
            dpg.add_text("Stopping the Vagrant environment...")
            dpg.add_spacer(width=100)
            dpg.add_loading_indicator(pos=[170,50])
            dpg.set_item_pos(self.POPUPSTOP_TAG, [720,400])
            dpg.show_item(self.POPUPSTOP_TAG)
        try:
            subprocess.run(["vagrant", "halt", f"{id_env_stop}"], capture_output=True, text=True)
            dpg.delete_item(self.POPUPSTAT_TAG)
        except Exception as e: 
            messagebox.showerror(title='ERROR', message=f'The environment {id_env_stop} could not be stopped. Make sure Vagrant is installed (or the machine is off or not created yet.\n\n{e}')
            dpg.delete_item(self.POPUPSTOP_TAG)           
        return
        
        

          
    