import os
import subprocess
import sys
from contextlib import contextmanager
from tkinter import messagebox

import dearpygui.dearpygui as dpg

from gui.components.gui_core import CallbacksGUI

# Decorator (stays in the app's pwd after executing a vagrant up that changes the dir in order to execute it)
@contextmanager
def change_directory(target_dir):
    current_dir: str = os.getcwd()
    os.chdir(target_dir)
    try:
        yield
    finally:
        os.chdir(current_dir)

class CallbacksCoreEnv(CallbacksGUI):
    
# Vagrant env list ------------------------------------------------------------------------------------------------------------------------------------
    def get_vagrant_status(self, app_data, user_data):
        dpg.delete_item("right_click_popup")
        dpg.set_item_label(self.SEARCH_MACHINES_BTN_TAG,"Loading...")
        dpg.set_item_width(self.SEARCH_MACHINES_BTN_TAG,125)
        self.env_disable_gui(text="Loading state of the environments...", text_tag=self.LOADING_ENV_TEXT_TAG)
        
        check_prune = dpg.get_value(self.PRUNE_CHECKBOX_TAG)

        try:
            cmd = ["vagrant", "global-status", "--prune"] if check_prune else ["vagrant", "global-status"]
            command_status = subprocess.run(cmd, capture_output=True, text=True)
            
        except subprocess.CalledProcessError as e:
            self.show_topmost_messagebox(title='ERROR', message=f'Failed to search the environments (Vagrant error): {e}', error=True)
        except Exception as e:
            self.show_topmost_messagebox(title='ERROR', message=f'Machines on your system could not be found. Make sure Vagrant is installed\n\n{e}', error=True)
        
        finally:
            dpg.set_item_label(self.SEARCH_MACHINES_BTN_TAG,"Refresh")
            dpg.set_item_width(self.SEARCH_MACHINES_BTN_TAG,100)
            dpg.delete_item(self.LOADING_ENV_TEXT_TAG)
            for i in self.ENV_HID_ITEMS:    
                dpg.show_item(i)
                
            for i in self.ENV_DIS_ITEMS:
                dpg.enable_item(i)
        
        if "failed" in command_status.stdout.lower():
            self.show_topmost_messagebox('ERROR', 
                                        'Vagrant failed because an error in syntax of a Vagrantfile ', error=True)
            if dpg.does_item_exist(self.ENV_TABLE_TAG):
                dpg.delete_item(self.ENV_TABLE_TAG)
            if dpg.does_item_exist(self.TEMP_ENV_WINDOW_TAG):
                dpg.delete_item(self.TEMP_ENV_WINDOW_TAG)
            return
        
        if "no active Vagrant environments" in command_status.stdout:
            self.show_topmost_messagebox('INFO', 
                                        'You don’t have any Vagrant environment in your computer. Try creating one with the options below.')
            if dpg.does_item_exist(self.ENV_TABLE_TAG):
                dpg.delete_item(self.ENV_TABLE_TAG)
            if dpg.does_item_exist(self.TEMP_ENV_WINDOW_TAG):
                dpg.delete_item(self.TEMP_ENV_WINDOW_TAG)
            return
        
        # ------- Gets output of vagrant global-status and formats it into a table ------- 
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

# Create function of an env --------------------------------------------------------------------------------------------------------------------------
    def create_vagrant_env(self, app_data, user_data):
        dpg.delete_item("right_click_popup")
        folder_selected = self.select_folder(text="Select the directory containing the Vagrantfile")
        
        if not folder_selected:
            self.show_topmost_messagebox("ERROR", f"Directory not selected", error=True)
            return

        if not os.path.exists(folder_selected):
            self.show_topmost_messagebox("ERROR", f"Directory does not exist: {folder_selected}", error=True)
            return
            
        self.env_disable_gui(text="Creating the environment...", text_tag=self.CREATING_ENV_TEXT_TAG)
            
        try:
            with change_directory(folder_selected):
                if sys.platform == "win32":
                    cmd = f'start /wait cmd /c "vagrant up & pause"'
                else:
                    cmd = "vagrant up"
                
                subprocess.run(cmd, shell=True, check=True)
                
        except subprocess.CalledProcessError as e:
            self.show_topmost_messagebox("ERROR", f"Failed to create the environment (Vagrant error): {e}", error=True)
        except Exception as e:
            self.show_topmost_messagebox("ERROR", f"Failed to start Vagrant: {str(e)}", error=True)
        
        finally:
            self.env_enable_gui(text_tag=self.CREATING_ENV_TEXT_TAG)

# Start function of an env -------------------------------------------------------------------------------------------------------------------------
    def start_vagrant_env(self, sender, app_data, user_data):
        dpg.delete_item("right_click_popup")
        id_env_start: str = user_data
        
        self.env_disable_gui(text=f"Booting up the {user_data} environment...", text_tag=self.BOOTING_ENV_TEXT_TAG)
        
        try:
            provision_check = messagebox.askokcancel("INFO",
            f"Do you want to start the environment {id_env_start} with the provisioning?")
            if provision_check:
                cmd = f"vagrant up {id_env_start} --provision"
            else:
                cmd = f"vagrant up {id_env_start}"

            # Platform check-------------------------------
            if sys.platform == "win32":
                cmd = f'start /wait cmd /c "{cmd} & pause"'
            
            subprocess.run(cmd, shell=True, check=True)

        except subprocess.CalledProcessError as e:
            self.show_topmost_messagebox("ERROR", f"Failed to start the environment (Vagrant error): {e}", error=True)
        except Exception as e:
            self.show_topmost_messagebox("ERROR", f"Unexpected error: {str(e)}", error=True)
        
        finally:
            self.env_enable_gui(text_tag=self.BOOTING_ENV_TEXT_TAG)

