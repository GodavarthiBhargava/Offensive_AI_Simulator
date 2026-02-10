import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from backend.dictionary_attack import dictionary_attack_plain, dictionary_attack_hash
from backend.brute_force import brute_force_plain, brute_force_hash
from backend.ai_attack import ai_attack_plain, ai_attack_hash
from backend.hashing_utils import hash_password
from backend.database import init_database, save_case_record
import os
from PIL import Image, ImageTk

class PasswordUI:
    def __init__(self, window):
        self.window = window
        self.window.title("Password Attack Simulation")
        self.window.geometry("900x800")
        self.window.resizable(False, False)
        self.window.configure(bg="#1e1e1e")
        
        # Initialize database
        init_database()
        
        # Wordlist files
        self.wordlist_files = []
        
        # Try to load background image
        self.bg_image = None
        bg_path = "assets/bg.png"
        if os.path.exists(bg_path):
            try:
                img = Image.open(bg_path)
                img = img.resize((900, 800), Image.Resampling.LANCZOS)
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
        title_frame = tk.Frame(main_container, bg="#2d2d2d", relief="flat")
        title_frame.pack(fill="x", pady=(0, 20))
        
        title = tk.Label(title_frame, text="PASSWORD ATTACK SIMULATION", 
                        font=("Segoe UI", 18, "bold"), bg="#2d2d2d", fg="#00d9ff")
        title.pack(pady=15)
        
        # 1. User Details Section
        user_frame = self._create_section(main_container, "User Details")
        
        user_grid = tk.Frame(user_frame, bg="#2d2d2d")
        user_grid.pack(fill="x", padx=15, pady=10)
        
        tk.Label(user_grid, text="First Name:", font=("Segoe UI", 10), 
                bg="#2d2d2d", fg="#cccccc").grid(row=0, column=0, sticky="w", pady=8)
        self.first_name_entry = tk.Entry(user_grid, width=25, font=("Segoe UI", 10), 
                                        bg="#3c3c3c", fg="#ffffff", insertbackground="#ffffff", 
                                        relief="flat", bd=5)
        self.first_name_entry.grid(row=0, column=1, pady=8, padx=10, sticky="ew")
        
        tk.Label(user_grid, text="Last Name:", font=("Segoe UI", 10), 
                bg="#2d2d2d", fg="#cccccc").grid(row=0, column=2, sticky="w", pady=8, padx=(20,0))
        self.last_name_entry = tk.Entry(user_grid, width=25, font=("Segoe UI", 10), 
                                       bg="#3c3c3c", fg="#ffffff", insertbackground="#ffffff", 
                                       relief="flat", bd=5)
        self.last_name_entry.grid(row=0, column=3, pady=8, padx=10, sticky="ew")
        
        user_grid.columnconfigure(1, weight=1)
        user_grid.columnconfigure(3, weight=1)
        
        # Password Type Selection
        type_frame = self._create_section(main_container, "Password Type")
        
        type_grid = tk.Frame(type_frame, bg="#2d2d2d")
        type_grid.pack(fill="x", padx=15, pady=10)
        
        tk.Label(type_grid, text="Password Type:", font=("Segoe UI", 10), 
                bg="#2d2d2d", fg="#cccccc").grid(row=0, column=0, sticky="w", pady=8)
        
        self.password_type_var = tk.StringVar(value="Plain Password")
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('Custom.TCombobox', fieldbackground="#3c3c3c", 
                       background="#3c3c3c", foreground="#ffffff", borderwidth=0)
        
        password_type_combo = ttk.Combobox(type_grid, textvariable=self.password_type_var, 
                                          values=["Plain Password", "Hash Value"], 
                                          state="readonly", width=47, 
                                          font=("Segoe UI", 10), style='Custom.TCombobox')
        password_type_combo.grid(row=0, column=1, pady=8, padx=15, sticky="ew")
        password_type_combo.bind("<<ComboboxSelected>>", self._on_password_type_change)
        
        type_grid.columnconfigure(1, weight=1)
        
        # Credential Input
        cred_frame = self._create_section(main_container, "Credential Input")
        
        cred_grid = tk.Frame(cred_frame, bg="#2d2d2d")
        cred_grid.pack(fill="x", padx=15, pady=10)
        
        self.cred_label = tk.Label(cred_grid, text="Password:", font=("Segoe UI", 10), 
                                   bg="#2d2d2d", fg="#cccccc")
        self.cred_label.grid(row=0, column=0, sticky="w", pady=8)
        
        self.credential_entry = tk.Entry(cred_grid, width=50, font=("Segoe UI", 10), 
                                        bg="#3c3c3c", fg="#ffffff", insertbackground="#ffffff", 
                                        relief="flat", bd=5, show="*")
        self.credential_entry.grid(row=0, column=1, pady=8, padx=15, sticky="ew")
        
        cred_grid.columnconfigure(1, weight=1)
        
        # Hash Algorithm Selection (Hidden by default)
        self.algo_frame = self._create_section(main_container, "Hash Algorithm")
        self.algo_frame.pack_forget()
        
        algo_grid = tk.Frame(self.algo_frame, bg="#2d2d2d")
        algo_grid.pack(fill="x", padx=15, pady=10)
        
        tk.Label(algo_grid, text="Algorithm:", font=("Segoe UI", 10), 
                bg="#2d2d2d", fg="#cccccc").grid(row=0, column=0, sticky="w", pady=8)
        
        self.algorithm_var = tk.StringVar(value="MD5")
        algorithm_combo = ttk.Combobox(algo_grid, textvariable=self.algorithm_var, 
                                      values=["MD5", "SHA256"], state="readonly", 
                                      width=47, font=("Segoe UI", 10), style='Custom.TCombobox')
        algorithm_combo.grid(row=0, column=1, pady=8, padx=15, sticky="ew")
        
        algo_grid.columnconfigure(1, weight=1)
        
        # Attack Type Selection
        attack_frame = self._create_section(main_container, "Attack Type")
        
        attack_grid = tk.Frame(attack_frame, bg="#2d2d2d")
        attack_grid.pack(fill="x", padx=15, pady=10)
        
        tk.Label(attack_grid, text="Select Attack Type:", font=("Segoe UI", 10), 
                bg="#2d2d2d", fg="#cccccc").grid(row=0, column=0, sticky="w", pady=8)
        
        self.attack_type_var = tk.StringVar(value="Dictionary Attack")
        attack_combo = ttk.Combobox(attack_grid, textvariable=self.attack_type_var, 
                                    values=["Brute Force", "Dictionary Attack", "AI Search"], 
                                    state="readonly", width=47, 
                                    font=("Segoe UI", 10), style='Custom.TCombobox')
        attack_combo.grid(row=0, column=1, pady=8, padx=15, sticky="ew")
        attack_combo.bind("<<ComboboxSelected>>", self._on_attack_type_change)
        
        attack_grid.columnconfigure(1, weight=1)
        
        # Dictionary Upload Section (Hidden by default)
        self.dict_frame = self._create_section(main_container, "Dictionary Files")
        
        dict_grid = tk.Frame(self.dict_frame, bg="#2d2d2d")
        dict_grid.pack(fill="x", padx=15, pady=10)
        
        upload_btn = tk.Button(dict_grid, text="Upload Wordlist Files (.txt)", 
                              font=("Segoe UI", 10, "bold"), bg="#ff9800", fg="#000000",
                              activebackground="#f57c00", activeforeground="#000000",
                              command=self._upload_wordlists, width=25, height=1, 
                              relief="flat", bd=0, cursor="hand2")
        upload_btn.pack(pady=5)
        
        self.wordlist_label = tk.Label(dict_grid, text="No files uploaded", 
                                       font=("Segoe UI", 9), bg="#2d2d2d", fg="#888888")
        self.wordlist_label.pack(pady=5)
        
        # Action Button
        btn_frame = tk.Frame(main_container, bg="#1e1e1e")
        btn_frame.pack(pady=20)
        
        crack_btn = tk.Button(btn_frame, text="CRACK PASSWORD", 
                             font=("Segoe UI", 12, "bold"), bg="#00d9ff", fg="#000000",
                             activebackground="#00b8d4", activeforeground="#000000",
                             command=self.run_attack, width=35, height=2, 
                             relief="flat", bd=0, cursor="hand2")
        crack_btn.pack()
    
    def _create_section(self, parent, title):
        """Create a styled section frame"""
        frame = tk.LabelFrame(parent, text=title, font=("Segoe UI", 11, "bold"), 
                             bg="#2d2d2d", fg="#00d9ff", relief="flat", bd=2, 
                             labelanchor="nw", padx=5, pady=5)
        frame.pack(fill="x", pady=10)
        return frame
    
    def _on_password_type_change(self, event=None):
        """Show/hide hash algorithm based on password type"""
        if self.password_type_var.get() == "Hash Value":
            self.algo_frame.pack(fill="x", pady=10, after=self.credential_entry.master.master)
            self.cred_label.config(text="Hash Value:")
            self.credential_entry.config(show="")
        else:
            self.algo_frame.pack_forget()
            self.cred_label.config(text="Password:")
            self.credential_entry.config(show="*")
    
    def _on_attack_type_change(self, event=None):
        """Show/hide dictionary upload based on attack type"""
        if self.attack_type_var.get() == "Dictionary Attack":
            self.dict_frame.pack(fill="x", pady=10)
        else:
            self.dict_frame.pack_forget()
    
    def _upload_wordlists(self):
        """Upload multiple wordlist files"""
        files = filedialog.askopenfilenames(
            title="Select Wordlist Files",
            filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")]
        )
        
        if files:
            self.wordlist_files = list(files)
            self.wordlist_label.config(
                text=f"{len(self.wordlist_files)} file(s) uploaded",
                fg="#00ff00"
            )
    
    def run_attack(self):
        """Execute the selected attack"""
        first_name = self.first_name_entry.get().strip()
        last_name = self.last_name_entry.get().strip()
        credential = self.credential_entry.get().strip()
        password_type = self.password_type_var.get()
        attack_type = self.attack_type_var.get()
        algorithm = self.algorithm_var.get() if password_type == "Hash Value" else None
        
        # Validation
        if not first_name or not last_name:
            messagebox.showerror("Error", "Please enter first name and last name")
            return
        
        if not credential:
            messagebox.showerror("Error", "Please enter password or hash value")
            return
        
        if attack_type == "Dictionary Attack" and not self.wordlist_files:
            messagebox.showerror("Error", "Please upload wordlist files for Dictionary Attack")
            return
        
        # Execute attack
        try:
            cracked = False
            found_password = None
            method = ""
            
            if attack_type == "Dictionary Attack":
                if password_type == "Plain Password":
                    cracked, found_password, method = dictionary_attack_plain(
                        credential, self.wordlist_files, first_name, last_name
                    )
                else:
                    cracked, found_password, method = dictionary_attack_hash(
                        credential, algorithm, self.wordlist_files, first_name, last_name
                    )
            
            elif attack_type == "Brute Force":
                if password_type == "Plain Password":
                    cracked, found_password, method = brute_force_plain(credential)
                else:
                    cracked, found_password, method = brute_force_hash(credential, algorithm)
            
            elif attack_type == "AI Search":
                if password_type == "Plain Password":
                    cracked, found_password, method = ai_attack_plain(
                        credential, first_name, last_name
                    )
                else:
                    cracked, found_password, method = ai_attack_hash(
                        credential, algorithm, first_name, last_name
                    )
            
            # Prepare result
            if cracked:
                result = f"Password cracked using {method}. Found: {found_password}"
            else:
                result = f"Password not cracked. {method}"
            
            # Save to database
            save_case_record(
                first_name, last_name, password_type, attack_type, 
                algorithm if algorithm else "N/A", result
            )
            
            # Display result
            self.display_result(cracked, result, found_password)
            
        except Exception as e:
            messagebox.showerror("Error", f"Attack failed: {str(e)}")
    
    def display_result(self, cracked, result_text, found_password):
        """Display result in popup window"""
        result_window = tk.Toplevel(self.window)
        result_window.title("Attack Result")
        result_window.geometry("600x400")
        result_window.resizable(False, False)
        result_window.configure(bg="#1e1e1e")
        
        # Title
        title_frame = tk.Frame(result_window, bg="#2d2d2d", relief="flat")
        title_frame.pack(fill="x", pady=(0, 20))
        
        title = tk.Label(title_frame, text="ATTACK RESULT", 
                        font=("Segoe UI", 16, "bold"), bg="#2d2d2d", fg="#00d9ff")
        title.pack(pady=15)
        
        # Result container
        result_container = tk.Frame(result_window, bg="#1e1e1e")
        result_container.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Status
        status_color = "#00ff00" if cracked else "#ff4444"
        status_text = "SUCCESS" if cracked else "FAILED"
        
        status_card = tk.Frame(result_container, bg="#3c3c3c", relief="flat", bd=1)
        status_card.pack(fill="x", pady=10)
        
        tk.Label(status_card, text="Status:", font=("Segoe UI", 12, "bold"), 
                bg="#3c3c3c", fg="#cccccc").pack(side="left", padx=20, pady=15)
        tk.Label(status_card, text=status_text, font=("Segoe UI", 14, "bold"), 
                bg="#3c3c3c", fg=status_color).pack(side="right", padx=20, pady=15)
        
        # Result message
        msg_card = tk.Frame(result_container, bg="#3c3c3c", relief="flat", bd=1)
        msg_card.pack(fill="both", expand=True, pady=10)
        
        tk.Label(msg_card, text=result_text, font=("Segoe UI", 11), 
                bg="#3c3c3c", fg="#ffffff", wraplength=550, justify="left").pack(padx=20, pady=20)
        
        # Close button
        close_btn = tk.Button(result_window, text="CLOSE", 
                             font=("Segoe UI", 10, "bold"), bg="#00d9ff", fg="#000000",
                             activebackground="#00b8d4", activeforeground="#000000",
                             command=result_window.destroy, width=20, height=1, 
                             relief="flat", bd=0, cursor="hand2")
        close_btn.pack(pady=15)
