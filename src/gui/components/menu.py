import webbrowser

import dearpygui.dearpygui as dpg

from .themes import *
from .fonts import *
from core.env_core import CallbacksCoreEnv
from core.plg_core import CallbacksCorePlg


# Elements from GUI--------------------------------------------------------------------------------
class MenuElementsGUI(CallbacksCoreEnv, CallbacksCorePlg): 

# Initial settings (viewport)----------------------------------------------------------------------
    def initial_settings(self): 
        dpg.create_context()
        dpg.create_viewport(
            title="XenoCore", 
            width=1400, 
            height=900,
            small_icon=self.icon_path,
            large_icon=self.icon_path,
            decorated=True
        )

# Components and structure-----------------------------------------------------------------------------------------------------------------------------------------------
    def gui_main_components(self): 
        with dpg.window(tag=self.MAIN_WINDOW_TAG):
            with dpg.tab_bar(tag=self.TAB_BAR_TAG): 
                
# Machines tab & Widgets--------------------------------------------------------------------------------------------------------------------------------------------------
                with dpg.tab(label="Machines", tag=self.MACHINES_TAB):
                    with dpg.child_window(tag=self.MACHINES_WIN_TAG, label="machineswin", use_internal_label=True, border=True, auto_resize_x=False, auto_resize_y=False):
                        with dpg.group(horizontal=False):
                            with dpg.group(horizontal=True, tag=self.OPTIONS_ENV_TAG):
                                dpg.add_button(
                                    label="Search for Vagrant Machines",
                                    callback=self.get_vagrant_status,
                                    width=333,
                                    tag=self.SEARCH_MACHINES_BTN_TAG
                                )
                                dpg.add_checkbox(tag=self.PRUNE_CHECKBOX_TAG)
                                dpg.add_text("Prune")
                                dpg.add_text("?")
                                self.tooltip(text="Refreshes the cache of the environments on your system.\nCheck help if you need more info")  
                                dpg.add_text("Right click any of the local environments to see the available options", color=[255, 255, 0], tag=self.ENV_HELP_RCLK_TAG) 
                            
                        dpg.add_separator()
                        # Main options machines --------------------------------------------------------------------------------------------------------------------------
                        with dpg.group(horizontal=False):
                            with dpg.group(horizontal=True):
                                dpg.add_text("Create an environment (Vagrantfile):")
                                dpg.add_button(
                                    label="Select folder",
                                    callback=self.create_vagrant_env,
                                    width=160,
                                    tag=self.FOLDER_SELECTION_BTN_TAG
                                )
                                dpg.add_text("?")
                                self.tooltip(text="Select a folder containing the Vagrantfile\n(check vagrantfiles folder in the root folder if you want to try one of them)")  
                            dpg.add_separator()
                            with dpg.group(horizontal=False):
                                with dpg.group(horizontal=True):
                                    dpg.add_text("Enter the name of the machine (IN VirtualBox GUI) you want to package:")
                                    dpg.add_input_text(width=220, hint="Name (VboxGUI)", tag=self.PACK_VB_INPUT_TAG)
                                with dpg.group(horizontal=True):
                                    with dpg.group(horizontal=True):
                                        dpg.add_button(
                                            label="Package",
                                            callback=self.pack_vagrant_env,
                                            width=95,
                                            tag=self.PACK_ENV_BTN_TAG
                                        )
                                        dpg.add_text("?")
                                self.tooltip(text="Packs a Vbox environment as a reusable box for a Vagrantfile")
                                dpg.add_separator()
                                
# VgFileGenerator tab & Widgets ------------------------------------------------------------------------------------------------------------------------------------------               
                with dpg.tab(label="VgFileGenerator", tag=self.VGFILEGENERATOR_TAB):
                    with dpg.child_window(tag=self.VGFILEGENERATOR_WIN_TAG, label="vgfilewin", use_internal_label=True, border=True, auto_resize_x=False, auto_resize_y=False):
                        with dpg.group(horizontal=False, tag=self.SELECTOR_GROUP_TAG):
                            with dpg.group(horizontal=True, tag = self.VGFILE_BTN_GROUP_TAG):
                                dpg.add_input_text(
                                    tag=self.NUM_ENV_INPUT_TAG,
                                    hint="Enter number",
                                    width=220,
                                    # ------- Limits the number of environments to 50 (fixes some bugs) ------- 
                                    callback=lambda s, a, u: dpg.set_value(
                                        s,
                                        str(min(max(1, int(a)) if a.isdigit() else 1, 50))
                                    )
                                )
                                dpg.add_button(
                                    label="Add",
                                    width=70,
                                    callback=self.vgfile_add_machines,
                                    tag=self.ADD_ENV_VGFILE_TAG
                                )

                                dpg.add_text("?", tag=self.VGFILE_TOOLTIP_TAG)
                                self.tooltip(text="The number of environments is capped at 50")
                                                            
                                dpg.add_text("Select the number of environments you want to create", 
                                            color=[255, 255, 0], 
                                            tag=self.HELP_TEXT_VGFILE_TAG)
                                
