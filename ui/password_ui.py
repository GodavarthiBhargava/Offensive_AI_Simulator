import tkinter as tk
from tkinter import ttk, messagebox
from backend.password_engine import simulate_password_attack
import os
from PIL import Image, ImageTk

class PasswordUI:
    def __init__(self, window):
        self.window = window
        self.window.title("Password Attack Simulation")
        self.window.geometry("850x750")
        self.window.resizable(False, False)
        self.window.configure(bg="#1e1e1e")
        
        # Try to load background image
        self.bg_image = None
        bg_path = "assets/bg.png"
        if os.path.exists(bg_path):
            try:
                img = Image.open(bg_path)
                img = img.resize((850, 750), Image.Resampling.LANCZOS)
                self.bg_image = ImageTk.PhotoImage(img)
            except:
                pass
        
        # Background
        if self.bg_image:
            bg_label = tk.Label(window, image=self.bg_image)
            bg_label.place(x=0, y=0, relwidth=1, relheight=1)
        
        # Main container
        main_container = tk.Frame(window, bg="#1e1e1e")
        if self.bg_image:
            main_container.configure(bg="")
        main_container.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Title
        title_frame = tk.Frame(main_container, bg="#2d2d2d", relief="flat", bd=0)
        title_frame.pack(fill="x", pady=(0, 20))
        
        title = tk.Label(title_frame, text="PASSWORD ATTACK SIMULATION", 
                        font=("Segoe UI", 18, "bold"), bg="#2d2d2d", fg="#00d9ff")
        title.pack(pady=15)
        
        subtitle = tk.Label(title_frame, text="Hashing Engine & Security Analysis", 
                           font=("Segoe UI", 10), bg="#2d2d2d", fg="#888888")
        subtitle.pack(pady=(0, 10))
        
        # User Context Section
        context_frame = self._create_section(main_container, "User Context (Optional)")
        
        context_grid = tk.Frame(context_frame, bg="#2d2d2d")
        context_grid.pack(fill="x", padx=15, pady=10)
        
        tk.Label(context_grid, text="Username:", font=("Segoe UI", 10), 
                bg="#2d2d2d", fg="#cccccc").grid(row=0, column=0, sticky="w", pady=8)
        self.username_entry = tk.Entry(context_grid, width=35, font=("Segoe UI", 10), 
                                      bg="#3c3c3c", fg="#ffffff", insertbackground="#ffffff", 
                                      relief="flat", bd=5)
        self.username_entry.grid(row=0, column=1, pady=8, padx=15, sticky="ew")
        
        tk.Label(context_grid, text="Full Name:", font=("Segoe UI", 10), 
                bg="#2d2d2d", fg="#cccccc").grid(row=1, column=0, sticky="w", pady=8)
        self.fullname_entry = tk.Entry(context_grid, width=35, font=("Segoe UI", 10), 
                                      bg="#3c3c3c", fg="#ffffff", insertbackground="#ffffff", 
                                      relief="flat", bd=5)
        self.fullname_entry.grid(row=1, column=1, pady=8, padx=15, sticky="ew")
        
        context_grid.columnconfigure(1, weight=1)
        
        # Input Mode Section
        mode_frame = self._create_section(main_container, "Input Mode")
        
        mode_label = tk.Label(mode_frame, text="Enter Password to Test:", 
                             font=("Segoe UI", 10), bg="#2d2d2d", fg="#cccccc")
        mode_label.pack(padx=15, pady=10, anchor="w")
        
        # Credential Input Section
        cred_frame = self._create_section(main_container, "Credential Input")
        
        cred_grid = tk.Frame(cred_frame, bg="#2d2d2d")
        cred_grid.pack(fill="x", padx=15, pady=10)
        
        self.input_label = tk.Label(cred_grid, text="Password:", font=("Segoe UI", 10), 
                                    bg="#2d2d2d", fg="#cccccc")
        self.input_label.grid(row=0, column=0, sticky="w", pady=8)
        
        self.credential_entry = tk.Entry(cred_grid, width=50, font=("Segoe UI", 10), 
                                        bg="#3c3c3c", fg="#ffffff", insertbackground="#ffffff", 
                                        relief="flat", bd=5, show="*")
        self.credential_entry.grid(row=0, column=1, pady=8, padx=15, sticky="ew")
        
        cred_grid.columnconfigure(1, weight=1)
        
        # Hash Algorithm Section
        algo_frame = self._create_section(main_container, "Hash Algorithm")
        
        algo_grid = tk.Frame(algo_frame, bg="#2d2d2d")
        algo_grid.pack(fill="x", padx=15, pady=10)
        
        tk.Label(algo_grid, text="Algorithm:", font=("Segoe UI", 10), 
                bg="#2d2d2d", fg="#cccccc").grid(row=0, column=0, sticky="w", pady=8)
        
        self.algorithm_var = tk.StringVar(value="MD5")
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('Custom.TCombobox', fieldbackground="#3c3c3c", 
                       background="#3c3c3c", foreground="#ffffff", 
                       borderwidth=0, relief="flat")
        
        algorithm_combo = ttk.Combobox(algo_grid, textvariable=self.algorithm_var, 
                                      values=["MD5", "SHA256"], state="readonly", 
                                      width=47, font=("Segoe UI", 10), style='Custom.TCombobox')
        algorithm_combo.grid(row=0, column=1, pady=8, padx=15, sticky="ew")
        
        algo_grid.columnconfigure(1, weight=1)
        
        # Action Button
        btn_frame = tk.Frame(main_container, bg="#1e1e1e")
        btn_frame.pack(pady=20)
        
        simulate_btn = tk.Button(btn_frame, text="SIMULATE PASSWORD ATTACK", 
                                font=("Segoe UI", 12, "bold"), bg="#00d9ff", fg="#000000",
                                activebackground="#00b8d4", activeforeground="#000000",
                                command=self.run_simulation, width=35, height=2, 
                                relief="flat", bd=0, cursor="hand2")
        simulate_btn.pack()
    
    def _create_section(self, parent, title):
        """Create a styled section frame"""
        frame = tk.LabelFrame(parent, text=title, font=("Segoe UI", 11, "bold"), 
                             bg="#2d2d2d", fg="#00d9ff", relief="flat", bd=2, 
                             labelanchor="nw", padx=5, pady=5)
        frame.pack(fill="x", pady=10)
        return frame
    
    def run_simulation(self):
        password = self.credential_entry.get().strip()
        algorithm = self.algorithm_var.get()
        username = self.username_entry.get().strip()
        fullname = self.fullname_entry.get().strip()
        
        if not password:
            messagebox.showerror("Error", "Please enter a password")
            return
        
        try:
            # Run simulation
            result = simulate_password_attack(password, algorithm, username, fullname)
            
            # Display results
            self.display_results(result)
            
        except Exception as e:
            messagebox.showerror("Error", f"Simulation failed: {str(e)}")
    
    def display_results(self, result):
        """Display results in a separate popup window"""
        # Create popup window
        result_window = tk.Toplevel(self.window)
        result_window.title("Simulation Results")
        result_window.geometry("500x400")
        result_window.resizable(False, False)
        result_window.configure(bg="#1e1e1e")
        
        # Title
        title_frame = tk.Frame(result_window, bg="#2d2d2d", relief="flat")
        title_frame.pack(fill="x", pady=(0, 20))
        
        title = tk.Label(title_frame, text="SIMULATION RESULTS", 
                        font=("Segoe UI", 16, "bold"), bg="#2d2d2d", fg="#00d9ff")
        title.pack(pady=15)
        
        # Results container
        results_container = tk.Frame(result_window, bg="#1e1e1e")
        results_container.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Status card
        status_color = "#ff4444" if result['cracked'] else "#00ff00"
        status_text = "CRACKED" if result['cracked'] else "NOT CRACKED"
        self._create_result_card(results_container, "Status", status_text, status_color)
        
        # Attack Used card
        attack_color = "#ff9800" if result['attack_used'] != "None" else "#888888"
        self._create_result_card(results_container, "Attack Used", result['attack_used'], attack_color)
        
        # Password Strength card
        strength_colors = {"Weak": "#ff4444", "Medium": "#ff9800", "Strong": "#00ff00", "Unknown": "#888888"}
        strength_color = strength_colors.get(result['password_strength'], "#888888")
        self._create_result_card(results_container, "Password Strength", result['password_strength'], strength_color)
        
        # AI Risk Level card
        risk_colors = {"High": "#ff4444", "Medium": "#ff9800", "Low": "#00ff00", "Unknown": "#888888"}
        risk_color = risk_colors.get(result['ai_risk_level'], "#888888")
        self._create_result_card(results_container, "AI Risk Level", result['ai_risk_level'], risk_color)
        
        # Cracked Password card (if applicable)
        if result['cracked']:
            self._create_result_card(results_container, "Cracked Password", result['cracked_password'], "#00d9ff")
        
        # Warning footer
        warning_frame = tk.Frame(result_window, bg="#2d2d2d", relief="flat")
        warning_frame.pack(side="bottom", fill="x", pady=(10, 0))
        tk.Label(warning_frame, text="WARNING: Educational Simulation Only", 
                font=("Segoe UI", 9, "bold"), bg="#2d2d2d", fg="#ff9800").pack(pady=10)
        
        # Close button
        close_btn = tk.Button(result_window, text="CLOSE", 
                             font=("Segoe UI", 10, "bold"), bg="#00d9ff", fg="#000000",
                             activebackground="#00b8d4", activeforeground="#000000",
                             command=result_window.destroy, width=20, height=1, 
                             relief="flat", bd=0, cursor="hand2")
        close_btn.pack(pady=10)
    
    def _create_result_card(self, parent, label, value, color):
        """Create a colored result card"""
        card = tk.Frame(parent, bg="#3c3c3c", relief="flat", bd=1)
        card.pack(fill="x", pady=5, padx=10)
        
        # Label
        tk.Label(card, text=label + ":", font=("Segoe UI", 10, "bold"), 
                bg="#3c3c3c", fg="#cccccc", anchor="w").pack(side="left", padx=15, pady=10)
        
        # Value with color
        tk.Label(card, text=value, font=("Segoe UI", 11, "bold"), 
                bg="#3c3c3c", fg=color, anchor="e").pack(side="right", padx=15, pady=10)