# Stop function of an env -------------------------------------------------------------------------------------------------------------------
    def stop_vagrant_env(self, sender, app_data, user_data):
        dpg.delete_item("right_click_popup")
        id_env_stop: str = user_data
        
        self.env_disable_gui(text=f"Stopping the {user_data} environment...", text_tag=self.STOPPING_ENV_TEXT_TAG)

        try:
            cmd = f"vagrant halt {id_env_stop}"          
            subprocess.run(cmd, check=True)
            
        except subprocess.CalledProcessError as e:
            self.show_topmost_messagebox("ERROR", f"Failed to stop the environment (Vagrant error): {e}", error=True)
        except Exception as e: 
            self.show_topmost_messagebox("ERROR", f'The environment {id_env_stop} could not be stopped. Make sure Vagrant is installed.\n\n{e}', error=True)
            
        finally:
            self.env_enable_gui(text_tag=self.STOPPING_ENV_TEXT_TAG)
            
# Delete function of an env -----------------------------------------------------------------------------------------------------------------
    def delete_vagrant_env(self, sender, app_data, user_data):
        dpg.delete_item("right_click_popup")
        id_env_delete: str = user_data
        
        check_delete = messagebox.askokcancel("Info",
        f"This option will delete all of the files (but not the Vagrantfile and the additional ones) of the environment {id_env_delete}\nAre you sure to do this?")
        
        self.env_disable_gui(text=f"Deleting the {user_data} environment...", text_tag=self.DESTROYING_ENV_TEXT_TAG)
        
        if check_delete:
            try:
                cmd: str = f"vagrant destroy {id_env_delete} -f"
                subprocess.run(cmd, check=True)
                
            except subprocess.CalledProcessError as e:
                self.show_topmost_messagebox("ERROR", f"Failed to delete the environment (Vagrant error): {e}", error=True)    
            except Exception as e:
                self.show_topmost_messagebox("ERROR", f"Failed to delete the environment: {str(e)}", error=True)
                
            finally:
                self.env_enable_gui(text_tag=self.DESTROYING_ENV_TEXT_TAG)

# Pack function of an env -----------------------------------------------------------------------------------------------------------------
    def pack_vagrant_env(self, sender, app_data, user_data):
        dpg.delete_item("right_click_popup")
        env_name_vb: str = dpg.get_value(self.PACK_VB_INPUT_TAG)

        save_path = self.ask_save_path(default_name=f"{env_name_vb}.box")

        if not save_path:
            self.show_topmost_messagebox("ERROR", "No destination folder selected", error=True)
            return

        self.env_disable_gui(text=f"Packaging the {env_name_vb} environment...", text_tag=self.PACKAGING_ENV_TEXT_TAG)

        try:
            cmd = f'vagrant package --base {env_name_vb} --output "{save_path}"'
            if sys.platform == "win32":
                cmd = f'start /wait cmd /c "{cmd} & pause"'

            subprocess.run(cmd, shell=True, check=True)

        except subprocess.CalledProcessError as e:
            self.show_topmost_messagebox("ERROR", f"Failed to pack the environment (Vagrant error): {e}", error=True)
        except Exception as e:
            self.show_topmost_messagebox("ERROR", f"Unexpected error: {str(e)}", error=True)
        finally:
            self.env_enable_gui(text_tag=self.PACKAGING_ENV_TEXT_TAG)

# Reload function of an env -------------------------------------------------------------------------------------------------------------------
    def reload_vagrant_env(self, sender, app_data, user_data):
        dpg.delete_item("right_click_popup")
        id_env_reload: str = user_data

        self.env_disable_gui(text=f"Reloading the {user_data} environment...", text_tag=self.RELOADING_ENV_TEXT_TAG)
        
        try:
            cmd = f'vagrant reload {id_env_reload}'
            if sys.platform == "win32":
                cmd = f'start /wait cmd /c "{cmd} & pause"'
                
            subprocess.run(cmd, shell=True, check=True)
            
        except subprocess.CalledProcessError as e:
            self.show_topmost_messagebox("ERROR", f"Failed to reload the environment (Vagrant error): {e}", error=True)
        except Exception as e:
            self.show_topmost_messagebox("ERROR", f"Unexpected error: {str(e)}", error=True)
        
        finally:
            self.env_enable_gui(text_tag=self.RELOADING_ENV_TEXT_TAG)
            
# Connect function to an env----------------------------------------------------------------------------------------------------------------------------
    def connect_vagrant_env(self, sender, app_data, user_data):
        dpg.delete_item("right_click_popup")
        try:
            # ------- Uses internal Vagrant ssh (fixes some bugs and errors) ------- 
            if sys.platform == "win32":
                cmd = f'start powershell -NoExit -Command "$Env:VAGRANT_PREFER_SYSTEM_BIN=0; vagrant ssh {user_data}"'
            else:
                cmd = f"vagrant ssh {user_data}"

            subprocess.run(cmd, shell=True, check=True)
        
        except subprocess.CalledProcessError as e:
            self.show_topmost_messagebox(title='ERROR', message=f"Failed to connect to the environment (Vagrant error): {e}", error=True)
        except Exception as e:
            self.show_topmost_messagebox(title='ERROR', message=f"Unexpected error: {str(e)}", error=True)
                
# Right click menu env----------------------------------------------------------------------------------------------------------------------------
    def env_right_click_context_menu(self, sender, app_data, user_data):
        self.right_click_context_menu(sender, app_data, user_data, menu_type="env")