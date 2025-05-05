import os
import subprocess
from tkinter import filedialog as fd
from tkinter import Tk
from contextlib import contextmanager
import pyperclip

import dearpygui.dearpygui as dpg
from tkinter import messagebox

from .menu import MenuElementsGUI

#Decorator (stays in the app's pwd after executing a vagrant up that changes the dir in order to execute it)
@contextmanager
def change_directory(target_dir):
    current_dir: str  = os.getcwd()
    os.chdir(target_dir)
    try:
        yield
    finally:
        os.chdir(current_dir)

class CallbacksCoreEnv(MenuElementsGUI):
    # Misc---------------------------------------------
    ENV_TABLE_TAG = "vagrant_table"
    PLG_TABLE_TAG = "plg_table"
    TEMP_ENV_WINDOW_TAG = "table_tempwin"
    TEMP_PLG_WINDOW_TAG = "table_plg_tempwin"
    SEARCH_MACHINES_BTN_TAG = "search_machines_btn"
    ROW_GROUP_TAG = "row_group"
    ENV_HEADER_TAG = "env_header"
    # Popups ------------------------------------------
    POPUP_STATUS_TAG = "searching_machines"
    POPUP_CREATE_TAG = "creating_machine"
    POPUP_START_TAG = "starting_machine"
    POPUP_STOP_TAG = "stopping_machine"
    POPUP_DELETE_TAG = "destroying_machine"
    POPUP_RELOAD_TAG = "reloading_machine"    
    POPUP_PACK_TAG = "packaging_machine"
    POPUP_PLG_LIST_TAG = "searching_plg"
    POPUP_INSTALL_PLG_TAG = "installing_plg"
    POPUP_UNINSTALL_PLG_TAG = "uninstalling_plg"
    # Inputs ------------------------------------------
    START_ENV_INPUT_TAG = "id_input_start"
    STOP_ENV_INPUT_TAG = "id_input_stop"
    DELETE_ENV_INPUT_TAG = "id_input_delete"
    PACK_VB_INPUT_TAG = "id_input_pack_vboxname"
    PACK_OUTPUT_INPUT_TAG = "output_input_name"
    RELOAD_ENV_INPUT_TAG = "id_input_reload"
    
    UNINSTALL_PLG_INPUT_TAG = "id_input_plg_uninstall"
    # Checkboxes --------------------------------------
    PRUNE_CHECKBOX_TAG = "check_prune_search"
    FORCE_DELETE_CHECKBOX_TAG = "force_check_delete"
    FORCE_STOP_CHECKBOX_TAG = "force_check_stop"
    PROVISION_CHECKBOX_TAG = "check_provision"
    LOCAL_PLG_CHECKBOX_TAG = "local_plg_search"

