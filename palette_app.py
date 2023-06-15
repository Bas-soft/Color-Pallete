import tkinter as tk
import requests
import customtkinter
import random
from colorharmonies import Color,complementaryColor,triadicColor,splitComplementaryColor,tetradicColor,analogousColor,monochromaticColor
import PIL.Image
from PIL import ImageTk, Image,ImageDraw,ImageFont,ImageColor
from textblob import TextBlob

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

# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

#---------------database file creation-----------------
db9=sq.connect('./dbs/System.db')
cc9=db9.cursor()
cc9.execute('''CREATE TABLE IF NOT EXISTS subscription(ID integer PRIMARY KEY,dateSubscription TEXT)''')
db9.commit()
db9.close()

db10=sq.connect('./dbs/serial_keys.db')
cc10=db10.cursor()
cc10.execute('''CREATE TABLE IF NOT EXISTS keys(ID integer PRIMARY KEY,keys_codes TEXT)''')
db10.commit()
db10.close()

db11=sq.connect('./dbs/temp_colors.db')
cc11=db11.cursor()
cc11.execute('''CREATE TABLE IF NOT EXISTS temp_colors(ID integer PRIMARY KEY,Color_hex TEXT)''')
db11.commit()
db11.close()




class TkinterAnimation:
    def __init__(self, widget, property_name, end_value, duration):
        self.widget = widget
        self.property_name = property_name
        self.start_value = self.widget.cget(self.property_name)
        self.end_value = end_value
        self.duration = duration
        self.start_time = None

    def start(self):
        self.start_time = self.widget.after(0)
        self.update()

    def update(self):
        elapsed_time = self.widget.after(0) - self.start_time
        if elapsed_time >= self.duration:
            self.widget.config({self.property_name: self.end_value})
        else:
            # Calculate the current value based on the elapsed time
            current_value = self.calculate_current_value(elapsed_time)
            self.widget.config({self.property_name: current_value})
            self.widget.after(10, self.update)  # Update every 10 milliseconds

    def calculate_current_value(self, elapsed_time):
        # Perform interpolation calculation based on elapsed time
        start_value = float(self.start_value)
        end_value = float(self.end_value)
        return start_value + (end_value - start_value) * elapsed_time / self.duration







# Usage example
    '''
    root = tk.Tk()

    label = tk.Label(root, text="Hello", font=("Arial", 24))
    label.pack()

    animation = TkinterAnimation(label, "foreground", "red", 2000)  # Animate foreground color to red over 2 seconds
    animation.start()

    root.mainloop()'''


# Usage example
'''

root = tk.Tk()

label = tk.Label(root, text="Hello", font=("Arial", 24))
label.pack()

animation = TkinterAnimation(label, "foreground", "red", 2000)  # Animate foreground color to red over 2 seconds
animation.start()

root.mainloop()
'''

def gen_color(n):
    rgb_values=[]
    hex_value=[]

    r=int(random.random()*256)
    g = int(random.random() * 256)
    b = int(random.random() * 256)

    step=256/n

    for _ in range(n):
        r+=step
        g+=step
        b +=step
        r =int(r)% 256
        g = int(r) % 256
        b = int(r) % 256

        r_hex =hex(r)[2:]
        g_hex = hex(g)[2:]
        b_hex = hex(b)[2:]

        hex_value.append('#'+ r_hex +g_hex+b_hex)
        rgb_values.append((r,g,b))
        return rgb_values, hex_value

def show_values():
    rgbval,hexval=gen_color(6)
    print(rgbval, rgbval)

def module_color():
    cyan=Color([0,255,255],'','')
    com_palette=triadicColor(cyan)
    print(com_palette)




class compare_colors:
    def check_color_combination(colors):
        # Convert colors to RGB tuples
        rgb_colors = [ImageColor.getrgb(c) for c in colors]

        # Check color contrast
        contrast_ratio = compare_colors.calculate_color_contrast(rgb_colors[0], rgb_colors[1])

        # Check color similarity
        similarity = compare_colors.calculate_color_similarity(rgb_colors)

        # Return the evaluation results
        return contrast_ratio, similarity


    def calculate_color_contrast(color1, color2):
        # Convert RGB values to relative luminance
        # higher value indicates better contrast
        luminance1 = compare_colors.calculate_relative_luminance(color1)
        luminance2 = compare_colors.calculate_relative_luminance(color2)

        # Calculate the contrast ratio
        contrast_ratio = (luminance1 + 0.05) / (luminance2 + 0.05)

        return contrast_ratio


    def calculate_relative_luminance(color):
        # Calculate relative luminance based on RGB values
        r, g, b = color
        luminance = (0.2126 * (r / 255) + 0.7152 * (g / 255) + 0.0722 * (b / 255))

        return luminance


    def calculate_color_similarity(colors):
        # Calculate color similarity based on RGB Euclidean distance
        """ a higher similarity value indicates that
        the colors are closer in terms of their appearance, potentially resulting in a more
        harmonious or cohesive color  scheme."""

        similarity = 0
        count = 0

        for i in range(len(colors)):
            for j in range(i + 1, len(colors)):
                similarity += compare_colors.calculate_euclidean_distance(colors[i], colors[j])
                count += 1

        similarity /= count

        return similarity


    def calculate_euclidean_distance(color1, color2):
        # Calculate Euclidean distance between two RGB colors
        r1, g1, b1 = color1
        r2, g2, b2 = color2
        distance = ((r1 - r2) ** 2 + (g1 - g2) ** 2 + (b1 - b2) ** 2) ** 0.5

        return distance


# Example usage
user_colors = ['#FF0000', '#00FF00', '#0000FF']  # User-selected colors

contrast_ratio, similarity = compare_colors.check_color_combination(user_colors)

print("Contrast Ratio:", contrast_ratio)
print("Color Similarity:", similarity)


