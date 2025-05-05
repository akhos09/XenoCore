import sys
import subprocess

import dearpygui.dearpygui as dpg

from gui.components.gui_core import CallbacksGUI

class CallbacksCorePlg(CallbacksGUI):
    
# Get list plugin function -----------------------------------------------------------------------------------------------------------------------------------
    def get_list_plugins(self, app_data, user_data):
        self.show_loading_popup(message="   Updating Vagrant plugins list...  ", loading_pos=[177, 50], popup_tag=self.POPUP_PLG_LIST_TAG)
        check_local = dpg.get_value(self.LOCAL_PLG_CHECKBOX_TAG)
        try:
            cmd = ["vagrant", "plugin", "list", "--local"] if check_local else ["vagrant", "plugin", "list"]
            command_status = subprocess.run(cmd, capture_output=True, text=True)

        except subprocess.CalledProcessError as e:
            self.show_topmost_messagebox(title='ERROR', message=f'Failed to search the plugins (Vagrant error): {e}', error=True)
            return
        except Exception as e:
            self.show_topmost_messagebox(title='ERROR', message=f'Machines on your system could not be found. Make sure Vagrant is installed\n\n{e}', error=True)
            return

        finally:
            dpg.delete_item(self.POPUP_PLG_LIST_TAG)

        if "No plugins installed" in command_status.stdout:
            self.show_topmost_messagebox(title='INFO', message='You don’t have any Vagrant plugin in your computer. Try installing one with the options below.')

            if dpg.does_item_exist(self.PLG_TABLE_TAG):
                dpg.delete_item(self.PLG_TABLE_TAG)
            if dpg.does_item_exist(self.TEMP_PLG_WINDOW_TAG):
                dpg.delete_item(self.TEMP_PLG_WINDOW_TAG)
            return

        lines = command_status.stdout.splitlines()
        data_lines = []
        for line in lines:
            if line.startswith(".html"):
                break
            data_lines.append(line)

        plugins = []
        for line in data_lines:
            line = line.strip()
            if not line:
                continue

            name_end = line.find('(')
            if name_end == -1:
                continue

            plugin_name = line[:name_end].strip()

            version_start = name_end + 1
            version_end = line.find(',', version_start)
            if version_end == -1:
                version_end = line.find(')', version_start)
            if version_end == -1:
                continue

            plugin_version = line[version_start:version_end].strip()

            plugin = {
                "name": plugin_name,
                "version": plugin_version
            }
            plugins.append(plugin)

        if dpg.does_item_exist(self.PLG_TABLE_TAG):
            dpg.delete_item(self.PLG_TABLE_TAG)
        if dpg.does_item_exist(self.TEMP_PLG_WINDOW_TAG):
            dpg.delete_item(self.TEMP_PLG_WINDOW_TAG)

        with dpg.child_window(auto_resize_x=True, auto_resize_y=True, parent=self.PLUGINS_WIN_TAG, tag=self.TEMP_PLG_WINDOW_TAG):
            with dpg.table(header_row=True, row_background=True,
                        borders_innerH=True, borders_outerH=True,
                        borders_innerV=True, borders_outerV=True,
                        tag=self.PLG_TABLE_TAG, policy=dpg.mvTable_SizingStretchProp,
                        context_menu_in_body=True):

                dpg.add_table_column(label=" Installed plugins ")
                dpg.add_table_column(label=" Version ")

                for plugin in plugins:
                    with dpg.table_row():
                        name_row = dpg.add_text(f" {plugin['name']} ")
                        dpg.set_item_user_data(name_row, plugin["name"])
                        version_row = dpg.add_text(f" {plugin['version']} ")

                    with dpg.item_handler_registry() as registry:
                        dpg.add_item_clicked_handler(button=dpg.mvMouseButton_Right,
                                                    callback=self.plg_right_click_context_menu,
                                                    user_data=plugin["name"])

                    rows = [name_row, version_row]
                    for row in rows:
                        dpg.bind_item_handler_registry(row, registry)

        dpg.set_item_label(self.SEARCH_PLUGINS_BTN_TAG, "Refresh")
        dpg.set_item_width(self.SEARCH_PLUGINS_BTN_TAG, 100)
        
# Install plugin function ----------------------------------------------------------------------------------------------------------------------------------- 
    def install_vagrant_plg(self, app_data, user_data):
        dpg.delete_item("right_click_popup")
        name_plg_install: str = dpg.get_value(self.INSTALL_PLG_INPUT_TAG)
        self.show_loading_popup(message="      Installing the plugin...      ", loading_pos=[177, 50], popup_tag=self.POPUP_INSTALL_PLG_TAG)

        try:
            if sys.platform == "win32":
                cmd = f'start /wait cmd /c "set VAGRANT_DISABLE_STRICT_DEPENDENCY_ENFORCEMENT=1 && vagrant plugin install {name_plg_install} && pause"'
            else:
                cmd = f'VAGRANT_DISABLE_STRICT_DEPENDENCY_ENFORCEMENT=1 vagrant plugin install {name_plg_install}'

            subprocess.run(cmd, shell=True, check=True)

        except subprocess.CalledProcessError as e:
            self.show_topmost_messagebox(title='ERROR', message=f"Failed to install the plugin (Vagrant error): {e}", error=True)
            return
        except Exception as e:
            self.show_topmost_messagebox(title='ERROR', message=f'The plugin {name_plg_install} could not be installed. Make sure Vagrant is installed.\n\n{e}', error=True)
            return

        finally:
            self.get_list_plugins(None, "search_plugins_button")
            dpg.delete_item(self.POPUP_INSTALL_PLG_TAG)
            
# Uninstall plugin function -----------------------------------------------------------------------------------------------------------------------------------
    def uninstall_vagrant_plg(self, sender, app_data, user_data):
        dpg.delete_item("right_click_popup")
        name_plg_uninstall: str = user_data
        self.show_loading_popup(message="Uninstalling....", loading_pos=[170, 50], popup_tag=self.POPUP_UNINSTALL_PLG_TAG)

        try:
            if sys.platform == "win32":
                cmd = f'cmd /c "vagrant plugin uninstall {name_plg_uninstall}"'
            else:
                cmd = f'vagrant plugin uninstall {name_plg_uninstall}'

            subprocess.run(cmd, shell=True, check=True)

        except subprocess.CalledProcessError as e:
            self.show_topmost_messagebox(title='ERROR', message=f"Failed to uninstall plugin '{name_plg_uninstall}':\n{e}", error=True)
            return
        except Exception as e:
            self.show_topmost_messagebox(title='ERROR', message=f"An unexpected error occurred while uninstalling plugin '{name_plg_uninstall}':\n{e}", error=True)
            return

        finally:
            self.get_list_plugins(None, "search_plugins_button")
            dpg.delete_item(self.POPUP_UNINSTALL_PLG_TAG)
            
# Update plugin function -----------------------------------------------------------------------------------------------------------------------------------
    def update_vagrant_plg(self, app_data, user_data):
        pass
    
# Repair plugin function -----------------------------------------------------------------------------------------------------------------------------------
    def repair_vagrant_plg(self, app_data, user_data):
        pass
    
# Expunge plugin function -----------------------------------------------------------------------------------------------------------------------------------
    def expunge_vagrant_plg(self, app_data, user_data):
        pass
    
# Right click context menu plgs -----------------------------------------------------------------------------------------------------------------------------
    def plg_right_click_context_menu(self, sender, app_data, user_data):
        self.right_click_context_menu(sender, app_data, user_data, menu_type="plugin")
