from typing import List, Any, Callable, Union, Tuple
import dearpygui.dearpygui as dpg

def default_theme() -> Union[str, int]:

    with dpg.theme() as theme_id:
        with dpg.theme_component(0):
            # Text and Background Colors
            dpg.add_theme_color(dpg.mvThemeCol_Text                   , (220, 220, 220, 255))  # Light gray text
            dpg.add_theme_color(dpg.mvThemeCol_TextDisabled           , (128, 128, 128, 255))  # Disabled text
            dpg.add_theme_color(dpg.mvThemeCol_WindowBg               , (45, 45, 45, 255))     # Dark background
            dpg.add_theme_color(dpg.mvThemeCol_ChildBg                , (35, 35, 35, 255))     # Slightly darker child background
            dpg.add_theme_color(dpg.mvThemeCol_PopupBg                , (50, 50, 50, 230))     # Popup background
            
            # Interactive Elements
            dpg.add_theme_color(dpg.mvThemeCol_Button                 , (70, 70, 70, 180))     # Button color
            dpg.add_theme_color(dpg.mvThemeCol_ButtonHovered          , (90, 90, 90, 220))     # Button hover
            dpg.add_theme_color(dpg.mvThemeCol_ButtonActive           , (100, 100, 100, 255))  # Button active
            
            # Frames and Borders
            dpg.add_theme_color(dpg.mvThemeCol_Border                 , (80, 80, 80, 150))     # Border color
            dpg.add_theme_color(dpg.mvThemeCol_FrameBg                , (55, 55, 55, 200))     # Frame background
            dpg.add_theme_color(dpg.mvThemeCol_FrameBgHovered         , (75, 75, 75, 180))     # Frame hover
            dpg.add_theme_color(dpg.mvThemeCol_FrameBgActive          , (65, 65, 65, 255))     # Frame active
            
            # Scrollbar and Resize Grip
            dpg.add_theme_color(dpg.mvThemeCol_ScrollbarBg            , (40, 40, 40, 255))     # Scrollbar background
            dpg.add_theme_color(dpg.mvThemeCol_ScrollbarGrab          , (80, 80, 80, 255))     # Scrollbar grab
            dpg.add_theme_color(dpg.mvThemeCol_ScrollbarGrabHovered   , (100, 100, 100, 255))  # Scrollbar grab hover
            dpg.add_theme_color(dpg.mvThemeCol_ScrollbarGrabActive    , (120, 120, 120, 255))  # Scrollbar grab active
            
            # Highlights and Accents
            dpg.add_theme_color(dpg.mvThemeCol_CheckMark              , (150, 150, 150, 255))  # Checkbox mark
            dpg.add_theme_color(dpg.mvThemeCol_SliderGrab             , (120, 120, 120, 200))  # Slider grab
            dpg.add_theme_color(dpg.mvThemeCol_SliderGrabActive       , (150, 150, 150, 255))  # Slider grab active
            dpg.add_theme_color(dpg.mvThemeCol_TextSelectedBg         , (100, 100, 100, 100))  # Text selection background
            
            # Header and Separator
            dpg.add_theme_color(dpg.mvThemeCol_Header                 , (60, 60, 60, 255))     # Header
            dpg.add_theme_color(dpg.mvThemeCol_HeaderHovered          , (70, 70, 70, 255))     # Header hover
            dpg.add_theme_color(dpg.mvThemeCol_HeaderActive           , (80, 80, 80, 255))     # Header active
            dpg.add_theme_color(dpg.mvThemeCol_Separator              , (80, 80, 80, 255))     # Separator
            
            # Styles
            dpg.add_theme_style(dpg.mvStyleVar_WindowRounding, 5)
            dpg.add_theme_style(dpg.mvStyleVar_FrameRounding, 3)
            dpg.add_theme_style(dpg.mvStyleVar_ScrollbarRounding, 3)
            dpg.add_theme_style(dpg.mvStyleVar_GrabRounding, 3)
            dpg.add_theme_style(dpg.mvStyleVar_ItemSpacing, 10, 10) 
    return theme_id

