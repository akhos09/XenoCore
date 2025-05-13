import threading
import os
from tkinter import filedialog as fd
from tkinter import Tk, messagebox

import dearpygui.dearpygui as dpg

from .themes import default_theme, dark_theme, light_theme, cyberpunk_theme, gruvboxdark_theme, nyx_theme
from .fonts import reset_font_binding
from .constants import TagsCoreGUI
from core.generator_core import VgFileGenerator

class CallbacksGUI(TagsCoreGUI):
    def __init__(self):
        self.machine_index_counter = 1
        self.provision_counter = {}
        self.sync_folder_configs = {}
        self.provisioner_configs = {}
    
    ENV_DIS_ITEMS = [TagsCoreGUI.PACK_ENV_BTN_TAG, TagsCoreGUI.SEARCH_MACHINES_BTN_TAG, TagsCoreGUI.FOLDER_SELECTION_BTN_TAG]
    ENV_HID_ITEMS =  [TagsCoreGUI.PLUGINS_TAB, TagsCoreGUI.OTHER_TAB, TagsCoreGUI.ENV_HELP_RCLK_TAG, TagsCoreGUI.VGFILEGENERATOR_TAB]
    
    PLG_DIS_ITEMS = [TagsCoreGUI.SEARCH_PLUGINS_BTN_TAG, TagsCoreGUI.INSTALL_PLG_BTN_TAG, TagsCoreGUI.REPAIR_PLG_BTN_TAG]
    PLG_HID_ITEMS =  [TagsCoreGUI.MACHINES_TAB, TagsCoreGUI.OTHER_TAB, TagsCoreGUI.PLG_HELP_RCLK_TAG, TagsCoreGUI.VGFILEGENERATOR_TAB]
    
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

# Show tooltip function -----------------------------------------------------------------------------------
    def tooltip(self, text):
        with dpg.tooltip(parent=dpg.last_item(), hide_on_activity=True):
            dpg.add_text(text)
            
# Select folder function ----------------------------------------------------------------------------------
    def select_folder(self, text="Select a folder"):

        result = {"path": None}

        def run_dialog():
            try:
                root = Tk()
                root.withdraw()
                result["path"] = fd.askdirectory(title=text, parent=root)
            finally:
                root.destroy()

        thread = threading.Thread(target=run_dialog)
        thread.start()
        thread.join()
        
        return result["path"]
            
# Topmost Tk messagebox -----------------------------------------------------------------------------------
    def show_topmost_messagebox(self, title, message, error=False):
        def run_messagebox():
            try:
                root = Tk()
                root.withdraw()
                root.wm_attributes("-topmost", 1)

                if error:
                    messagebox.showerror(title, message, parent=root)
                else:
                    messagebox.showinfo(title, message, parent=root)
            finally:
                try:
                    root.destroy()
                except:
                    pass

        thread = threading.Thread(target=run_messagebox)
        thread.start()
        
    def ask_save_path(self, default_name="output.box"):
        def run_dialog():
            try:
                root = Tk()
                root.withdraw()
                root.wm_attributes("-topmost", 1)

                path = fd.asksaveasfilename(
                    title="Save .box file",
                    defaultextension=".box",
                    initialfile=default_name,
                    filetypes=[("Vagrant Box", "*.box")]
                )
                self.save_path = path
            finally:
                try:
                    root.destroy()
                except:
                    pass

        thread = threading.Thread(target=run_dialog)
        thread.start()
        thread.join()
        return getattr(self, "save_path", None)


