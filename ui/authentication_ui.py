import tkinter as tk
from tkinter import messagebox
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from backend.authentication import AuthenticationSystem

class AuthenticationUI:
    def __init__(self, root, on_success_callback):
        self.root = root
        self.on_success_callback = on_success_callback
        self.auth_system = AuthenticationSystem()
        self.current_email = None
        self.current_password = None
        self.is_signup = False
        
        self.root.title("SECURENETRA - Authentication")
        self.root.geometry("600x700")
        self.root.configure(bg="#1F1F1F")
        
        self.show_login_screen()
    
    def clear_screen(self):
        """Clear all widgets"""
        for widget in self.root.winfo_children():
            widget.destroy()
    
    def show_login_screen(self):
        """Display login screen"""
        self.clear_screen()
        
        # Header
        header = tk.Frame(self.root, bg="#000000", height=80)
        header.pack(fill="x")
        header.pack_propagate(False)
        
        tk.Label(header, text="🔐 SECURENETRA", font=("Consolas", 20, "bold"),
                bg="#000000", fg="#00FF66").pack(pady=25)
        
        # Main content
        content = tk.Frame(self.root, bg="#1F1F1F")
        content.pack(expand=True, fill="both", padx=50, pady=30)
        
        tk.Label(content, text="LOGIN", font=("Consolas", 18, "bold"),
                bg="#1F1F1F", fg="#00FF66").pack(pady=(0, 30))
        
        # Email
        tk.Label(content, text="Email Address:", font=("Consolas", 11, "bold"),
                bg="#1F1F1F", fg="#00FF66").pack(anchor="w", pady=(10, 5))
        
        self.login_email = tk.Entry(content, font=("Consolas", 12, "bold"),
                                    bg="#000000", fg="#00FF66", relief="solid", bd=2)
        self.login_email.pack(fill="x", ipady=10)
        
        # Password
        tk.Label(content, text="Password:", font=("Consolas", 11, "bold"),
                bg="#1F1F1F", fg="#00FF66").pack(anchor="w", pady=(20, 5))
        
        self.login_password = tk.Entry(content, font=("Consolas", 12, "bold"),
                                       bg="#000000", fg="#00FF66", relief="solid", bd=2, show="*")
        self.login_password.pack(fill="x", ipady=10)
        
        # Login button
        login_btn = tk.Button(content, text="🔓 LOGIN WITH OTP",
                             font=("Consolas", 13, "bold"), bg="#00FF66", fg="#000000",
                             activebackground="#00CC52", relief="solid", bd=0,
                             cursor="hand2", command=self.handle_login)
        login_btn.pack(fill="x", ipady=15, pady=(30, 10))
        
        # Divider
        tk.Frame(content, bg="#00FF66", height=1).pack(fill="x", pady=20)
        
        # Signup link
        signup_frame = tk.Frame(content, bg="#1F1F1F")
        signup_frame.pack()
        
        tk.Label(signup_frame, text="Don't have an account?", font=("Consolas", 10, "bold"),
                bg="#1F1F1F", fg="#FFFFFF").pack(side="left", padx=(0, 5))
        
        signup_link = tk.Label(signup_frame, text="Sign Up", font=("Consolas", 10, "bold", "underline"),
                              bg="#1F1F1F", fg="#00FF66", cursor="hand2")
        signup_link.pack(side="left")
        signup_link.bind("<Button-1>", lambda e: self.show_signup_screen())
        
        # Info
        tk.Label(content, text="🔐 Two-Factor Authentication Enabled",
                font=("Consolas", 9, "bold"), bg="#1F1F1F", fg="#666666").pack(pady=(30, 5))
        tk.Label(content, text="OTP will be sent to your email",
                font=("Consolas", 9, "bold"), bg="#1F1F1F", fg="#666666").pack()
    
    def show_signup_screen(self):
        """Display signup screen"""
        self.clear_screen()
        
        # Header
        header = tk.Frame(self.root, bg="#000000", height=80)
        header.pack(fill="x")
        header.pack_propagate(False)
        
        tk.Label(header, text="🔐 SECURENETRA", font=("Consolas", 20, "bold"),
                bg="#000000", fg="#00FF66").pack(pady=25)
        
        # Main content
        content = tk.Frame(self.root, bg="#1F1F1F")
        content.pack(expand=True, fill="both", padx=50, pady=30)
        
        tk.Label(content, text="CREATE ACCOUNT", font=("Consolas", 18, "bold"),
                bg="#1F1F1F", fg="#00FF66").pack(pady=(0, 30))
        
        # Email
        tk.Label(content, text="Email Address:", font=("Consolas", 11, "bold"),
                bg="#1F1F1F", fg="#00FF66").pack(anchor="w", pady=(10, 5))
        
        self.signup_email = tk.Entry(content, font=("Consolas", 12, "bold"),
                                     bg="#000000", fg="#00FF66", relief="solid", bd=2)
        self.signup_email.pack(fill="x", ipady=10)
        
        # Password
        tk.Label(content, text="Password:", font=("Consolas", 11, "bold"),
                bg="#1F1F1F", fg="#00FF66").pack(anchor="w", pady=(20, 5))
        
        self.signup_password = tk.Entry(content, font=("Consolas", 12, "bold"),
                                        bg="#000000", fg="#00FF66", relief="solid", bd=2, show="*")
        self.signup_password.pack(fill="x", ipady=10)
        
        # Confirm Password
        tk.Label(content, text="Confirm Password:", font=("Consolas", 11, "bold"),
                bg="#1F1F1F", fg="#00FF66").pack(anchor="w", pady=(20, 5))
        
        self.signup_confirm = tk.Entry(content, font=("Consolas", 12, "bold"),
                                       bg="#000000", fg="#00FF66", relief="solid", bd=2, show="*")
        self.signup_confirm.pack(fill="x", ipady=10)
        
        # Signup button
        signup_btn = tk.Button(content, text="📧 SIGN UP WITH OTP",
                              font=("Consolas", 13, "bold"), bg="#00FF66", fg="#000000",
                              activebackground="#00CC52", relief="solid", bd=0,
                              cursor="hand2", command=self.handle_signup)
        signup_btn.pack(fill="x", ipady=15, pady=(30, 10))
        
        # Divider
        tk.Frame(content, bg="#00FF66", height=1).pack(fill="x", pady=20)
        
        # Login link
        login_frame = tk.Frame(content, bg="#1F1F1F")
        login_frame.pack()
        
        tk.Label(login_frame, text="Already have an account?", font=("Consolas", 10, "bold"),
                bg="#1F1F1F", fg="#FFFFFF").pack(side="left", padx=(0, 5))
        
        login_link = tk.Label(login_frame, text="Login", font=("Consolas", 10, "bold", "underline"),
                             bg="#1F1F1F", fg="#00FF66", cursor="hand2")
        login_link.pack(side="left")
        login_link.bind("<Button-1>", lambda e: self.show_login_screen())
    
    def show_otp_screen(self):
        """Display OTP verification screen"""
        self.clear_screen()
        
        # Header
        header = tk.Frame(self.root, bg="#000000", height=80)
        header.pack(fill="x")
        header.pack_propagate(False)
        
        tk.Label(header, text="🔐 SECURENETRA", font=("Consolas", 20, "bold"),
                bg="#000000", fg="#00FF66").pack(pady=25)
        
        # Main content
        content = tk.Frame(self.root, bg="#1F1F1F")
        content.pack(expand=True, fill="both", padx=50, pady=30)
        
        tk.Label(content, text="VERIFY OTP", font=("Consolas", 18, "bold"),
                bg="#1F1F1F", fg="#00FF66").pack(pady=(0, 20))
        
        # Info
        tk.Label(content, text=f"📧 OTP sent to:", font=("Consolas", 10, "bold"),
                bg="#1F1F1F", fg="#FFFFFF").pack(pady=(10, 5))
        tk.Label(content, text=self.current_email, font=("Consolas", 11, "bold"),
                bg="#1F1F1F", fg="#00FF66").pack(pady=(0, 20))
        
        tk.Label(content, text="⏱️ Valid for 5 minutes", font=("Consolas", 9, "bold"),
                bg="#1F1F1F", fg="#FFAA00").pack(pady=(0, 30))
        
        # OTP Entry
        tk.Label(content, text="Enter 6-Digit OTP:", font=("Consolas", 11, "bold"),
                bg="#1F1F1F", fg="#00FF66").pack(anchor="w", pady=(10, 5))
        
        self.otp_entry = tk.Entry(content, font=("Consolas", 20, "bold"),
                                  bg="#000000", fg="#00FF66", relief="solid", bd=2,
                                  justify="center")
        self.otp_entry.pack(fill="x", ipady=15)
        
        # Verify button
        verify_btn = tk.Button(content, text="✅ VERIFY OTP",
                              font=("Consolas", 13, "bold"), bg="#00FF66", fg="#000000",
                              activebackground="#00CC52", relief="solid", bd=0,
                              cursor="hand2", command=self.handle_otp_verification)
        verify_btn.pack(fill="x", ipady=15, pady=(30, 10))
        
        # Resend OTP
        resend_frame = tk.Frame(content, bg="#1F1F1F")
        resend_frame.pack(pady=20)
        
        tk.Label(resend_frame, text="Didn't receive OTP?", font=("Consolas", 10, "bold"),
                bg="#1F1F1F", fg="#FFFFFF").pack(side="left", padx=(0, 5))
        
        resend_link = tk.Label(resend_frame, text="Resend", font=("Consolas", 10, "bold", "underline"),
                              bg="#1F1F1F", fg="#00FF66", cursor="hand2")
        resend_link.pack(side="left")
        resend_link.bind("<Button-1>", lambda e: self.resend_otp())
        
        # Back button
        back_btn = tk.Button(content, text="← BACK",
                            font=("Consolas", 10, "bold"), bg="#1F1F1F", fg="#00FF66",
                            activebackground="#2E2E2E", relief="flat",
                            cursor="hand2", command=self.show_login_screen)
        back_btn.pack(pady=(20, 0))
    
    def handle_login(self):
        """Handle login button click"""
        email = self.login_email.get().strip()
        password = self.login_password.get().strip()
        
        if not email or not password:
            messagebox.showerror("Error", "Please enter email and password")
            return
        
        # Verify credentials
        success, message = self.auth_system.login(email, password)
        
        if not success:
            messagebox.showerror("Login Failed", message)
            return
        
        # Send OTP using email_config.py
        self.current_email = email
        self.current_password = password
        self.is_signup = False
        
        success, message = self.auth_system.request_otp(email)
        
        if success:
            messagebox.showinfo("OTP Sent", f"OTP sent to {email}")
            self.show_otp_screen()
        else:
            messagebox.showerror("Error", message)
    
    def handle_signup(self):
        """Handle signup button click"""
        email = self.signup_email.get().strip()
        password = self.signup_password.get().strip()
        confirm = self.signup_confirm.get().strip()
        
        if not email or not password or not confirm:
            messagebox.showerror("Error", "Please fill all fields")
            return
        
        if password != confirm:
            messagebox.showerror("Error", "Passwords do not match")
            return
        
        if len(password) < 6:
            messagebox.showerror("Error", "Password must be at least 6 characters")
            return
        
        # Create account
        success, message = self.auth_system.signup(email, password)
        
        if not success:
            messagebox.showerror("Signup Failed", message)
            return
        
        # Send OTP using email_config.py
        self.current_email = email
        self.current_password = password
        self.is_signup = True
        
        success, message = self.auth_system.request_otp(email)
        
        if success:
            messagebox.showinfo("OTP Sent", f"OTP sent to {email}\n\nVerify to complete registration.")
            self.show_otp_screen()
        else:
            messagebox.showerror("Error", message)
    
    def handle_otp_verification(self):
        """Handle OTP verification"""
        otp = self.otp_entry.get().strip()
        
        if not otp or len(otp) != 6:
            messagebox.showerror("Error", "Please enter 6-digit OTP")
            return
        
        success, message = self.auth_system.verify_otp(self.current_email, otp)
        
        if success:
            if self.is_signup:
                # Mark user as verified
                self.auth_system.verify_user(self.current_email)
                messagebox.showinfo("Success", "Account verified successfully!\n\nYou can now access SECURENETRA.")
            else:
                messagebox.showinfo("Success", "Login successful!\n\nWelcome to SECURENETRA.")
            
            # Call success callback to show main dashboard
            self.on_success_callback(self.current_email)
        else:
            messagebox.showerror("Verification Failed", message)
    
    def resend_otp(self):
        """Resend OTP"""
        success, message = self.auth_system.request_otp(self.current_email)
        
        if success:
            messagebox.showinfo("OTP Sent", f"New OTP has been sent to {self.current_email}")
        else:
            messagebox.showerror("Error", message)


if __name__ == "__main__":
    root = tk.Tk()
    
    def on_auth_success(email):
        print(f"User {email} authenticated successfully")
        root.destroy()
    
    AuthenticationUI(root, on_auth_success)
    root.mainloop()