def dark_theme() -> Union[str, int]:

    with dpg.theme() as theme_id:
        with dpg.theme_component(0):
            dpg.add_theme_color(dpg.mvThemeCol_Text                   , (1.00 * 255, 1.00 * 255, 1.00 * 255, 1.00 * 255))
            dpg.add_theme_color(dpg.mvThemeCol_TextDisabled           , (0.50 * 255, 0.50 * 255, 0.50 * 255, 1.00 * 255))
            dpg.add_theme_color(dpg.mvThemeCol_WindowBg               , (0.06 * 255, 0.06 * 255, 0.06 * 255, 0.94 * 255))
            dpg.add_theme_color(dpg.mvThemeCol_ChildBg                , (0.00 * 255, 0.00 * 255, 0.00 * 255, 0.00 * 255))
            dpg.add_theme_color(dpg.mvThemeCol_PopupBg                , (0.08 * 255, 0.08 * 255, 0.08 * 255, 0.94 * 255))
            dpg.add_theme_color(dpg.mvThemeCol_Border                 , (0.43 * 255, 0.43 * 255, 0.50 * 255, 0.50 * 255))
            dpg.add_theme_color(dpg.mvThemeCol_BorderShadow           , (0.00 * 255, 0.00 * 255, 0.00 * 255, 0.00 * 255))
            dpg.add_theme_color(dpg.mvThemeCol_FrameBg                , (0.16 * 255, 0.29 * 255, 0.48 * 255, 0.54 * 255))
            dpg.add_theme_color(dpg.mvThemeCol_FrameBgHovered         , (0.26 * 255, 0.59 * 255, 0.98 * 255, 0.40 * 255))
            dpg.add_theme_color(dpg.mvThemeCol_FrameBgActive          , (0.26 * 255, 0.59 * 255, 0.98 * 255, 0.67 * 255))
            dpg.add_theme_color(dpg.mvThemeCol_TitleBg                , (0.04 * 255, 0.04 * 255, 0.04 * 255, 1.00 * 255))
            dpg.add_theme_color(dpg.mvThemeCol_TitleBgActive          , (0.16 * 255, 0.29 * 255, 0.48 * 255, 1.00 * 255))
            dpg.add_theme_color(dpg.mvThemeCol_TitleBgCollapsed       , (0.00 * 255, 0.00 * 255, 0.00 * 255, 0.51 * 255))
            dpg.add_theme_color(dpg.mvThemeCol_MenuBarBg              , (0.14 * 255, 0.14 * 255, 0.14 * 255, 1.00 * 255))
            dpg.add_theme_color(dpg.mvThemeCol_ScrollbarBg            , (0.02 * 255, 0.02 * 255, 0.02 * 255, 0.53 * 255))
            dpg.add_theme_color(dpg.mvThemeCol_ScrollbarGrab          , (0.31 * 255, 0.31 * 255, 0.31 * 255, 1.00 * 255))
            dpg.add_theme_color(dpg.mvThemeCol_ScrollbarGrabHovered   , (0.41 * 255, 0.41 * 255, 0.41 * 255, 1.00 * 255))
            dpg.add_theme_color(dpg.mvThemeCol_ScrollbarGrabActive    , (0.51 * 255, 0.51 * 255, 0.51 * 255, 1.00 * 255))
            dpg.add_theme_color(dpg.mvThemeCol_CheckMark              , (0.26 * 255, 0.59 * 255, 0.98 * 255, 1.00 * 255))
            dpg.add_theme_color(dpg.mvThemeCol_SliderGrab             , (0.24 * 255, 0.52 * 255, 0.88 * 255, 1.00 * 255))
            dpg.add_theme_color(dpg.mvThemeCol_SliderGrabActive       , (0.26 * 255, 0.59 * 255, 0.98 * 255, 1.00 * 255))
            dpg.add_theme_color(dpg.mvThemeCol_Button                 , (0.26 * 255, 0.59 * 255, 0.98 * 255, 0.40 * 255))
            dpg.add_theme_color(dpg.mvThemeCol_ButtonHovered          , (0.26 * 255, 0.59 * 255, 0.98 * 255, 1.00 * 255))
            dpg.add_theme_color(dpg.mvThemeCol_ButtonActive           , (0.06 * 255, 0.53 * 255, 0.98 * 255, 1.00 * 255))
            dpg.add_theme_color(dpg.mvThemeCol_Header                 , (0.26 * 255, 0.59 * 255, 0.98 * 255, 0.31 * 255))
            dpg.add_theme_color(dpg.mvThemeCol_HeaderHovered          , (0.26 * 255, 0.59 * 255, 0.98 * 255, 0.80 * 255))
            dpg.add_theme_color(dpg.mvThemeCol_HeaderActive           , (0.26 * 255, 0.59 * 255, 0.98 * 255, 1.00 * 255))
            dpg.add_theme_color(dpg.mvThemeCol_Separator              , (0.43 * 255, 0.43 * 255, 0.50 * 255, 0.50 * 255))
            dpg.add_theme_color(dpg.mvThemeCol_SeparatorHovered       , (0.10 * 255, 0.40 * 255, 0.75 * 255, 0.78 * 255))
            dpg.add_theme_color(dpg.mvThemeCol_SeparatorActive        , (0.10 * 255, 0.40 * 255, 0.75 * 255, 1.00 * 255))
            dpg.add_theme_color(dpg.mvThemeCol_ResizeGrip             , (0.26 * 255, 0.59 * 255, 0.98 * 255, 0.20 * 255))
            dpg.add_theme_color(dpg.mvThemeCol_ResizeGripHovered      , (0.26 * 255, 0.59 * 255, 0.98 * 255, 0.67 * 255))
            dpg.add_theme_color(dpg.mvThemeCol_ResizeGripActive       , (0.26 * 255, 0.59 * 255, 0.98 * 255, 0.95 * 255))
            dpg.add_theme_color(dpg.mvThemeCol_Tab                    , (0.18 * 255, 0.35 * 255, 0.58 * 255, 0.86 * 255))
            dpg.add_theme_color(dpg.mvThemeCol_TabHovered             , (0.26 * 255, 0.59 * 255, 0.98 * 255, 0.80 * 255))
            dpg.add_theme_color(dpg.mvThemeCol_TabActive              , (0.20 * 255, 0.41 * 255, 0.68 * 255, 1.00 * 255))
            dpg.add_theme_color(dpg.mvThemeCol_TabUnfocused           , (0.07 * 255, 0.10 * 255, 0.15 * 255, 0.97 * 255))
            dpg.add_theme_color(dpg.mvThemeCol_TabUnfocusedActive     , (0.14 * 255, 0.26 * 255, 0.42 * 255, 1.00 * 255))
            dpg.add_theme_color(dpg.mvThemeCol_DockingPreview         , (0.26 * 255, 0.59 * 255, 0.98 * 255, 0.70 * 255))
            dpg.add_theme_color(dpg.mvThemeCol_DockingEmptyBg         , (0.20 * 255, 0.20 * 255, 0.20 * 255, 1.00 * 255))
            dpg.add_theme_color(dpg.mvThemeCol_PlotLines              , (0.61 * 255, 0.61 * 255, 0.61 * 255, 1.00 * 255))
            dpg.add_theme_color(dpg.mvThemeCol_PlotLinesHovered       , (1.00 * 255, 0.43 * 255, 0.35 * 255, 1.00 * 255))
            dpg.add_theme_color(dpg.mvThemeCol_PlotHistogram          , (0.90 * 255, 0.70 * 255, 0.00 * 255, 1.00 * 255))
            dpg.add_theme_color(dpg.mvThemeCol_PlotHistogramHovered   , (1.00 * 255, 0.60 * 255, 0.00 * 255, 1.00 * 255))
            dpg.add_theme_color(dpg.mvThemeCol_TableHeaderBg          , (0.19 * 255, 0.19 * 255, 0.20 * 255, 1.00 * 255))
            dpg.add_theme_color(dpg.mvThemeCol_TableBorderStrong      , (0.31 * 255, 0.31 * 255, 0.35 * 255, 1.00 * 255))
            dpg.add_theme_color(dpg.mvThemeCol_TableBorderLight       , (0.23 * 255, 0.23 * 255, 0.25 * 255, 1.00 * 255))
            dpg.add_theme_color(dpg.mvThemeCol_TableRowBg             , (0.00 * 255, 0.00 * 255, 0.00 * 255, 0.00 * 255))
            dpg.add_theme_color(dpg.mvThemeCol_TableRowBgAlt          , (1.00 * 255, 1.00 * 255, 1.00 * 255, 0.06 * 255))
            dpg.add_theme_color(dpg.mvThemeCol_TextSelectedBg         , (0.26 * 255, 0.59 * 255, 0.98 * 255, 0.35 * 255))
            dpg.add_theme_color(dpg.mvThemeCol_DragDropTarget         , (1.00 * 255, 1.00 * 255, 0.00 * 255, 0.90 * 255))
            dpg.add_theme_color(dpg.mvThemeCol_NavHighlight           , (0.26 * 255, 0.59 * 255, 0.98 * 255, 1.00 * 255))
            dpg.add_theme_color(dpg.mvThemeCol_NavWindowingHighlight  , (1.00 * 255, 1.00 * 255, 1.00 * 255, 0.70 * 255))
            dpg.add_theme_color(dpg.mvThemeCol_NavWindowingDimBg      , (0.80 * 255, 0.80 * 255, 0.80 * 255, 0.20 * 255))
            dpg.add_theme_color(dpg.mvThemeCol_ModalWindowDimBg       , (0.80 * 255, 0.80 * 255, 0.80 * 255, 0.35 * 255))
            dpg.add_theme_color(dpg.mvPlotCol_FrameBg                 , (1.00 * 255, 1.00 * 255, 1.00 * 255, 0.07 * 255), category=dpg.mvThemeCat_Plots)
            dpg.add_theme_color(dpg.mvPlotCol_PlotBg                  , (0.00 * 255, 0.00 * 255, 0.00 * 255, 0.50 * 255), category=dpg.mvThemeCat_Plots)
            dpg.add_theme_color(dpg.mvPlotCol_PlotBorder              , (0.43 * 255, 0.43 * 255, 0.50 * 255, 0.50 * 255), category=dpg.mvThemeCat_Plots)
            dpg.add_theme_color(dpg.mvPlotCol_LegendBg                , (0.08 * 255, 0.08 * 255, 0.08 * 255, 0.94 * 255), category=dpg.mvThemeCat_Plots)
            dpg.add_theme_color(dpg.mvPlotCol_LegendBorder            , (0.43 * 255, 0.43 * 255, 0.50 * 255, 0.50 * 255), category=dpg.mvThemeCat_Plots)
            dpg.add_theme_color(dpg.mvPlotCol_LegendText              , (1.00 * 255, 1.00 * 255, 1.00 * 255, 1.00 * 255), category=dpg.mvThemeCat_Plots)
            dpg.add_theme_color(dpg.mvPlotCol_TitleText               , (1.00 * 255, 1.00 * 255, 1.00 * 255, 1.00 * 255), category=dpg.mvThemeCat_Plots)
            dpg.add_theme_color(dpg.mvPlotCol_InlayText               , (1.00 * 255, 1.00 * 255, 1.00 * 255, 1.00 * 255), category=dpg.mvThemeCat_Plots)
            dpg.add_theme_color(dpg.mvPlotCol_AxisBg                  , (0.00 * 255, 0.00 * 255, 0.00 * 255, 0.00 * 255), category=dpg.mvThemeCat_Plots)
            dpg.add_theme_color(dpg.mvPlotCol_AxisBgActive            , (0.06 * 255, 0.53 * 255, 0.98 * 255, 1.00 * 255), category=dpg.mvThemeCat_Plots)
            dpg.add_theme_color(dpg.mvPlotCol_AxisBgHovered           , (0.26 * 255, 0.59 * 255, 0.98 * 255, 1.00 * 255), category=dpg.mvThemeCat_Plots)
            dpg.add_theme_color(dpg.mvPlotCol_AxisGrid                , (1.00 * 255, 1.00 * 255, 1.00 * 255, 1.00 * 255), category=dpg.mvThemeCat_Plots)
            dpg.add_theme_color(dpg.mvPlotCol_AxisText                , (1.00 * 255, 1.00 * 255, 1.00 * 255, 1.00 * 255), category=dpg.mvThemeCat_Plots)
            dpg.add_theme_color(dpg.mvPlotCol_Selection               , (1.00 * 255, 0.60 * 255, 0.00 * 255, 1.00 * 255), category=dpg.mvThemeCat_Plots)
            dpg.add_theme_color(dpg.mvPlotCol_Crosshairs              , (1.00 * 255, 1.00 * 255, 1.00 * 255, 0.50 * 255), category=dpg.mvThemeCat_Plots)
            dpg.add_theme_color(dpg.mvNodeCol_NodeBackground, (50, 50, 50, 255), category=dpg.mvThemeCat_Nodes)
            dpg.add_theme_color(dpg.mvNodeCol_NodeBackgroundHovered, (75, 75, 75, 255), category=dpg.mvThemeCat_Nodes)
            dpg.add_theme_color(dpg.mvNodeCol_NodeBackgroundSelected, (75, 75, 75, 255), category=dpg.mvThemeCat_Nodes)
            dpg.add_theme_color(dpg.mvNodeCol_NodeOutline, (100, 100, 100, 255), category=dpg.mvThemeCat_Nodes)
            dpg.add_theme_color(dpg.mvNodeCol_TitleBar, (41, 74, 122, 255), category=dpg.mvThemeCat_Nodes)
            dpg.add_theme_color(dpg.mvNodeCol_TitleBarHovered, (66, 150, 250, 255), category=dpg.mvThemeCat_Nodes)
            dpg.add_theme_color(dpg.mvNodeCol_TitleBarSelected, (66, 150, 250, 255), category=dpg.mvThemeCat_Nodes)
            dpg.add_theme_color(dpg.mvNodeCol_Link, (61, 133, 224, 200), category=dpg.mvThemeCat_Nodes)
            dpg.add_theme_color(dpg.mvNodeCol_LinkHovered, (66, 150, 250, 255), category=dpg.mvThemeCat_Nodes)
            dpg.add_theme_color(dpg.mvNodeCol_LinkSelected, (66, 150, 250, 255), category=dpg.mvThemeCat_Nodes)
            dpg.add_theme_color(dpg.mvNodeCol_Pin, (53, 150, 250, 180), category=dpg.mvThemeCat_Nodes)
            dpg.add_theme_color(dpg.mvNodeCol_PinHovered, (53, 150, 250, 255), category=dpg.mvThemeCat_Nodes)
            dpg.add_theme_color(dpg.mvNodeCol_BoxSelector, (61, 133, 224, 30), category=dpg.mvThemeCat_Nodes)
            dpg.add_theme_color(dpg.mvNodeCol_BoxSelectorOutline, (61, 133, 224, 150), category=dpg.mvThemeCat_Nodes)
            dpg.add_theme_color(dpg.mvNodeCol_GridBackground, (40, 40, 50, 200), category=dpg.mvThemeCat_Nodes)
            dpg.add_theme_color(dpg.mvNodeCol_GridLine, (200, 200, 200, 40), category=dpg.mvThemeCat_Nodes)
            
            dpg.add_theme_style(dpg.mvStyleVar_ItemSpacing, 18, 18) 

    return theme_id