# Unified right click context menu-----------------------------------------------------------------------------------
    def right_click_context_menu(self, sender, app_data, user_data, menu_type):
                
        if dpg.does_item_exist("right_click_popup"):
            dpg.delete_item("right_click_popup")

        with dpg.window(tag="right_click_popup", popup=True, no_focus_on_appearing=False,
                        height=120 if menu_type == "plugin" else 90, width=130, no_background=False):

            if menu_type == "env":
                dpg.add_button(label="Start " + str(user_data), callback=self.start_vagrant_env, user_data=user_data)
                dpg.add_button(label="Stop " + str(user_data), callback=self.stop_vagrant_env, user_data=user_data)
                dpg.add_button(label="Reload " + str(user_data), callback=self.reload_vagrant_env, user_data=user_data)
                dpg.add_button(label="Delete " + str(user_data), callback=self.delete_vagrant_env, user_data=user_data)
                dpg.add_button(label="Connect " + str(user_data), callback=self.connect_vagrant_env, user_data=user_data)

                
            elif menu_type == "plugin":
                dpg.add_button(label="Update " + str(user_data), callback=self.update_vagrant_plg, user_data=user_data)
                dpg.add_button(label="Uninstall " + str(user_data), callback=self.uninstall_vagrant_plg, user_data=user_data)

# Disable gui env ----------------------------------------------------------------------------------------------------
    def env_disable_gui (self,text,text_tag):
        dpg.add_text(f'{text}', color=[255, 255, 0], parent=self.OPTIONS_ENV_TAG, tag=text_tag)
        
        for i in self.ENV_HID_ITEMS:
            dpg.hide_item(i)
        for i in self.ENV_DIS_ITEMS:
            dpg.disable_item(i)
    
    def env_enable_gui (self, text_tag):
        dpg.delete_item(text_tag)
        self.get_vagrant_status(None, "search_machines_btn")
        
        for i in self.ENV_HID_ITEMS:    
            dpg.show_item(i)
        for i in self.ENV_DIS_ITEMS:
            dpg.enable_item(i)
            
# Disable gui plgs ----------------------------------------------------------------------------------------------------
    def plg_disable_gui (self,text,text_tag):
        dpg.add_text(f'{text}', color=[255, 255, 0], parent=self.OPTIONS_PLG_TAG, tag=text_tag)
        
        for i in self.PLG_HID_ITEMS:
            dpg.hide_item(i)
            
        for i in self.PLG_DIS_ITEMS:
            dpg.disable_item(i)
            
    def plg_enable_gui (self, text_tag):
        dpg.delete_item(text_tag)
        self.get_list_plugins(None, "search_plugins_btn")
        
        for i in self.PLG_HID_ITEMS:    
            dpg.show_item(i)
            
        for i in self.PLG_DIS_ITEMS:
            dpg.enable_item(i)

