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

class CallbacksGUI(MenuElementsGUI):  # Callbacks Class for the actions of the widgets
    # Constants for tags
    TAG_TABLE = "vagrant_table"
    TAG_POPUP_STATUS = "searching_machines"
    TAG_POPUP_STOP = "stopping_machine"
    TAG_POPUP_DELETE = "destroying_machine"
    TAG_POPUP_CREATE = "creating_machine"
    TAG_POPUP_START = "starting_machine"
    TAG_TEMP_WINDOW = "table_tempwin"
    TAG_INPUT_DELETE_ID = "id_input_delete"
    TAG_INPUT_START_ID = "id_input_start"
    TAG_INPUT_STOP_ID = "id_input_stop"
    TAG_CHECKBOX_DELETE_FORCE = "force_check_delete"
    TAG_CHECKBOX_STOP_FORCE = "force_check_stop"
    TAG_CHECKBOX_PROVISION = "check_provision"
    SEARCH_MACHINES_BTN_TAG = "search_machines_button"

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

# Vagrant env list -----------------------------------------------------------------------------------------------------------------------------------
    def get_vagrant_status(self, app_data, user_data):
        with dpg.window(label="Loading", modal=True, show=False, tag=self.TAG_POPUP_STATUS, no_title_bar=True, no_move=True, no_resize=True):
            dpg.add_text("Searching for Vagrant environments...")
            dpg.add_spacer(width=100)
            dpg.add_loading_indicator(pos=[170,50])
            dpg.set_item_pos(self.TAG_POPUP_STATUS, [720,400])
            dpg.show_item(self.TAG_POPUP_STATUS)

        try:                
            command_status = subprocess.run(["vagrant", "global-status"], capture_output=True, text=True)
        
        except subprocess.CalledProcessError as e:
            messagebox.showerror("Error", f"Failed to search the environments (Vagrant error): {e}")
        except Exception as e:
            messagebox.showerror(title='ERROR', message=f'Machines on your system could not be found. Make sure Vagrant is installed\n\n{e}')
            dpg.delete_item(self.TAG_POPUP_STATUS)
            return
        
        dpg.delete_item(self.TAG_POPUP_STATUS)
        
        if "no active Vagrant environments" in command_status.stdout:
            messagebox.showinfo(title='INFO', 
                            message='You don’t have any Vagrant environment in your computer. Try creating one with the options below.')
            if dpg.does_item_exist(self.TAG_TABLE):
                dpg.delete_item(self.TAG_TABLE)
            if dpg.does_item_exist(self.TAG_TEMP_WINDOW):
                dpg.delete_item(self.TAG_TEMP_WINDOW)
            return
        
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

        if dpg.does_item_exist(self.TAG_TABLE):
            dpg.delete_item(self.TAG_TABLE)
        if dpg.does_item_exist(self.TAG_TEMP_WINDOW):
            dpg.delete_item(self.TAG_TEMP_WINDOW)

        with dpg.child_window(auto_resize_x=True, auto_resize_y=True, parent=self.ENV_HEADER_TAG, tag=self.TAG_TEMP_WINDOW):
            with dpg.table(header_row=True, row_background=True, 
                           borders_innerH=True, borders_outerH=True, 
                           borders_innerV=True, borders_outerV=True, 
                           tag=self.TAG_TABLE, policy=dpg.mvTable_SizingStretchProp, 
                           context_menu_in_body=True):

                dpg.add_table_column(label="ID")
                dpg.add_table_column(label="Name")
                dpg.add_table_column(label="Provider")
                dpg.add_table_column(label="State")
                dpg.add_table_column(label="Directory")

                for machine in instances:
                    with dpg.table_row():
                        dpg.add_text(machine["id"])
                        dpg.add_text(machine["name"])
                        dpg.add_text(machine["provider"])
                        dpg.add_text(machine["state"])
                        dpg.add_text(machine["directory"])
        
        dpg.set_item_label(self.SEARCH_MACHINES_BTN_TAG,"Refresh")
        dpg.set_item_width(self.SEARCH_MACHINES_BTN_TAG,100)

# Create function of an env---------------------------------------------------------------------------------------------------------------------------
    def create_vagrant_env(self, app_data, user_data):
        def select_folder():
            root = Tk()
            root.withdraw()
            root.wm_attributes("-topmost", 1)
            
            try:
                folder_selected = fd.askdirectory(title="Select the folder containing the Vagrantfile")
                return folder_selected
            finally:
                root.destroy()

        folder_selected = select_folder()
        
        if not folder_selected:
            messagebox.showwarning("Warning", "No directory selected")
            return

        if not os.path.exists(folder_selected):
            messagebox.showerror("Error", f"Directory does not exist: {folder_selected}")
            return
        with dpg.window(label="Creating the Vagrant environment", 
                    modal=True, 
                    show=False, 
                    tag=self.TAG_POPUP_CREATE, 
                    no_title_bar=True, 
                    no_move=True,
                    no_resize=True):
            
            dpg.add_text("Creating the Vagrant environment...")
            dpg.add_spacer(width=100)
            dpg.add_loading_indicator(pos=[170,50])
            dpg.set_item_pos(self.TAG_POPUP_CREATE, [720,400])
            dpg.show_item(self.TAG_POPUP_CREATE)
            
        try:
            with change_directory(folder_selected):
                cmd = f'start /wait cmd /c "vagrant up & pause"'
                subprocess.run(cmd ,shell=True, check=True)
                
        except subprocess.CalledProcessError as e:
            messagebox.showerror("Error", f"Failed to create the environment (Vagrant error): {e}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to start Vagrant: {str(e)}")
        
        dpg.delete_item(self.TAG_POPUP_CREATE)   
                     