def light_theme() -> Union[str, int]:

    with dpg.theme() as theme_id:
        with dpg.theme_component(0):
            dpg.add_theme_color(dpg.mvThemeCol_Text                   , (0.00 * 255, 0.00 * 255, 0.00 * 255, 1.00 * 255))
            dpg.add_theme_color(dpg.mvThemeCol_TextDisabled           , (0.60 * 255, 0.60 * 255, 0.60 * 255, 1.00 * 255))
            dpg.add_theme_color(dpg.mvThemeCol_WindowBg               , (0.94 * 255, 0.94 * 255, 0.94 * 255, 1.00 * 255))
            dpg.add_theme_color(dpg.mvThemeCol_ChildBg                , (0.00 * 255, 0.00 * 255, 0.00 * 255, 0.00 * 255))
            dpg.add_theme_color(dpg.mvThemeCol_PopupBg                , (1.00 * 255, 1.00 * 255, 1.00 * 255, 0.98 * 255))
            dpg.add_theme_color(dpg.mvThemeCol_Border                 , (0.00 * 255, 0.00 * 255, 0.00 * 255, 0.30 * 255))
            dpg.add_theme_color(dpg.mvThemeCol_BorderShadow           , (0.00 * 255, 0.00 * 255, 0.00 * 255, 0.00 * 255))
            dpg.add_theme_color(dpg.mvThemeCol_FrameBg                , (1.00 * 255, 1.00 * 255, 1.00 * 255, 1.00 * 255))
            dpg.add_theme_color(dpg.mvThemeCol_FrameBgHovered         , (0.26 * 255, 0.59 * 255, 0.98 * 255, 0.40 * 255))
            dpg.add_theme_color(dpg.mvThemeCol_FrameBgActive          , (0.26 * 255, 0.59 * 255, 0.98 * 255, 0.67 * 255))
            dpg.add_theme_color(dpg.mvThemeCol_TitleBg                , (0.96 * 255, 0.96 * 255, 0.96 * 255, 1.00 * 255))
            dpg.add_theme_color(dpg.mvThemeCol_TitleBgActive          , (0.82 * 255, 0.82 * 255, 0.82 * 255, 1.00 * 255))
            dpg.add_theme_color(dpg.mvThemeCol_TitleBgCollapsed       , (1.00 * 255, 1.00 * 255, 1.00 * 255, 0.51 * 255))
            dpg.add_theme_color(dpg.mvThemeCol_MenuBarBg              , (0.86 * 255, 0.86 * 255, 0.86 * 255, 1.00 * 255))
            dpg.add_theme_color(dpg.mvThemeCol_ScrollbarBg            , (0.98 * 255, 0.98 * 255, 0.98 * 255, 0.53 * 255))
            dpg.add_theme_color(dpg.mvThemeCol_ScrollbarGrab          , (0.69 * 255, 0.69 * 255, 0.69 * 255, 0.80 * 255))
            dpg.add_theme_color(dpg.mvThemeCol_ScrollbarGrabHovered   , (0.49 * 255, 0.49 * 255, 0.49 * 255, 0.80 * 255))
            dpg.add_theme_color(dpg.mvThemeCol_ScrollbarGrabActive    , (0.49 * 255, 0.49 * 255, 0.49 * 255, 1.00 * 255))
            dpg.add_theme_color(dpg.mvThemeCol_CheckMark              , (0.26 * 255, 0.59 * 255, 0.98 * 255, 1.00 * 255))
            dpg.add_theme_color(dpg.mvThemeCol_SliderGrab             , (0.26 * 255, 0.59 * 255, 0.98 * 255, 0.78 * 255))
            dpg.add_theme_color(dpg.mvThemeCol_SliderGrabActive       , (0.46 * 255, 0.54 * 255, 0.80 * 255, 0.60 * 255))
            dpg.add_theme_color(dpg.mvThemeCol_Button                 , (0.26 * 255, 0.59 * 255, 0.98 * 255, 0.40 * 255))
            dpg.add_theme_color(dpg.mvThemeCol_ButtonHovered          , (0.26 * 255, 0.59 * 255, 0.98 * 255, 1.00 * 255))
            dpg.add_theme_color(dpg.mvThemeCol_ButtonActive           , (0.06 * 255, 0.53 * 255, 0.98 * 255, 1.00 * 255))
            dpg.add_theme_color(dpg.mvThemeCol_Header                 , (0.26 * 255, 0.59 * 255, 0.98 * 255, 0.31 * 255))
            dpg.add_theme_color(dpg.mvThemeCol_HeaderHovered          , (0.26 * 255, 0.59 * 255, 0.98 * 255, 0.80 * 255))
            dpg.add_theme_color(dpg.mvThemeCol_HeaderActive           , (0.26 * 255, 0.59 * 255, 0.98 * 255, 1.00 * 255))
            dpg.add_theme_color(dpg.mvThemeCol_Separator              , (0.39 * 255, 0.39 * 255, 0.39 * 255, 0.62 * 255))
            dpg.add_theme_color(dpg.mvThemeCol_SeparatorHovered       , (0.14 * 255, 0.44 * 255, 0.80 * 255, 0.78 * 255))
            dpg.add_theme_color(dpg.mvThemeCol_SeparatorActive        , (0.14 * 255, 0.44 * 255, 0.80 * 255, 1.00 * 255))
            dpg.add_theme_color(dpg.mvThemeCol_ResizeGrip             , (0.35 * 255, 0.35 * 255, 0.35 * 255, 0.17 * 255))
            dpg.add_theme_color(dpg.mvThemeCol_ResizeGripHovered      , (0.26 * 255, 0.59 * 255, 0.98 * 255, 0.67 * 255))
            dpg.add_theme_color(dpg.mvThemeCol_ResizeGripActive       , (0.26 * 255, 0.59 * 255, 0.98 * 255, 0.95 * 255))
            dpg.add_theme_color(dpg.mvThemeCol_Tab                    , (0.76 * 255, 0.80 * 255, 0.84 * 255, 0.93 * 255))
            dpg.add_theme_color(dpg.mvThemeCol_TabHovered             , (0.26 * 255, 0.59 * 255, 0.98 * 255, 0.80 * 255))
            dpg.add_theme_color(dpg.mvThemeCol_TabActive              , (0.60 * 255, 0.73 * 255, 0.88 * 255, 1.00 * 255))
            dpg.add_theme_color(dpg.mvThemeCol_TabUnfocused           , (0.92 * 255, 0.93 * 255, 0.94 * 255, 0.99 * 255))
            dpg.add_theme_color(dpg.mvThemeCol_TabUnfocusedActive     , (0.74 * 255, 0.82 * 255, 0.91 * 255, 1.00 * 255))
            dpg.add_theme_color(dpg.mvThemeCol_DockingPreview         , (0.26 * 255, 0.59 * 255, 0.98 * 255, 0.22 * 255))
            dpg.add_theme_color(dpg.mvThemeCol_DockingEmptyBg         , (0.20 * 255, 0.20 * 255, 0.20 * 255, 1.00 * 255))
            dpg.add_theme_color(dpg.mvThemeCol_PlotLines              , (0.39 * 255, 0.39 * 255, 0.39 * 255, 1.00 * 255))
            dpg.add_theme_color(dpg.mvThemeCol_PlotLinesHovered       , (1.00 * 255, 0.43 * 255, 0.35 * 255, 1.00 * 255))
            dpg.add_theme_color(dpg.mvThemeCol_PlotHistogram          , (0.90 * 255, 0.70 * 255, 0.00 * 255, 1.00 * 255))
            dpg.add_theme_color(dpg.mvThemeCol_PlotHistogramHovered   , (1.00 * 255, 0.45 * 255, 0.00 * 255, 1.00 * 255))
            dpg.add_theme_color(dpg.mvThemeCol_TableHeaderBg          , (0.78 * 255, 0.87 * 255, 0.98 * 255, 1.00 * 255))
            dpg.add_theme_color(dpg.mvThemeCol_TableBorderStrong      , (0.57 * 255, 0.57 * 255, 0.64 * 255, 1.00 * 255))
            dpg.add_theme_color(dpg.mvThemeCol_TableBorderLight       , (0.68 * 255, 0.68 * 255, 0.74 * 255, 1.00 * 255))
            dpg.add_theme_color(dpg.mvThemeCol_TableRowBg             , (0.00 * 255, 0.00 * 255, 0.00 * 255, 0.00 * 255))
            dpg.add_theme_color(dpg.mvThemeCol_TableRowBgAlt          , (0.30 * 255, 0.30 * 255, 0.30 * 255, 0.09 * 255))
            dpg.add_theme_color(dpg.mvThemeCol_TextSelectedBg         , (0.26 * 255, 0.59 * 255, 0.98 * 255, 0.35 * 255))
            dpg.add_theme_color(dpg.mvThemeCol_DragDropTarget         , (0.26 * 255, 0.59 * 255, 0.98 * 255, 0.95 * 255))
            dpg.add_theme_color(dpg.mvThemeCol_NavHighlight           , (0.26 * 255, 0.59 * 255, 0.98 * 255, 0.80 * 255))
            dpg.add_theme_color(dpg.mvThemeCol_NavWindowingHighlight  , (0.70 * 255, 0.70 * 255, 0.70 * 255, 0.70 * 255))
            dpg.add_theme_color(dpg.mvThemeCol_NavWindowingDimBg      , (0.20 * 255, 0.20 * 255, 0.20 * 255, 0.20 * 255))
            dpg.add_theme_color(dpg.mvThemeCol_ModalWindowDimBg       , (0.20 * 255, 0.20 * 255, 0.20 * 255, 0.35 * 255))
            dpg.add_theme_color(dpg.mvPlotCol_FrameBg       , (1.00 * 255, 1.00 * 255, 1.00 * 255, 1.00 * 255), category=dpg.mvThemeCat_Plots)
            dpg.add_theme_color(dpg.mvPlotCol_PlotBg        , (0.42 * 255, 0.57 * 255, 1.00 * 255, 0.13 * 255), category=dpg.mvThemeCat_Plots)
            dpg.add_theme_color(dpg.mvPlotCol_PlotBorder    , (0.00 * 255, 0.00 * 255, 0.00 * 255, 0.00 * 255), category=dpg.mvThemeCat_Plots)
            dpg.add_theme_color(dpg.mvPlotCol_LegendBg      , (1.00 * 255, 1.00 * 255, 1.00 * 255, 0.98 * 255), category=dpg.mvThemeCat_Plots)
            dpg.add_theme_color(dpg.mvPlotCol_LegendBorder  , (0.82 * 255, 0.82 * 255, 0.82 * 255, 0.80 * 255), category=dpg.mvThemeCat_Plots)
            dpg.add_theme_color(dpg.mvPlotCol_LegendText    , (0.00 * 255, 0.00 * 255, 0.00 * 255, 1.00 * 255), category=dpg.mvThemeCat_Plots)
            dpg.add_theme_color(dpg.mvPlotCol_TitleText     , (0.00 * 255, 0.00 * 255, 0.00 * 255, 1.00 * 255), category=dpg.mvThemeCat_Plots)
            dpg.add_theme_color(dpg.mvPlotCol_InlayText     , (0.00 * 255, 0.00 * 255, 0.00 * 255, 1.00 * 255), category=dpg.mvThemeCat_Plots)
            dpg.add_theme_color(dpg.mvPlotCol_AxisBg        , (0.00 * 255, 0.00 * 255, 0.00 * 255, 0.00 * 255), category=dpg.mvThemeCat_Plots)
            dpg.add_theme_color(dpg.mvPlotCol_AxisBgActive  , (0.06 * 255, 0.53 * 255, 0.98 * 255, 1.00 * 255), category=dpg.mvThemeCat_Plots)
            dpg.add_theme_color(dpg.mvPlotCol_AxisBgHovered , (0.26 * 255, 0.59 * 255, 0.98 * 255, 1.00 * 255), category=dpg.mvThemeCat_Plots)
            dpg.add_theme_color(dpg.mvPlotCol_AxisGrid      , (0.00 * 255, 0.00 * 255, 0.00 * 255, 1.00 * 255), category=dpg.mvThemeCat_Plots)
            dpg.add_theme_color(dpg.mvPlotCol_AxisText      , (0.00 * 255, 0.00 * 255, 0.00 * 255, 1.00 * 255), category=dpg.mvThemeCat_Plots)
            dpg.add_theme_color(dpg.mvPlotCol_Selection     , (0.82 * 255, 0.64 * 255, 0.03 * 255, 1.00 * 255), category=dpg.mvThemeCat_Plots)
            dpg.add_theme_color(dpg.mvPlotCol_Crosshairs    , (0.00 * 255, 0.00 * 255, 0.00 * 255, 0.50 * 255), category=dpg.mvThemeCat_Plots)
            dpg.add_theme_color(dpg.mvNodeCol_NodeBackground, (240, 240, 240, 255), category=dpg.mvThemeCat_Nodes)
            dpg.add_theme_color(dpg.mvNodeCol_NodeBackgroundHovered, (240, 240, 240, 255), category=dpg.mvThemeCat_Nodes)
            dpg.add_theme_color(dpg.mvNodeCol_NodeBackgroundSelected, (240, 240, 240, 255), category=dpg.mvThemeCat_Nodes)
            dpg.add_theme_color(dpg.mvNodeCol_NodeOutline, (100, 100, 100, 255), category=dpg.mvThemeCat_Nodes)
            dpg.add_theme_color(dpg.mvNodeCol_TitleBar, (248, 248, 248, 255), category=dpg.mvThemeCat_Nodes)
            dpg.add_theme_color(dpg.mvNodeCol_TitleBarHovered, (209, 209, 209, 255), category=dpg.mvThemeCat_Nodes)
            dpg.add_theme_color(dpg.mvNodeCol_TitleBarSelected, (209, 209, 209, 255), category=dpg.mvThemeCat_Nodes)
            dpg.add_theme_color(dpg.mvNodeCol_Link, (66, 150, 250, 100), category=dpg.mvThemeCat_Nodes)
            dpg.add_theme_color(dpg.mvNodeCol_LinkHovered, (66, 150, 250, 242), category=dpg.mvThemeCat_Nodes)
            dpg.add_theme_color(dpg.mvNodeCol_LinkSelected, (66, 150, 250, 242), category=dpg.mvThemeCat_Nodes)
            dpg.add_theme_color(dpg.mvNodeCol_Pin, (66, 150, 250, 160), category=dpg.mvThemeCat_Nodes)
            dpg.add_theme_color(dpg.mvNodeCol_PinHovered, (66, 150, 250, 255), category=dpg.mvThemeCat_Nodes)
            dpg.add_theme_color(dpg.mvNodeCol_BoxSelector, (90, 170, 250, 30), category=dpg.mvThemeCat_Nodes)
            dpg.add_theme_color(dpg.mvNodeCol_BoxSelectorOutline, (90, 170, 250, 150), category=dpg.mvThemeCat_Nodes)
            dpg.add_theme_color(dpg.mvNodeCol_GridBackground, (225, 225, 225, 255), category=dpg.mvThemeCat_Nodes)
            dpg.add_theme_color(dpg.mvNodeCol_GridLine, (180, 180, 180, 100), category=dpg.mvThemeCat_Nodes)
            
            dpg.add_theme_style(dpg.mvStyleVar_ItemSpacing, 18, 18) 

    return theme_id