# Env creation function-----------------------------------------------------------------------------------------------
    def vgfile_add_machines(self, sender=None, app_data=None, user_data=None):
        buttons_functions = [self.VG_FILE_GENERATE_BTN_TAG, self.RESET_VGFILE_TAG, "help_text_fill"]
        buttons_functions_hide = [self.NUM_ENV_INPUT_TAG, self.VGFILE_TOOLTIP_TAG]
        for i in buttons_functions_hide:
            if dpg.does_item_exist(i):
                dpg.hide_item(i)
        for i in buttons_functions:
            if dpg.does_item_exist(i):
                dpg.show_item(i)
            else:
                dpg.add_button(
                    label=" Generate ",
                    callback=self.load_machine_data,
                    tag=self.VG_FILE_GENERATE_BTN_TAG,
                    parent=self.VGFILE_BTN_GROUP_TAG
                )
                dpg.add_button(
                    label=" Reset ",
                    callback=self.vgfile_reset,
                    tag=self.RESET_VGFILE_TAG,
                    parent=self.VGFILE_BTN_GROUP_TAG
                )
                dpg.add_text("Fill the fields of the environments you want to create", color=[255, 255, 0], parent=self.VGFILE_BTN_GROUP_TAG,tag=f"help_text_fill")
        
        dpg.hide_item(self.ADD_ENV_VGFILE_TAG)
        num_machines_str = dpg.get_value(self.NUM_ENV_INPUT_TAG)
        
        try:
            num_machines = int(num_machines_str)
        except ValueError:
            num_machines = 1

        self.machine_input_data = {}

        for _ in range(num_machines):
            i = self.machine_index_counter
            self.machine_index_counter += 1
            
            with dpg.group(parent=self.SELECTOR_GROUP_TAG, horizontal=False):
                with dpg.collapsing_header(label=f"Environment {i}"):
                    with dpg.group(horizontal=False):

                        # Required fields--------------------------------------------------------------------------------------------------------
                        dpg.add_text("Required fields:", color=[255, 184, 0])
                        dpg.add_separator()

                        # Name-------------------------------------------------------------------------------------------
                        with dpg.group(horizontal=True):    
                            dpg.add_text("Name: ", bullet=True)
                            tag_name = f"env_name_{i}"
                            dpg.add_input_text(default_value=f"Environment {i}", width=349, tag=tag_name)
                            self.machine_input_data[tag_name] = f"Environment {i}"

                        # Hostname-------------------------------------------------------------------------------------------
                        with dpg.group(horizontal=True):    
                            dpg.add_text("Hostname: ", bullet=True)
                            tag_hostname = f"env_hostname_{i}"
                            dpg.add_input_text(default_value=f"HostEnvironment{i}", width=305, tag=tag_hostname)
                            self.machine_input_data[tag_hostname] = f"HostEnvironment{i}"

                        # Box-------------------------------------------------------------------------------------------
                        with dpg.group(horizontal=True): 
                            dpg.add_text("Box:  ", bullet=True)
                            tag_box = f"env_box_{i}"
                            dpg.add_input_text(hint="e.g: hashicorp/bionic64", width=350, tag=tag_box)
                            self.machine_input_data[tag_box] = "hashicorp/bionic64"  # Default value

                        # Box Version-------------------------------------------------------------------------------------------
                        with dpg.group(horizontal=True): 
                            dpg.add_text("Box Version: ", bullet=True)
                            tag_box_version = f"env_box_version_{i}"
                            dpg.add_input_text(hint="(Latest by default)", width=274, tag=tag_box_version)
                            self.machine_input_data[tag_box_version] = "" # Default value

                        # CPU-------------------------------------------------------------------------------------------
                        with dpg.group(horizontal=True): 
                            dpg.add_text("Number of cores:  ", bullet=True)
                            tag_cpu = f"env_cpu_{i}"
                            dpg.add_input_text(hint="CPUs", width=218, tag=tag_cpu)
                            self.machine_input_data[tag_cpu] = "1" # Default value

                        # RAM-------------------------------------------------------------------------------------------
                        with dpg.group(horizontal=True): 
                            dpg.add_text("RAM (MB): ", bullet=True)
                            tag_ram = f"env_ram_{i}"
                            dpg.add_input_text(hint="e.g: 1024, 2048, 4096, etc.", width=307, tag=tag_ram)
                            self.machine_input_data[tag_ram] = "1024"

                        # Optional fields-------------------------------------------------------------------------------------------
                        dpg.add_text("Optional fields:", color=[255, 184, 0])
                        dpg.add_separator()

                        # Network Interfaces-------------------------------------------------------------------------------------------
                        current_env_index = i
                        group_tag = f"net_config_group{current_env_index}"

                        dpg.add_combo(
                            items=["1", "2", "3", "4"],
                            callback=self.make_combo_callback(current_env_index),
                            default_value="Select number of network interfaces",
                            width=500,
                            )
                        with dpg.group(horizontal=False, tag=group_tag):
                            pass

                        # Disk Size-------------------------------------------------------------------------------------------
                        dpg.add_separator()
                        with dpg.group(horizontal=True): 
                            dpg.add_text("Disk Size (GB): ", bullet=True)
                            tag_disk_size = f"env_disk_size_{i}"
                            dpg.add_input_text(hint="e.g: 20, 30, 40, 50, etc.", width=325, tag=tag_disk_size)
                            self.machine_input_data[tag_disk_size] = ""
                            dpg.add_text("?")
                            self.tooltip("This requires vagrant-disksize plugin")

                        # Sync Folders-------------------------------------------------------------------------------------------
                        dpg.add_separator()
                        with dpg.group(horizontal=True):
                            dpg.add_text("Synchronized folder ", bullet=True)
                            dpg.add_button(label=" Add ", callback=self.make_sync_folder_callback(current_env_index))
                            dpg.add_button(label=" Remove ", callback=self.make_sync_folder_remove_callback(current_env_index))
                            dpg.add_text("?")
                            self.tooltip("It syncs a folder from your PC to one of your environments.")
                        
                        with dpg.group(horizontal=False, tag=f"sync_folder_group{i}"):
                            pass

                        # Provisioners-------------------------------------------------------------------------------------------
                        dpg.add_separator()
                        with dpg.group(horizontal=True):
                            dpg.add_text("Provisioners ", bullet=True)
                            dpg.add_button(label=" Add File ", callback=self.make_provisioner_callback("File", current_env_index))
                            dpg.add_button(label=" Add Folder ", callback=self.make_provisioner_callback("Folder", current_env_index))
                            dpg.add_button(label=" Add Script ", callback=self.make_provisioner_callback("Script", current_env_index))

                            dpg.add_text("?")
                            self.tooltip("Executes a script or transfers a file from your PC.")
                        
                        with dpg.group(horizontal=False, tag=f"provision_group{i}"):
                            pass

                dpg.add_separator()

        dpg.hide_item(self.HELP_TEXT_VGFILE_TAG)
                    
