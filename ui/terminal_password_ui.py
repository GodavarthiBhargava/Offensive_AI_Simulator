import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from backend.password_engine import simulate_password_attack
import time

class TerminalModuleUI:
    def __init__(self, window, module_title):
        self.window = window
        self.window.title(module_title)
        self.window.geometry("1200x700")
        self.window.configure(bg="#000000")
        
        # Header
        header = tk.Frame(window, bg="#000000", height=50)
        header.pack(fill="x", padx=2, pady=2)
        tk.Label(header, text=f"SKILL PALAVAR - {module_title}", 
                font=("Consolas", 14, "bold"), bg="#000000", fg="#00FF00").pack(pady=10)
        
        # Separator
        tk.Frame(window, bg="#00FF00", height=2).pack(fill="x")
        
        # Main content
        content = tk.Frame(window, bg="#000000")
        content.pack(fill="both", expand=True, padx=2, pady=2)
        
        # Left panel - Input
        self.left_panel = tk.Frame(content, bg="#000000", width=400)
        self.left_panel.pack(side="left", fill="both", padx=(0, 1))
        self.left_panel.pack_propagate(False)
        
        # Vertical separator
        tk.Frame(content, bg="#00FF00", width=2).pack(side="left", fill="y")
        
        # Right panel - Output
        right_panel = tk.Frame(content, bg="#000000")
        right_panel.pack(side="right", fill="both", expand=True, padx=(1, 0))
        
        # Output console
        self.console = tk.Text(right_panel, bg="#000000", fg="#00FF00", 
                              font=("Consolas", 10), insertbackground="#00FF00",
                              relief="flat", state="disabled")
        self.console.pack(fill="both", expand=True, padx=10, pady=10)
        
        scrollbar = tk.Scrollbar(self.console, command=self.console.yview)
        scrollbar.pack(side="right", fill="y")
        self.console.config(yscrollcommand=scrollbar.set)
    
    def add_input_field(self, label_text, show=None):
        frame = tk.Frame(self.left_panel, bg="#000000")
        frame.pack(fill="x", padx=20, pady=10)
        
        tk.Label(frame, text=label_text, font=("Consolas", 10), 
                bg="#000000", fg="#00FF00").pack(anchor="w", pady=(0, 5))
        
        entry = tk.Entry(frame, font=("Consolas", 10), bg="#FFFFFF", fg="#000000",
                        relief="solid", bd=1, show=show)
        entry.pack(fill="x")
        return entry
    
    def add_dropdown(self, label_text, values):
        frame = tk.Frame(self.left_panel, bg="#000000")
        frame.pack(fill="x", padx=20, pady=10)
        
        tk.Label(frame, text=label_text, font=("Consolas", 10),
                bg="#000000", fg="#00FF00").pack(anchor="w", pady=(0, 5))
        
        var = tk.StringVar(value=values[0])
        combo = ttk.Combobox(frame, textvariable=var, values=values, 
                            state="readonly", font=("Consolas", 10))
        combo.pack(fill="x")
        return var
    
    def add_button(self, text, command):
        btn = tk.Button(self.left_panel, text=text, font=("Consolas", 11, "bold"),
                       bg="#000000", fg="#00FF00", relief="solid", bd=2,
                       activebackground="#001100", activeforeground="#00FF00",
                       cursor="hand2", command=command)
        btn.pack(fill="x", padx=20, pady=20)
        
        def on_enter(e):
            btn.config(bd=3)
        def on_leave(e):
            btn.config(bd=2)
        
        btn.bind("<Enter>", on_enter)
        btn.bind("<Leave>", on_leave)
    
    def print_console(self, text, delay=0.05):
        self.console.config(state="normal")
        self.console.insert("end", text + "\n")
        self.console.see("end")
        self.console.config(state="disabled")
        self.window.update()
        time.sleep(delay)
    
    def clear_console(self):
        self.console.config(state="normal")
        self.console.delete(1.0, "end")
        self.console.config(state="disabled")


class PasswordAttackUI:
    def __init__(self, window):
        self.ui = TerminalModuleUI(window, "MODULE 1: PASSWORD ATTACK SIMULATION")
        
        # Input fields
        self.password_entry = self.ui.add_input_field("PASSWORD:", show="*")
        self.hash_entry = self.ui.add_input_field("HASH:")
        self.hash_type = self.ui.add_dropdown("HASH TYPE:", ["MD5", "SHA256"])
        self.attack_type = self.ui.add_dropdown("ATTACK TYPE:", ["Dictionary", "Brute Force", "Auto"])
        
        # Username/Name fields
        self.username_entry = self.ui.add_input_field("USERNAME (Optional):")
        self.fullname_entry = self.ui.add_input_field("FULL NAME (Optional):")
        
        # Button
        self.ui.add_button("[ CRACK HASH ]", self.start_attack)
        
        # Initial message
        self.ui.print_console("[SYSTEM] Ready. Awaiting input...", 0)
    
    def start_attack(self):
        password = self.password_entry.get().strip()
        hash_input = self.hash_entry.get().strip()
        algorithm = self.hash_type.get()
        username = self.username_entry.get().strip()
        fullname = self.fullname_entry.get().strip()
        
        if not password and not hash_input:
            messagebox.showerror("Error", "Enter password or hash")
            return
        
        self.ui.clear_console()
        
        # Determine input mode
        if password:
            credential = password
            input_mode = "password"
            self.ui.print_console("[INFO] Starting attack on password...", 0.1)
        else:
            credential = hash_input
            input_mode = "hash"
            self.ui.print_console("[INFO] Starting attack on hash...", 0.1)
        
        self.ui.print_console(f"[INFO] Algorithm: {algorithm}", 0.1)
        self.ui.print_console(f"[INFO] Attack Type: {self.attack_type.get()}", 0.1)
        self.ui.print_console("[INFO] Loading wordlist...", 0.2)
        
        # Simulate loading
        try:
            with open("resources/wordlist.txt", "r") as f:
                words = f.readlines()
            self.ui.print_console(f"[INFO] Loaded {len(words)} words.", 0.1)
        except:
            self.ui.print_console("[WARN] Wordlist not found. Using default.", 0.1)
        
        self.ui.print_console("[INFO] Starting dictionary attack...", 0.2)
        
        # Simulate trying passwords
        sample_tries = ["admin", "password", "123456", "qwerty", "letmein"]
        for word in sample_tries:
            self.ui.print_console(f"[TRYING] {word}", 0.05)
        
        # Run actual attack
        try:
            result = simulate_password_attack(
                credential=credential,
                algorithm=algorithm,
                input_mode=input_mode,
                username=username,
                fullname=fullname
            )
            
            self.ui.print_console("", 0.1)
            
            if result['cracked']:
                self.ui.print_console("[SUCCESS] PASSWORD FOUND!", 0.2)
                self.ui.print_console(f"[RESULT] Password: {result['cracked_password']}", 0.1)
                self.ui.print_console(f"[RESULT] Attack Method: {result['attack_used']}", 0.1)
            else:
                self.ui.print_console("[FAILED] Password not found in wordlist.", 0.2)
            
            self.ui.print_console("", 0.1)
            self.ui.print_console(f"[ANALYSIS] Password Strength: {result['password_strength']}", 0.1)
            self.ui.print_console(f"[ANALYSIS] AI Risk Level: {result['ai_risk_level']}", 0.1)
            self.ui.print_console("", 0.1)
            self.ui.print_console("[SYSTEM] Attack completed.", 0.1)
            
        except Exception as e:
            self.ui.print_console(f"[ERROR] {str(e)}", 0.1)
