import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from backend.dictionary_attack import dictionary_attack_plain, dictionary_attack_hash
from backend.brute_force import brute_force_plain, brute_force_hash
from backend.ai_attack import ai_attack_plain, ai_attack_hash
from backend.hashing_utils import hash_password
from backend.database import init_database, save_case_record, generate_case_id
import time
import threading
import os

class PasswordAttackModule:
    def __init__(self, window):
        self.window = window
        self.window.title("Skill Palavar - Module 1")
        self.window.geometry("1200x650")
        self.window.configure(bg="#2E2E2E")
        
        # Initialize database
        init_database()
        
        # Wordlist files
        self.wordlist_files = []
        
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
        # First Name
        self.first_name_frame = self._create_input(left_panel, "FIRST NAME")
        
        # Last Name
        self.last_name_frame = self._create_input(left_panel, "LAST NAME")
        
        # Password Type
        self.input_type_var = tk.StringVar(value="Plain Password")
        input_type_dropdown = self._create_dropdown(left_panel, "PASSWORD TYPE", self.input_type_var,
                             ["Plain Password", "Hash Value"], self.toggle_input_mode)
        
        # Password/Hash input
        self.password_frame = self._create_input(left_panel, "PASSWORD", show="*")
        
        # Hash Algorithm (hidden by default)
        self.hash_algo_var = tk.StringVar(value="MD5")
        self.hash_algo_frame = tk.Frame(left_panel, bg="#2E2E2E")
        tk.Label(self.hash_algo_frame, text="HASH ALGORITHM", font=("Consolas", 10),
                bg="#2E2E2E", fg="#00FF66").pack(anchor="w", pady=(0, 5))
        hash_combo = ttk.Combobox(self.hash_algo_frame, textvariable=self.hash_algo_var,
                                 values=["MD5", "SHA256"], state="readonly",
                                 font=("Consolas", 10), style='Custom.TCombobox', height=10)
        hash_combo.pack(fill="x", ipady=8)
        self.hash_algo_frame.pack_forget()
        
        # Attack Type
        self.attack_type_var = tk.StringVar(value="Dictionary Attack")
        self._create_dropdown(left_panel, "ATTACK TYPE", self.attack_type_var,
                             ["Brute Force", "Dictionary Attack", "AI Search"], self.toggle_attack_type)
        
        # Dictionary Upload (shown only for Dictionary Attack)
        self.dict_upload_frame = tk.Frame(left_panel, bg="#2E2E2E")
        tk.Label(self.dict_upload_frame, text="WORDLIST FILES", font=("Consolas", 10),
                bg="#2E2E2E", fg="#00FF66").pack(anchor="w", pady=(0, 5))
        
        upload_btn = tk.Button(self.dict_upload_frame, text="Upload Wordlist Files",
                              font=("Consolas", 9, "bold"), bg="#000000", fg="#00FF66",
                              activebackground="#003300", relief="solid", bd=1,
                              cursor="hand2", command=self.upload_wordlists)
        upload_btn.pack(fill="x", ipady=5)
        
        self.wordlist_label = tk.Label(self.dict_upload_frame, text="No files uploaded",
                                       font=("Consolas", 8), bg="#2E2E2E", fg="#666666")
        self.wordlist_label.pack(pady=(5, 0))
        self.dict_upload_frame.pack(fill="x", pady=(0, 15))
        
        # Crack button
        btn_frame = tk.Frame(left_panel, bg="#2E2E2E")
        btn_frame.pack(fill="x", pady=15)
        
        self.crack_btn = tk.Button(btn_frame, text="CRACK PASSWORD",
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
        if self.input_type_var.get() == "Plain Password":
            self.password_frame.entry.config(show="*")
            self.hash_algo_frame.pack_forget()
        else:
            self.password_frame.entry.config(show="")
            self.hash_algo_frame.pack(fill="x", pady=(0, 15), before=self.attack_type_var.master)
    
    def toggle_attack_type(self):
        if self.attack_type_var.get() == "Dictionary Attack":
            self.dict_upload_frame.pack(fill="x", pady=(0, 15))
        else:
            self.dict_upload_frame.pack_forget()
    
    def upload_wordlists(self):
        files = filedialog.askopenfilenames(
            title="Select Wordlist Files",
            filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")]
        )
        
        if files:
            self.wordlist_files = list(files)
            self.wordlist_label.config(
                text=f"{len(self.wordlist_files)} file(s) uploaded",
                fg="#00FF66"
            )
    
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
        first_name = self.first_name_frame.entry.get().strip()
        last_name = self.last_name_frame.entry.get().strip()
        credential = self.password_frame.entry.get().strip()
        password_type = self.input_type_var.get()
        attack_type = self.attack_type_var.get()
        algorithm = self.hash_algo_var.get() if password_type == "Hash Value" else None
        
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
        
        # Clear console and run attack in thread
        self.clear_console()
        thread = threading.Thread(target=self._execute_attack,
                                 args=(first_name, last_name, credential, password_type,
                                      attack_type, algorithm))
        thread.daemon = True
        thread.start()
    
    def _execute_attack(self, first_name, last_name, credential, password_type, attack_type, algorithm):
        """Execute attack with real-time logging"""
        try:
            self.print_console("="*60, 0.05)
            self.print_console(f"[INFO] Starting {attack_type}...", 0.1)
            self.print_console(f"[INFO] Target: {first_name} {last_name}", 0.05)
            self.print_console(f"[INFO] Mode: {password_type}", 0.05)
            if algorithm:
                self.print_console(f"[INFO] Algorithm: {algorithm}", 0.05)
            self.print_console("="*60, 0.05)
            self.print_console("", 0.05)
            
            cracked = False
            found_password = None
            method = ""
            
            if attack_type == "Dictionary Attack":
                if password_type == "Plain Password":
                    cracked, found_password, method = self._dict_attack_plain_log(
                        credential, first_name, last_name
                    )
                else:
                    cracked, found_password, method = self._dict_attack_hash_log(
                        credential, algorithm, first_name, last_name
                    )
            
            elif attack_type == "Brute Force":
                self.print_console("[INFO] Starting brute force attack...", 0.1)
                if password_type == "Plain Password":
                    cracked, found_password, method = brute_force_plain(credential)
                else:
                    cracked, found_password, method = brute_force_hash(credential, algorithm)
                
                if cracked:
                    self.print_console(f"[SUCCESS] Password cracked: {found_password}", 0.1)
                else:
                    self.print_console("[FAILED] Brute force failed", 0.1)
            
            elif attack_type == "AI Search":
                self.print_console("[INFO] Starting AI-based search...", 0.1)
                if password_type == "Plain Password":
                    cracked, found_password, method = ai_attack_plain(credential, first_name, last_name)
                else:
                    cracked, found_password, method = ai_attack_hash(credential, algorithm, first_name, last_name)
                
                if cracked:
                    self.print_console(f"[SUCCESS] Password found: {found_password}", 0.1)
                else:
                    self.print_console("[FAILED] AI search failed", 0.1)
            
            # Final result
            self.print_console("", 0.05)
            self.print_console("="*60, 0.05)
            if cracked:
                result_text = f"SUCCESS: Password cracked using {method}. Found: {found_password}"
                self.print_console(f"[SUCCESS] {result_text}", 0.1)
            else:
                result_text = f"FAILED: Password not cracked. {method}"
                self.print_console(f"[FAILED] {result_text}", 0.1)
            self.print_console("="*60, 0.05)
            
            # Generate case ID and save to database
            case_id = generate_case_id()
            result_status = "Cracked" if cracked else "Not Cracked"
            
            save_case_record(
                case_id, first_name, last_name, credential, password_type, attack_type,
                algorithm if algorithm else "N/A", result_status, found_password if found_password else "N/A"
            )
            self.print_console(f"[INFO] Case saved to database: {case_id}", 0.1)
            
        except Exception as e:
            self.print_console(f"[ERROR] {str(e)}", 0.1)
    
    def _dict_attack_plain_log(self, password, first_name, last_name):
        """Dictionary attack for plain password with logging"""
        self.print_console("[INFO] Checking personal information...", 0.1)
        
        if password.lower() == first_name.lower():
            self.print_console(f"[SUCCESS] Match found: First name '{first_name}'", 0.1)
            return True, password, "Personal Information Match"
        
        if password.lower() == last_name.lower():
            self.print_console(f"[SUCCESS] Match found: Last name '{last_name}'", 0.1)
            return True, password, "Personal Information Match"
        
        self.print_console("[INFO] No personal information match", 0.05)
        self.print_console("", 0.05)
        
        self.print_console("[INFO] Scanning wordlist files...", 0.1)
        total_checked = 0
        
        for idx, wordlist_path in enumerate(self.wordlist_files, 1):
            filename = os.path.basename(wordlist_path)
            self.print_console(f"[INFO] File {idx}/{len(self.wordlist_files)}: {filename}", 0.05)
            
            try:
                with open(wordlist_path, 'r', encoding='utf-8', errors='ignore') as f:
                    for line_num, line in enumerate(f, 1):
                        word = line.strip()
                        if not word:  # Skip empty lines
                            continue
                        
                        total_checked += 1
                        
                        if total_checked % 100 == 0:
                            self.print_console(f"[INFO] Checked {total_checked} passwords...", 0.01)
                        
                        # Case-insensitive comparison
                        if word.lower() == password.lower():
                            self.print_console(f"[SUCCESS] MATCH FOUND at line {line_num}: '{word}'", 0.1)
                            return True, word, "Dictionary Attack"
                
                self.print_console(f"[INFO] Completed: {line_num} passwords checked", 0.05)
            except Exception as e:
                self.print_console(f"[ERROR] Error reading file: {str(e)}", 0.05)
        
        self.print_console(f"[INFO] Total passwords checked: {total_checked}", 0.05)
        self.print_console("[FAILED] No match found in wordlists", 0.1)
        return False, None, "Not Found"
    
    def _dict_attack_hash_log(self, target_hash, algorithm, first_name, last_name):
        """Dictionary attack for hash with logging"""
        self.print_console("[INFO] Checking personal information...", 0.1)
        
        for name in [first_name, last_name]:
            if name:
                name_hash = hash_password(name, algorithm)
                self.print_console(f"[INFO] Hashing '{name}': {name_hash[:16]}...", 0.05)
                if name_hash.lower() == target_hash.lower():
                    self.print_console(f"[SUCCESS] Match found: '{name}'", 0.1)
                    return True, name, f"Personal Information Match with {algorithm}"
        
        self.print_console("[INFO] No personal information match", 0.05)
        self.print_console("", 0.05)
        
        self.print_console("[INFO] Scanning wordlist files...", 0.1)
        total_checked = 0
        
        for idx, wordlist_path in enumerate(self.wordlist_files, 1):
            filename = os.path.basename(wordlist_path)
            self.print_console(f"[INFO] File {idx}/{len(self.wordlist_files)}: {filename}", 0.05)
            
            try:
                with open(wordlist_path, 'r', encoding='utf-8', errors='ignore') as f:
                    for line_num, line in enumerate(f, 1):
                        word = line.strip()
                        if not word:  # Skip empty lines
                            continue
                        
                        total_checked += 1
                        
                        if total_checked % 100 == 0:
                            self.print_console(f"[INFO] Checked {total_checked} passwords...", 0.01)
                        
                        word_hash = hash_password(word, algorithm)
                        if word_hash.lower() == target_hash.lower():
                            self.print_console(f"[SUCCESS] MATCH FOUND at line {line_num}: '{word}'", 0.1)
                            return True, word, f"Dictionary Attack with {algorithm}"
                
                self.print_console(f"[INFO] Completed: {line_num} passwords checked", 0.05)
            except Exception as e:
                self.print_console(f"[ERROR] Error reading file: {str(e)}", 0.05)
        
        self.print_console(f"[INFO] Total passwords checked: {total_checked}", 0.05)
        self.print_console(f"[FAILED] No match found with {algorithm}", 0.1)
        return False, None, f"Not Cracked with {algorithm}"


if __name__ == "__main__":
    root = tk.Tk()
    PasswordAttackModule(root)
    root.mainloop()