# Network interfaces creation-------------------------------------------------------------------------------------------
    def vgfile_netint_gui(self, sender, app_data, index):
        group_tag = f"net_config_group{index}"
        if not dpg.does_item_exist(group_tag):
            return

        self.delete_child_widgets(group_tag)
        
        interface_number = int(app_data)
        for i in range(interface_number):
            interface_tag = f"netint_{index}_{i}" 
            with dpg.tree_node(parent=group_tag, label=f"Network Interface {i+1}", tag=f"{interface_tag}_node"):
                dpg.add_combo(
                    items=["Host Only/Private Interface", "Public/Bridge Interface"],
                    default_value="Select type of interface",
                    width=500,
                    tag=f"{interface_tag}_type"
                )
                with dpg.group(horizontal=True, tag=f"{interface_tag}_ip_group"):
                    dpg.add_text("IP Address: ")
                    dpg.add_input_text(width=185, tag=f"ip_address_{index}_{i}")
                with dpg.group(horizontal=True, tag=f"{interface_tag}_subnet_group"):
                    dpg.add_text("Subnet Mask:")
                    dpg.add_input_text(width=185, tag=f"subnet_mask_{index}_{i}")
                with dpg.group(horizontal=True, tag=f"{interface_tag}_gateway_group"):
                    dpg.add_text("Gateway:    ")
                    dpg.add_input_text(width=185, tag=f"gateway_{index}_{i}")
                
                network_details = {
                    "type": f"{interface_tag}_type",
                    "ip": f"ip_address_{index}_{i}",
                    "subnet": f"subnet_mask_{index}_{i}",
                    "gateway": f"gateway_{index}_{i}"
                }

                self.network_configs = getattr(self, "network_configs", {})
                self.network_configs[f"interface_{index}_{i}"] = network_details

    # Needed for the index-----------------------------------------------------------------------------------------------
    def make_combo_callback(self, index):
        return lambda sender, app_data: self.vgfile_netint_gui(sender, app_data, str(index))
    # Fix late binding for sync folder
    def make_sync_folder_callback(self, index):
        return lambda s, a: self.vgfile_add_sync_folder(s, a, str(index))

    def make_sync_folder_remove_callback(self, index):
        return lambda s, a: self.delete_child_widgets(group=f"sync_folder_group{index}")

    # Fix late binding for provisioners
    def make_provisioner_callback(self, provision_type, index):
        return lambda s, a: self.type_provisioner(s, a, provision_type, str(index))

            
