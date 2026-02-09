import tkinter as tk
from tkinter import messagebox
from ui.password_ui import PasswordUI
import os
from PIL import Image, ImageTk

class MainWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("Offensive AI Simulator")
        self.root.geometry("700x550")
        self.root.resizable(False, False)
        self.root.configure(bg="#1e1e1e")
        
        # Try to load background image
        self.bg_image = None
        bg_path = "assets/bg.png"
        if os.path.exists(bg_path):
            try:
                img = Image.open(bg_path)
                img = img.resize((700, 550), Image.Resampling.LANCZOS)
                self.bg_image = ImageTk.PhotoImage(img)
            except:
                pass
        
        # Main container with background
        if self.bg_image:
            bg_label = tk.Label(root, image=self.bg_image)
            bg_label.place(x=0, y=0, relwidth=1, relheight=1)
            main_container = tk.Frame(root, bg="#1e1e1e")
            main_container.configure(bg="")
        else:
            main_container = tk.Frame(root, bg="#1e1e1e")
        
        main_container.pack(fill="both", expand=True, padx=30, pady=30)
        
        # Title section
        title_frame = tk.Frame(main_container, bg="#2d2d2d", relief="flat")
        title_frame.pack(fill="x", pady=(0, 20))
        
        title = tk.Label(title_frame, text="OFFENSIVE AI SIMULATOR", 
                        font=("Segoe UI", 22, "bold"), bg="#2d2d2d", fg="#00d9ff")
        title.pack(pady=20)
        
        subtitle = tk.Label(title_frame, text="Educational Cybersecurity Simulation Tool", 
                           font=("Segoe UI", 11), bg="#2d2d2d", fg="#888888")
        subtitle.pack(pady=(0, 15))
        
        # Module buttons frame
        btn_container = tk.Frame(main_container, bg="#1e1e1e")
        btn_container.pack(pady=20, fill="both", expand=True)
        
        # Module 1 - Active
        btn1 = tk.Button(btn_container, 
                        text="Module 1: Password Attack Simulation", 
                        font=("Segoe UI", 11, "bold"), 
                        bg="#00d9ff", fg="#000000",
                        activebackground="#00b8d4", activeforeground="#000000",
                        width=45, height=2, 
                        relief="flat", bd=0, cursor="hand2",
                        command=self.open_password_module)
        btn1.pack(pady=12)
        
        # Module 2 - Coming Soon
        btn2 = tk.Button(btn_container, 
                        text="Module 2: Social Engineering & Phishing", 
                        font=("Segoe UI", 11), 
                        bg="#3c3c3c", fg="#666666",
                        width=45, height=2, 
                        relief="flat", bd=0, state="disabled")
        btn2.pack(pady=12)
        
        # Module 3 - Coming Soon
        btn3 = tk.Button(btn_container, 
                        text="Module 3: AI Learning & Behaviour Analysis", 
                        font=("Segoe UI", 11), 
                        bg="#3c3c3c", fg="#666666",
                        width=45, height=2, 
                        relief="flat", bd=0, state="disabled")
        btn3.pack(pady=12)
        
        # Module 4 - Coming Soon
        btn4 = tk.Button(btn_container, 
                        text="Module 4: Awareness Training & Feedback", 
                        font=("Segoe UI", 11), 
                        bg="#3c3c3c", fg="#666666",
                        width=45, height=2, 
                        relief="flat", bd=0, state="disabled")
        btn4.pack(pady=12)
        
        # Footer
        footer_frame = tk.Frame(main_container, bg="#2d2d2d", relief="flat")
        footer_frame.pack(side="bottom", fill="x", pady=(20, 0))
        
        footer = tk.Label(footer_frame, text="WARNING: FOR EDUCATIONAL PURPOSES ONLY", 
                         font=("Segoe UI", 9, "bold"), bg="#2d2d2d", fg="#ff4444")
        footer.pack(pady=10)
    
    def open_password_module(self):
        password_window = tk.Toplevel(self.root)
        password_window.configure(bg="#1e1e1e")
        PasswordUI(password_window)
