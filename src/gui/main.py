#import customtkinter
from tkinter import ttk
import tkinter as tk
import ttkbootstrap as ttk

# def printhello():
#     print(entryInt.get())
def valueentry():
    print(entryint.get())
    entrystr.set('test')

window= ttk.Window(themename='darkly')
window.title('test')
window.geometry('200x200')
button = ttk.Button (window,text="click",command=valueentry)
entryint = tk.IntVar()
entryframeint = ttk.Entry(window,
				  textvariable=entryint)

entrystr = tk.StringVar()
entryframestr = ttk.Label(window,
						  textvariable=entrystr,
						  text='test')
entryframestr.pack()
entryframeint.pack()
button.pack()

#title one div for the text
label = ttk.Label(window, text='Test', font='Cambria 12 italic')
label.pack()

#one big div for ex 2 widg for him
input_frame = ttk.Frame(window)
entryInt = tk.IntVar()
entry = ttk.Entry(input_frame, textvariable=entryInt)
entry.pack(side='top',padx=10)
button.pack(side='left')
input_frame.pack(pady=20)
output_label = ttk.Label(window, text='output test')
output_label.pack()
window.mainloop()


















# #main window config



# app = customtkinter.CTk()
# app.geometry("800x400")
# app.title("GUI Test")

# #themes config
# customtkinter.set_appearance_mode("dark") #system, light, dark
# customtkinter.set_default_color_theme("dark-blue") #blue, dark-blue

# #testbutton
# testseg = customtkinter.CTkSegmentedButton(app, text_color="black")

# labelbut = customtkinter.CTkLabel(app, text="hello")
# labelbut.pack(pady=20)
# testbut = customtkinter.CTkButton(app, command="test")
# testbut.pack(pady=80)

# #mainloop needed for execution
# app.mainloop()