# Add sync folder function---------------------------------------------------------------------------------------------
    def vgfile_add_sync_folder(self, sender, app_data, index):
        if not hasattr(self, 'sync_folder_counter'):
            self.sync_folder_counter = {}

        if not hasattr(self, 'sync_folder_configs'):
            self.sync_folder_configs = {}

        if index not in self.sync_folder_counter:
            self.sync_folder_counter[index] = 1
        else:
            self.sync_folder_counter[index] += 1

        sync_id = self.sync_folder_counter[index]
        base_tag = f"syncfolder_{index}_{sync_id}"
        #Handler--------------------------------------------------------------------------------------
        def handle_host_folder_select():
            path = self.select_folder("Select host folder")
            if path:
                self.sync_folder_configs[f"{index}_{sync_id}"] = {"host_folder": path}
                dpg.set_item_label(f"{base_tag}_host_btn", f"{os.path.basename(path)}")

        with dpg.group(horizontal=True, parent=f"sync_folder_group{index}", tag=f"{base_tag}_group"):
            with dpg.group(horizontal=True):
                dpg.add_button(
                    label=" Select host folder ",
                    callback=lambda: handle_host_folder_select(),
                    tag=f"{base_tag}_host_btn"
                )
            with dpg.group(horizontal=True):
                dpg.add_text("VM destination path: ")
                dpg.add_input_text(
                    hint="/home/vagrant/",
                    width=200,
                    tag=f"{base_tag}_dest_input"
                )
                
# Type provisioner--------------------------------------------------------------------------------------------------------------
    def type_provisioner(self, sender, app_data, user_data, index):
        if not hasattr(self, 'provisioner_counter'):
            self.provisioner_counter = {}

        if not hasattr(self, 'provisioner_configs'):
            self.provisioner_configs = {}

        if index not in self.provisioner_counter:
            self.provisioner_counter[index] = 1
        else:
            self.provisioner_counter[index] += 1

        provision_id = self.provisioner_counter[index]
        base_tag = f"provision_{index}_{provision_id}"
        config_key = f"{index}_{provision_id}"

        def handle_select_file_or_folder():
            path = None
            if user_data == "Script":
                path = fd.askopenfilename(title="Select a script file", filetypes=[("Script Files", "*.sh;*.bat;*.ps1"), ("All Files", "*.*")])
            elif user_data == "File":
                path = fd.askopenfilename(title="Select a file")
            elif user_data == "Folder":
                path = fd.askdirectory(title="Select a folder")

            if path:
                if config_key not in self.provisioner_configs:
                    self.provisioner_configs[config_key] = {"type": user_data, "path": path, "destination": ""}
                else:
                    self.provisioner_configs[config_key]["path"] = path
                dpg.set_item_label(f"{base_tag}_select_btn", os.path.basename(path))

        with dpg.group(horizontal=True, parent=f"provision_group{index}", tag=f"{base_tag}_group"):
            if user_data == "File":
                dpg.add_text(f"{user_data}:  ")
            else:
                dpg.add_text(f"{user_data}:")
            dpg.add_button(
                label=" Select ",
                callback=lambda: handle_select_file_or_folder(),
                tag=f"{base_tag}_select_btn"
            )
            if user_data in ["File", "Folder"]:
                dpg.add_text("Destination: ")
                dpg.add_input_text(
                    hint="/destination/path",
                    width=200,
                    tag=f"{base_tag}_dest_input",
                    callback=lambda s, a: self._update_provisioner_destination(config_key, a)
                )
            dpg.add_button(
                label=" Remove ",
                callback=lambda: self._remove_provisioner(index, provision_id),
                tag=f"{base_tag}_remove_btn"
            )
# Handlers required for logic----------------------------------------------------------------
    def _remove_provisioner(self, index, provision_id):
        base_tag = f"provision_{index}_{provision_id}_group"
        config_key = f"{index}_{provision_id}"

        if dpg.does_item_exist(base_tag):
            dpg.delete_item(base_tag)

        if hasattr(self, 'provisioner_configs') and config_key in self.provisioner_configs:
            self.provisioner_configs.pop(config_key, None)
            
    def _update_provisioner_destination(self, config_key, destination):
        if config_key in self.provisioner_configs:
            self.provisioner_configs[config_key]["destination"] = destination

