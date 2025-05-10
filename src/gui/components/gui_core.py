import threading
from tkinter import filedialog as fd
from tkinter import Tk, messagebox

import dearpygui.dearpygui as dpg

from .themes import default_theme, dark_theme, light_theme, cyberpunk_theme, gruvboxdark_theme, nyx_theme
from .fonts import reset_font_binding
from .constants import TagsCoreGUI

class CallbacksGUI(TagsCoreGUI):
    
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
                self.save_path = path  # store result
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
        num_machines_str = dpg.get_value(self.NUM_ENV_INPUT_TAG)
        try:
            num_machines = int(num_machines_str)
        except ValueError:
            num_machines = 1
        
        for i in range(1, num_machines + 1):
            with dpg.group(parent=self.SELECTOR_GROUP_TAG, horizontal=False):
                with dpg.collapsing_header(label=f"Environment {i}"):
                    with dpg.group(horizontal=False):
                        
                        # Required fields--------------------------------------------------------------------------
                        dpg.add_text("Required fields:", color=[255, 184, 0])
                        dpg.add_separator()
                        # Name Section -----------------------------------------------------------------------------
                        with dpg.group(horizontal=True):    
                            dpg.add_text("Name: ", bullet=True)
                            dpg.add_input_text(default_value=f"Environment {i}", width=349)
                        
                        # Name vb Section -----------------------------------------------------------------------------
                        with dpg.group(horizontal=True):    
                            dpg.add_text("Name (VBox): ", bullet=True)
                            dpg.add_input_text(default_value=f"Environment {i}", width=271)
                            dpg.add_text("?")
                            self.tooltip("This is the display name in the VirtualBox GUI")
                            
                        # Hostname Section -----------------------------------------------------------------------------
                        with dpg.group(horizontal=True):    
                            dpg.add_text("Hostname: ", bullet=True)
                            dpg.add_input_text(default_value=f"HostEnvironment{i}", width=305)
                            dpg.add_text("?")
                            self.tooltip("This is the name of the machine itself")
                            
                        # Box Section--------------------------------------------------------------------------------
                        with dpg.group(horizontal=True): 
                            dpg.add_text("Box:  ", bullet=True)
                            dpg.add_input_text(hint="e.g: hashicorp/bionic64", width=350)
                            dpg.add_text("?")
                            self.tooltip("The box is the template Vagrant uses to create the environment (downloads the box if Vagrant doesn't find it).\nCheck the Other section to see the boxes available.")
                            
                    
                        # Box Version Section--------------------------------------------------------------------------------
                        with dpg.group(horizontal=True): 
                            dpg.add_text("Box Version: ", bullet=True)
                            dpg.add_input_text(hint="(Latest by default)", width=274)
                            dpg.add_text("?")
                            self.tooltip("Leave blank to use the latest one downloaded on your PC.")
                            
                        # Cpu Section--------------------------------------------------------------------------------
                        with dpg.group(horizontal=True): 
                            dpg.add_text("Number of cores:  ", bullet=True)
                            dpg.add_input_text(hint="CPUs",width=218)
                            dpg.add_text("?")
                            self.tooltip("Be careful with this paremeter, ensure to check how many cores you have in your PC and how many you really need.")
                            
                        # RAM Section--------------------------------------------------------------------------------
                        with dpg.group(horizontal=True): 
                            dpg.add_text("RAM (MB): ", bullet=True)
                            dpg.add_input_text(hint="e.g: 1024, 2048, 4096, etc.", width=307)
                            dpg.add_text("?")
                            self.tooltip("Also be careful with this parameter, check how much RAM do you have and need.")
                        dpg.add_separator()
                        
                        # Optional fields:----------------------------------------------------------------------------
                        dpg.add_text("Optional fields:", color=[255, 184, 0])

                
                dpg.add_separator()
                
        dpg.hide_item(self.HELP_TEXT_VGFILE_TAG)
        
# Reset environments created--------------------------------------------------------------------------------------------
    def vgfile_reset(self, sender=None, app_data=None, user_data=None):
        if not dpg.does_item_exist(self.SELECTOR_GROUP_TAG):
            return
            
        children = dpg.get_item_children(self.SELECTOR_GROUP_TAG, slot=1) 
        
        if not children:
            return
            
        if len(children) > 0:
            for i in range(1, len(children)):
                if dpg.does_item_exist(children[i]):
                    dpg.delete_item(children[i])
                    
        dpg.show_item(self.HELP_TEXT_VGFILE_TAG)