def dracula_theme() -> Union[str, int]:

    with dpg.theme() as theme_id:
        with dpg.theme_component(0):
            # Text and Background Colors
            dpg.add_theme_color(dpg.mvThemeCol_Text                   , (248, 248, 242, 255))  # Dracula Foreground
            dpg.add_theme_color(dpg.mvThemeCol_TextDisabled           , (98, 114, 164, 255))  # Dracula Comment
            dpg.add_theme_color(dpg.mvThemeCol_WindowBg               , (40, 42, 54, 255))   # Dracula Background
            dpg.add_theme_color(dpg.mvThemeCol_ChildBg                , (33, 34, 44, 255))   # Slightly darker background
            dpg.add_theme_color(dpg.mvThemeCol_PopupBg                , (40, 42, 54, 230))   # Popup with slight transparency
            
            # Interactive Elements
            dpg.add_theme_color(dpg.mvThemeCol_Button                 , (98, 114, 164, 180)) # Dracula Purple
            dpg.add_theme_color(dpg.mvThemeCol_ButtonHovered          , (189, 147, 249, 220)) # Dracula Purple Bright
            dpg.add_theme_color(dpg.mvThemeCol_ButtonActive           , (255, 121, 198, 255)) # Dracula Pink
            
            # Frames and Borders
            dpg.add_theme_color(dpg.mvThemeCol_Border                 , (98, 114, 164, 150)) # Dracula Purple
            dpg.add_theme_color(dpg.mvThemeCol_FrameBg                , (68, 71, 90, 200))   # Dark frame background
            dpg.add_theme_color(dpg.mvThemeCol_FrameBgHovered         , (98, 114, 164, 100)) # Dracula Purple
            
            # Highlights and Selections
            dpg.add_theme_color(dpg.mvThemeCol_CheckMark              , (80, 250, 123, 255)) # Dracula Green
            dpg.add_theme_color(dpg.mvThemeCol_SliderGrab             , (189, 147, 249, 200)) # Dracula Purple
            dpg.add_theme_color(dpg.mvThemeCol_TextSelectedBg         , (255, 121, 198, 100)) # Dracula Pink
            
            # Special Categories
            dpg.add_theme_color(dpg.mvPlotCol_Line                    , (139, 233, 253, 255), category=dpg.mvThemeCat_Plots) # Dracula Cyan
            dpg.add_theme_color(dpg.mvNodeCol_NodeBackground          , (68, 71, 90, 255), category=dpg.mvThemeCat_Nodes)
            dpg.add_theme_color(dpg.mvNodeCol_NodeOutline             , (98, 114, 164, 255), category=dpg.mvThemeCat_Nodes)
            
            dpg.add_theme_style(dpg.mvStyleVar_ItemSpacing, 18, 18) 

    return theme_id