# Load machine_data--------------------------------------------------------------------------
    def load_machine_data(self):
        machine_data = {}

        for i in range(1, self.machine_index_counter):
            env_data = {}

            env_data["name"] = dpg.get_value(f"env_name_{i}")
            env_data["hostname"] = dpg.get_value(f"env_hostname_{i}")
            env_data["box"] = dpg.get_value(f"env_box_{i}")
            env_data["box_version"] = dpg.get_value(f"env_box_version_{i}")
            env_data["cpu"] = dpg.get_value(f"env_cpu_{i}")
            env_data["ram"] = dpg.get_value(f"env_ram_{i}")
            env_data["disk_size"] = dpg.get_value(f"env_disk_size_{i}")

            # Network interfaces-----------------------------------------------------------------
            network_interfaces = []
            for j in range(4):  
                interface_tag = f"netint_{i}_{j}"
                
                if dpg.does_item_exist(f"{interface_tag}_node"):
                    interface_type = dpg.get_value(f"{interface_tag}_type")
                    ip = dpg.get_value(f"ip_address_{i}_{j}")
                    subnet = dpg.get_value(f"subnet_mask_{i}_{j}")
                    gateway = dpg.get_value(f"gateway_{i}_{j}")
                    
                    if interface_type != "Select type of interface" and (ip or subnet or gateway):
                        network_interfaces.append({
                            "type": interface_type,
                            "ip": ip or "",
                            "subnet_mask": subnet or "",
                            "gateway": gateway or ""
                        })
                    
            env_data["network_interfaces"] = network_interfaces

            # Synced folders------------------------------------------------------------------
            sync_folders = []
            for config_key, config in self.sync_folder_configs.items():
                idx, sid = map(int, config_key.split("_"))
                if idx == i:
                    host_folder = config.get("host_folder", "")
                    vm_destination = dpg.get_value(f"syncfolder_{idx}_{sid}_dest_input") or ""
                    
                    if host_folder or vm_destination:
                        sync_folders.append({
                            "host_folder": host_folder,
                            "vm_destination": vm_destination
                        })
            env_data["sync_folders"] = sync_folders

            provisioners = []
            for config_key, config in self.provisioner_configs.items():
                idx, sid = map(int, config_key.split("_"))
                if idx == i:
                    provisioner_type = config["type"]
                    provisioner_path = config["path"]
                    provisioner_destination = config.get("destination", "")

                    if provisioner_type == "File" or provisioner_type == "Folder":
                        provisioners.append({
                            "type": "file",
                            "path": provisioner_path,
                            "destination": provisioner_destination
                        })
                    elif provisioner_type == "Script":
                        provisioners.append({
                            "type": "shell",
                            "path": provisioner_path
                        })
            env_data["provisioners"] = provisioners

            machine_data[f"environment_{i}"] = env_data

        # debug
        print(machine_data)

        generator = VgFileGenerator(machine_data)
        generator.render_template()

        return machine_data
    
    # Reset environments created--------------------------------------------------------------------------------------------
    def vgfile_reset(self, sender, app_data, user_data):
        dpg.hide_item("help_text_fill")
        dpg.hide_item(self.RESET_VGFILE_TAG)
        dpg.hide_item(self.VG_FILE_GENERATE_BTN_TAG)
        self.machine_index_counter = 1
        if not dpg.does_item_exist(self.SELECTOR_GROUP_TAG):
            return
            
        children = dpg.get_item_children(self.SELECTOR_GROUP_TAG, slot=1) 
        
        if not children:
            return
            
        if len(children) > 0:
            for i in range(1, len(children)):
                if dpg.does_item_exist(children[i]):
                    dpg.delete_item(children[i])
        
        buttons_functions_show = [self.NUM_ENV_INPUT_TAG, self.HELP_TEXT_VGFILE_TAG, self.ADD_ENV_VGFILE_TAG, self.VGFILE_TOOLTIP_TAG]
        for i in buttons_functions_show:
            if dpg.does_item_exist(i):
                dpg.show_item(i)
                
    # Delete child widgets------------------------------------------------------------------------------------------------
    def delete_child_widgets(self, group):
        if not dpg.does_item_exist(group):
            return
            
        children = dpg.get_item_children(group, slot=1)
        if children:
            for child in children:
                if dpg.does_item_exist(child):
                    dpg.delete_item(child)