# Plugins tab & Widgets---------------------------------------------------------------------------------------------------------------------------------------------------
                with dpg.tab(label="Plugins", tag=self.PLUGINS_TAB):
                    with dpg.child_window(label="pluginswin", use_internal_label=True, border=True, auto_resize_x=False, auto_resize_y=False, tag=self.PLUGINS_WIN_TAG):
                        # Main options plugins ---------------------------------------------------------------------------------------------------------------------------
                            with dpg.group(horizontal=True, tag=self.OPTIONS_PLG_TAG):
                                dpg.add_button(
                                    label="Search for plugins",
                                    callback=self.get_list_plugins,
                                    width=215,
                                    tag=self.SEARCH_PLUGINS_BTN_TAG
                                )
                                dpg.add_checkbox(tag=self.LOCAL_PLG_CHECKBOX_TAG)
                                dpg.add_text("Local")
                                dpg.add_text("?")
                                self.tooltip(text="Displays the plugins that are only installed in a local environment.\nCheck Vagrant documentation for more info")
                                dpg.add_text("Right click any of the installed plugins to see the available options", color=[255, 255, 0], tag=self.PLG_HELP_RCLK_TAG)
                            
                            dpg.add_separator()
                            
                            with dpg.group(horizontal=True):
                                dpg.add_text("Repair all the plugins")
                                dpg.add_button(
                                    label="Repair",
                                    callback=self.repair_vagrant_plg,
                                    width=95,
                                    tag=self.REPAIR_PLG_BTN_TAG
                                )
                                dpg.add_checkbox(tag=self.LOCAL_PLG_REPAIR_CHECKBOX_TAG)   
                                dpg.add_text("Local")
                                dpg.add_text("?")
                                self.tooltip(text="Repair tries to uninstall and install all the plugins of the system (Local is for a local plugin)")
                            
                            dpg.add_separator()  
                            
                            with dpg.group(horizontal=True):
                                dpg.add_text("Enter the name of the plugin you want to install: ")
                                dpg.add_input_text(width=200, hint="Name", tag=self.INSTALL_PLG_INPUT_TAG)
                                dpg.add_button(
                                    label="Install",
                                    callback=self.install_vagrant_plg,
                                    width=95,
                                    tag=self.INSTALL_PLG_BTN_TAG
                                )
                                
                                dpg.add_text("?")
                                self.tooltip(text="Check the recommended plugins if you want to try new ones")

                            dpg.add_separator()
                            
                            # Recommended plugins ---------------------------------------------------------------------------------------------------------------------------
                            with dpg.collapsing_header(label="List of recommended plugins", default_open=True):
                                with dpg.group(horizontal=False):

                                    with dpg.table(tag=self.RECOMMENDED_PLUGINS_TABLE_TAG, header_row=True, 
                                                borders_innerH=True, borders_outerH=True, borders_innerV=True, 
                                                borders_outerV=True, resizable=True, policy=dpg.mvTable_SizingStretchProp):
                                        
                                        dpg.add_table_column(label="Plugin Name")
                                        dpg.add_table_column(label="Description")
                                        
                                        with dpg.table_row():
                                            dpg.add_text("vagrant-vbguest")
                                            dpg.add_text("Automatically installs VirtualBox guest additions")
                                            
                                        with dpg.table_row():
                                            dpg.add_text("vagrant-disksize")
                                            dpg.add_text("Modify disk size for VirtualBox VMs")
                                            
                                        with dpg.table_row():
                                            dpg.add_text("vagrant-hostmanager")
                                            dpg.add_text("Manages hosts file entries for VMs")
                                            
                                        with dpg.table_row():
                                            dpg.add_text("vagrant-share")
                                            dpg.add_text("Share Vagrant environments with others")
                                            
                                        with dpg.table_row():
                                            dpg.add_text("vagrant-scp")
                                            dpg.add_text("Copy files to/from Vagrant VMs via SCP")
                                            
                                            
                                        with dpg.table_row():
                                            dpg.add_text("vagrant-vbguest")
                                            dpg.add_text("Automatically installs VirtualBox guest additions")
                                            
                                        with dpg.table_row():
                                            dpg.add_text("vagrant-env")
                                            dpg.add_text("Loads environment variables from .env files")
                                            
                                        with dpg.table_row():
                                            dpg.add_text("vagrant-proxyconf")
                                            dpg.add_text("Auto-configure proxy settings in VMs")
                                dpg.add_separator()