def cyberpunk_theme() -> Union[str, int]:

    with dpg.theme() as theme_id:
        with dpg.theme_component(0):
            # Core Colors
            dpg.add_theme_color(dpg.mvThemeCol_Text                   , (0, 255, 255, 255))   # Bright Cyan
            dpg.add_theme_color(dpg.mvThemeCol_TextDisabled           , (128, 128, 128, 200)) # Gray
            dpg.add_theme_color(dpg.mvThemeCol_WindowBg               , (16, 16, 24, 255))   # Deep Dark Blue
            dpg.add_theme_color(dpg.mvThemeCol_ChildBg                , (22, 22, 32, 255))   # Slightly lighter dark blue
            
            # Interactive Elements
            dpg.add_theme_color(dpg.mvThemeCol_Button                 , (255, 0, 255, 180))  # Neon Magenta
            dpg.add_theme_color(dpg.mvThemeCol_ButtonHovered          , (0, 255, 255, 220))  # Bright Cyan
            dpg.add_theme_color(dpg.mvThemeCol_ButtonActive           , (255, 255, 0, 255))  # Neon Yellow
            
            # Frames and Borders
            dpg.add_theme_color(dpg.mvThemeCol_Border                 , (0, 255, 255, 150))  # Cyan Border
            dpg.add_theme_color(dpg.mvThemeCol_FrameBg                , (32, 32, 48, 200))   # Dark Frame
            dpg.add_theme_color(dpg.mvThemeCol_FrameBgHovered         , (64, 64, 96, 180))   # Hover Effect
            
            # Highlights
            dpg.add_theme_color(dpg.mvThemeCol_CheckMark              , (0, 255, 0, 255))    # Bright Green
            dpg.add_theme_color(dpg.mvThemeCol_SliderGrab             , (255, 0, 255, 200))  # Magenta
            dpg.add_theme_color(dpg.mvThemeCol_TextSelectedBg         , (0, 255, 255, 100))  # Cyan Selection
            
            # Specialized Categories
            dpg.add_theme_color(dpg.mvPlotCol_Line                    , (255, 0, 255, 255), category=dpg.mvThemeCat_Plots) # Magenta
            dpg.add_theme_color(dpg.mvNodeCol_NodeBackground          , (32, 32, 48, 255), category=dpg.mvThemeCat_Nodes)
            dpg.add_theme_color(dpg.mvNodeCol_NodeOutline             , (0, 255, 255, 255), category=dpg.mvThemeCat_Nodes)
            
            dpg.add_theme_style(dpg.mvStyleVar_ItemSpacing, 18, 18) 

    return theme_id

