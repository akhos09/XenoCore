import os

import dearpygui.dearpygui as dpg

# ------- Storage dict for the fonts ------- 
fonts = {} 

def load_fonts():
        with dpg.font_registry():
            
            fonts["Conthrax-SemiBold"] = dpg.add_font(os.path.join(os.path.dirname(__file__), "../../assets/fonts/Conthrax-SemiBold.otf"), 18)
            fonts["Average-Regular"] = dpg.add_font(os.path.join(os.path.dirname(__file__),"../../assets/fonts/Average-Regular.ttf"), 29)
            fonts["Default"] = dpg.add_font(os.path.join(os.path.dirname(__file__),"../../assets/fonts/JetBrainsMono.ttf"), 24)
            
def reset_font_binding(font_name: str = None):
    dpg.bind_font(0)
    dpg.bind_font(fonts["Default"])

    if font_name and font_name in fonts:
        dpg.bind_font(fonts[font_name])