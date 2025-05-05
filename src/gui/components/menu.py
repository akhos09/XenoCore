import webbrowser

import dearpygui.dearpygui as dpg

from .themes import *
from .fonts import *

class MenuElementsGUI: # Elements from GUI--------------------------------------------------------------------------------
    MACHINES_TAB = "machines"
    PLUGINS_TAB = "plugins"
    OTHER_TAB = "other"
    HELP_TAB = "help_tab"
    ABOUT_TAB = "about_tab"
    APPEARANCE_TAB = "appearance_tab"
    # Tabs --------------------------------------
    MAIN_WINDOW_TAG = "main_window"
    TAB_BAR_TAG = "tab_bar"
    MACHINES_WIN_TAG = "machines_win"
    RECOMMENDED_PLUGINS_TABLE_TAG = "rec_plugins_table"
    # Buttons --------------------------------------
    SEARCH_MACHINES_BTN_TAG = "search_machines_btn"
    SEARCH_PLUGINS_BTN_TAG = "search_plugins_btn"
    START_ENV_BTN_TAG = "start_env_btn"
    STOP_ENV_BTN_TAG = "stop_env_btn"
    DELETE_ENV_BTN_TAG = "delete_env_btn"
    FOLDER_SELECTION_BTN_TAG = "folder_selection_btn"
    PACK_ENV_BTN_TAG = "pack_env_btn"
    RELOAD_ENV_BTN_TAG = "reload_env_btn"
    INSTALL_PLG_BTN_TAG = "install_plg_btn"
    UNINSTALL_PLG_BTN_TAG = "uninstall_plg_btn"
    # Checkboxes --------------------------------------
    PRUNE_CHECKBOX_TAG = "check_prune_search"
    PROVISION_CHECKBOX_TAG = "check_provision"
    FORCE_STOP_CHECKBOX_TAG = "force_check_stop"
    FORCE_DELETE_CHECKBOX_TAG = "force_check_delete"
    LOCAL_PLG_CHECKBOX_TAG = "local_plg_search"
    # Inputs ------------------------------------------
    START_ENV_INPUT_TAG = "id_input_start"
    STOP_ENV_INPUT_TAG = "id_input_stop"
    DELETE_ENV_INPUT_TAG = "id_input_delete"
    RELOAD_ENV_INPUT_TAG = "id_input_reload"
    PACK_VB_INPUT_TAG = "id_input_pack_vboxname"
    PACK_OUTPUT_INPUT_TAG = "output_input_name"
    INSTALL_PLG_INPUT_TAG = "id_input_plg_install"
    UNINSTALL_PLG_INPUT_TAG = "id_input_plg_uninstall"
    # Misc ------------------------------------------
    PLUGINS_WIN_TAG = "pluginswin"
    OTHER_WIN_TAG = "otherwin"
    THEME_SELECTOR_TAG = "theme_selector"
    FONT_SELECTOR_TAG = "font_selector"
    THEME_ADV_SETTINGS_TAG = "theme_advance_settings"
    THEME_SETTINGS_ALERT_TAG = "theme_settings_alert"
    THEME_SETTINGS_BTN_TAG = "theme_settings"

# Initial settings (viewport)--------------------------------------------------------
    def initial_settings(self): 
        dpg.create_context()
        dpg.create_viewport(
            title="XenoVagrant", 
            width=1400, 
            height=900,
            small_icon=self.icon_path,
            large_icon=self.icon_path,
            decorated=True
        )
# Components and structure--------------------------------------------------------------
    def gui_main_components(self): 
        with dpg.window(tag=self.MAIN_WINDOW_TAG):
            with dpg.tab_bar(tag=self.TAB_BAR_TAG): 
                