def gruvboxdark_theme() -> Union[str, int]:

    with dpg.theme() as theme_id:
        with dpg.theme_component(0):
            # Gruvbox Dark Color Palette
            dpg.add_theme_color(dpg.mvThemeCol_Text                   , (235, 219, 178, 255)) # Light Foreground
            dpg.add_theme_color(dpg.mvThemeCol_TextDisabled           , (146, 131, 116, 255)) # Muted Foreground
            dpg.add_theme_color(dpg.mvThemeCol_WindowBg               , (29, 32, 33, 255))   # Dark Background
            dpg.add_theme_color(dpg.mvThemeCol_ChildBg                , (40, 40, 40, 255))   # Slightly Lighter Background
            dpg.add_theme_color(dpg.mvThemeCol_PopupBg                , (29, 32, 33, 230))   # Background with Transparency
            
            # Interactive Elements
            dpg.add_theme_color(dpg.mvThemeCol_Button                 , (104, 157, 106, 180)) # Green
            dpg.add_theme_color(dpg.mvThemeCol_ButtonHovered          , (142, 192, 124, 220)) # Bright Green
            dpg.add_theme_color(dpg.mvThemeCol_ButtonActive           , (215, 153, 33, 255))  # Orange
            
            # Frames and Borders
            dpg.add_theme_color(dpg.mvThemeCol_Border                 , (146, 131, 116, 150)) # Muted Border
            dpg.add_theme_color(dpg.mvThemeCol_FrameBg                , (56, 56, 56, 200))   # Dark Frame
            dpg.add_theme_color(dpg.mvThemeCol_FrameBgHovered         , (102, 92, 84, 180))  # Hover Effect
            
            # Highlights and Accents
            dpg.add_theme_color(dpg.mvThemeCol_CheckMark              , (184, 31, 31, 255))  # Red
            dpg.add_theme_color(dpg.mvThemeCol_SliderGrab             , (215, 153, 33, 200)) # Orange
            dpg.add_theme_color(dpg.mvThemeCol_TextSelectedBg         , (168, 153, 132, 100)) # Neutral Selection
            
            # Specialized Categories
            dpg.add_theme_color(dpg.mvPlotCol_Line                    , (251, 73, 52, 255), category=dpg.mvThemeCat_Plots)  # Bright Red
            dpg.add_theme_color(dpg.mvNodeCol_NodeBackground          , (50, 48, 47, 255), category=dpg.mvThemeCat_Nodes)
            dpg.add_theme_color(dpg.mvNodeCol_NodeOutline             , (102, 92, 84, 255), category=dpg.mvThemeCat_Nodes)


            dpg.add_theme_style(dpg.mvStyleVar_ItemSpacing, 18, 18) 
    return theme_id

