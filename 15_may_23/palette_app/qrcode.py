import customtkinter
import PIL.Image
from PIL import ImageTk

import datetime
from datetime import datetime,timedelta
import os
import sqlite3 as sq

import hashlib
from tkinter import filedialog
import pyqrcode

from tkinter import *

from configparser import ConfigParser
import pickle

import tkinter.messagebox as ms




def qr_generator():
    def load_image(path, image_size):
        """ load rectangular image with path relative to PATH """
        return ImageTk.PhotoImage(PIL.Image.open(path).resize((image_size, image_size)))


    app_wind=customtkinter.CTkToplevel()
    app_wind.title("QR-Code Generator")

    app_wind.geometry("300x200+460+200")
    app_wind.maxsize(300,200)
    app_wind.minsize(300,200)
    app_wind.iconbitmap(r'gearbox.ico')
    app_wind.focus_set()
    app_wind.grab_set()

    customtkinter.set_appearance_mode("dark")  # Modes: "System" (standard), "Dark", "Light"
    customtkinter.set_default_color_theme("green")  # Themes:
    #---------declarations-------------------------

    today=datetime.now()
    #today= datetime.now()
    datetimenow=today.strftime('%d-%B-%Y')


    # configure grid layout (2x1)
    app_wind.grid_columnconfigure(0, weight=1)
    app_wind.grid_rowconfigure(0, weight=1)


    #--------------------function--------------------------------------


    def generate():
        from pyzbar import pyzbar
        from pyzbar.pyzbar import decode

        if code_entry.get()!="":





            input_path= filedialog.asksaveasfilename(title="Save QRCode",filetype=(("PNG File",".png"),("All Files","*.*")))

            if input_path:
                if input_path.endswith(".png"):
                    get_code=pyqrcode.create(code_entry.get())
                    get_code.png(input_path,scale=5)
                    ms.showinfo("Qr Code","Code Generated Successfully!")
                else:
                    input_path=f"{input_path}.png"
                    get_code=pyqrcode.create(code_entry.get())
                    get_code.png(input_path,scale=5)
                    ms.showinfo("Qr Code","Code Generated Successfully!")


        else:
            ms.showerror("Generate QR-Code","Please Enter Data")





    detail_icon = load_image("logout_side.png", 15)

    top_right = customtkinter.CTkFrame(master=app_wind,height=50,width=200,fg_color='#aebaca')
    top_right.grid(row=0, column=0, sticky="nswe")


    space=customtkinter.CTkLabel(master=top_right,text="",fg_color='#aebaca')
    space.grid(column=0,row=0,pady=20,padx=10)

    label_prev_sub=customtkinter.CTkLabel(master=top_right,text="",fg_color='#aebaca',text_color='black')
    label_prev_sub.place(y=10,x=2)


    frame_right = customtkinter.CTkFrame(master=top_right,height=150,width=280)
    frame_right.place(y=40,x=10)

    code_entry = customtkinter.CTkEntry(master=frame_right,width=220,placeholder_text="Enter Data")
    code_entry.place(y=50,x=36)

    subscribe_btn = customtkinter.CTkButton(master=frame_right,fg_color="#a36da2", hover_color="#eaa2e9",
                                            text="Generate",command=generate)
    subscribe_btn.place(y=100,x=80)



    #app_wind.mainloop()


