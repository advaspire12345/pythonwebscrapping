import customtkinter as ctk
import tkinter as tk
from selenium import webdriver
import multiprocessing
from selenium.webdriver.support.ui import WebDriverWait
import tkinter.font as tkFont
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from datetime import datetime
from time import sleep
import requests
import random
import urllib
import re
import json
from PIL import Image
from io import BytesIO
import pyautogui as pag
import base64
 
# Sets the appearance of the window
# Supported modes : Light, Dark, System
# "System" sets the appearance mode to
# the appearance mode of the system
ctk.set_appearance_mode("Dark")  
 
# Sets the color of the widgets in the window
# Supported themes : green, dark-blue, blue   
ctk.set_default_color_theme("blue")   
 
# Dimensions of the window
appWidth, appHeight = 600, 450

display_text = []

username01 = ""

# Read saved username & password
try:
    with open("userlist.txt", "r") as file:
        # Read the entire contents of the file
        username01 = file.read()
except FileNotFoundError:
    with open("userlist.txt", "w") as file:
        file.write("liewkokkheong@gmail.com\n ONESLiKoKh!4457@")

if username01 != "":
    USERNAME = username01.split("\n")[0]
    PASSWORD = username01.split("\n")[1]
else:
    USERNAME = "username"
    PASSWORD = "password"

# Updated Scrapper Function on 17th July 2023
# Remove redundant element
# User Interface changed to Customtkinter Modern Design

testing = False
zoom_ratio = 0
orig_height = 0
len_keywords = 0
len_keywords_2 = 0

if testing == True:
    quit()

# App Class
class App(ctk.CTk):

    # in the init function itself
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
 
        # Sets the title of the window
        self.title("ONES PLATFORM WEBSCRAPPING APP")  
        # Sets the dimensions of the window
        self.geometry(f"{appWidth}x{appHeight}")   
 
        # Name Label
        self.nameLabel = ctk.CTkLabel(self,
                                text="Facebook Username")
        self.nameLabel.grid(row=0, column=0,
                            padx=20, pady=20,
                            sticky="ew")
 
        # Name Entry Field
        self.usernameEntry = ctk.CTkEntry(self,
                          placeholder_text=USERNAME)
        
        if USERNAME != "username":
            self.usernameEntry.insert(0, USERNAME)

        self.usernameEntry.grid(row=0, column=1,
                            columnspan=3, padx=20,
                            pady=20, sticky="ew")
 
        # Age Label
        self.passwordLabel = ctk.CTkLabel(self, text="Password")
        self.passwordLabel.grid(row=1, column=0,
                           padx=20, pady=20,
                           sticky="ew")
 
        # Age Entry Field
        self.pwEntry = ctk.CTkEntry(self,
                            placeholder_text=PASSWORD, show="*")
        
        if PASSWORD != "password":
            self.pwEntry.insert(0, PASSWORD)

        self.pwEntry.grid(row=1, column=1,
                           columnspan=3, padx=20,
                           pady=20, sticky="ew")
 
        # Start Button
        self.startButton = ctk.CTkButton(self,
                                         text="Start Scrapping",
                                         command=self.sponsor_start)
        self.startButton.grid(row=5,
                                columnspan=2, padx=20,
                                pady=20, sticky="ew")
 
        # Display Box
        self.displayBox = ctk.CTkTextbox(self,
                                         width=200,
                                         height=200)
        self.displayBox.grid(row=6, column=0,
                             columnspan=4, padx=20,
                             pady=20, sticky="nsew")
        
        # Set display box disabled for entry
        self.displayBox.configure(state="disabled")

        # Set the column width to fill up 100% horizontally
        self.grid_columnconfigure(1, weight=1)

        self.display_queue = multiprocessing.Queue()
  
    # This function is used to insert the
    # details entered by users into the textbox

    # This function is to print out text on the display
    def display_text_output(self, text):
        
        global display_text

        if text != "":
            self.display_queue.put(text)
        
        while not self.display_queue.empty():
            display_text = self.display_queue.get()
            if len(display_text) > 12:
                display_text.pop(0)
            if len(display_text) > 1:
                output_text = "\n".join(display_text)
            else:
                output_text = text

            self.displayBox.configure(state="normal")
            self.displayBox.delete("0.0", tk.END)
            self.displayBox.insert(tk.END, output_text)
            self.displayBox.configure(state="disabled")

    # def print_to_display(self, text):
    #     print_process = multiprocessing.Process(target=self.display_text_output, args=(text,))
    #     print_process.start()

    def sponsor_start(self):
        scrap_data = [self.usernameEntry.get(), self.pwEntry.get()]
        sponsor_process = multiprocessing.Process(target=inizializer, args=(scrap_data,))
        sponsor_process.start()

def inizializer(scrap_data):

    PATH = r"C:\Users\khsra\Desktop\python webscrapping\chromedriver\chromedriver.exe"
    websitePath = "https://www.facebook.com/"
    # USERNAME = "leehoiching22@gmail.com"
    # PASSWORD = "OPLeHoCi!735@"

    # USERNAME = "liewkokkheong@gmail.com"
    # PASSWORD = "ONESLiKoKh!4457@"

    USERNAME = scrap_data[0]
    PASSWORD = scrap_data[1]

    App().displayBox.configure(state="normal")
    App().displayBox.delete("0.0", tk.END)
    App().displayBox.insert(tk.END, "Hello")
    App().displayBox.configure(state="disabled")
    print(USERNAME)
    print(PASSWORD)

if __name__ == "__main__":
    app = App()

    app.mainloop()