def nyx_theme() -> Union[str, int]:
    with dpg.theme() as theme_id:
        with dpg.theme_component(0):
            # Core Color Palette
            PURPLE = (128, 64, 255, 255)     # Vibrant purple
            BLUE = (64, 128, 255, 255)       # Bright blue
            YELLOW = (255, 224, 64, 255)     # Warm yellow
            PINK = (255, 64, 196, 255)       # Vibrant pink
            MEDIUM_DARK_GRAY = (40, 40, 50, 255)  # Medium dark gray background

            # Text and Background Colors
            dpg.add_theme_color(dpg.mvThemeCol_Text, (230, 230, 230, 255))  # Light text
            dpg.add_theme_color(dpg.mvThemeCol_TextDisabled, (120, 120, 140, 255))  # Muted text
            dpg.add_theme_color(dpg.mvThemeCol_WindowBg, MEDIUM_DARK_GRAY)  # Window background
            dpg.add_theme_color(dpg.mvThemeCol_ChildBg, (35, 35, 45, 255))  # Child window background
            dpg.add_theme_color(dpg.mvThemeCol_PopupBg, (45, 45, 55, 230))  # Popup background

            # Interactive Elements
            dpg.add_theme_color(dpg.mvThemeCol_Button, PURPLE)  # Button color
            dpg.add_theme_color(dpg.mvThemeCol_ButtonHovered, BLUE)  # Button hover
            dpg.add_theme_color(dpg.mvThemeCol_ButtonActive, YELLOW)  # Button active

            # Frames and Borders
            dpg.add_theme_color(dpg.mvThemeCol_Border, PINK)  # Border color
            dpg.add_theme_color(dpg.mvThemeCol_FrameBg, (50, 50, 60, 200))  # Frame background
            dpg.add_theme_color(dpg.mvThemeCol_FrameBgHovered, (60, 60, 70, 180))  # Frame hover
            dpg.add_theme_color(dpg.mvThemeCol_FrameBgActive, (70, 70, 80, 255))  # Frame active

            # Highlights and Accents
            dpg.add_theme_color(dpg.mvThemeCol_CheckMark, YELLOW)  # Checkbox mark
            dpg.add_theme_color(dpg.mvThemeCol_SliderGrab, BLUE)  # Slider grab
            dpg.add_theme_color(dpg.mvThemeCol_SliderGrabActive, PINK)  # Slider grab active
            dpg.add_theme_color(dpg.mvThemeCol_TextSelectedBg, PURPLE)  # Text selection background

            # Scrollbar
            dpg.add_theme_color(dpg.mvThemeCol_ScrollbarBg, (30, 30, 40, 255))  # Scrollbar background
            dpg.add_theme_color(dpg.mvThemeCol_ScrollbarGrab, BLUE)  # Scrollbar grab
            dpg.add_theme_color(dpg.mvThemeCol_ScrollbarGrabHovered, PINK)  # Scrollbar grab hover
            dpg.add_theme_color(dpg.mvThemeCol_ScrollbarGrabActive, YELLOW)  # Scrollbar grab active

            # Header and Separator
            dpg.add_theme_color(dpg.mvThemeCol_Header, PURPLE)  # Header
            dpg.add_theme_color(dpg.mvThemeCol_HeaderHovered, BLUE)  # Header hover
            dpg.add_theme_color(dpg.mvThemeCol_HeaderActive, YELLOW)  # Header active
            dpg.add_theme_color(dpg.mvThemeCol_Separator, PINK)  # Separator

            # Specialized Categories
            dpg.add_theme_color(dpg.mvPlotCol_Line, BLUE, category=dpg.mvThemeCat_Plots)  # Plot line
            dpg.add_theme_color(dpg.mvNodeCol_NodeBackground, (50, 50, 60, 255), category=dpg.mvThemeCat_Nodes)  # Node background
            dpg.add_theme_color(dpg.mvNodeCol_NodeOutline, PURPLE, category=dpg.mvThemeCat_Nodes)  # Node outline

            # Styles
            dpg.add_theme_style(dpg.mvStyleVar_WindowRounding, 6)
            dpg.add_theme_style(dpg.mvStyleVar_FrameRounding, 4)
            dpg.add_theme_style(dpg.mvStyleVar_ScrollbarRounding, 4)
            dpg.add_theme_style(dpg.mvStyleVar_GrabRounding, 4)
            
            dpg.add_theme_style(dpg.mvStyleVar_ItemSpacing, 18, 18) 
    return theme_id