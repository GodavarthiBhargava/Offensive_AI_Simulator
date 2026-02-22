import tkinter as tk
from tkinter import messagebox
import sys
import os
import random
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from backend.authentication import AuthenticationSystem

class MatrixRain:
    """Matrix rain effect background"""
    def __init__(self, canvas):
        self.canvas = canvas
        self.drops = []
        self.chars = "01"
        self.create_drops()
        self.animate()
    
    def create_drops(self):
        width = self.canvas.winfo_width()
        for x in range(0, width, 20):
            self.drops.append({
                'x': x,
                'y': random.randint(-500, 0),
                'speed': random.randint(2, 5)
            })
    
    def animate(self):
        self.canvas.delete("matrix")
        for drop in self.drops:
            char = random.choice(self.chars)
            self.canvas.create_text(
                drop['x'], drop['y'],
                text=char, fill="#00FF88", font=("Courier", 12),
                tags="matrix"
            )
            drop['y'] += drop['speed']
            if drop['y'] > self.canvas.winfo_height():
                drop['y'] = random.randint(-100, 0)
        
        self.canvas.after(50, self.animate)

class AuthenticationUI:
    def __init__(self, root, on_success_callback):
        self.root = root
        self.on_success_callback = on_success_callback
        self.auth_system = AuthenticationSystem()
        self.current_email = None
        self.current_password = None
        self.is_signup = False
        
        self.root.title("SECURENETRA - Authentication")
        self.root.geometry("800x600")
        self.root.configure(bg="#000000")
        
        self.show_login_screen()
    
    def clear_screen(self):
        """Clear all widgets"""
        for widget in self.root.winfo_children():
            widget.destroy()
    
    def show_login_screen(self):
        """Display login screen"""
        self.clear_screen()
        
        # Full screen black background with matrix effect
        bg_canvas = tk.Canvas(self.root, bg="#000000", highlightthickness=0)
        bg_canvas.pack(fill="both", expand=True)
        
        # Matrix rain effect
        self.root.update()
        MatrixRain(bg_canvas)
        
        # Center container
        center_frame = tk.Frame(bg_canvas, bg="#000000")
        center_frame.place(relx=0.5, rely=0.5, anchor="center")
        
        # Glowing login box
        login_box = tk.Frame(center_frame, bg="#0a0a0a", relief="solid", bd=0,
                            highlightbackground="#00FF88", highlightthickness=3)
        login_box.pack(padx=40, pady=40)
        
        # Inner padding
        inner = tk.Frame(login_box, bg="#0a0a0a")
        inner.pack(padx=40, pady=40)
        
        # Title
        title = tk.Label(inner, text="⚡ AI SECURITY CONSOLE", font=("Courier New", 24, "bold"),
                        bg="#0a0a0a", fg="#00FF88")
        title.pack(pady=(0, 30))
        
        # Email
        tk.Label(inner, text="EMAIL", font=("Courier New", 9, "bold"),
                bg="#0a0a0a", fg="#00FF88").pack(anchor="w", pady=(10, 5))
        
        self.login_email = tk.Entry(inner, font=("Courier New", 12, "bold"),
                                    bg="#000000", fg="#00FF88", relief="solid", bd=2,
                                    insertbackground="#00FF88", highlightbackground="#00FF88",
                                    highlightcolor="#00FF88", highlightthickness=1, width=30)
        self.login_email.pack(ipady=10)
        
        # Password
        tk.Label(inner, text="PASSWORD", font=("Courier New", 9, "bold"),
                bg="#0a0a0a", fg="#00FF88").pack(anchor="w", pady=(20, 5))
        
        self.login_password = tk.Entry(inner, font=("Courier New", 12, "bold"),
                                       bg="#000000", fg="#00FF88", relief="solid", bd=2, show="•",
                                       insertbackground="#00FF88", highlightbackground="#00FF88",
                                       highlightcolor="#00FF88", highlightthickness=1, width=30)
        self.login_password.pack(ipady=10)
        
        # Login button
        login_btn = tk.Button(inner, text="▶ ACCESS SYSTEM",
                             font=("Courier New", 13, "bold"), bg="#00FF88", fg="#000000",
                             activebackground="#00CC66", relief="flat", bd=0,
                             cursor="hand2", command=self.handle_login, width=28, height=2)
        login_btn.pack(pady=(30, 20))
        
        login_btn.bind("<Enter>", lambda e: login_btn.config(bg="#00CC66"))
        login_btn.bind("<Leave>", lambda e: login_btn.config(bg="#00FF88"))
        
        # Signup link
        link_frame = tk.Frame(inner, bg="#0a0a0a")
        link_frame.pack()
        
        tk.Label(link_frame, text="New User?", font=("Courier New", 9, "bold"),
                bg="#0a0a0a", fg="#666666").pack(side="left", padx=(0, 5))
        
        signup_link = tk.Label(link_frame, text="Register", font=("Courier New", 9, "bold", "underline"),
                              bg="#0a0a0a", fg="#00FF88", cursor="hand2")
        signup_link.pack(side="left")
        signup_link.bind("<Button-1>", lambda e: self.show_signup_screen())
        
        # Footer
        tk.Label(inner, text="🔒 2FA ENABLED", font=("Courier New", 8, "bold"),
                bg="#0a0a0a", fg="#004400").pack(pady=(20, 0))
    
    def show_signup_screen(self):
        """Display signup screen"""
        self.clear_screen()
        
        bg_canvas = tk.Canvas(self.root, bg="#000000", highlightthickness=0)
        bg_canvas.pack(fill="both", expand=True)
        
        self.root.update()
        MatrixRain(bg_canvas)
        
        center_frame = tk.Frame(bg_canvas, bg="#000000")
        center_frame.place(relx=0.5, rely=0.5, anchor="center")
        
        signup_box = tk.Frame(center_frame, bg="#0a0a0a", relief="solid", bd=0,
                             highlightbackground="#00FF88", highlightthickness=3)
        signup_box.pack(padx=40, pady=40)
        
        inner = tk.Frame(signup_box, bg="#0a0a0a")
        inner.pack(padx=40, pady=40)
        
        title = tk.Label(inner, text="⚡ REGISTER", font=("Courier New", 24, "bold"),
                        bg="#0a0a0a", fg="#00FF88")
        title.pack(pady=(0, 30))
        
        tk.Label(inner, text="EMAIL", font=("Courier New", 9, "bold"),
                bg="#0a0a0a", fg="#00FF88").pack(anchor="w", pady=(10, 5))
        
        self.signup_email = tk.Entry(inner, font=("Courier New", 12, "bold"),
                                     bg="#000000", fg="#00FF88", relief="solid", bd=2,
                                     insertbackground="#00FF88", highlightbackground="#00FF88",
                                     highlightcolor="#00FF88", highlightthickness=1, width=30)
        self.signup_email.pack(ipady=10)
        
        tk.Label(inner, text="PASSWORD", font=("Courier New", 9, "bold"),
                bg="#0a0a0a", fg="#00FF88").pack(anchor="w", pady=(20, 5))
        
        self.signup_password = tk.Entry(inner, font=("Courier New", 12, "bold"),
                                        bg="#000000", fg="#00FF88", relief="solid", bd=2, show="•",
                                        insertbackground="#00FF88", highlightbackground="#00FF88",
                                        highlightcolor="#00FF88", highlightthickness=1, width=30)
        self.signup_password.pack(ipady=10)
        
        tk.Label(inner, text="CONFIRM PASSWORD", font=("Courier New", 9, "bold"),
                bg="#0a0a0a", fg="#00FF88").pack(anchor="w", pady=(20, 5))
        
        self.signup_confirm = tk.Entry(inner, font=("Courier New", 12, "bold"),
                                       bg="#000000", fg="#00FF88", relief="solid", bd=2, show="•",
                                       insertbackground="#00FF88", highlightbackground="#00FF88",
                                       highlightcolor="#00FF88", highlightthickness=1, width=30)
        self.signup_confirm.pack(ipady=10)
        
        signup_btn = tk.Button(inner, text="▶ CREATE ACCOUNT",
                              font=("Courier New", 13, "bold"), bg="#00FF88", fg="#000000",
                              activebackground="#00CC66", relief="flat", bd=0,
                              cursor="hand2", command=self.handle_signup, width=28, height=2)
        signup_btn.pack(pady=(30, 20))
        
        signup_btn.bind("<Enter>", lambda e: signup_btn.config(bg="#00CC66"))
        signup_btn.bind("<Leave>", lambda e: signup_btn.config(bg="#00FF88"))
        
        link_frame = tk.Frame(inner, bg="#0a0a0a")
        link_frame.pack()
        
        tk.Label(link_frame, text="Already registered?", font=("Courier New", 9, "bold"),
                bg="#0a0a0a", fg="#666666").pack(side="left", padx=(0, 5))
        
        login_link = tk.Label(link_frame, text="Login", font=("Courier New", 9, "bold", "underline"),
                             bg="#0a0a0a", fg="#00FF88", cursor="hand2")
        login_link.pack(side="left")
        login_link.bind("<Button-1>", lambda e: self.show_login_screen())
    
    def show_otp_screen(self):
        """Display OTP verification screen"""
        self.clear_screen()
        
        bg_canvas = tk.Canvas(self.root, bg="#000000", highlightthickness=0)
        bg_canvas.pack(fill="both", expand=True)
        
        self.root.update()
        MatrixRain(bg_canvas)
        
        center_frame = tk.Frame(bg_canvas, bg="#000000")
        center_frame.place(relx=0.5, rely=0.5, anchor="center")
        
        otp_box = tk.Frame(center_frame, bg="#0a0a0a", relief="solid", bd=0,
                          highlightbackground="#00FF88", highlightthickness=3)
        otp_box.pack(padx=40, pady=40)
        
        inner = tk.Frame(otp_box, bg="#0a0a0a")
        inner.pack(padx=40, pady=40)
        
        title = tk.Label(inner, text="⚡ VERIFY OTP", font=("Courier New", 24, "bold"),
                        bg="#0a0a0a", fg="#00FF88")
        title.pack(pady=(0, 20))
        
        tk.Label(inner, text=f"📧 Code sent to:", font=("Courier New", 9, "bold"),
                bg="#0a0a0a", fg="#666666").pack(pady=(10, 5))
        tk.Label(inner, text=self.current_email, font=("Courier New", 10, "bold"),
                bg="#0a0a0a", fg="#00FF88").pack(pady=(0, 10))
        
        tk.Label(inner, text="⏱️ Valid for 5 minutes", font=("Courier New", 8, "bold"),
                bg="#0a0a0a", fg="#FFAA00").pack(pady=(0, 30))
        
        tk.Label(inner, text="ENTER 6-DIGIT CODE", font=("Courier New", 9, "bold"),
                bg="#0a0a0a", fg="#00FF88").pack(anchor="w", pady=(10, 5))
        
        self.otp_entry = tk.Entry(inner, font=("Courier New", 20, "bold"),
                                  bg="#000000", fg="#00FF88", relief="solid", bd=2,
                                  justify="center", insertbackground="#00FF88",
                                  highlightbackground="#00FF88", highlightcolor="#00FF88",
                                  highlightthickness=1, width=15)
        self.otp_entry.pack(ipady=15)
        
        verify_btn = tk.Button(inner, text="▶ VERIFY",
                              font=("Courier New", 13, "bold"), bg="#00FF88", fg="#000000",
                              activebackground="#00CC66", relief="flat", bd=0,
                              cursor="hand2", command=self.handle_otp_verification,
                              width=28, height=2)
        verify_btn.pack(pady=(30, 20))
        
        verify_btn.bind("<Enter>", lambda e: verify_btn.config(bg="#00CC66"))
        verify_btn.bind("<Leave>", lambda e: verify_btn.config(bg="#00FF88"))
        
        link_frame = tk.Frame(inner, bg="#0a0a0a")
        link_frame.pack()
        
        tk.Label(link_frame, text="Didn't receive?", font=("Courier New", 9, "bold"),
                bg="#0a0a0a", fg="#666666").pack(side="left", padx=(0, 5))
        
        resend_link = tk.Label(link_frame, text="Resend", font=("Courier New", 9, "bold", "underline"),
                              bg="#0a0a0a", fg="#00FF88", cursor="hand2")
        resend_link.pack(side="left")
        resend_link.bind("<Button-1>", lambda e: self.resend_otp())
        
        back_btn = tk.Button(inner, text="← BACK", font=("Courier New", 9, "bold"),
                            bg="#0a0a0a", fg="#00FF88", relief="flat",
                            cursor="hand2", command=self.show_login_screen)
        back_btn.pack(pady=(20, 0))
    
    def handle_login(self):
        """Handle login button click"""
        email = self.login_email.get().strip()
        password = self.login_password.get().strip()
        
        if not email or not password:
            messagebox.showerror("Error", "Please enter email and password")
            return
        
        success, message = self.auth_system.login(email, password)
        
        if not success:
            messagebox.showerror("Login Failed", message)
            return
        
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
        
        success, message = self.auth_system.signup(email, password)
        
        if not success:
            messagebox.showerror("Signup Failed", message)
            return
        
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
                self.auth_system.verify_user(self.current_email)
                messagebox.showinfo("Success", "Account verified successfully!\n\nYou can now access SECURENETRA.")
            else:
                messagebox.showinfo("Success", "Login successful!\n\nWelcome to SECURENETRA.")
            
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
