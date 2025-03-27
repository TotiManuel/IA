import tkinter as tk
import os
from tkinter import messagebox
from Control.Control import Control

class Visual:
    def __init__(self):
        self.messageBox = messagebox
        self.control = Control()
    
    def check_start(self, response):
        if response == True:
            print("Yes")
        else:
            print("No")

    def button_option(self, choice):
        if choice == "camera":
            self.messageBox.showwarning("Camera.", "The camera will start.")
            self.control.start_camera()
        elif choice == "recognition":
            self.messageBox.showwarning("Camera.", "The camera will start and facial recognition will be performed.")
            self.control.start_recognition()
        elif choice == "voice_recognition":
            self.messageBox.showwarning("Recognition.", "Voice recognition will start.")
            self.control.start_voice_recognition()
        elif choice == "ip_recognition":
            ip = self.control.start_recognize_ip()
            messagebox.showinfo("IP del Equipo", ip)
    
    def new_file(self):
        messagebox.showinfo("New", "Create a new file.")
    
    def open_file(self):
        messagebox.showinfo("Open", "Open an existing file.")
    
    def exit(self):
        self.root.quit()
    
    def paste(self):
        messagebox.showinfo("Paste", "Paste content.")
    
    def about(self):
        messagebox.showinfo("About", "Example application with menu in Tkinter.")

    def start(self):
        #self.messageBox.showwarning("WARNING: Unauthorized Access.","You do not have access to use this device. Please leave it, we use facial recognition to identify you.")
        #response = self.messageBox.askyesno("Continue?", "If you continue, your data will be used for purposes we deem appropriate for you to return the device.")
        #self.check_start(response)
        
        #region Window Configuration
        self.root = tk.Tk()
        self.root.title("JMM")
        self.root.geometry("500x500")
        #endregion
    
        #region menu

        # Create a menu at the top
        self.menu = tk.Menu(self.root)
        self.root.config(menu=self.menu)
        
        # Create the "File" menu
        file_menu = tk.Menu(self.menu, tearoff=0)
        self.menu.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="New", command=self.new_file)
        file_menu.add_command(label="Open", command=self.open_file)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.exit)
        
        # Create the "Functions" menu
        functions_menu = tk.Menu(self.menu, tearoff=0)
        self.menu.add_cascade(label="Functions", menu=functions_menu)
        functions_menu.add_command(label="Open Camera", command=lambda:self.button_option("camera"))
        functions_menu.add_command(label="Facial Recognition", command=lambda:self.button_option("recognition"))
        functions_menu.add_command(label="Voice Recognition", command=lambda:self.button_option("voice_recognition"))
        
        # Create the "Help" menu
        help_menu = tk.Menu(self.menu, tearoff=0)
        self.menu.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="About", command=self.about)

        #endregion

        self.camera_button = tk.Button(self.root, text="Start Camera", command=lambda:self.button_option("camera"))
        self.camera_button.pack(pady=1)
        self.facial_button = tk.Button(self.root, text="Facial Recognition", command=lambda:self.button_option("recognition"))
        self.facial_button.pack(pady=1)
        self.voice_button = tk.Button(self.root, text="Voice Recognition", command=lambda:self.button_option("voice_recognition"))
        self.voice_button.pack(pady=1)
        self.mail_button = tk.Button(self.root, text="Recognize IPs", command=lambda:self.button_option("ip_recognition"))
        self.mail_button.pack(pady=1)
        self.exit_button = tk.Button(self.root, text="Exit", command=lambda:self.root.destroy())
        self.exit_button.pack(pady=1)
        
        self.root.mainloop()
