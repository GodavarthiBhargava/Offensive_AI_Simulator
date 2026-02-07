import tkinter as tk
from tkinter import ttk, messagebox
from backend.password_engine import simulate_password_attack

class PasswordUI:
    def __init__(self, window):
        self.window = window
        self.window.title("Password Attack Simulation")
        self.window.geometry("850x750")
        self.window.resizable(False, False)
        self.window.configure(bg="#1e1e1e")
        
        # Main container
        main_container = tk.Frame(window, bg="#1e1e1e")
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
        
        mode_radio_frame = tk.Frame(mode_frame, bg="#2d2d2d")
        mode_radio_frame.pack(fill="x", padx=15, pady=10)
        
        self.input_mode = tk.StringVar(value="password")
        
        rb1 = tk.Radiobutton(mode_radio_frame, text="Enter Password", variable=self.input_mode, 
                            value="password", font=("Segoe UI", 10), bg="#2d2d2d", fg="#cccccc", 
                            selectcolor="#3c3c3c", activebackground="#2d2d2d", 
                            activeforeground="#00d9ff", command=self._toggle_input_mode)
        rb1.pack(side="left", padx=20)
        
        rb2 = tk.Radiobutton(mode_radio_frame, text="Enter Hash", variable=self.input_mode, 
                            value="hash", font=("Segoe UI", 10), bg="#2d2d2d", fg="#cccccc", 
                            selectcolor="#3c3c3c", activebackground="#2d2d2d", 
                            activeforeground="#00d9ff", command=self._toggle_input_mode)
        rb2.pack(side="left", padx=20)
        
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
        
        # Results Section
        results_frame = self._create_section(main_container, "Simulation Results")
        
        self.result_text = tk.Text(results_frame, height=10, width=85, 
                                   font=("Consolas", 10), bg="#0d0d0d", fg="#00ff00", 
                                   insertbackground="#00ff00", relief="flat", bd=0, 
                                   state="disabled", padx=15, pady=15)
        self.result_text.pack(fill="both", expand=True, padx=15, pady=10)
    
    def _create_section(self, parent, title):
        """Create a styled section frame"""
        frame = tk.LabelFrame(parent, text=title, font=("Segoe UI", 11, "bold"), 
                             bg="#2d2d2d", fg="#00d9ff", relief="flat", bd=2, 
                             labelanchor="nw", padx=5, pady=5)
        frame.pack(fill="x", pady=10)
        return frame
    
    def _toggle_input_mode(self):
        """Toggle between password and hash input modes"""
        if self.input_mode.get() == "password":
            self.input_label.config(text="Password:")
            self.credential_entry.config(show="*")
        else:
            self.input_label.config(text="Hash:")
            self.credential_entry.config(show="")
    
    def run_simulation(self):
        print("Button clicked!")  # Debug
        credential = self.credential_entry.get().strip()
        algorithm = self.algorithm_var.get()
        username = self.username_entry.get().strip()
        fullname = self.fullname_entry.get().strip()
        input_mode = self.input_mode.get()
        
        print(f"Credential: {credential}")  # Debug
        print(f"Algorithm: {algorithm}")  # Debug
        print(f"Input mode: {input_mode}")  # Debug
        
        if not credential:
            messagebox.showerror("Error", "Please enter a password or hash")
            return
        
        try:
            print("Starting simulation...")  # Debug
            # Run simulation
            result = simulate_password_attack(
                credential=credential,
                algorithm=algorithm,
                input_mode=input_mode,
                username=username,
                fullname=fullname
            )
            
            print(f"Result: {result}")  # Debug
            
            # Display results
            self.result_text.config(state="normal")
            self.result_text.delete(1.0, tk.END)
            
            output = "=" * 80 + "\n"
            output += "  SIMULATION RESULTS\n"
            output += "=" * 80 + "\n\n"
            output += f"  Status:            {'CRACKED [X]' if result['cracked'] else 'NOT CRACKED [OK]'}\n"
            output += f"  Attack Used:       {result['attack_used']}\n"
            output += f"  Password Strength: {result['password_strength']}\n"
            output += f"  AI Risk Level:     {result['ai_risk_level']}\n"
            
            if result['cracked']:
                output += f"\n  Cracked Password:  {result['cracked_password']}\n"
            
            output += "\n" + "=" * 80 + "\n"
            output += "  WARNING: This is a simulation for educational purposes only\n"
            output += "=" * 80
            
            print("Inserting output...")  # Debug
            self.result_text.insert(1.0, output)
            self.result_text.config(state="disabled")
            print("Done!")  # Debug
        except Exception as e:
            print(f"ERROR: {e}")  # Debug
            import traceback
            traceback.print_exc()
            messagebox.showerror("Error", f"Simulation failed: {str(e)}")