# Machines tab & Widgets--------------------------------------------------------------------------------------------------------------------------
                with dpg.tab(label="Machines", tag=self.MACHINES_TAB):
                    with dpg.child_window(tag=self.MACHINES_WIN_TAG, label="machineswin", use_internal_label=True, border=True, auto_resize_x=False, auto_resize_y=False):
                        with dpg.group(horizontal=False):
                            with dpg.group(horizontal=True):
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
                        with dpg.group(horizontal=False):
                            with dpg.group(horizontal=True):
                                dpg.add_text("Create an environment (Vagrantfile):")
                                dpg.add_button(
                                    label="Select folder",
                                    callback=self.create_vagrant_env,
                                    width=160,
                                    tag=self.FOLDER_SELECTION_BTN_TAG
                                )
                            dpg.add_separator()
                            with dpg.group(horizontal=False):
                                with dpg.group(horizontal=True):
                                    dpg.add_text("Enter the name of the machine (IN VirtualBox GUI) you want to package:")
                                    dpg.add_input_text(width=220, hint="Name (VboxGUI)", tag=self.PACK_VB_INPUT_TAG)
                                
                                with dpg.group(horizontal=True):
                                    dpg.add_text("Enter the name of the output box (without the .box format at the end):")
                                    dpg.add_input_text(width=220, hint="Output name (.box)", tag=self.PACK_OUTPUT_INPUT_TAG)
                                with dpg.group(horizontal=True):
                                    with dpg.group(horizontal=True):
                                        dpg.add_button(
                                            label="Package",
                                            callback=self.pack_vagrant_env,
                                            width=95,
                                            tag=self.PACK_ENV_BTN_TAG
                                        )
                                        dpg.add_text("?")
                                self.tooltip(text="Packs a VBox environment as a reusable box for a Vagrantfile")
                                dpg.add_separator()   
                        # #----------------------------------------------------
                        # with dpg.collapsing_header(label="Main Options (Start Halt/Stop Delete Package Reload)"):
                        #     #------------------------------------------------------------------------------------        
                        #     with dpg.tree_node(label="Start environment"):
                        #         with dpg.group(horizontal=True):
                        #             dpg.add_text("Enter the ID of the machine you want to start: ", bullet=True)
                        #             dpg.add_input_text(width=200, hint="ID", tag=self.START_ENV_INPUT_TAG)
                        #             dpg.add_button(
                        #                 label="Start",
                        #                 callback=self.start_vagrant_env,
                        #                 width=80,
                        #                 tag=self.START_ENV_BTN_TAG
                        #             )
                        #             dpg.add_checkbox(label="Provision", tag=self.PROVISION_CHECKBOX_TAG)
                        #             with dpg.tooltip(parent=dpg.last_item(), hide_on_activity=True):
                        #                 dpg.add_text("Runs again the provisioners (scripts, commands, etc.)")
                        #     dpg.add_separator()
                        #     #------------------------------------------------------------------------------------        
                        #     with dpg.tree_node(label="Halt/Stop environment"):
                        #         with dpg.group(horizontal=True):
                        #             dpg.add_text("Enter the ID of the machine you want to stop: ", bullet=True)
                        #             dpg.add_input_text(width=200, hint="ID", tag=self.STOP_ENV_INPUT_TAG)
                        #             dpg.add_button(
                        #                 label="Stop",
                        #                 callback=self.stop_vagrant_env,
                        #                 width=80,
                        #                 tag=self.STOP_ENV_BTN_TAG
                        #             )
                        #             dpg.add_checkbox(label="Force", tag=self.FORCE_STOP_CHECKBOX_TAG)
                        #     dpg.add_separator()
                        #     #------------------------------------------------------------------------------------        
                        #     with dpg.tree_node(label="Delete environment"):
                        #         with dpg.group(horizontal=True):
                        #             dpg.add_text("Enter the ID of the machine you want to delete: ", bullet=True)
                        #             dpg.add_input_text(width=200, hint="ID", tag=self.DELETE_ENV_INPUT_TAG)
                        #             dpg.add_button(
                        #                 label="Delete",
                        #                 callback=self.delete_vagrant_env,
                        #                 width=80,
                        #                 tag=self.DELETE_ENV_BTN_TAG
                        #             )
                        #             dpg.add_checkbox(label="Force", tag=self.FORCE_DELETE_CHECKBOX_TAG)
                        #     dpg.add_separator()
                        #     #------------------------------------------------------------------------------------        
                        #     with dpg.tree_node(label="Reload environment"):
                        #         with dpg.group(horizontal=True):
                        #             dpg.add_text("Enter the ID of the machine you want to reload: ", bullet=True)
                        #             dpg.add_input_text(width=200, hint="ID", tag=self.RELOAD_ENV_INPUT_TAG)
                        #             dpg.add_button(
                        #                 label="Reload",
                        #                 callback=self.reload_vagrant_env,
                        #                 width=80,
                        #                 tag=self.RELOAD_ENV_BTN_TAG
                        #             )
                        #             dpg.add_text("?")
                        #             with dpg.tooltip(parent=dpg.last_item(), hide_on_activity=True):
                        #                 dpg.add_text("Applies the changes made in the Vagrantfile of the environment")
                        #     dpg.add_separator()        
