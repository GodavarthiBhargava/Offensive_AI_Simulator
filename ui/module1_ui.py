import tkinter as tk
from tkinter import ttk, messagebox
from backend.password_engine import simulate_password_attack
import time

class PasswordAttackModule:
    def __init__(self, window):
        self.window = window
        self.window.title("Skill Palavar - Module 1")
        self.window.geometry("1200x650")
        self.window.configure(bg="#2E2E2E")
        
        # Set icon
        try:
            from PIL import Image
            import os
            if os.path.exists("ui/assessts/icon.jpg"):
                img = Image.open("ui/assessts/icon.jpg")
                img.save("assets/icon.ico", format="ICO")
            self.window.iconbitmap("assets/icon.ico")
        except:
            pass
        
        # Top Navigation Bar
        navbar = tk.Frame(window, bg="#1F1F1F", height=50)
        navbar.pack(fill="x")
        navbar.pack_propagate(False)
        
        tk.Label(navbar, text="Skill Palavar - Module 1: Password Attack Simulation",
                font=("Consolas", 12), bg="#1F1F1F", fg="#00FF66").pack(side="left", padx=20, pady=15)
        
        # Bottom border
        tk.Frame(window, bg="#003300", height=1).pack(fill="x")
        
        # Main content area
        content = tk.Frame(window, bg="#2E2E2E")
        content.pack(fill="both", expand=True)
        
        # Left panel (40%)
        left_panel = tk.Frame(content, bg="#2E2E2E")
        left_panel.pack(side="left", fill="both", padx=20, pady=20)
        left_panel.config(width=int(1200 * 0.4))
        
        # Right panel (60%)
        right_panel = tk.Frame(content, bg="#2E2E2E")
        right_panel.pack(side="right", fill="both", expand=True, padx=15, pady=20)
        
        # Configure style for combobox
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('Custom.TCombobox',
                       fieldbackground="#000000",
                       background="#000000",
                       foreground="#00FF66",
                       bordercolor="#003300",
                       arrowcolor="#00FF66",
                       selectbackground="#003300",
                       selectforeground="#00FF66")
        style.map('Custom.TCombobox',
                 fieldbackground=[('readonly', '#000000')],
                 selectbackground=[('readonly', '#000000')])
        
        # LEFT PANEL - Input fields
        self.input_type_var = tk.StringVar(value="Provide Password Directly")
        input_type_dropdown = self._create_dropdown(left_panel, "INPUT TYPE", self.input_type_var,
                             ["Provide Password Directly", "Provide Hash Code"], self.toggle_input_mode)
        
        self.password_frame = self._create_input(left_panel, "PASSWORD", show="*")
        self.hash_frame = self._create_input(left_panel, "HASH CODE")
        self.hash_frame.pack_forget()
        
        self.hash_algo_var = tk.StringVar(value="MD5")
        self._create_dropdown(left_panel, "HASH ALGORITHM", self.hash_algo_var,
                             ["MD5", "SHA1", "SHA256"])
        
        self.attack_type_var = tk.StringVar(value="Dictionary Attack")
        self._create_dropdown(left_panel, "ATTACK TYPE", self.attack_type_var,
                             ["Dictionary Attack", "Brute Force Attack", "AI Guided Guess"])
        
        # Crack button
        btn_frame = tk.Frame(left_panel, bg="#2E2E2E")
        btn_frame.pack(fill="x", pady=15)
        
        self.crack_btn = tk.Button(btn_frame, text="CRACK HASH",
                                   font=("Consolas", 11, "bold"),
                                   bg="#000000", fg="#00FF66",
                                   activebackground="#003300", activeforeground="#00FF66",
                                   relief="solid", bd=2, height=2,
                                   cursor="hand2", command=self.start_attack)
        self.crack_btn.pack(fill="x")
        
        self.crack_btn.bind("<Enter>", lambda e: self.crack_btn.config(bg="#003300"))
        self.crack_btn.bind("<Leave>", lambda e: self.crack_btn.config(bg="#000000"))
        
        # RIGHT PANEL - Output console
        console_container = tk.Frame(right_panel, bg="#000000", relief="solid", bd=2, highlightbackground="#003300", highlightthickness=2)
        console_container.pack(fill="both", expand=True)
        
        self.console = tk.Text(console_container, bg="#000000", fg="#00FF00",
                              font=("Consolas", 10), insertbackground="#00FF00",
                              relief="flat", state="disabled", padx=15, pady=15)
        self.console.pack(side="left", fill="both", expand=True)
        
        scrollbar = tk.Scrollbar(console_container, command=self.console.yview, bg="#000000", troughcolor="#000000")
        scrollbar.pack(side="right", fill="y")
        self.console.config(yscrollcommand=scrollbar.set)
        
        # Open output button
        open_btn = tk.Button(right_panel, text="Open Output in New Window",
                            font=("Consolas", 9), bg="#000000", fg="#00FF66",
                            relief="solid", bd=1, height=1, cursor="hand2")
        open_btn.pack(fill="x", pady=(10, 0))
        
        # Initial message
        self.print_console("[SYSTEM] Ready. Awaiting input...")
    
    def _create_input(self, parent, label_text, show=None):
        frame = tk.Frame(parent, bg="#2E2E2E")
        frame.pack(fill="x", pady=(0, 15))
        
        tk.Label(frame, text=label_text, font=("Consolas", 10),
                bg="#2E2E2E", fg="#00FF66").pack(anchor="w", pady=(0, 5))
        
        entry = tk.Entry(frame, font=("Consolas", 10), bg="#000000", fg="#00FF66",
                        relief="solid", bd=1, insertbackground="#00FF66", show=show)
        entry.pack(fill="x", ipady=8)
        entry.config(highlightbackground="#003300", highlightcolor="#00FF66", highlightthickness=1)
        
        frame.entry = entry
        return frame
    
    def _create_dropdown(self, parent, label_text, variable, values, command=None):
        frame = tk.Frame(parent, bg="#2E2E2E")
        frame.pack(fill="x", pady=(0, 15))
        
        tk.Label(frame, text=label_text, font=("Consolas", 10),
                bg="#2E2E2E", fg="#00FF66").pack(anchor="w", pady=(0, 5))
        
        combo = ttk.Combobox(frame, textvariable=variable, values=values,
                            state="readonly", font=("Consolas", 10),
                            style='Custom.TCombobox', height=10)
        combo.pack(fill="x", ipady=8)
        
        if command:
            combo.bind("<<ComboboxSelected>>", lambda e: command())
        
        return combo
    
    def toggle_input_mode(self):
        if self.input_type_var.get() == "Provide Password Directly":
            self.hash_frame.pack_forget()
            self.password_frame.pack(fill="x", pady=(0, 15), before=self.hash_algo_var.master)
        else:
            self.password_frame.pack_forget()
            self.hash_frame.pack(fill="x", pady=(0, 15), before=self.hash_algo_var.master)
    
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
    
    def start_attack(self):
        input_type = self.input_type_var.get()
        algorithm = self.hash_algo_var.get()
        
        if input_type == "Provide Password Directly":
            credential = self.password_frame.entry.get().strip()
            input_mode = "password"
        else:
            credential = self.hash_frame.entry.get().strip()
            input_mode = "hash"
        
        if not credential:
            messagebox.showerror("Error", "Please enter password or hash")
            return
        
        self.clear_console()
        
        self.print_console("[INFO] Initializing attack engine...", 0.1)
        self.print_console(f"[INFO] Hash type detected: {algorithm}", 0.1)
        self.print_console(f"[INFO] Attack mode: {self.attack_type_var.get()}", 0.1)
        self.print_console("[INFO] Loading wordlist...", 0.2)
        
        try:
            with open("resources/wordlist.txt", "r") as f:
                words = [w.strip() for w in f.readlines()[:10]]
            self.print_console(f"[INFO] Loaded wordlist successfully.", 0.1)
        except:
            words = ["admin", "password", "123456"]
            self.print_console("[WARN] Using default wordlist.", 0.1)
        
        self.print_console("[INFO] Starting attack...", 0.2)
        
        for word in words[:5]:
            self.print_console(f"[TRYING] {word}", 0.05)
        
        try:
            result = simulate_password_attack(
                credential=credential,
                algorithm=algorithm,
                input_mode=input_mode,
                username="",
                fullname=""
            )
            
            self.print_console("", 0.1)
            
            if result['cracked']:
                self.print_console("[SUCCESS] Password Found.", 0.2)
                self.print_console(f"[RESULT] Password: {result['cracked_password']}", 0.1)
                self.print_console(f"[RESULT] Method: {result['attack_used']}", 0.1)
            else:
                self.print_console("[FAILED] Password not found.", 0.2)
            
            self.print_console("", 0.1)
            self.print_console(f"[ANALYSIS] Strength: {result['password_strength']}", 0.1)
            self.print_console(f"[ANALYSIS] Risk: {result['ai_risk_level']}", 0.1)
            self.print_console("", 0.1)
            self.print_console("[SYSTEM] Attack completed.", 0.1)
            
        except Exception as e:
            self.print_console(f"[ERROR] {str(e)}", 0.1)


if __name__ == "__main__":
    root = tk.Tk()
    PasswordAttackModule(root)
    root.mainloop()