# Other tab & Help--------------------------------------------------------------------------------------------------------------------------------------------------------
                with dpg.tab(label="Other", tag=self.OTHER_TAB):
                    with dpg.child_window(label="otherwin", use_internal_label=True, border=True, auto_resize_x=False, auto_resize_y=False, tag=self.OTHER_WIN_TAG):
                        with dpg.group(horizontal=False):
                            with dpg.tab_bar():
                                with dpg.tab(label="Help", tag=self.HELP_TAB):
                                    with dpg.child_window(autosize_x=True, autosize_y=True):
                                        
                                        with dpg.collapsing_header(label="Troubleshooting"):
                                            with dpg.tree_node(label="Connection Problems"):
                                                dpg.add_text("Check network interfaces in VirtualBox and delete the ones that aren't used anymore.", bullet=True)
                                                dpg.add_text("Check the type of network interface you have created.", bullet=True)
                                            with dpg.tree_node(label="Performance Issues"):
                                                dpg.add_text("It is common to have slow performance on Windows (not in Linux), this is due to the inner workings of powershell.", bullet=True)
                                                dpg.add_text("Check Vagrantfile's syntax if the creation is stucked at some point.", bullet=True)

                                        with dpg.collapsing_header(label="Support"):
                                            dpg.add_text("For additional help:", bullet=True)
                                            with dpg.group(horizontal=True):
                                                dpg.add_text("GitHub Issues:", bullet=True)
                                                dpg.add_button(
                                                    label="Open Issue",
                                                    callback=lambda: webbrowser.open("https://github.com/akhos09/XenoCore/issues"),
                                                    width=135
                                                )
                                            dpg.add_text("Email: xenocore09@gmail.com", bullet=True)
                                            dpg.add_text("Discord: pabi09", bullet=True)

                                with dpg.tab(label="About", tag=self.ABOUT_TAB):
                                    with dpg.collapsing_header(label="Application Overview", default_open=True):
                                        dpg.add_text("Version: 1.0.0", bullet=True)
                                        dpg.add_text("License: GPL-3.0 license", bullet=True)
                                        dpg.add_text("Author: @akhos09", bullet=True)
                                        with dpg.group(horizontal=True):
                                            dpg.add_text("Documentation:", bullet=True)
                                            dpg.add_button(
                                                label="GitHub README",
                                                callback=lambda: webbrowser.open("https://github.com/akhos09/XenoCore/blob/main/README.md"),
                                                width=180
                                            )

                                with dpg.tab(label="Appearance", tag=self.APPEARANCE_TAB):
                                    with dpg.child_window(label="appearancetab", use_internal_label=True, border=True, auto_resize_x=False, auto_resize_y=False):
                                        with dpg.group(horizontal=False):
                                            with dpg.group(horizontal=False):
                                                dpg.add_combo(
                                                    items=["Default Theme", 
                                                        "Dark Theme", 
                                                        "Light Theme",
                                                        "CyberPunk Theme", 
                                                        "Dark Gruvbox Theme", 
                                                        "Nyx Theme"], 
                                                    callback=self.theme_callback,
                                                    default_value="Default Theme",
                                                    width=300,
                                                    tag=self.THEME_SELECTOR_TAG
                                                )
                                                dpg.add_combo(
                                                    items=["Default Font", 
                                                        "Conthrax-SemiBold", 
                                                        "Average-Regular"], 
                                                    callback=self.font_callback,
                                                    default_value="Default Font",
                                                    width=300,
                                                    tag=self.FONT_SELECTOR_TAG
                                                )
                                                dpg.add_button(label="Advanced Appearance Settings", tag=self.THEME_ADV_SETTINGS_TAG, callback=self.advanced_theme_callback)

#Final setup----------------------------------------------------------------------------------------------------------------------------------------------------------------
    def final_setup_menu(self): 
        load_fonts()
        dpg.bind_font(fonts["Default"])
        dpg.bind_theme(default_theme())
        dpg.set_primary_window("main_window", True)                    
        dpg.setup_dearpygui()
        dpg.show_viewport()
        dpg.start_dearpygui()
        
#Menu startup---------------------------------------
    def menu(self): 
        self.initial_settings()
        self.gui_main_components()
        self.final_setup_menu()