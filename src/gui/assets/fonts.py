import dearpygui.dearpygui as dpg
from typing import Union

fonts = {}
def load_fonts():
        with dpg.font_registry():
            
            fonts["Conthrax-SemiBold"] = dpg.add_font("./assets/Conthrax-SemiBold.otf", 22)
            fonts["Average-Regular"] = dpg.add_font("./assets/Average-Regular.ttf", 29)
            fonts["Default"] = dpg.add_font("./assets/JetBrainsMono.ttf", 24)
            
def reset_font_binding(font_name: str = None):
    dpg.bind_font(0)
    dpg.bind_font(fonts["Default"])

    if font_name and font_name in fonts:
        dpg.bind_font(fonts[font_name])