# Plugins tab & Widgets-------------------------------------------------------------------------------------------------------------------------
                with dpg.tab(label="Plugins", tag=self.PLUGINS_TAB):
                    with dpg.child_window(label="pluginswin", use_internal_label=True, border=True, auto_resize_x=False, auto_resize_y=False, tag=self.PLUGINS_WIN_TAG):
                            with dpg.group(horizontal=True):
                                dpg.add_button(
                                    label="Search for plugins",
                                    callback=self.get_list_plugins,
                                    width=215,
                                    tag=self.SEARCH_PLUGINS_BTN_TAG
                                )
                                dpg.add_checkbox(tag=self.LOCAL_PLG_CHECKBOX_TAG)
                                dpg.add_text("Local")
                                dpg.add_text("?")
                                self.tooltip(text="Displays the plugins that are only installed in a local environment.\nCheck Vagrant documentation for more info.")
                                dpg.add_text("Right click any of the installed plugins to see the available options", color=[255, 255, 0])
                                
                                
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
                                self.tooltip(text="Check the recommended plugins if you want to try new ones.")
                                
                                

                            dpg.add_separator()
                            
                            with dpg.collapsing_header(label="List of recommended plugins"):
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
                            #     with dpg.tree_node(label="Uninstall plugins"):
                            #         with dpg.group(horizontal=True):
                            #             dpg.add_text("Enter the name/s of the plugin/s you want to uninstall: ", bullet=True)
                            #             dpg.add_input_text(width=200, hint="Name", tag=self.UNINSTALL_PLG_INPUT_TAG)
                            #             dpg.add_button(
                            #                 label="Uninstall",
                            #                 callback=self.uninstall_vagrant_plg,
                            #                 width=110,
                            #                 tag=self.UNINSTALL_PLG_BTN_TAG
                            #             )
                            #             dpg.add_text("?")
                            #         with dpg.tooltip(parent=dpg.last_item(), hide_on_activity=True):
                            #             dpg.add_text("If you want to uninstall multiple plugins, enter their names separated by spaces")                                                                            
                            #     dpg.add_separator()
                            
