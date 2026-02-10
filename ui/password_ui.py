import tkinter as tk
from tkinter import ttk, messagebox, filedialog, scrolledtext
from backend.dictionary_attack import dictionary_attack_plain, dictionary_attack_hash
from backend.brute_force import brute_force_plain, brute_force_hash
from backend.ai_attack import ai_attack_plain, ai_attack_hash
from backend.hashing_utils import hash_password
from backend.database import init_database, save_case_record
import os
from PIL import Image, ImageTk
import threading

class PasswordUI:
    def __init__(self, window):
        self.window = window
        self.window.title("Password Attack Simulation")
        self.window.geometry("1100x750")
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
                img = img.resize((1100, 750), Image.Resampling.LANCZOS)
                self.bg_image = ImageTk.PhotoImage(img)
            except:
                pass
        
        # Background
        if self.bg_image:
            bg_label = tk.Label(window, image=self.bg_image)
            bg_label.place(x=0, y=0, relwidth=1, relheight=1)
        
        # Main container with two columns
        main_container = tk.Frame(window, bg="#1e1e1e")
        main_container.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Left column - Input
        left_frame = tk.Frame(main_container, bg="#1e1e1e")
        left_frame.pack(side="left", fill="both", expand=True, padx=(0, 10))
        
        # Right column - Output
        right_frame = tk.Frame(main_container, bg="#1e1e1e")
        right_frame.pack(side="right", fill="both", expand=True, padx=(10, 0))
        
        # Title
        title_frame = tk.Frame(left_frame, bg="#2d2d2d", relief="flat")
        title_frame.pack(fill="x", pady=(0, 15))
        
        title = tk.Label(title_frame, text="PASSWORD ATTACK SIMULATION", 
                        font=("Segoe UI", 16, "bold"), bg="#2d2d2d", fg="#00d9ff")
        title.pack(pady=12)
        
        # User Details Section
        user_frame = self._create_section(left_frame, "User Details")
        
        user_grid = tk.Frame(user_frame, bg="#2d2d2d")
        user_grid.pack(fill="x", padx=10, pady=8)
        
        tk.Label(user_grid, text="First Name:", font=("Segoe UI", 9), 
                bg="#2d2d2d", fg="#cccccc").grid(row=0, column=0, sticky="w", pady=5)
        self.first_name_entry = tk.Entry(user_grid, width=20, font=("Segoe UI", 9), 
                                        bg="#3c3c3c", fg="#ffffff", insertbackground="#ffffff", 
                                        relief="flat", bd=3)
        self.first_name_entry.grid(row=0, column=1, pady=5, padx=8, sticky="ew")
        
        tk.Label(user_grid, text="Last Name:", font=("Segoe UI", 9), 
                bg="#2d2d2d", fg="#cccccc").grid(row=1, column=0, sticky="w", pady=5)
        self.last_name_entry = tk.Entry(user_grid, width=20, font=("Segoe UI", 9), 
                                       bg="#3c3c3c", fg="#ffffff", insertbackground="#ffffff", 
                                       relief="flat", bd=3)
        self.last_name_entry.grid(row=1, column=1, pady=5, padx=8, sticky="ew")
        
        user_grid.columnconfigure(1, weight=1)
        
        # Password Type Selection
        type_frame = self._create_section(left_frame, "Password Type")
        
        type_grid = tk.Frame(type_frame, bg="#2d2d2d")
        type_grid.pack(fill="x", padx=10, pady=8)
        
        self.password_type_var = tk.StringVar(value="Plain Password")
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('Custom.TCombobox', fieldbackground="#3c3c3c", 
                       background="#3c3c3c", foreground="#ffffff", borderwidth=0)
        
        password_type_combo = ttk.Combobox(type_grid, textvariable=self.password_type_var, 
                                          values=["Plain Password", "Hash Value"], 
                                          state="readonly", width=35, 
                                          font=("Segoe UI", 9), style='Custom.TCombobox')
        password_type_combo.pack(fill="x", pady=5)
        password_type_combo.bind("<<ComboboxSelected>>", self._on_password_type_change)
        
        # Credential Input
        cred_frame = self._create_section(left_frame, "Credential Input")
        
        cred_grid = tk.Frame(cred_frame, bg="#2d2d2d")
        cred_grid.pack(fill="x", padx=10, pady=8)
        
        self.cred_label = tk.Label(cred_grid, text="Password:", font=("Segoe UI", 9), 
                                   bg="#2d2d2d", fg="#cccccc")
        self.cred_label.pack(anchor="w", pady=(0,5))
        
        self.credential_entry = tk.Entry(cred_grid, width=40, font=("Segoe UI", 9), 
                                        bg="#3c3c3c", fg="#ffffff", insertbackground="#ffffff", 
                                        relief="flat", bd=3, show="*")
        self.credential_entry.pack(fill="x", pady=5)
        
        # Hash Algorithm Selection (Hidden by default)
        self.algo_frame = self._create_section(left_frame, "Hash Algorithm")
        self.algo_frame.pack_forget()
        
        algo_grid = tk.Frame(self.algo_frame, bg="#2d2d2d")
        algo_grid.pack(fill="x", padx=10, pady=8)
        
        self.algorithm_var = tk.StringVar(value="MD5")
        algorithm_combo = ttk.Combobox(algo_grid, textvariable=self.algorithm_var, 
                                      values=["MD5", "SHA256"], state="readonly", 
                                      width=35, font=("Segoe UI", 9), style='Custom.TCombobox')
        algorithm_combo.pack(fill="x", pady=5)
        
        # Attack Type Selection
        attack_frame = self._create_section(left_frame, "Attack Type")
        
        attack_grid = tk.Frame(attack_frame, bg="#2d2d2d")
        attack_grid.pack(fill="x", padx=10, pady=8)
        
        self.attack_type_var = tk.StringVar(value="Dictionary Attack")
        attack_combo = ttk.Combobox(attack_grid, textvariable=self.attack_type_var, 
                                    values=["Brute Force", "Dictionary Attack", "AI Search"], 
                                    state="readonly", width=35, 
                                    font=("Segoe UI", 9), style='Custom.TCombobox')
        attack_combo.pack(fill="x", pady=5)
        attack_combo.bind("<<ComboboxSelected>>", self._on_attack_type_change)
        
        # Dictionary Upload Section
        self.dict_frame = self._create_section(left_frame, "Dictionary Files")
        
        dict_grid = tk.Frame(self.dict_frame, bg="#2d2d2d")
        dict_grid.pack(fill="x", padx=10, pady=8)
        
        upload_btn = tk.Button(dict_grid, text="Upload Wordlist Files", 
                              font=("Segoe UI", 9, "bold"), bg="#ff9800", fg="#000000",
                              activebackground="#f57c00", activeforeground="#000000",
                              command=self._upload_wordlists, width=20, height=1, 
                              relief="flat", bd=0, cursor="hand2")
        upload_btn.pack(pady=5)
        
        self.wordlist_label = tk.Label(dict_grid, text="No files uploaded", 
                                       font=("Segoe UI", 8), bg="#2d2d2d", fg="#888888")
        self.wordlist_label.pack(pady=3)
        
        # Action Button
        btn_frame = tk.Frame(left_frame, bg="#1e1e1e")
        btn_frame.pack(pady=15)
        
        crack_btn = tk.Button(btn_frame, text="CRACK PASSWORD", 
                             font=("Segoe UI", 11, "bold"), bg="#00d9ff", fg="#000000",
                             activebackground="#00b8d4", activeforeground="#000000",
                             command=self.run_attack, width=30, height=2, 
                             relief="flat", bd=0, cursor="hand2")
        crack_btn.pack()
        
        # Right side - Real-time Output
        output_title_frame = tk.Frame(right_frame, bg="#2d2d2d", relief="flat")
        output_title_frame.pack(fill="x", pady=(0, 15))
        
        output_title = tk.Label(output_title_frame, text="REAL-TIME PROCESS LOG", 
                               font=("Segoe UI", 16, "bold"), bg="#2d2d2d", fg="#00d9ff")
        output_title.pack(pady=12)
        
        # Output text area
        output_frame = tk.Frame(right_frame, bg="#2d2d2d", relief="flat", bd=2)
        output_frame.pack(fill="both", expand=True)
        
        self.output_text = scrolledtext.ScrolledText(output_frame, 
                                                     font=("Consolas", 9),
                                                     bg="#1a1a1a", fg="#00ff00",
                                                     insertbackground="#00ff00",
                                                     relief="flat", bd=10,
                                                     wrap=tk.WORD, state="disabled")
        self.output_text.pack(fill="both", expand=True)
        
        # Configure text tags for colors
        self.output_text.tag_config("info", foreground="#00d9ff")
        self.output_text.tag_config("success", foreground="#00ff00")
        self.output_text.tag_config("error", foreground="#ff4444")
        self.output_text.tag_config("warning", foreground="#ff9800")
    
    def _create_section(self, parent, title):
        """Create a styled section frame"""
        frame = tk.LabelFrame(parent, text=title, font=("Segoe UI", 10, "bold"), 
                             bg="#2d2d2d", fg="#00d9ff", relief="flat", bd=2, 
                             labelanchor="nw", padx=5, pady=5)
        frame.pack(fill="x", pady=8)
        return frame
    
    def _on_password_type_change(self, event=None):
        """Show/hide hash algorithm based on password type"""
        if self.password_type_var.get() == "Hash Value":
            self.algo_frame.pack(fill="x", pady=8, after=self.credential_entry.master.master)
            self.cred_label.config(text="Hash Value:")
            self.credential_entry.config(show="")
        else:
            self.algo_frame.pack_forget()
            self.cred_label.config(text="Password:")
            self.credential_entry.config(show="*")
    
    def _on_attack_type_change(self, event=None):
        """Show/hide dictionary upload based on attack type"""
        if self.attack_type_var.get() == "Dictionary Attack":
            self.dict_frame.pack(fill="x", pady=8)
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
    
    def log_output(self, message, tag="info"):
        """Add message to output text area"""
        self.output_text.config(state="normal")
        self.output_text.insert(tk.END, message + "\n", tag)
        self.output_text.see(tk.END)
        self.output_text.config(state="disabled")
        self.window.update()
    
    def clear_output(self):
        """Clear output text area"""
        self.output_text.config(state="normal")
        self.output_text.delete(1.0, tk.END)
        self.output_text.config(state="disabled")
    
    def run_attack(self):
        """Execute the selected attack in a thread"""
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
        
        # Clear previous output
        self.clear_output()
        
        # Run attack in thread
        thread = threading.Thread(target=self._execute_attack, 
                                 args=(first_name, last_name, credential, password_type, 
                                      attack_type, algorithm))
        thread.daemon = True
        thread.start()
    
    def _execute_attack(self, first_name, last_name, credential, password_type, attack_type, algorithm):
        """Execute attack with real-time logging"""
        try:
            self.log_output("="*50, "info")
            self.log_output(f"Starting {attack_type}...", "info")
            self.log_output(f"Target: {first_name} {last_name}", "info")
            self.log_output(f"Mode: {password_type}", "info")
            if algorithm:
                self.log_output(f"Algorithm: {algorithm}", "info")
            self.log_output("="*50, "info")
            self.log_output("")
            
            cracked = False
            found_password = None
            method = ""
            
            if attack_type == "Dictionary Attack":
                if password_type == "Plain Password":
                    cracked, found_password, method = self._dict_attack_plain_with_log(
                        credential, first_name, last_name
                    )
                else:
                    cracked, found_password, method = self._dict_attack_hash_with_log(
                        credential, algorithm, first_name, last_name
                    )
            
            elif attack_type == "Brute Force":
                self.log_output("Starting brute force attack...", "warning")
                if password_type == "Plain Password":
                    cracked, found_password, method = brute_force_plain(credential)
                else:
                    cracked, found_password, method = brute_force_hash(credential, algorithm)
                
                if cracked:
                    self.log_output(f"✓ Password cracked: {found_password}", "success")
                else:
                    self.log_output("✗ Brute force failed", "error")
            
            elif attack_type == "AI Search":
                self.log_output("Starting AI-based search...", "warning")
                if password_type == "Plain Password":
                    cracked, found_password, method = ai_attack_plain(credential, first_name, last_name)
                else:
                    cracked, found_password, method = ai_attack_hash(credential, algorithm, first_name, last_name)
                
                if cracked:
                    self.log_output(f"✓ Password found: {found_password}", "success")
                else:
                    self.log_output("✗ AI search failed", "error")
            
            # Final result
            self.log_output("")
            self.log_output("="*50, "info")
            if cracked:
                result = f"SUCCESS: Password cracked using {method}. Found: {found_password}"
                self.log_output(result, "success")
            else:
                result = f"FAILED: Password not cracked. {method}"
                self.log_output(result, "error")
            self.log_output("="*50, "info")
            
            # Save to database
            save_case_record(
                first_name, last_name, password_type, attack_type, 
                algorithm if algorithm else "N/A", result
            )
            self.log_output("Case saved to database.", "info")
            
        except Exception as e:
            self.log_output(f"ERROR: {str(e)}", "error")
    
    def _dict_attack_plain_with_log(self, password, first_name, last_name):
        """Dictionary attack for plain password with logging"""
        # Check personal information first
        self.log_output("Checking personal information...", "info")
        
        if password.lower() == first_name.lower():
            self.log_output(f"✓ Match found: First name '{first_name}'", "success")
            return True, password, "Personal Information Match"
        
        if password.lower() == last_name.lower():
            self.log_output(f"✓ Match found: Last name '{last_name}'", "success")
            return True, password, "Personal Information Match"
        
        self.log_output("✗ No personal information match", "warning")
        self.log_output("")
        
        # Check wordlists
        self.log_output("Scanning wordlist files...", "info")
        total_checked = 0
        
        for idx, wordlist_path in enumerate(self.wordlist_files, 1):
            filename = os.path.basename(wordlist_path)
            self.log_output(f"File {idx}/{len(self.wordlist_files)}: {filename}", "info")
            
            try:
                with open(wordlist_path, 'r', encoding='utf-8', errors='ignore') as f:
                    for line_num, line in enumerate(f, 1):
                        word = line.strip()
                        total_checked += 1
                        
                        if total_checked % 100 == 0:
                            self.log_output(f"  Checked {total_checked} passwords...", "info")
                        
                        if word == password:
                            self.log_output(f"✓ MATCH FOUND at line {line_num}: '{word}'", "success")
                            return True, word, "Dictionary Attack"
                
                self.log_output(f"  Completed: {line_num} passwords checked", "info")
            except Exception as e:
                self.log_output(f"  Error reading file: {str(e)}", "error")
        
        self.log_output(f"Total passwords checked: {total_checked}", "info")
        self.log_output("✗ No match found in wordlists", "error")
        return False, None, "Not Found"
    
    def _dict_attack_hash_with_log(self, target_hash, algorithm, first_name, last_name):
        """Dictionary attack for hash with logging"""
        # Check personal information first
        self.log_output("Checking personal information...", "info")
        
        for name in [first_name, last_name]:
            if name:
                name_hash = hash_password(name, algorithm)
                self.log_output(f"  Hashing '{name}': {name_hash[:16]}...", "info")
                if name_hash == target_hash:
                    self.log_output(f"✓ Match found: '{name}'", "success")
                    return True, name, f"Personal Information Match with {algorithm}"
        
        self.log_output("✗ No personal information match", "warning")
        self.log_output("")
        
        # Check wordlists
        self.log_output("Scanning wordlist files...", "info")
        total_checked = 0
        
        for idx, wordlist_path in enumerate(self.wordlist_files, 1):
            filename = os.path.basename(wordlist_path)
            self.log_output(f"File {idx}/{len(self.wordlist_files)}: {filename}", "info")
            
            try:
                with open(wordlist_path, 'r', encoding='utf-8', errors='ignore') as f:
                    for line_num, line in enumerate(f, 1):
                        word = line.strip()
                        total_checked += 1
                        
                        if total_checked % 100 == 0:
                            self.log_output(f"  Checked {total_checked} passwords...", "info")
                        
                        word_hash = hash_password(word, algorithm)
                        if word_hash == target_hash:
                            self.log_output(f"✓ MATCH FOUND at line {line_num}: '{word}'", "success")
                            return True, word, f"Dictionary Attack with {algorithm}"
                
                self.log_output(f"  Completed: {line_num} passwords checked", "info")
            except Exception as e:
                self.log_output(f"  Error reading file: {str(e)}", "error")
        
        self.log_output(f"Total passwords checked: {total_checked}", "info")
        self.log_output(f"✗ No match found with {algorithm}", "error")
        return False, None, f"Not Cracked with {algorithm}"