# Vagrant env list ------------------------------------------------------------------------------------------------------------------------------------
    def get_vagrant_status(self, app_data, user_data):
        self.show_loading_popup(message="Updating Vagrant environments list...", loading_pos=[170,50], popup_tag=self.POPUP_STATUS_TAG)
        check_prune = dpg.get_value(self.PRUNE_CHECKBOX_TAG)

        try:
            cmd = ["vagrant", "global-status", "--prune"] if check_prune else ["vagrant", "global-status"]
            command_status = subprocess.run(cmd, capture_output=True, text=True)
            
        except subprocess.CalledProcessError as e:
            messagebox.showerror("Error", f"Failed to search the environments (Vagrant error): {e}")
            return
        except Exception as e:
            messagebox.showerror(title='ERROR', message=f'Machines on your system could not be found. Make sure Vagrant is installed\n\n{e}')
            return
        
        finally:
            dpg.delete_item(self.POPUP_STATUS_TAG)
        
        if "no active Vagrant environments" in command_status.stdout:
            self.show_topmost_messagebox('INFO', 
                                        'You don’t have any Vagrant environment in your computer. Try creating one with the options below.')
            if dpg.does_item_exist(self.ENV_TABLE_TAG):
                dpg.delete_item(self.ENV_TABLE_TAG)
            if dpg.does_item_exist(self.TEMP_ENV_WINDOW_TAG):
                dpg.delete_item(self.TEMP_ENV_WINDOW_TAG)
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

        if dpg.does_item_exist(self.ENV_TABLE_TAG):
            dpg.delete_item(self.ENV_TABLE_TAG)
        if dpg.does_item_exist(self.TEMP_ENV_WINDOW_TAG):
            dpg.delete_item(self.TEMP_ENV_WINDOW_TAG)

        with dpg.child_window(auto_resize_x=True, auto_resize_y=True, parent=self.MACHINES_WIN_TAG, tag=self.TEMP_ENV_WINDOW_TAG):
            with dpg.table(header_row=True, row_background=True, 
                        borders_innerH=True, borders_outerH=True, 
                        borders_innerV=True, borders_outerV=True, 
                        tag=self.ENV_TABLE_TAG, policy=dpg.mvTable_SizingStretchProp, 
                        context_menu_in_body=True):

                dpg.add_table_column(label="ID")
                dpg.add_table_column(label="Name")
                dpg.add_table_column(label="Provider")
                dpg.add_table_column(label="State")
                dpg.add_table_column(label="Directory")

                for machine in instances:
                    with dpg.table_row():
                        id_row = dpg.add_text(machine["id"])
                        dpg.set_item_user_data(id_row, machine["id"])
                        name_row = dpg.add_text(machine["name"])
                        provider_row = dpg.add_text(machine["provider"])
                        machine_row = dpg.add_text(machine["state"])
                        dir_row = dpg.add_text(machine["directory"])
                        
                    with dpg.item_handler_registry() as registry:
                        dpg.add_item_clicked_handler(button=dpg.mvMouseButton_Right, 
                                                    callback=self.env_right_click_context_menu, 
                                                    user_data=machine["id"])
                        
                    rows = [id_row, name_row, provider_row, machine_row, dir_row]
                    for row in rows:
                        dpg.bind_item_handler_registry(row, registry)
                
        dpg.set_item_label(self.SEARCH_MACHINES_BTN_TAG,"Refresh")
        dpg.set_item_width(self.SEARCH_MACHINES_BTN_TAG,100)

# Create function of an env --------------------------------------------------------------------------------------------------------------------------
    def create_vagrant_env(self, app_data, user_data):
        folder_selected = self.select_folder(text="Select the directory containing the Vagrantfile")
        
        if not folder_selected:
            messagebox.showwarning("Warning", "No directory selected")
            return

        if not os.path.exists(folder_selected):
            messagebox.showerror("Error", f"Directory does not exist: {folder_selected}")
            return
            
        self.show_loading_popup(message="Creating the Vagrant environment...", loading_pos=[170,50], popup_tag=self.POPUP_CREATE_TAG)
            
        try:
            with change_directory(folder_selected):
                cmd = f'start /wait cmd /c "vagrant up & pause"'
                subprocess.run(cmd ,shell=True, check=True)
                
        except subprocess.CalledProcessError as e:
            messagebox.showerror("Error", f"Failed to create the environment (Vagrant error): {e}")
            return
        except Exception as e:
            messagebox.showerror("Error", f"Failed to start Vagrant: {str(e)}")
            return
        
        finally:
            self.refresh(popup_tag=self.POPUP_CREATE_TAG)

# Vagrant env start -----------------------------------------------------------------------------------------------------------------------------------------
    def start_vagrant_env(self, app_data, user_data):
        id_env_start: str = dpg.get_value(self.START_ENV_INPUT_TAG)
        
        self.show_loading_popup(message="Booting up the Vagrant environment...", loading_pos=[170,50], popup_tag=self.POPUP_START_TAG)
                
        try:
            provision_check = dpg.get_value(self.PROVISION_CHECKBOX_TAG)

            if provision_check:
                cmd = f'start /wait cmd /c "vagrant up {id_env_start} --provision & pause"'
            else:
                cmd = f'start /wait cmd /c "vagrant up {id_env_start} & pause"'

            subprocess.run(cmd, shell=True, check=True)

        except subprocess.CalledProcessError as e:
            messagebox.showerror("Error", f"Failed to start the environment (Vagrant error): {e}")
            return
        except Exception as e:
            messagebox.showerror("Error", f"Unexpected error: {str(e)}")
            return
        
        finally:
            self.refresh(popup_tag=self.POPUP_START_TAG)