# Other tab & Widgets---------------------------------------------------------------------------------------------------------------------------
                with dpg.tab(label="Other", tag=self.OTHER_TAB):
                    with dpg.child_window(label="otherwin", use_internal_label=True, border=True, auto_resize_x=False, auto_resize_y=False, tag=self.OTHER_WIN_TAG):
                        with dpg.group(horizontal=False):
                            with dpg.tab_bar():
                                with dpg.tab(label="Help", tag=self.HELP_TAB):
                                    with dpg.child_window(autosize_x=True, autosize_y=True):
                                        
                                        with dpg.collapsing_header(label="Troubleshooting"):
                                            with dpg.tree_node(label="Connection Problems"):
                                                dpg.add_text("Check network settings", bullet=True)
                                                dpg.add_text("Verify credentials", bullet=True)
                                            with dpg.tree_node(label="Performance Issues"):
                                                dpg.add_text("Reduce concurrent operations", bullet=True)
                                                dpg.add_text("Allocate more resources", bullet=True)

                                        with dpg.collapsing_header(label="Support"):
                                            dpg.add_text("For additional help:", bullet=True)
                                            with dpg.group(horizontal=True):
                                                dpg.add_text("GitHub Issues:", bullet=True)
                                                dpg.add_button(
                                                    label="Open Issue",
                                                    callback=lambda: webbrowser.open("https://github.com/akhos09/XenoVagrant/issues"),
                                                    width=135
                                                )
                                            dpg.add_text("Email: discordpbl09@gmail.com", bullet=True)
                                            dpg.add_text("Discord: pabi09", bullet=True)

                                with dpg.tab(label="About", tag=self.ABOUT_TAB):
                                    
                                    with dpg.collapsing_header(label="Quick Start Guide"):
                                        dpg.add_text("1. Configure your settings in the Settings tab", bullet=True)
                                        dpg.add_text("2. Add new machines in the Machines tab", bullet=True)
                                        dpg.add_text("3. Manage plugins in the Plugins tab", bullet=True)
                                        dpg.add_text("4. Use the status bar to monitor operations", bullet=True)

                                    with dpg.collapsing_header(label="Application Overview"):
                                        dpg.add_text("Version: 1.0.0", bullet=True)
                                        dpg.add_text("License: Apache License 2.0", bullet=True)
                                        dpg.add_text("Author: @akhos09", bullet=True)
                                        with dpg.group(horizontal=True):
                                            dpg.add_text("Documentation:", bullet=True)
                                            dpg.add_button(
                                                label="GitHub README",
                                                callback=lambda: webbrowser.open("https://github.com/akhos09/XenoVagrant/blob/main/README.md"),
                                                width=180
                                            )

                                with dpg.tab(label="Appearance", tag=self.APPEARANCE_TAB):
                                    with dpg.child_window(label="appearancetab", use_internal_label=True, border=True, auto_resize_x=False, auto_resize_y=False):
                                        with dpg.group(horizontal=False):
                                            with dpg.group(horizontal=False):
                                                dpg.add_combo(
                                                    label="  Theme Selector",
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
                                                    label="  Font Selector",
                                                    items=["Default Font", 
                                                        "Conthrax-SemiBold", 
                                                        "Average-Regular"], 
                                                    callback=self.font_callback,
                                                    default_value="Default Font",
                                                    width=300,
                                                    tag=self.FONT_SELECTOR_TAG
                                                )
                                                dpg.add_button(label="Advanced Appearance Settings", tag=self.THEME_ADV_SETTINGS_TAG)
                                            with dpg.popup(tag=self.THEME_SETTINGS_ALERT_TAG,
                                                        modal=False, 
                                                        mousebutton=0,
                                                        parent=dpg.last_item(),
                                                        max_size=[1000,300],
                                                        no_move=True):
                                                
                                                dpg.set_item_pos(self.THEME_SETTINGS_ALERT_TAG, pos=[540,350])
                                                dpg.add_spacer(height=20)
                                                dpg.add_text("Be careful with these settings. They could break the appearance of the app.")
                                                dpg.add_spacer(height=30)
                                                dpg.add_spacer(width=100, height=80)
                                                dpg.add_button(label="Go to Default Theme Settings", tag=self.THEME_SETTINGS_BTN_TAG, callback=self.advanced_theme_callback)
                                                dpg.set_item_pos(dpg.last_item(), pos=[250,130])
                                                
    def final_setup_menu(self): #Final setup--------------------------------------------------
        load_fonts()
        dpg.bind_font(fonts["Default"])
        dpg.bind_theme(default_theme())
        dpg.set_primary_window("main_window", True)                    
        dpg.setup_dearpygui()
        dpg.show_viewport()
        dpg.start_dearpygui()
    
    def menu(self): #Menu startup--------------------------------------------------
        self.initial_settings()
        self.gui_main_components()
        self.final_setup_menu()