def app():
    app_wind = customtkinter.CTk()
    app_wind.title("GearBox")

    app_wind.geometry("1500x740+10+10")
    app_wind.maxsize(1500, 740)
    app_wind.minsize(1500, 740)
    app_wind.iconbitmap(r'gearbox.ico')
    app_wind.focus_set()
    app_wind.grab_set()
    #app_wind.configure(fg_color='#aebaca')

    #declare global variables
    global check_floating_frame
    check_floating_frame=0

    #-----------------system check fuunctions---------------------
    def check_expiry():
        today = datetime.now()
        #today= datetime.now()
        datetimenow = today.strftime('%d-%B-%Y')

        conn11 = sq.connect("./dbs/System.db")
        cur11 = conn11.cursor()
        cur11.execute("SELECT dateSubscription FROM subscription")
        data = cur11.fetchall()

        last_date = ""
        for i in data:
            last_date = i[0]

        db_date = datetime.strptime(last_date, '%d-%B-%Y')
        db_date = db_date + timedelta(days=180)

        diff = db_date - datetime.strptime(datetimenow, '%d-%B-%Y')

        if datetime.strptime(datetimenow, '%d-%B-%Y') > db_date:
            ms.showerror("Product Subscription", "Sorry Your Product Has Expired, Please Contact The Developer")
            image_color_btn.configure(state='disabled')
            qr_code_btn.configure(state='disabled')
            generate_btn.configure(state='disabled')
            generate_pair_btn.configure(state='disabled')

    def save_start_date():
        today = datetime.now()
        # today= datetime.now()
        datetimenow = today.strftime('%d-%B-%Y')

        conn11 = sq.connect("./dbs/System.db")
        cur11 = conn11.cursor()
        cur11.execute("SELECT * FROM subscription")

        if not cur11.fetchall():
            conn11.execute("INSERT INTO subscription (dateSubscription) VALUES (?)", (datetimenow,))
            conn11.commit()
            conn11.close()


        else:
            pass
            conn11.close()

    def subscribe():
        # cJ1a-Zbk1-bJ1a-cbJd-kbd1
        # 4bGH-kLcc-kLH9-bbcL-FcHk
        # 0LbZ-ccdd-dc4L-dd2J-LkZG
        # aId4-bFbI-GLkZ-ZkdJ-IJaa
        app_wind = customtkinter.CTkToplevel()
        app_wind.title("Subscriptions")

        app_wind.geometry("500x200+460+200")
        app_wind.maxsize(500, 200)
        app_wind.minsize(500, 200)
        app_wind.iconbitmap(r'gearbox.ico')
        app_wind.focus_set()
        app_wind.grab_set()

        # ---------declarations-------------------------

        today = datetime.now()
        # today= datetime.now()
        datetimenow = today.strftime('%d-%B-%Y')

        conn11 = sq.connect("./dbs/System.db")
        cur11 = conn11.cursor()
        cur11.execute("SELECT dateSubscription FROM subscription")
        data = cur11.fetchall()

        conn11.close()
        prev_subscription = ""
        for i in data:
            prev_subscription = i[0]

        # -----------------functions-------------------
        def verify(key):
            global score
            global score_2
            alphanumeric = 'abcdEFGHIJkLZ123490'

            score = 0
            last_four_score = 0
            each_chunk = 0

            check_digit = key[1]
            check_digit_occurrances = 0

            check_digit2 = key[3]
            check_digit_occurrances2 = 0

            # separate blobs
            chunks = key.split('-')
            idk = key[-1]

            _chunk_score_set = 0
            for chunk in chunks:
                if len(chunk) != 4:
                    return False

                for letter in chunk:
                    _chunk_score_set += ord(letter)
                    if _chunk_score_set > 220 and _chunk_score_set < 330:
                        each_chunk += 1
                for char in chunk:
                    if char not in alphanumeric:
                        break
                        ms.showerror("Activation Code", "Please Enter a Valid Key")
                    elif char == check_digit:
                        check_digit_occurrances += 1
                    elif char == check_digit2:
                        check_digit_occurrances2 += 1

                    score += ord(char)

            last_digits = key[-4:]
            for i in last_digits:
                last_four_score += ord(i)

            if score > 1700 and score < 1740 and check_digit_occurrances == 3 and each_chunk > 1:  # [-3]==check_digit2:
                conn12 = sq.connect("./dbs/Serial_Keys.db")
                cur12 = conn12.cursor()
                cur12.execute("INSERT INTO keys (keys_codes) VALUES(?)", [key])
                conn12.commit()
                conn12.close()

                # ----update expiry date--------------
                conn11 = sq.connect("./dbs/System.db")
                cur11 = conn11.cursor()
                cur11.execute("UPDATE  subscription SET dateSubscription=? WHERE ID=?", [datetimenow, 1])
                conn11.commit()
                conn11.close()
                ms.showinfo("Activation Key", "Successfully Activated!")
                # configure buttons
                subscribe_btn.configure(state="normal")


                app_wind.destroy()
                return True
            else:
                ms.showerror("Activation Key", "Please Enter a Valid Key")

        def activate():
            if code_entry.get() and len(code_entry.get()) == 24:
                key = code_entry.get()
                conn12 = sq.connect("./dbs/Serial_Keys.db")
                cur12 = conn12.cursor()
                cur12.execute("SELECT *  FROM keys WHERE keys_codes=?", [key])

                if cur12.fetchall():
                    ms.showerror("Activation Key", "Sorry! The Subscription Code Has Expired")
                    conn12.close()
                else:
                    verify(key)
                    image_color_btn.configure(state='normal')
                    qr_code_btn.configure(state='normal')
                    generate_btn.configure(state='normal')
                    generate_pair_btn.configure(state='normal')


            else:
                ms.showerror("Activation Code", "Please Enter a Valid Code")

        # configure grid layout (2x1)
        app_wind.grid_columnconfigure(0, weight=1)
        app_wind.grid_rowconfigure(0, weight=1)

        top_right = customtkinter.CTkFrame(master=app_wind, height=50, width=200, fg_color='#aebaca')
        top_right.grid(row=0, column=0, sticky="nswe")

        space = customtkinter.CTkLabel(master=top_right, text="", fg_color='#aebaca')
        space.grid(column=0, row=0, pady=20, padx=10)

        label_prev_sub = customtkinter.CTkLabel(master=top_right, text=f"({prev_subscription})", fg_color='#aebaca',
                                                text_color='black')
        label_prev_sub.place(y=10, x=2)

        frame_right = customtkinter.CTkFrame(master=top_right, height=150, width=480)
        frame_right.place(y=40, x=10)

        code_entry = customtkinter.CTkEntry(master=frame_right, width=400, placeholder_text="Enter Subscription Code")
        code_entry.place(y=50, x=36)

        subscribe_btn = customtkinter.CTkButton(master=frame_right, fg_color="#a36da2", hover_color="#eaa2e9",
                                                text="Activate", command=activate)
        subscribe_btn.place(y=100, x=170)

    def on_clicked_(widget):
        c_name=widget.cget('text')
        print(c_name)


    #generate color function
    global gen_rgbs
    gen_rgbs=[]

    def monochromatic_gradient(start_color,end_color,steps=15,brightness_range=(0.2,0.8)):
        import colorsys
        from colormap import rgb2hex, rgb2hls, hls2rgb
        global color_gen
        global rgb_monochrome
        base_hsv=colorsys.rgb_to_hsv(*start_color)
        #-----calculating the brightness step----------------------------
        step_size=(brightness_range[1]-brightness_range[0])/(steps-1)

        color_gen=[]
        rgb_monochrome=[]
        for i in range(steps):
            bright=brightness_range[0]+(step_size*i)

            c=colorsys.hsv_to_rgb(base_hsv[0],base_hsv[1],bright)
            c=tuple(int(co *255) for co in c)
            #print(c)
            cc=rgb2hex(int(c[0]), int(c[1]), int(c[2]))
            #
            color_gen.append(cc)
            rgb_monochrome.append(list(c))



        return color_gen
        return rgb_monochrome

    def specify():
        global com_palette
        from colormap import rgb2hex, rgb2hls, hls2rgb

        if not color_entry.get():
            ms.showerror("Oops!","Please Enter a HEX Color Value")
        else:

            get_hex=color_entry.get().lstrip("#")
            lv=len(get_hex)
            conv_color=tuple(int(get_hex[i:i + lv // 3],16) for i in range(0,lv,lv//3))
            conv2=tuple(int(get_hex[i:i+2], 16) for i in (0,2,4))

            rgb_values=[conv2[0],conv2[1],conv2[2]]



            cyan=Color(rgb_values,'','')

            if select.get()=="Analogue Colors":
                com_palette = analogousColor(cyan)
            elif select.get()=="Triadic Colors":
                com_palette = triadicColor(cyan)
            elif select.get() == "Complementary Colors":
                com_palette = list([complementaryColor(cyan)])
            elif select.get() == "Split Complementary Colors":
                com_palette = splitComplementaryColor(cyan)
            elif select.get() == "Tetradic Colors":
                com_palette = tetradicColor(cyan)
            elif select.get() == "Monochromatic Colors":
                com_palette = monochromaticColor(cyan)
            com_palette.append(rgb_values)

            gen_rgbs=[]
            gen_rgbs.append(com_palette)

            c_col = 0
            c_row = 0
            l_col = 0
            l_row = 0

            if select.get() == "Monochromatic Colors":

                end = (255, 255, 255)
                # print(start,end)
                monochromatic_gradient(rgb_values, end)
                com_palette = color_gen
            else:
                pass
            for widget in color_frame.winfo_children():
                widget.destroy()
            '''if select.get() == "Complementary Colors":
                color = f'#{com_palette[0]:02x}{com_palette[1]:02x}{com_palette[2]:02x}'
                color_label = customtkinter.CTkLabel(color_frame, fg_color=color, width=126, height=80, text='')
                color_label.grid(row=0, column=c_col, padx=5, pady=15)
                hex_label = customtkinter.CTkLabel(color_frame, text=color, width=10)
                hex_label.grid(row=1, column=l_col, pady=15, padx=5)
    
                color2 = f'#{rgb_values[0]:02x}{rgb_values[1]:02x}{rgb_values[2]:02x}'
                color_label2 = customtkinter.CTkLabel(color_frame, fg_color=color2, width=126, height=80, text='')
                color_label2.grid(row=0, column=1, padx=5, pady=15)
                hex_label2 = customtkinter.CTkLabel(color_frame, text=color2, width=10)
                hex_label2.grid(row=1, column=1, pady=15, padx=5)
            else:
                pass'''
            for i in com_palette:
                if select.get() == "Monochromatic Colors":
                    color = i
                else:
                    color = f'#{i[0]:02x}{i[1]:02x}{i[2]:02x}'

                #color = f'#{i[0]:02x}{i[1]:02x}{i[2]:02x}'
                if select.get() == "Monochromatic Colors":
                    width_w = 65
                    height_w = 90
                    pad_x = 2
                else:
                    width_w = 126
                    height_w = 80
                    pad_x = 5

                color_label = customtkinter.CTkLabel(color_frame, fg_color=color, width=width_w, height=height_w,
                                                     text='',corner_radius=15)
                color_label.grid(row=c_row, column=c_col, padx=pad_x, pady=15)

                hex_label_entry = customtkinter.CTkEntry(color_frame, fg_color='#0e1821', width=100,text_color=color, \
                                                         border_color='#0e1821', border_width=0)
                hex_label_entry.grid(row=2, column=l_col, padx=pad_x)

                hex_label_entry.delete(0, END)
                hex_label_entry.insert(0, color)
                c_col += 1
                l_col += 1

            if select.get() == "Monochromatic Colors":
                com_palette = rgb_monochrome
            else:
                pass
            return com_palette

            return color_label

    def gen():
        global com_palette
        global color_label

        r = random.randint(0, 255)
        g = random.randint(0, 255)
        b = random.randint(0, 255)

        rgb_value=[r, g, b]

        cyan = Color(rgb_value, '', '')


        if select.get()=="Analogue Colors":
            com_palette = analogousColor(cyan)
        elif select.get()=="Triadic Colors":
            com_palette = triadicColor(cyan)
        elif select.get() == "Complementary Colors":
            com_palette = list([complementaryColor(cyan)])
        elif select.get() == "Split Complementary Colors":
            com_palette = splitComplementaryColor(cyan)
        elif select.get() == "Tetradic Colors":
            com_palette = tetradicColor(cyan)
        elif select.get() == "Monochromatic Colors":
            com_palette = monochromaticColor(cyan)

        com_palette.append(rgb_value)
        #print(com_palette)



        gen_rgbs=com_palette
        #print(gen_rgbs)

        c_col=0
        c_row=0
        l_col=0
        l_row=0

        count_col=0

        if select.get() == "Monochromatic Colors":
            color_start = f'#{rgb_value[0]:02x}{rgb_value[1]:02x}{rgb_value[2]:02x}'
            print(f'start_color: {color_start}')
            end=(255,255,255)
            #print(start,end)
            monochromatic_gradient(rgb_value,end)
            com_palette=color_gen
        else:
            pass

        def click_me():

            butn=color_label.cget('fg_color')
            print(butn)


        global color_label
        for widget in color_frame.winfo_children():
            widget.destroy()

        '''if select.get() == "Complementary Colors":
            color = f'#{com_palette[0]:02x}{com_palette[1]:02x}{com_palette[2]:02x}'
            color_label = customtkinter.CTkLabel(color_frame, fg_color=color, width=126, height=80, text='')
            color_label.grid(row=0, column=c_col, padx=5, pady=15)


            hex_label = customtkinter.CTkLabel(color_frame, text=color, width=10)
            hex_label.grid(row=1, column=l_col, pady=5, padx=15)

            color2 = f'#{rgb_value[0]:02x}{rgb_value[1]:02x}{rgb_value[2]:02x}'
            color_label2 = customtkinter.CTkLabel(color_frame, fg_color=color2, width=126, height=80, text='')
            color_label2.grid(row=0, column=1, padx=5, pady=15)
            hex_label2 = customtkinter.CTkLabel(color_frame, text=color2, width=10)
            hex_label2.grid(row=1, column=1, pady=15, padx=5)

        else:
            pass'''
        for i in com_palette:
            if select.get()=="Monochromatic Colors":
                color=i
            else:
                color = f'#{i[0]:02x}{i[1]:02x}{i[2]:02x}'
            if select.get()=="Monochromatic Colors":
                width_w=65
                height_w=90
                pad_x=2
            else:
                width_w = 126
                height_w = 80
                pad_x = 5

            color_label = customtkinter.CTkButton(color_frame, fg_color=color, width=width_w, height=height_w,\
                                                  hover_color=color,text='',corner_radius=15,command=click_me)

            color_label.grid(row=c_row, column=c_col, padx=pad_x, pady=15)
            hex_label_entry=customtkinter.CTkEntry(color_frame,fg_color='#0e1821',width=100,text_color=color,\
                                                   border_color='#0e1821',border_width=0)
            hex_label_entry.grid(row=2, column=l_col, padx=pad_x)

            hex_label_entry.delete(0,END)
            hex_label_entry.insert(0,color)


            c_col+=1
            l_col+=1



        if select.get()=="Monochromatic Colors":
            com_palette=rgb_monochrome
        else:
            pass
        return com_palette

        return color_label

    def generate_pairs():
        global full_palette
        if not color_entry.get():
            ms.showerror('Oops!',"Please Enter a Hex Color Value")

        else:

            type_one=_type_one.get()
            type_two=_type_two.get()

            #get hex value from entered RGB
            get_hex = color_entry.get().lstrip("#")
            lv = len(get_hex)
            conv2 = tuple(int(get_hex[i:i + 2], 16) for i in (0, 2, 4))

            rgb_values = [conv2[0], conv2[1], conv2[2]]

            cyan = Color(rgb_values, '', '')

            #-------------generate color palette for type one------------------------

            if _type_one.get()=="Analogue Colors":
                com_palette1 = analogousColor(cyan)
            elif _type_one.get()=="Triadic Colors":
                com_palette1 = triadicColor(cyan)
            elif _type_one.get() == "Complementary Colors":
                com_palette1 = list([complementaryColor(cyan)])
            elif _type_one.get() == "Split Complementary Colors":
                com_palette1 = splitComplementaryColor(cyan)
            elif _type_one.get() == "Tetradic Colors":
                com_palette1 = tetradicColor(cyan)
            elif _type_one.get() == "Monochromatic Colors":
                com_palette1 = monochromaticColor(cyan)


            ##1dc72f
            # -----------------------generate color palette for type two-------------------------

            if _type_two.get()=="Analogue Colors":
                com_palette_two = analogousColor(cyan)
            elif _type_two.get()=="Triadic Colors":
                com_palette_two = triadicColor(cyan)
            elif _type_two.get() == "Complementary Colors":
                com_palette_two = list([complementaryColor(cyan)])
            elif _type_two.get() == "Split Complementary Colors":
                com_palette_two = splitComplementaryColor(cyan)
            elif _type_two.get() == "Tetradic Colors":
                com_palette_two = tetradicColor(cyan)
            elif _type_two.get() == "Monochromatic Colors":
                com_palette_two = monochromaticColor(cyan)

            com_palette_two.append(rgb_values)
            full_palette=com_palette_two+com_palette1
            #print(full_palette)
            #print(com_palette_two)
            #print(com_palette)

            c_col = 0
            c_row = 0
            l_col = 0
            l_row = 0



            for widget in colorPair_frame.winfo_children():
                widget.destroy()
            '''if select.get() == "Complementary Colors":
                color = f'#{com_palette[0]:02x}{com_palette[1]:02x}{com_palette[2]:02x}'
                color_label = customtkinter.CTkLabel(color_frame, fg_color=color, width=126, height=80, text='')
                color_label.grid(row=0, column=c_col, padx=5, pady=15)
                hex_label = customtkinter.CTkLabel(color_frame, text=color, width=10)
                hex_label.grid(row=1, column=l_col, pady=15, padx=5)

                color2 = f'#{rgb_values[0]:02x}{rgb_values[1]:02x}{rgb_values[2]:02x}'
                color_label2 = customtkinter.CTkLabel(color_frame, fg_color=color2, width=126, height=80, text='')
                color_label2.grid(row=0, column=1, padx=5, pady=15)
                hex_label2 = customtkinter.CTkLabel(color_frame, text=color2, width=10)
                hex_label2.grid(row=1, column=1, pady=15, padx=5)
            else:
                pass'''
            for i in full_palette:
                color = f'#{i[0]:02x}{i[1]:02x}{i[2]:02x}'

                width_w = 126
                height_w = 80
                pad_x = 5

                color_label2 = customtkinter.CTkLabel(colorPair_frame, fg_color=color, width=width_w, height=height_w,
                                                     text='',corner_radius=15)
                color_label2.grid(row=c_row, column=c_col, padx=pad_x, pady=15)

                hex_label_entry = customtkinter.CTkEntry(colorPair_frame, fg_color='#0e1821', width=100, text_color=color,\
                                                         border_color='#0e1821', border_width=0)
                hex_label_entry.grid(row=2, column=l_col, padx=pad_x)

                hex_label_entry.delete(0, END)
                hex_label_entry.insert(0, color)
                c_col += 1
                l_col += 1

            return full_palette
            return color_label2
            return hex_label2

    def adjust_lightness(r,g,b,factor):
        global new_rgb
        from colormap import rgb2hex,rgb2hls,hls2rgb
        h,l,s = rgb2hls(r/255.0,g/255.0,b/255.0)
        l=max(min(l*factor,1.0),0.0)
        r,g,b=hls2rgb(h,l,s)

        new_rgb=rgb2hex(int(r*255),int(g*255),int(b*255))


        return new_rgb

    def adjust_rgb(r,g,b,factor):
        global new_rgb_value
        fact_r=(factor/r)*int(255)
        fact_g = (factor / g) * int(255)
        fact_b = (factor / b) * int(255)
        if r>0 :
            r+=fact_r
        elif r<255:
            r=r-fact_r

        if g>0 :
            g+=fact_g
        elif g<255:
            g=g-fact_g

        if b>0 :
            b+=fact_b
        elif b<255:
            b=b-fact_b

        return new_rgb_value

    def adjust_rgb_two(r,g,b ,factor):
        from colormap import rgb2hex, rgb2hls, hls2rgb
        global rgb_new
        rgb_new=[]
        fact=(factor/100)  * 255

        if r>0 :
            r-=fact
            if r<0:
                r=0


        if g>0 :
            g+=fact
            if g>255:
                g=  255


        if b>0 :
            b+=fact
            if b>255:
                b=  255


        if r>255:
            r=255
        elif g >255:
            g=255
        elif b >255:
            b=255
        else:
            pass


        global new
        new = rgb2hex(int(r), int(g), int(b))

        #new=[round(r),round(g),round(b)]
        #rgb_new.append(new)


        return new

    def slider_func(value):
        c_col = 0
        c_row = 0
        l_col = 0
        round_number=round(value)
        value_label_rgb.configure(text=f'{round_number}%')
        lil_rgbs=[]


        for i in com_palette:
            color = i
            r = color[0]
            g = color[1]
            b = color[2]

            adjust_rgb_two(r,g,b,value)
            lil_rgbs.append(new)
        # print(lil_rgbs)
        for widget in color_frame.winfo_children():
            widget.destroy()

        for i in lil_rgbs:
            color=i

            if select.get() == "Monochromatic Colors":
                width_w = 65
                height_w = 90
                pad_x = 2
            else:
                width_w = 126
                height_w = 80
                pad_x = 5

            color_label = customtkinter.CTkLabel(color_frame, fg_color=color, width=width_w, height=height_w, text='',
                                                 corner_radius=15)
            color_label.grid(row=c_row, column=c_col, padx=pad_x, pady=15)

            hex_label_entry = customtkinter.CTkEntry(color_frame, fg_color='#0e1821', width=100,text_color=color, \
                                                     border_color='#0e1821', border_width=0)
            hex_label_entry.grid(row=2, column=l_col, padx=pad_x)

            hex_label_entry.delete(0, END)
            hex_label_entry.insert(0, color)
            c_col += 1
            l_col += 1

    def slider2_func(value):
        c_col = 0
        c_row = 0
        l_col = 0
        round_number=round(value)
        value_label_rgb2.configure(text=f'{round_number}%')
        lil_rgbs=[]



        for i in full_palette:
            color = i
            r = color[0]
            g = color[1]
            b = color[2]

            adjust_rgb_two(r,g,b,value)
            lil_rgbs.append(new)
        # print(lil_rgbs)
        for widget in colorPair_frame.winfo_children():
            widget.destroy()

        for i in lil_rgbs:
            color = i
            if select.get() == "Monochromatic Colors":
                width_w = 126
                height_w = 80
                pad_x = 5
            else:
                width_w = 126
                height_w = 80
                pad_x = 5

            color_label2 = customtkinter.CTkLabel(colorPair_frame, fg_color=color, width=width_w, height=height_w,
                                                  text='', corner_radius=15)
            color_label2.grid(row=c_row, column=c_col, padx=pad_x, pady=15)
            hex_label_entry = customtkinter.CTkEntry(colorPair_frame, fg_color='#0e1821', width=100,text_color=color, \
                                                     border_color='#0e1821', border_width=0)
            hex_label_entry.grid(row=2, column=l_col, padx=pad_x)

            hex_label_entry.delete(0, END)
            hex_label_entry.insert(0, color)
            c_col += 1
            l_col += 1

    def adj_bright(value):
        #print(com_palette)
        value_label.configure(text=value)
        lil=[]
        c_col = 0
        c_row = 0
        l_col = 0
        l_row = 0


        for i in com_palette:
            color=i
            r=color[0]
            g=color[1]
            b=color[2]

            adjust_lightness(r,g,b,value)
            lil.append(new_rgb)

        for widget in color_frame.winfo_children():
            widget.destroy()

        for i in lil:
            color=i
            if select.get() == "Monochromatic Colors":
                width_w = 65
                height_w = 90
                pad_x = 2
            else:
                width_w = 126
                height_w = 80
                pad_x = 5

            color_label = customtkinter.CTkLabel(color_frame, fg_color=color, width=width_w, height=height_w, text='',corner_radius=15)
            color_label.grid(row=c_row, column=c_col, padx=pad_x, pady=15)
            hex_label_entry = customtkinter.CTkEntry(color_frame, fg_color='#0e1821', width=100,text_color=color, \
                                                     border_color='#0e1821', border_width=0)
            hex_label_entry.grid(row=2, column=l_col, padx=pad_x)

            hex_label_entry.delete(0, END)
            hex_label_entry.insert(0, color)
            c_col += 1
            l_col += 1
            #widget[0].configure(fg_color=lil[0])

        #print(lil)


    def adj_bright_two(value):
        #print(com_palette)
        value_label2.configure(text=value)
        lil=[]
        c_col = 0
        c_row = 0
        l_col = 0
        l_row = 0
        for i in full_palette:
            color=i
            r=color[0]
            g=color[1]
            b=color[2]

            adjust_lightness(r,g,b,value)
            lil.append(new_rgb)

        for widget in colorPair_frame.winfo_children():
            widget.destroy()

        for i in lil:
            color=i

            if select.get() == "Monochromatic Colors":
                width_w = 126
                height_w = 80
                pad_x = 5
            else:
                width_w = 126
                height_w = 80
                pad_x = 5

            color_label2 = customtkinter.CTkLabel(colorPair_frame, fg_color=color, width=width_w, height=height_w, text='',corner_radius=15)
            color_label2.grid(row=c_row, column=c_col, padx=pad_x, pady=15)
            hex_label_entry = customtkinter.CTkEntry(colorPair_frame, fg_color='#0e1821', width=100,text_color=color, \
                                                     border_color='#0e1821', border_width=0)
            hex_label_entry.grid(row=2, column=l_col, padx=pad_x)

            hex_label_entry.delete(0, END)
            hex_label_entry.insert(0, color)
            c_col += 1
            l_col += 1
            #widget[0].configure(fg_color=lil[0])

        #print(lil)


    def open_qr_code_gui():
        import qrcode
        qrcode.qr_generator()

    def open_color_extraction():
        app_wind = customtkinter.CTkToplevel()
        app_wind.title("Color Extraction Tool")

        app_wind.geometry("1000x500+270+150")
        app_wind.maxsize(1000, 500)
        app_wind.minsize(1000, 500)
        app_wind.iconbitmap(r'gearbox.ico')
        app_wind.focus_set()
        app_wind.grab_set()

        frame_right = customtkinter.CTkFrame(master=app_wind)
        frame_right.pack(padx=20, pady=20)

        #----------------functions--------------------
        def browse():
            global data

            from tkinter import filedialog
            filename = filedialog.askopenfilename(initialdir="/", title="Select file", filetypes= \
                (("jpeg files", "*.jpg"), ("All files", "*.*")))

            # print (filename)
            _, extension = os.path.splitext(filename)
            data=filename


            return data

        def extract_func():
            global palette_list
            from colorthief import ColorThief
            color_list=[]
            ct= ColorThief(data)
            dominant_color=list(ct.get_color(quality=int(select_number.get())))
            color_palette=ct.get_palette(color_count=int(select_number.get()))

            palette_list=[]
            for i in color_palette:
                r=i[0]
                g=i[1]
                b=i[2]
                all_color=[r,g,b]
                palette_list.append(all_color)


            #print(palette_list)
            c_col = 0
            c_row = 0
            l_col = 0

            for widget in color_frame.winfo_children():
                widget.destroy()

            for widget in extract_color_frame.winfo_children():
                widget.destroy()

            for i in palette_list:

                color = f'#{i[0]:02x}{i[1]:02x}{i[2]:02x}'
                #print(color)

                width_w = 126
                height_w = 80
                pad_x = 5

                color_label = customtkinter.CTkLabel(extract_color_frame, fg_color=color, width=width_w, height=height_w, text='',
                                                     corner_radius=15)
                color_label.grid(row=c_row, column=c_col, padx=pad_x, pady=15)
                hex_label_entry = customtkinter.CTkEntry(extract_color_frame, fg_color='#0e1821', width=100,text_color=color, \
                                                         border_color='#0e1821', border_width=0)
                hex_label_entry.grid(row=2, column=l_col, padx=pad_x)

                hex_label_entry.delete(0, END)
                hex_label_entry.insert(0, color)

                #------------home palette---------------------------------
                color_label = customtkinter.CTkLabel(color_frame, fg_color=color, width=width_w, height=height_w,
                                                     text='', corner_radius=15)
                color_label.grid(row=c_row, column=c_col, padx=pad_x, pady=15)
                hex_label_entry2 = customtkinter.CTkEntry(color_frame, fg_color='#0e1821', width=100,text_color=color, \
                                                         border_color='#0e1821', border_width=0)
                hex_label_entry2.grid(row=2, column=l_col, padx=pad_x)

                hex_label_entry2.delete(0, END)
                hex_label_entry2.insert(0, color)
                c_col += 1
                l_col += 1

                c_col += 1
                l_col += 1
                #color_list.append([i])

            #color = f'#{dominant_color[0]:02x}{dominant_color[1]:02x}{dominant_color[2]:02x}'
            #print(color_list)
            return palette_list

        def adj_bright(value):
            # print(com_palette)
            value_label_image.configure(text=value)
            lil = []
            c_col = 0
            c_row = 0
            l_col = 0
            l_row = 0
            for i in palette_list:
                color = i
                r = color[0]
                g = color[1]
                b = color[2]

                adjust_lightness(r, g, b, value)
                lil.append(new_rgb)

            for widget in extract_color_frame.winfo_children():
                widget.destroy()

            for widget in color_frame.winfo_children():
                widget.destroy()

            for i in lil:
                color = i
                if select.get() == "Monochromatic Colors":
                    width_w = 126
                    height_w = 80
                    pad_x = 5
                else:
                    width_w = 126
                    height_w = 80
                    pad_x = 5

                color_label = customtkinter.CTkLabel(extract_color_frame, fg_color=color, width=width_w, height=height_w,
                                                     text='', corner_radius=15)
                color_label.grid(row=c_row, column=c_col, padx=pad_x, pady=15)
                hex_label_entry = customtkinter.CTkEntry(extract_color_frame, fg_color='#0e1821', width=100,text_color=color, \
                                                         border_color='#0e1821', border_width=0)
                hex_label_entry.grid(row=2, column=l_col, padx=pad_x)

                hex_label_entry.delete(0, END)
                hex_label_entry.insert(0, color)
                c_col += 1
                l_col += 1

                # ------------home palette---------------------------------
                color_label = customtkinter.CTkLabel(color_frame, fg_color=color, width=width_w, height=height_w,
                                                     text='', corner_radius=15)
                color_label.grid(row=c_row, column=c_col, padx=pad_x, pady=15)
                hex_label_entry2 = customtkinter.CTkEntry(color_frame, fg_color='#0e1821', width=100,text_color=color, \
                                                         border_color='#0e1821', border_width=0)
                hex_label_entry2.grid(row=2, column=l_col, padx=pad_x)

                hex_label_entry2.delete(0, END)
                hex_label_entry2.insert(0, color)
                c_col += 1
                l_col += 1
                # widget[0].configure(fg_color=lil[0])

            # print(lil)

        def slider3_func(value):

            c_col = 0
            c_row = 0
            l_col = 0
            round_number = round(value)
            value_label_rgb2.configure(text=f'{round_number}%')
            lil_rgbs = []
            for i in palette_list:
                color = i
                r = color[0]
                g = color[1]
                b = color[2]

                adjust_rgb_two(r, g, b, value)
                lil_rgbs.append(new)
            # print(lil_rgbs)
            for widget in color_frame.winfo_children():
                widget.destroy()

            for widget in extract_color_frame.winfo_children():
                widget.destroy()

            for i in lil_rgbs:
                color=i
                # print(color)

                width_w = 126
                height_w = 80
                pad_x = 5

                color_label = customtkinter.CTkLabel(extract_color_frame, fg_color=color, width=width_w,
                                                     height=height_w, text='',
                                                     corner_radius=15)
                color_label.grid(row=c_row, column=c_col, padx=pad_x, pady=15)
                hex_label_entry = customtkinter.CTkEntry(extract_color_frame, fg_color='#0e1821', width=100,text_color=color, \
                                                         border_color='#0e1821', border_width=0)
                hex_label_entry.grid(row=2, column=l_col, padx=pad_x)

                hex_label_entry.delete(0, END)
                hex_label_entry.insert(0, color)

                # ------------home palette---------------------------------
                color_label = customtkinter.CTkLabel(color_frame, fg_color=color, width=width_w, height=height_w,
                                                     text='', corner_radius=15)
                color_label.grid(row=c_row, column=c_col, padx=pad_x, pady=15)
                hex_label_entry2 = customtkinter.CTkEntry(color_frame, fg_color='#0e1821', width=100, text_color=color,\
                                                         border_color='#0e1821', border_width=0)
                hex_label_entry2.grid(row=2, column=l_col, padx=pad_x)

                hex_label_entry2.delete(0, END)
                hex_label_entry2.insert(0, color)
                c_col += 1
                l_col += 1

                c_col += 1
                l_col += 1
        # -------------------------add frame------------------------------------------------------
        add_menu_right = customtkinter.CTkFrame(master=frame_right)
        add_menu_right.grid(row=0, column=0, sticky="we", padx=20, pady=20)



        add_file_btn = customtkinter.CTkButton(master=add_menu_right, image=add_image, compound='left', text="Load Image",
                                     border_width=1.5,  # <- custom border_width
                                     corner_radius=5, width=900, height=120, fg_color="#1f1f1f", hover_color="#252525",
                                     border_color="#1b84a4",command=browse)
        add_file_btn.grid(padx=10)

        #----------------------options frame---------------------------
        option_frame = customtkinter.CTkFrame(master=app_wind)
        option_frame.pack(pady=5)

        select_number = customtkinter.CTkOptionMenu(master=option_frame, values=['2','3','4','5','6'], width=80)
        select_number.set('2')
        select_number.grid(row=0, column=0, padx=20, pady=10)

        generate_btn = customtkinter.CTkButton(master=option_frame, text='Extract', fg_color="#a36da2",
                                               hover_color="#eaa2e9",command=extract_func)
        generate_btn.grid(row=0, column=1, pady=10,padx=10)

        brightness_image = customtkinter.CTkSlider(master=option_frame, from_=0, to=2,command=adj_bright)
        brightness_image.grid(column=0, row=1, columnspan=3, pady=10)
        brightness_image.set(1)

        value_label_image = customtkinter.CTkLabel(master=option_frame, text='1')
        value_label_image.place(y=55, x=250)

        bright_rgb2 = customtkinter.CTkSlider(master=option_frame, from_=0, to=100, command=slider3_func)
        bright_rgb2.grid(column=0, row=2, columnspan=3)
        bright_rgb2.set(1)

        value_label_rgb2 = customtkinter.CTkLabel(master=option_frame, text='1%')
        value_label_rgb2.place(y=74, x=250)

        #--------------------extracted colors--------------------------------------
        extract_color_frame = customtkinter.CTkFrame(master=app_wind)
        extract_color_frame.pack(padx=20, pady=20)


    def open_details():
        pass

    def color_scheme_function():
        brightness.set(1)
        bright_rgb.set(1)
        value_label.configure(text='1')
        value_label_rgb.configure()

        if gen_type.get()=="Random":
            gen()

        elif gen_type.get()=="Specify":
            specify()

    def open_saved_palette():
        from colormap import rgb2hex, rgb2hls, hls2rgb
        # -----------------open temp colors into db---------------------------
        db11 = sq.connect('./dbs/temp_colors.db')
        cc11 = db11.cursor()
        cc11.execute('''SELECT * FROM temp_colors''')
        data=cc11.fetchall()

        #db11.commit()
        db11.close()



        # Create a customtkinter window
        window = customtkinter.CTkToplevel()
        window.geometry("1000x500+270+150")
        window.maxsize(1000, 500)
        window.minsize(1000, 500)
        window.iconbitmap(r'gearbox.ico')
        window.focus_set()
        window.grab_set()

        # Create a canvas to hold the scrollable content
        canvas = customtkinter.CTkCanvas(window, width=400, height=300)
        canvas.pack(side="left", fill="both", expand=True)

        # Create a scrollbar
        scrollbar = customtkinter.CTkScrollbar(window, command=canvas.yview)
        scrollbar.pack(side="right", fill="y")

        # Configure the canvas to scroll with the scrollbar
        canvas.configure(yscrollcommand=scrollbar.set)

        # Create a frame inside the canvas to hold the content
        content_frame = customtkinter.CTkFrame(canvas)
        canvas.create_window((0, 0), window=content_frame, anchor="nw")

        # Add some content to the frame
        color_palette=None
        for i in data:
            color=i[1].split(',')
            #print(color)
        for rgb in color:
            print(rgb)
            color_palette=color
        #for rgb in list(color):
         #   print(rgb)
            #hex = rgb2hex(int(color[0]), int(color[1]), int(color[2]))
            #print(hex)
        #for color_ in color_palette:
            #print(color_)
            #hex=rgb2hex(int(color_[0]), int(color_[1]), int(color_[2]))
            #label = customtkinter.CTkLabel(content_frame, text=f"Label {int(i[0]) + 1}",fg_color=hex)
            #label.pack()

        # Update the canvas scroll region when the content frame changes size
        def update_scroll_region(event):
            canvas.configure(scrollregion=canvas.bbox("all"))

        content_frame.bind("<Configure>", update_scroll_region)

        # Run the customtkinter event loop
        #window.mainloop()

    def add_palette_widget():
        global canvas
        from colormap import rgb2hex, rgb2hls, hls2rgb
        add_palette_function()


        if check_floating_frame==0:
            pass
        else:
            canvas.destroy()

        # Create a canvas to hold the scrollable content
        canvas = customtkinter.CTkCanvas(app_wind)
        canvas.place(y=80,x=360)



        # Create a frame inside the canvas to hold the content
        content_frame = customtkinter.CTkFrame(canvas)
        canvas.create_window((0, 0), window=content_frame, anchor="nw")

        # Create a scrollbar
        scrollbar = customtkinter.CTkScrollbar(content_frame, command=canvas.yview)
        scrollbar.place(y=10, x=280)

        # Configure the canvas to scroll with the scrollbar
        canvas.configure(yscrollcommand=scrollbar.set)

        #animation = TkinterAnimation(canvas, "width", 200, 2000)  # Animate foreground color to red over 2 seconds
        #animation.start()
        _row_=0
        _row_l=0
        for i in saved_colors:
            color = rgb2hex(int(i[0]), int(i[1]), int(i[2]))
            color_btn=customtkinter.CTkButton(content_frame,fg_color=color,text='',width=150,height=50)
            color_btn.grid(column=0,row=_row_,pady=5,padx=10)

            _row_+=1

            hex_label_entry = customtkinter.CTkEntry(content_frame, fg_color='#0e1821', width=100, text_color=color, \
                                                     border_color='#0e1821', border_width=0)
            hex_label_entry.grid(row=_row_l, column=1, padx=10,pady=5)

            hex_label_entry.delete(0, END)
            hex_label_entry.insert(0, color)
            _row_l+=1
            #print(color)
        #frame=customtkinter.CTkFrame()

        # Update the canvas scroll region when the content frame changes size
        def update_scroll_region(event):
            canvas.configure(scrollregion=canvas.bbox("all"))

        check_floating_frame+=1
        return check_floating_frame
        return canvas
        content_frame.bind("<Configure>", update_scroll_region)

    def add_palette_function():
        global saved_colors

        saved_colors=None


        if select.get()=="Monochromatic Colors":
            saved_colors=rgb_monochrome
        else:
            saved_colors=com_palette

        #-----------------save temp colors into db---------------------------

        return saved_colors

    def asset_generator(keyword):
        icon_size=(200,200)
        bg_color=(255,255,255)
        text_color=(0,0,0)

        image_d=Image.new("RGB",icon_size,bg_color)
        draw=ImageDraw.Draw(image_d)


        font_size=60
        font=ImageFont.truetype("path_to_font")
        pass

    def search_icon(keyword):



        # Set up the API endpoint and headers
        url = "https://api.iconfinder.com/v4/icons/search"
        headers = {"Authorization": "Bearer YOUR_API_KEY"}

        # Set the parameters for the API request
        params = {
            "query": keyword,
            "count": 1,  # Number of icons to retrieve
            "premium": False,  # Only retrieve free icons
            "vector": True,  # Only retrieve vector icons
        }

        # Send the API request
        response = requests.get(url, headers=headers, params=params)
        data = response.json()

        # Extract the icon details
        if "icons" in data and len(data["icons"]) > 0:
            icon = data["icons"][0]
            download_icon(icon["raster_sizes"][0]["formats"][0]["preview_url"])
        else:
            print("No icons found for the keyword:", keyword)

    def download_icon(icon_url):
        # Set the filename for the downloaded icon
        filename = "icon.png"

        # Download the icon file
        response = requests.get(icon_url)
        with open(filename, "wb") as f:
            f.write(response.content)

        print("Icon downloaded as", filename)

    # Replace "YOUR_API_KEY" with your actual API key from IconFinder





    #show_color((22,24,201))
    def load_image(path, image_size):
        #return Image.open(path).resize((image_size, image_size))
        """ load rectangular image with path relative to PATH """
        return customtkinter.CTkImage(PIL.Image.open(path).resize((image_size, image_size)))

    def about_funct():
        ms.showinfo("About","GearBox, Developed By Bloom Administrative Systems. Contact +233 544 022 765")

    #--------------------load images------------------------------
    qr_image = load_image("./images/qr_image.png", 20)
    colo_image=load_image("./images/googleDrive.png", 20)
    setting_image = load_image("./images/settings_icon.png", 20)
    add_image=load_image("./images/add_image.png", 20)
    about_image = load_image("./images/info_image.png", 20)
    _image = load_image("./images/image.png", 20)
    detail_image = load_image("./images/detail_image.png", 20)


    harmonies=['Complementary Colors','Triadic Colors','Split Complementary Colors','Tetradic Colors','Analogue Colors','Monochromatic Colors']

    customtkinter.set_appearance_mode("dark")  # Modes: "System" (standard), "Dark", "Light"
    customtkinter.set_default_color_theme("green")  # Themes:

    # configure grid layout (2x1)
    app_wind.grid_columnconfigure(1, weight=1)
    app_wind.grid_rowconfigure(0, weight=1)

    frame_left = customtkinter.CTkFrame(master=app_wind,
                                             width=180,
                                             corner_radius=0)
    frame_left.grid(row=0, column=0, sticky="nswe")

    frame_right = customtkinter.CTkFrame(master=app_wind)
    frame_right.grid(row=0, column=1, sticky="nswe", padx=20, pady=20)

    #------------------------main layout-----------------------------------------

    label_1 = customtkinter.CTkButton(master=frame_left,
                                      text="Daily Coins Group of Companies",
                                       fg_color="#2e2e2e",
                                      hover_color="#1f1f1f")  # font name and size in px
    label_1.grid(row=1, column=0, pady=10, padx=10)

    domain_btn = customtkinter.CTkButton(master=frame_left,
                                              text="Color Lab                        ", \
                                              height=32,image=colo_image,
                                              compound="left", fg_color="#2e2e2e", hover_color="#1f1f1f")
    domain_btn.grid(row=2, column=0, columnspan=2, padx=20, pady=10, sticky="ew")

    qr_code_btn = customtkinter.CTkButton(master=frame_left, text="Qr-Code                            ", \
                                             height=32,image=qr_image,compound='left',
                                             fg_color="#2e2e2e", hover_color="#1f1f1f",command=open_qr_code_gui)
    qr_code_btn.grid(row=3, column=0, columnspan=2, padx=20, pady=10, sticky="ew")

    image_color_btn = customtkinter.CTkButton(master=frame_left, text="Image Extract                ", \
                                        height=32, image=_image, compound='left',
                                        fg_color="#2e2e2e", hover_color="#1f1f1f",command=open_color_extraction)
    image_color_btn.grid(row=4, column=0, columnspan=2, padx=20, pady=10, sticky="ew")

    saved_palette_btn = customtkinter.CTkButton(master=frame_left, text="Saved Palette                 ", \
                                              height=32, image=colo_image, compound='left',
                                              fg_color="#2e2e2e", hover_color="#1f1f1f", command=open_saved_palette)
    saved_palette_btn.grid(row=5, column=0, columnspan=2, padx=20, pady=10, sticky="ew")



    settings = customtkinter.CTkButton(master=frame_left, height=32,image=setting_image,
                                            compound="left", fg_color="#2e2e2e", hover_color="#1f1f1f",
                                            text="Subscriptions                  ",command=subscribe)
    settings.grid(row=7, column=0, columnspan=2, padx=20, pady=10, sticky="ew")  # place(x=40,y=320)

    about_btn = customtkinter.CTkButton(master=frame_left, height=32, image=about_image,
                                       compound="left", fg_color="#2e2e2e", hover_color="#1f1f1f",
                                       text="About                                  ", command=about_funct)
    about_btn.grid(row=8, column=0, columnspan=2, padx=20, pady=10, sticky="ew")  # place(x=40,y=320)


    #-------------------frame right-------------------------

    detail_btn=customtkinter.CTkButton(frame_right,image=detail_image,text='',width=15,height=15,command=open_details,fg_color='#0e1821')
    #detail_btn.place(y=10,x=10)

    option_frame = customtkinter.CTkFrame(master=frame_right)
    option_frame.pack(pady=10)

    select = customtkinter.CTkOptionMenu(master=option_frame, values=harmonies, width=200)
    select.set('Triadic Colors')
    select.grid(row=0, column=0, padx=20, pady=10)

    gen_type = customtkinter.CTkOptionMenu(master=option_frame, values=['Random', 'Specify'], width=200)
    gen_type.set('Random')
    gen_type.grid(row=0, column=1, padx=5, pady=10)

    color_entry = customtkinter.CTkEntry(master=option_frame, placeholder_text='Enter Color HEX Value (eg: #ffffff)',
                                         width=230)
    color_entry.grid(column=2, row=0, padx=20, pady=10)

    generate_btn = customtkinter.CTkButton(master=option_frame, text='Generate', fg_color="#a36da2",
                                           hover_color="#eaa2e9", command=color_scheme_function)
    generate_btn.grid(row=1, column=0, pady=5, columnspan=3)

    brightness=customtkinter.CTkSlider(master=option_frame,from_=0,to=2,command=adj_bright)
    brightness.grid(column=0,row=2,columnspan=3,pady=5)
    brightness.set(1)

    value_label=customtkinter.CTkLabel(master=option_frame,text='1')
    value_label.place(y=83,x=480)

    bright_rgb = customtkinter.CTkSlider(master=option_frame, from_=0, to=100,command=slider_func)
    bright_rgb.grid(column=0, row=3, columnspan=3)
    bright_rgb.set(1)

    value_label_rgb = customtkinter.CTkLabel(master=option_frame, text='1%')
    value_label_rgb.place(y=105, x=480)

    add_palette = customtkinter.CTkButton(option_frame, image=add_image, text='Add Palette',text_color='#437F70', width=15, height=15,
                                          fg_color='#0e1821')
    add_palette.place(y=95,x=600)

    #-----------------color frame-----------------------------
    color_frame = customtkinter.CTkFrame(master=frame_right, height=180, width=1200)
    color_frame.pack(pady=30)

    # -----------------color pair frame-----------------------------
    option_frame2 = customtkinter.CTkFrame(master=frame_right)
    option_frame2.pack()

    harmonies = ['Complementary Colors', 'Triadic Colors', 'Split Complementary Colors', 'Tetradic Colors',
                 'Analogue Colors', 'Monochromatic Colors']
    _type_one = customtkinter.CTkOptionMenu(master=option_frame2, values=['Complementary Colors', 'Triadic Colors'\
                                             ,'Analogue Colors','Split Complementary Colors', 'Tetradic Colors' ], width=200)
    _type_one.set('Complementary Colors')
    _type_one.grid(row=0, column=0, padx=10, pady=5)

    _type_two = customtkinter.CTkOptionMenu(master=option_frame2, values=['Complementary Colors', 'Triadic Colors'\
                                             ,'Analogue Colors','Split Complementary Colors', 'Tetradic Colors' ], width=200)
    _type_two.set('Analogue Colors')
    _type_two.grid(row=0, column=1, padx=10, pady=5)

    generate_pair_btn = customtkinter.CTkButton(master=option_frame2, text='Generate Palette Pair', fg_color="#a36da2",
                                           hover_color="#eaa2e9",command=generate_pairs)
    generate_pair_btn.grid(row=0, column=2, pady=5)

    brightness2 = customtkinter.CTkSlider(master=option_frame2, from_=0, to=2,command=adj_bright_two)
    brightness2.grid(column=0, row=1, columnspan=3,pady=10)
    brightness2.set(1)

    value_label2 = customtkinter.CTkLabel(master=option_frame2, text='1')
    value_label2.place(y=40, x=400)

    bright_rgb2 = customtkinter.CTkSlider(master=option_frame2, from_=0, to=100, command=slider2_func)
    bright_rgb2.grid(column=0, row=2, columnspan=3)
    bright_rgb2.set(1)

    value_label_rgb2 = customtkinter.CTkLabel(master=option_frame2, text='1%')
    value_label_rgb2.place(y=66, x=400)

    colorPair_frame = customtkinter.CTkFrame(master=frame_right, height=250, width=1200)
    colorPair_frame.pack(pady=10)

    '''top_right = customtkinter.CTkFrame(master=app_wind, height=200, width=680)
    top_right.pack(pady=5,padx=10)

    color_frame=customtkinter.CTkFrame(master=top_right,height=130,width=680)
    color_frame.pack(pady=20)

    options_frame = customtkinter.CTkFrame(master=app_wind,  width=680)
    options_frame.pack(padx=10)

    select_field =tk.StringVar(value='1')
    select=customtkinter.CTkOptionMenu(master=options_frame, values=harmonies,width=80)
    select.set('Triadic Colors')
    select.grid(row=0,column=0,padx=5,pady=3)

    gen_type = customtkinter.CTkOptionMenu(master=options_frame, values=['Random','Specify'], width=80)
    gen_type.set('Random')
    gen_type.grid(row=0, column=1, padx=5,pady=3)

    color_entry=customtkinter.CTkEntry(master=options_frame,placeholder_text='Enter Color HEX Value (eg: #ffffff)',width=230)
    color_entry.grid(column=2,row=0,padx=5,pady=3)

    generate_btn=customtkinter.CTkButton(master=options_frame,text='Generate',fg_color="#a36da2", hover_color="#eaa2e9",command=color_scheme_function)
    generate_btn.grid(row=1,column=0,pady=5,columnspan=3)'''

    save_start_date()
    check_expiry()
    app_wind.mainloop()

def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    app()
    #AppId={{295A883C-8226-4592-B584-F9F1F36535E9}

#See PyCharm help at https://www.jetbrains.com/help/pycharm/