# Stop function of an env -----------------------------------------------------------------------------------------------------------------------------------
    def stop_vagrant_env(self, app_data, user_data):
        id_env_stop: str = dpg.get_value(self.STOP_ENV_INPUT_TAG)
        
        self.show_loading_popup(message="Stopping the Vagrant environment...", loading_pos=[170,50], popup_tag=self.POPUP_STOP_TAG)

        try:
            force_stop_check_var =  dpg.get_value(self.FORCE_STOP_CHECKBOX_TAG)
            if force_stop_check_var:
                cmd = f"vagrant halt -f {id_env_stop}"
            else:
                cmd = f"vagrant halt {id_env_stop}"
            
            subprocess.run(cmd, check=True)
        
        except subprocess.CalledProcessError as e:
            messagebox.showerror("Error", f"Failed to stop the environment (Vagrant error): {e}")
            return
        except Exception as e: 
            messagebox.showerror(title='ERROR', message=f'The environment {id_env_stop} could not be stopped. Make sure Vagrant is installed.\n\n{e}')
            return
        
        finally:
            self.refresh(popup_tag=self.POPUP_STOP_TAG)

# Delete function of an env ---------------------------------------------------------------------------------------------------------------------------------
    def delete_vagrant_env(self, app_data, user_data):
        id_env_delete: str = dpg.get_value(self.DELETE_ENV_INPUT_TAG)
        check_delete = messagebox.askokcancel("Info",
        f"This option will delete all of the files (but not the Vagrantfile and the additional ones) of the environment {id_env_delete}\nAre you sure to do this?")
        
        if check_delete:
            
            self.show_loading_popup(message="Destroying the Vagrant environment...", loading_pos=[170,50], popup_tag=self.POPUP_DELETE_TAG)
            
            try:
                force_delete_check = dpg.get_value(self.FORCE_DELETE_CHECKBOX_TAG)
                
                if force_delete_check:
                    cmd: str = f"vagrant destroy {id_env_delete} -f"
                else:
                    cmd : str = f"vagrant destroy {id_env_delete}"
                
                subprocess.run(cmd, check=True)
            
            except subprocess.CalledProcessError as e:
                messagebox.showerror("Error", f"Failed to delete the environment (Vagrant error): {e}")
                return    
            except Exception as e:
                messagebox.showerror("Error", f"Failed to delete the environment: {str(e)}")
                return

            finally:
                self.refresh(popup_tag=self.POPUP_DELETE_TAG)

# Package function of an env ---------------------------------------------------------------------------------------------------------------------------------
    def pack_vagrant_env (self, app_data, user_data):
        folder_selected = self.select_folder(text="Select the destination of the .box file")
        
        if not folder_selected:
            messagebox.showwarning("Warning", "No directory selected")
            return

        if not os.path.exists(folder_selected):
            messagebox.showerror("Error", f"Directory does not exist: {folder_selected}")
            return
        
        env_name_vb: str = dpg.get_value(self.PACK_VB_INPUT_TAG)
        box_output_name: str = dpg.get_value(self.PACK_OUTPUT_INPUT_TAG)
        self.show_loading_popup(message="Packaging the Vagrant environment...", loading_pos=[170,50], popup_tag=self.POPUP_PACK_TAG)

        try:
            cmd = f'start /wait cmd /c vagrant package --base {env_name_vb} --output {folder_selected}/{box_output_name}.box'
            subprocess.run(cmd, shell=True, check=True)
            
        except subprocess.CalledProcessError as e:
            messagebox.showerror("Error", f"Failed to pack the environment (Vagrant error): {e}")
            return
        except Exception as e:
            messagebox.showerror("Error", f"Unexpected error: {str(e)}")
            return
        
        finally:
            self.refresh(popup_tag=self.POPUP_PACK_TAG)

# Reload function of an env ---------------------------------------------------------------------------------------------------------------------------------
    def reload_vagrant_env (self, app_data, user_data):
        id_env_reload: str = dpg.get_value(self.RELOAD_ENV_INPUT_TAG)
        self.show_loading_popup(message="Reloading the Vagrant environment...", loading_pos=[170,50], popup_tag=self.POPUP_RELOAD_TAG)
                
        try:
            cmd = f'start /wait cmd /c "vagrant reload {id_env_reload} & pause"'
            subprocess.run(cmd, shell=True, check=True)

        except subprocess.CalledProcessError as e:
            messagebox.showerror("Error", f"Failed to reload the environment (Vagrant error): {e}")
            return
        except Exception as e:
            messagebox.showerror("Error", f"Unexpected error: {str(e)}")
            return
        
        finally:
            self.refresh(popup_tag=self.POPUP_RELOAD_TAG)