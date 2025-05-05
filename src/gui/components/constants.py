class TagsCoreGUI:
    
    # Tabs --------------------------------------
    MACHINES_TAB = "machines"
    PLUGINS_TAB = "plugins"
    OTHER_TAB = "other"
    HELP_TAB = "help_tab"
    ABOUT_TAB = "about_tab"
    APPEARANCE_TAB = "appearance_tab"
    
    # Windows & Layout --------------------------------------
    MAIN_WINDOW_TAG = "main_window"
    TAB_BAR_TAG = "tab_bar"
    MACHINES_WIN_TAG = "machines_win"
    PLUGINS_WIN_TAG = "pluginswin"
    OTHER_WIN_TAG = "otherwin"
    
    # Tables --------------------------------------
    ENV_TABLE_TAG = "vagrant_table"
    PLG_TABLE_TAG = "plg_table"
    RECOMMENDED_PLUGINS_TABLE_TAG = "rec_plugins_table"
    TEMP_ENV_WINDOW_TAG = "table_tempwin"
    TEMP_PLG_WINDOW_TAG = "table_plg_tempwin"
    
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
    
    LOADING_ENV_TEXT_TAG = "loading_env"
    CREATING_ENV_TEXT_TAG = "creating_env"
    BOOTING_ENV_TEXT_TAG = "booting_env"
    STOPPING_ENV_TEXT_TAG = "stopping_env"
    DESTROYING_ENV_TEXT_TAG = "destroying_env"
    PACKAGING_ENV_TEXT_TAG = "packaging_env"
    RELOADING_ENV_TEXT_TAG = "reloading_env"
    
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
    THEME_SETTINGS_BTN_TAG = "theme_settings"
    
    # Inputs ------------------------------------------
    START_ENV_INPUT_TAG = "id_input_start"
    STOP_ENV_INPUT_TAG = "id_input_stop"
    DELETE_ENV_INPUT_TAG = "id_input_delete"
    RELOAD_ENV_INPUT_TAG = "id_input_reload"
    PACK_VB_INPUT_TAG = "id_input_pack_vboxname" #--------
    PACK_OUTPUT_INPUT_TAG = "output_input_name"
    INSTALL_PLG_INPUT_TAG = "id_input_plg_install" #--------
    UNINSTALL_PLG_INPUT_TAG = "id_input_plg_uninstall"
    
    # Checkboxes --------------------------------------
    PRUNE_CHECKBOX_TAG = "check_prune_search"
    FORCE_DELETE_CHECKBOX_TAG = "force_check_delete"
    FORCE_STOP_CHECKBOX_TAG = "force_check_stop"
    PROVISION_CHECKBOX_TAG = "check_provision"
    LOCAL_PLG_CHECKBOX_TAG = "local_plg_search"
    
    # Misc --------------------------------------
    ROW_GROUP_TAG = "row_group"
    ENV_HEADER_TAG = "env_header"
    THEME_SELECTOR_TAG = "theme_selector"
    FONT_SELECTOR_TAG = "font_selector"
    THEME_ADV_SETTINGS_TAG = "theme_advance_settings"
    THEME_SETTINGS_ALERT_TAG = "theme_settings_alert"
    OPTIONS_ENV_TAG = "options_env"
    ENV_HELP_RCLK_TAG = "help_rgk"
    ENV_HANDLER_RGCK_TAG = "right_click_popup"