# Vagrant env start -----------------------------------------------------------------------------------------------------------------------------------
    def start_vagrant_env(self, app_data, user_data):
        id_env_start = dpg.get_value(self.TAG_INPUT_START_ID)
        with dpg.window(label="Starting the Vagrant environment", 
                modal=True, 
                show=False, 
                tag=self.TAG_POPUP_START, 
                no_title_bar=True, 
                no_move=True,
                no_resize=True):
    
                dpg.add_text("Booting up the Vagrant environment...")
                dpg.add_spacer(width=100)
                dpg.add_loading_indicator(pos=[170,50])
                dpg.set_item_pos(self.TAG_POPUP_START, [720,400])
                dpg.show_item(self.TAG_POPUP_START)
                
        try:
            provision_check = dpg.get_value(self.TAG_CHECKBOX_PROVISION)

            if provision_check:
                cmd = f'start /wait cmd /c "vagrant up {id_env_start} --provision & pause"'
            else:
                cmd = f'start /wait cmd /c "vagrant up {id_env_start} & pause"'

            subprocess.run(cmd, shell=True, check=True)

        except subprocess.CalledProcessError as e:
            messagebox.showerror("Error", f"Failed to start the environment (Vagrant error): {e}")
        except Exception as e:
            messagebox.showerror("Error", f"Unexpected error: {str(e)}")

        dpg.delete_item(self.TAG_POPUP_START)

# Stop function of an env-----------------------------------------------------------------------------------------------------------------------------------
    def stop_vagrant_env(self, app_data, user_data):
        id_env_stop = dpg.get_value(self.TAG_INPUT_STOP_ID)

        with dpg.window(label="Stopping the environment",
                        modal=True,
                        show=False,
                        tag=self.TAG_POPUP_STOP,
                        no_title_bar=True,
                        no_move=True,
                        no_resize=True):
            
            dpg.add_text("Stopping the Vagrant environment...")
            dpg.add_spacer(width=100)
            dpg.add_loading_indicator(pos=[170,50])
            dpg.set_item_pos(self.TAG_POPUP_STOP, [720,400])
            dpg.show_item(self.TAG_POPUP_STOP)

        try:
            force_stop_check_var =  dpg.get_value(self.TAG_CHECKBOX_STOP_FORCE)
            if force_stop_check_var:
                cmd = f"vagrant halt -f {id_env_stop}"
            else:
                cmd = f"vagrant halt {id_env_stop}"
            
            subprocess.run(cmd, check=True)
        
        except subprocess.CalledProcessError as e:
            messagebox.showerror("Error", f"Failed to stop the environment (Vagrant error): {e}")
        except Exception as e: 
            messagebox.showerror(title='ERROR', message=f'The environment {id_env_stop} could not be stopped. Make sure Vagrant is installed.\n\n{e}')
            
        dpg.delete_item(self.TAG_POPUP_STOP)

# Delete function of an env---------------------------------------------------------------------------------------------------------------------------
    def delete_vagrant_env(self, app_data, user_data):
        id_env_delete = dpg.get_value(self.TAG_INPUT_DELETE_ID)
        check_delete = messagebox.askokcancel("Info",
        f"This option will delete all of the files (but not the Vagrantfile and the additional ones) of the environment {id_env_delete}\nAre you sure to do this?")
        
        if check_delete:
            with dpg.window(label="Destroying the Vagrant environment", 
                            modal=True, 
                            show=False, 
                            tag=self.TAG_POPUP_DELETE, 
                            no_title_bar=True, 
                            no_move=True,
                            no_resize=True):
                
                dpg.add_text("Destroying the Vagrant environment...")
                dpg.add_spacer(width=100)
                dpg.add_loading_indicator(pos=[170,50])
                dpg.set_item_pos(self.TAG_POPUP_DELETE, [720,400])
                dpg.show_item(self.TAG_POPUP_DELETE)
                
            try:
                force_delete_check = dpg.get_value(self.TAG_CHECKBOX_DELETE_FORCE)
                
                if force_delete_check:
                    cmd: str = f"vagrant destroy {id_env_delete} -f"
                else:
                    cmd : str = f"vagrant destroy {id_env_delete}"
                
                subprocess.run(cmd, check=True)
            
            except subprocess.CalledProcessError as e:
                messagebox.showerror("Error", f"Failed to delete the environment (Vagrant error): {e}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to delete the environment: {str(e)}")
                
            dpg.delete_item(self.TAG_POPUP_DELETE)