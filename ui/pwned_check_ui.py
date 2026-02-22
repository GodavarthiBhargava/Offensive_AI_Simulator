import tkinter as tk
from tkinter import messagebox, scrolledtext
from datetime import datetime
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from backend.pwned_check import check_password_exposure

class PwnedCheckModule:
    def __init__(self, root):
        self.root = root
        self.root.title("SECURENETRA - Pwned Password Checker")
        self.root.geometry("900x700")
        self.root.configure(bg="#2E2E2E")
        
        self.setup_ui()
    
    def setup_ui(self):
        # Header
        header_frame = tk.Frame(self.root, bg="#1F1F1F", height=60)
        header_frame.pack(fill="x")
        header_frame.pack_propagate(False)
        
        tk.Label(header_frame, text="🔍 PWNED PASSWORD CHECKER", 
                font=("Courier New", 18, "bold"), bg="#1F1F1F", fg="#00FF66").pack(pady=15)
        
        # Main container
        main_frame = tk.Frame(self.root, bg="#2E2E2E")
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Input section
        input_frame = tk.Frame(main_frame, bg="#1F1F1F", relief="solid", bd=2)
        input_frame.pack(fill="x", pady=(0, 20))
        
        tk.Label(input_frame, text="PASSWORD TO CHECK:", 
                font=("Courier New", 12, "bold"), bg="#1F1F1F", fg="#00FF66").pack(anchor="w", padx=20, pady=(15, 5))
        
        self.password_entry = tk.Entry(input_frame, font=("Courier New", 12, "bold"),
                                      bg="#000000", fg="#00FF66", relief="solid", bd=1,
                                      insertbackground="#00FF66", show="•", width=50)
        self.password_entry.pack(padx=20, pady=(0, 10), ipady=8)
        
        # Buttons
        btn_frame = tk.Frame(input_frame, bg="#1F1F1F")
        btn_frame.pack(pady=(0, 15))
        
        check_btn = tk.Button(btn_frame, text="🔍 CHECK EXPOSURE",
                             font=("Courier New", 12, "bold"), bg="#00FF66", fg="#000000",
                             activebackground="#00CC44", relief="flat", bd=0,
                             cursor="hand2", command=self.check_password, padx=20, pady=10)
        check_btn.pack(side="left", padx=5)
        
        clear_btn = tk.Button(btn_frame, text="🗑️ CLEAR",
                             font=("Courier New", 12, "bold"), bg="#FF4444", fg="#FFFFFF",
                             activebackground="#CC3333", relief="flat", bd=0,
                             cursor="hand2", command=self.clear_results, padx=20, pady=10)
        clear_btn.pack(side="left", padx=5)
        
        # Results section
        results_frame = tk.Frame(main_frame, bg="#1F1F1F", relief="solid", bd=2)
        results_frame.pack(fill="both", expand=True)
        
        tk.Label(results_frame, text="EXPOSURE CHECK RESULTS:", 
                font=("Courier New", 12, "bold"), bg="#1F1F1F", fg="#00FF66").pack(anchor="w", padx=20, pady=(15, 10))
        
        # Results display
        self.results_text = scrolledtext.ScrolledText(results_frame, 
                                                     font=("Courier New", 11),
                                                     bg="#000000", fg="#00FF66",
                                                     relief="solid", bd=1,
                                                     insertbackground="#00FF66",
                                                     selectbackground="#003300",
                                                     wrap=tk.WORD, height=15)
        self.results_text.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        
        # Info section
        info_frame = tk.Frame(main_frame, bg="#1F1F1F", relief="solid", bd=1)
        info_frame.pack(fill="x", pady=(10, 0))
        
        info_text = """ℹ️ ABOUT PWNED PASSWORDS:
• Uses Have I Been Pwned API with k-Anonymity model
• Only first 5 characters of password hash are sent
• Your actual password never leaves this system
• Risk Levels: Low (1-10), Medium (11-1000), High (1000+)"""
        
        tk.Label(info_frame, text=info_text, font=("Courier New", 9),
                bg="#1F1F1F", fg="#CCCCCC", justify="left").pack(anchor="w", padx=15, pady=10)
    
    def check_password(self):
        password = self.password_entry.get()
        
        if not password:
            messagebox.showerror("Error", "Please enter a password to check")
            return
        
        # Show loading message
        self.results_text.delete(1.0, tk.END)
        self.results_text.insert(tk.END, "🔄 Checking password exposure...\n\n")
        self.root.update()
        
        # Check password exposure
        result = check_password_exposure(password)
        
        # Clear loading message
        self.results_text.delete(1.0, tk.END)
        
        # Display results
        self.results_text.insert(tk.END, "=" * 60 + "\n")
        self.results_text.insert(tk.END, "PASSWORD EXPOSURE CHECK RESULTS\n")
        self.results_text.insert(tk.END, "=" * 60 + "\n\n")
        
        self.results_text.insert(tk.END, f"Password Length: {len(password)} characters\n")
        self.results_text.insert(tk.END, f"Status: {result['message']}\n\n")
        
        if result['found']:
            self.results_text.insert(tk.END, f"⚠️ EXPOSURE DETAILS:\n")
            self.results_text.insert(tk.END, f"Exposure Count: {result['exposure_count']:,} times\n")
            self.results_text.insert(tk.END, f"Risk Level: {result['risk_level']}\n\n")
            
            # Risk-based recommendations
            if result['risk_level'] == "High":
                self.results_text.insert(tk.END, "🚨 CRITICAL RISK - IMMEDIATE ACTION REQUIRED:\n")
                self.results_text.insert(tk.END, "• Change this password IMMEDIATELY\n")
                self.results_text.insert(tk.END, "• Check all accounts using this password\n")
                self.results_text.insert(tk.END, "• Enable 2FA on all accounts\n")
                self.results_text.insert(tk.END, "• Monitor accounts for suspicious activity\n")
            elif result['risk_level'] == "Medium":
                self.results_text.insert(tk.END, "⚠️ MODERATE RISK - ACTION RECOMMENDED:\n")
                self.results_text.insert(tk.END, "• Consider changing this password\n")
                self.results_text.insert(tk.END, "• Use unique passwords for each account\n")
                self.results_text.insert(tk.END, "• Enable two-factor authentication\n")
            else:  # Low
                self.results_text.insert(tk.END, "⚡ LOW RISK - MONITOR:\n")
                self.results_text.insert(tk.END, "• Password has minimal exposure\n")
                self.results_text.insert(tk.END, "• Still consider using unique passwords\n")
                self.results_text.insert(tk.END, "• Regular security checkups recommended\n")
        else:
            self.results_text.insert(tk.END, "✅ GOOD NEWS:\n")
            self.results_text.insert(tk.END, "Password not found in breach database.\n\n")
            self.results_text.insert(tk.END, "🛡️ SECURITY BEST PRACTICES:\n")
            self.results_text.insert(tk.END, "• Continue using unique passwords\n")
            self.results_text.insert(tk.END, "• Regularly check password security\n")
            self.results_text.insert(tk.END, "• Enable two-factor authentication\n")
            self.results_text.insert(tk.END, "• Use a password manager\n")
        
        self.results_text.insert(tk.END, "\n" + "=" * 60 + "\n")
        self.results_text.insert(tk.END, f"Check completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        
        # Clear password field for security
        self.password_entry.delete(0, tk.END)
    
    def clear_results(self):
        self.results_text.delete(1.0, tk.END)
        self.password_entry.delete(0, tk.END)
        self.results_text.insert(tk.END, "Results cleared. Enter a password to check exposure.\n")


if __name__ == "__main__":
    root = tk.Tk()
    PwnedCheckModule(root)
    root.mainloop()
